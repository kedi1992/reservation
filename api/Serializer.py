from rest_framework import serializers
from api.models import Cabin, Seat


class CabinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabin
        fields = "__all__"
        # exclude = ['id']


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"
        # exclude = ['id', 'reservationID']
