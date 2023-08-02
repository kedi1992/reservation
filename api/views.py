from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
from rest_framework import status

from api.Serializer import CabinSerializer, SeatSerializer
from api.models import Cabin, Seat
import uuid


def is_cabin_exist(cabin_name):
    try:
        cabin_info = Cabin.objects.get(pk=cabin_name)
        return cabin_info
    except Cabin.DoesNotExist:
        return None


@api_view(['POST'])
def create_cabin(request):
    name = request.data.get('cabinName')
    total_seats = request.data.get('totalSeats')
    q = Cabin.objects.filter(cabinName=name)
    if not q:
        Cabin(cabinName=name, capacity=total_seats).save()
        msg = f"cabin {name} created successfully"
        return Response({"status": "pass", "msg": msg}, status=status.HTTP_200_OK)
    else:
        # q[0].seatCapacity = total_seats
        # q[0].availableSeat = total_seats
        # q[0].save()
        msg = f"cabin {name} already exist"
        return Response({"status": "fail", "msg": msg}, status=status.HTTP_409_CONFLICT)


@api_view(['PATCH'])
def update_cabin(request):
    name = request.data.get('cabinName')
    total_seats = request.data.get('totalSeats')
    q = Cabin.objects.filter(cabinName=name)
    if not q:
        Cabin(cabinName=name, capacity=total_seats).save()
        msg = f"cabin {name} not exist"
        return Response({"status": "fail", "msg": msg}, status=status.HTTP_404_NOT_FOUND)
    q[0].capacity = total_seats
    q[0].save()
    msg = f"cabin {name} updated successfully"
    serializer = CabinSerializer(q[0])
    return Response({"status": "pass", "msg": msg, 'info': serializer.data})


@api_view(['POST'])
def add_seat(request):
    seat_name = request.data.get('seatNumber')
    cabin_name = request.data.get('cabinName')
    fare = request.data.get('fare')
    cabin_q = Cabin.objects.filter(pk=cabin_name)
    if not cabin_q:
        msg = f"cabin {cabin_name} not exist"
        return Response({"status": "fail", "msg": msg}, status=status.HTTP_404_NOT_FOUND)
    seat_q = Seat.objects.filter(cabin=cabin_q[0], seatNumber=seat_name)
    if seat_q:
        msg = f"seat {seat_name} already exist in {cabin_name}"
        return Response({"status": "fail", "msg": msg}, status=status.HTTP_409_CONFLICT)
    Seat(seatNumber=seat_name, cabin=cabin_q[0], fare=fare).save()
    msg = f"Seat {seat_name} added successfully"
    seat_q = Seat.objects.filter(cabin=cabin_q[0])
    data = SeatSerializer(seat_q, many=True)
    return Response({"status": "pass", "msg": msg, 'info': data.data}, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def update_seat(request):
    seat_name = request.data.get('seatNumber')
    cabin_name = request.data.get('cabinName')
    fare = request.data.get('fare')
    cabin_q = Cabin.objects.filter(pk=cabin_name)
    if not cabin_q:
        msg = f"cabin {cabin_name} not exist"
        return Response({"status": "fail", "msg": msg}, status=status.HTTP_404_NOT_FOUND)
    seat_q = Seat.objects.filter(cabin=cabin_q[0], seatNumber=seat_name)
    if not seat_q:
        msg = f"seat {seat_name} not exist in {cabin_name}"
        return Response({"status": "fail", "msg": msg}, status=status.HTTP_404_NOT_FOUND)
    seat_q[0].fare = fare
    seat_q[0].save()
    msg = f"Seat {seat_name} updated successfully"
    seat_q = Seat.objects.filter(cabin=cabin_q[0], seatNumber=seat_name)
    seat_serializer = SeatSerializer(seat_q[0])
    return Response({"status": "pass", "msg": msg, 'info': seat_serializer.data})


@api_view(['GET'])
def get_cabin_info(request):
    cabin_name = request.GET.get('cabinName')
    try:
        cabin_info = Cabin.objects.get(pk=cabin_name)
        serializer = CabinSerializer(cabin_info)
        return Response({'status': "pass", "msg": serializer.data}, status=status.HTTP_200_OK)
    except Cabin.DoesNotExist:
        msg = f"Cabin {cabin_name} not exist"
        return Response({'status': "fail", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_seat_availability(request):
    seat_count = request.data.get('seatCount')
    cabin_name = request.data.get('cabinName')
    cabin_q = is_cabin_exist(cabin_name)
    available_seat_q = Seat.objects.filter(isReserved=False, cabin=cabin_q)
    seat_serializer = SeatSerializer(available_seat_q, many=True)
    if not cabin_q:
        return Response({'status': "fail", "msg": f"cabin {cabin_name} not exist"}, status=status.HTTP_400_BAD_REQUEST)
    if seat_count > len(available_seat_q):
        return Response({'status': "fail", "msg": f"Seats {seat_count} are not available in cabin '{cabin_name}'",
                         "info": {'availableSeats': seat_serializer.data, "cabinName": cabin_name}},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({'status': "pass", "info": {'AvailableSeats': seat_serializer.data, "cabinName": cabin_name}},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def book_seats(request):
    seat_name_list = request.data.get('seatNumbers')
    if seat_name_list:
        seat_name_list = list(set(seat_name_list))
    cabin_name = request.data.get('cabinName')
    cabin_q = is_cabin_exist(cabin_name)
    if not cabin_q:
        return Response({'status': "fail", "msg": f"cabin {cabin_name} not exist"}, status=status.HTTP_400_BAD_REQUEST)
    available_seat_q = Seat.objects.filter(isReserved=False, cabin=cabin_q)
    fail_to_reserve = []
    for e in seat_name_list:
        seat_q = Seat.objects.filter(isReserved=False, cabin=cabin_q, seatNumber=e)
        if not seat_q:
            fail_to_reserve.append(e)
            break
    seat_serializer = SeatSerializer(available_seat_q, many=True)
    if len(seat_name_list) > len(available_seat_q):
        return Response({'status': "fail", "msg": f"Total {len(seat_name_list)} Seats are not available in cabin '{cabin_name}'",
                         "info": {'AvailableSeats': seat_serializer.data, "cabinName": cabin_name}},
                        status=status.HTTP_400_BAD_REQUEST)
    if len(fail_to_reserve) > 0:
        return Response({'status': "fail", "msg": f"Seats {','.join(str(e) for e in fail_to_reserve)} are already booked in cabin '{cabin_name}'",
                         "info": {'AvailableSeats': seat_serializer.data, "cabinName": cabin_name}},
                        status=status.HTTP_400_BAD_REQUEST)

    r_id = uuid.uuid4()
    reserved_seat_list = []
    total_fare = 0
    for e in seat_name_list:
        seat_q = Seat.objects.get(isReserved=False, cabin=cabin_q, seatNumber=e)
        seat_q.isReserved = True
        seat_q.reservationID = str(r_id)
        seat_q.save()
        total_fare = total_fare + seat_q.fare
        reserved_seat_list.append(e)
    return Response({'status': "pass", "info": {'bookedSeats': reserved_seat_list, 'reservationID': r_id,
                                                'totalFare': total_fare, "paymentLink":f"https://payme/{r_id}",
                                                "cabinName": cabin_name}},
                    status=status.HTTP_200_OK)
