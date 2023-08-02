from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Cabin, Seat


class CabinSeatReservationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        c_q_1 = Cabin.objects.create(cabinName='First Class', capacity=50)
        c_q_2 = Cabin.objects.create(cabinName='Second Class', capacity=50)
        Seat.objects.create(cabin=c_q_1, seatNumber='A1', fare=100)
        Seat.objects.create(cabin=c_q_1, seatNumber='A2', fare=100)
        Seat.objects.create(cabin=c_q_2, seatNumber='A1', fare=200)
        Seat.objects.create(cabin=c_q_2, seatNumber='A2', fare=300)

    def setUp(self):
        self.client = APIClient()
        self.cabin_name = 'First Class'
        self.total_seats = 50
        self.seat_number = 'A1'
        self.fare = 100
        self.create_cabin_url = reverse('create_cabin')
        self.update_cabin_url = reverse('update_cabin')
        self.add_seat_url = reverse('add_seat')
        self.book_seats_url = reverse('book_seats')
        # You may need to set up more test data as needed for other tests

    def test_create_cabin(self):
        data = {'cabinName': 'TestClass', 'totalSeats': self.total_seats}
        response = self.client.post(self.create_cabin_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'pass')
        self.assertEqual(response.data['msg'], f'cabin TestClass created successfully')

    def test_create_same_cabin(self):
        data = {'cabinName': self.cabin_name, 'totalSeats': self.total_seats}
        response = self.client.post(self.create_cabin_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['status'], 'fail')
        self.assertEqual(response.data['msg'], f'cabin {self.cabin_name} already exist')

    def test_update_cabin(self):
        data = {'cabinName': self.cabin_name, 'totalSeats': 60}
        response = self.client.patch(self.update_cabin_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'pass')
        self.assertEqual(response.data['msg'], f'cabin {self.cabin_name} updated successfully')

    def test_add_seat(self):
        data = {'cabinName': self.cabin_name, 'seatNumber': 'T1', 'fare': 120}
        response = self.client.post(self.add_seat_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'pass')
        self.assertEqual(response.data['msg'], f'Seat T1 added successfully')

    def test_add_duplicate_seat(self):
        data = {'cabinName': self.cabin_name, 'seatNumber': 'A1', 'fare': 100}
        response = self.client.post(self.add_seat_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['status'], 'fail')
        self.assertEqual(response.data['msg'], f'seat A1 already exist in First Class')

    def test_book_seat(self):
        data = {'seatNumbers': ['A1', 'A2'], 'cabinName': self.cabin_name}
        response = self.client.post(self.book_seats_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'pass')
