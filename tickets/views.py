from django.core.checks import messages
from django.http import request, response, Http404
from django.shortcuts import get_object_or_404, render
from django.http.response import Http404, JsonResponse
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from .models import Movie, Reservation, Guest
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from tickets import serializers
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework import generics, mixins, viewsets

from rest_framework.authentication import BasicAuthentication, TokenAuthentication 
from rest_framework.permissions import IsAuthenticated

# Create your views here.
# 1 sans rest et sans model query ... fbv
def no_rest_no_model(request):
    guest = [
        {
            'id':1,
            'name':'tina',
            'tel':454
        },        {
            'id':2,
            'name':'nada',
            'tel':45234
        }
    ]
    return JsonResponse(guest, safe=False)

# 2 sans rest et avec model query ... fbv
def no_rest_from_model(request):
    data = Guest.objects.all()
    response ={
        'guests':list(data.values('id','name', 'mobile'))
    }
    return JsonResponse(response)

# List == GET
# Create == POST
# pk query == GET 
# Update == PUT
# Delete destroy == DELETE

# 3 FBV  function base view a utiliser en cas de code compliqué
# 3.1 GET POST
@api_view(['GET', 'POST'])
def FBV_List(request):
    #GET
    if request.method=='GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    #POST
    elif request.method=='POST':
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST) 

# 3.1 GET PUT DELETE
@api_view(['GET','PUT', 'DELETE'])
def FBV_pk(request, pk):
    #declaratinon
    try:
        guest =Guest.objects.get(pk=pk)
    except Guest.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)
    #GET REATRIVE
    if request.method=='GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    #PUT
    elif request.method=='PUT':
        serializer=GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #DELETE
    if request.method=='DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 4 CBV
# 4.1 GET POST == list and create
class CBV_List(APIView):
    def get(self, request, *args, **kwargs):
        guest = Guest.objects.all()
        serializer = GuestSerializer(guest, many=True)
        return Response(serializer.data)
    def post(self, request, *args, **kwargs):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
                     # (serializer.data) ////////  ca retourne erreur 

# 4.2 GET PUT DELETE == retrive update delete ---  pk
class CBV_pk(APIView):
    def get_object(Self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest)
        return Response(serializer.data)
    def put(self, request, pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        guest=self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5 Mixins
# 5.1 mixins list
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)

# 5.2 mixins get put delete
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request, pk):
        return self.retrieve(request)
    def put(self, request, pk):
        return self.update(request)
    def delete(self, request, pk):
        return self.destroy(request)

# 6 generics
# 6.1 generics list and post
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

# 6.2 generics get put delete
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

# 7 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backend = [filters.SearchFilter]
    search_fields = ['movie']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

# 8 find movie avec : FBV
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(hall = request.data['hall'], movie = request.data['movie'])
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

# 9 create reservation avec : FBV ..... on creant new guest et query sur movie
@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        hall = request.data['hall'], #data hall qui vient de request dans le fields "hall"
        movie = request.data['movie']
    )
    guest = Guest() #creer un guest selon model Guest [vide]
    guest.name = request.data['name'] # remplir depuis request
    guest.mobile = request.data['mobile'] # remplir depuis request
    guest.save()

    reservation = Reservation() #creer un reservation selon model Reservation [vide]
    reservation.guest = guest # guest qu'on a creé
    reservation.movie = movie # movie qu'on a query
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)


