from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from tickets.models import Guest, Movie, Reservation

class MovieSerializer(serializers.ModelSerializer):
    titreDuFilm = serializers.CharField(source='movie') # pour renommer les field
    class Meta:
        model= Movie
        fields = '__all__'  # pour garder tous les fields
        # fields = ('id', 'titre',.....) pour garder ce quon veut   
        # exclude  = ['date',.....] pour exclure ce quon veut   

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Reservation
        fields = '__all__'

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model= Guest
        fields = ['pk','name','mobile', 'reservation']