from django.db import models
import uuid


class Cabin(models.Model):
    cabinName = models.CharField(primary_key=True, max_length=50)
    capacity = models.IntegerField()


class Seat(models.Model):
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)
    seatNumber = models.CharField(max_length=10)
    isReserved = models.BooleanField(default=False)
    fare = models.IntegerField()
    reservationID = models.UUIDField(null=True, default=None)