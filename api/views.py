from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
from rest_framework import status

from api.Serializer import CabinSerializer, SeatSerializer
from api.models import Cabin, Seat


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
        return Response({"status": "pass", "msg": msg}, status=status.HTTP_409_CONFLICT)


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
    if not cabin_q:
        return Response({'status': "fail", "msg": f"cabin {cabin_name} not exist"}, status=status.HTTP_400_BAD_REQUEST)
    available_seats = cabin_q.availableSeat
    available_seat_list = []
    booked_seats = str(cabin_q.bookedSeats).split(",")
    for e in range(1, available_seats+1):
        if str(e) not in booked_seats:
            available_seat_list.append(e)
    if seat_count > available_seats:
        return Response({'status': "fail", "msg": f"Seats {seat_count}  are not available in cabin '{cabin_name}'", "info": {'AvailableSeats': available_seat_list, "cabinName": cabin_name}}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'status': "pass", "info": {'AvailableSeats': available_seat_list, "cabinName": cabin_name}}, status=status.HTTP_200_OK)


@api_view(['POST'])
def book_seats(request):
    seat_name_list = request.data.get('seatNumbers')
    if seat_name_list:
        seat_name_list = list(set(seat_name_list))
    cabin_name = request.data.get('cabinName')
    cabin_q = is_cabin_exist(cabin_name)
    if not cabin_q:
        return Response({'status': "fail", "msg": f"cabin {cabin_name} not exist"}, status=status.HTTP_400_BAD_REQUEST)
    available_seats = cabin_q.availableSeat
    available_seat_list = []
    booked_seats = str(cabin_q.bookedSeats).split(",")
    reserved_seat_list = []
    fail_to_reserve = []
    for e in seat_name_list:
        if str(e) not in booked_seats:
            reserved_seat_list.append(e)
        else:
            fail_to_reserve.append(e)
    for e in range(1, available_seats+1):
        if str(e) not in booked_seats:
            available_seat_list.append(e)
    if len(seat_name_list) > available_seats:
        return Response({'status': "fail", "msg": f"Seats {seat_name_list} are not available in cabin '{cabin_name}'",
                         "info": {'AvailableSeats': available_seat_list, "cabinName": cabin_name}},
                        status=status.HTTP_400_BAD_REQUEST)
    if len(fail_to_reserve) > 0:
        return Response({'status': "fail", "msg": f"Seats {','.join(str(e) for e in fail_to_reserve)} are already booked in cabin '{cabin_name}'",
                         "info": {'AvailableSeats': available_seat_list, "cabinName": cabin_name}},
                        status=status.HTTP_400_BAD_REQUEST)
    cabin_q.bookedSeats = cabin_q.bookedSeats + "," + ",".join(str(e) for e in reserved_seat_list)
    cabin_q.save()
    return Response({'status': "pass", "info": {'BookedSeats': reserved_seat_list, "cabinName": cabin_name}},
                    status=status.HTTP_200_OK)
