from django.contrib import admin
from django.urls import path, include
from api import views

urlpatterns = [
    path('createCabin', views.create_cabin, name='create_cabin'),
    path('updateCabin', views.update_cabin, name='update_cabin'),
    path('addSeat', views.add_seat, name='add_seat'),
    path('updateSeatInfo', views.update_seat, name='update_seat'),
    path('getCabinInfo', views.get_cabin_info, name='get_cabin_info'),
    path('bookSeats', views.book_seats, name='book_seats'),
    path('checkSeatAvailability', views.check_seat_availability, name='check_seat_availability'),
    # path('seatReservations', views.book_seats),
]
