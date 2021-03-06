
from typing import DefaultDict
from django.contrib import admin
from django.db import router
from django.urls import path, include
from django.urls.conf import include
from tickets import views
from rest_framework.routers import DefaultRouter

import tickets 

app_name = 'pythonarabia'

router = DefaultRouter() 
router.register('guests', views.viewsets_guest)
router.register('movies', views.viewsets_movie)
router.register('reservations', views.viewsets_reservation)


urlpatterns = [
    # tutorial tickets python arabia 
    #1
    path('django/jsonresponsenomodel', views.no_rest_no_model),

    #2
    path('django/jsonresponsefrommodel', views.no_rest_from_model),

    #3.1 GET POST from rest FBV @api_view
    path('rest/fbv', views.FBV_List),

    #3.2 GET PUT DELETE  from rest FBV @api_view
    path('rest/fbv/<int:pk>', views.FBV_pk),

    #4.1 GET POST  from rest CBV APIView
    path('rest/cbv', views.CBV_List.as_view()),

    #4.2 GET PUT DELETE  from rest CBV APIView
    path('rest/cbv/<int:pk>', views.CBV_pk.as_view()),
    
    #5.1 GET POST  from rest CBV mixins
    path('rest/mixins', views.mixins_list.as_view()),

    #5.2 GET PUT DELETE  from rest CBV mixins
    path('rest/mixins/<int:pk>', views.mixins_pk.as_view()),

    #6.1 GET POST  from rest CBV generics
    path('rest/generics', views.generics_list.as_view()),

    #6.2 GET PUT DELETE  from rest CBV generics
    path('rest/generics/<int:pk>', views.generics_pk.as_view()),

    #7 list post  GET PUT DELETE  from rest CBV viewsets
    path('rest/viewsets/', include(router.urls)),

    #8 find movie  from rest FBV 
    path('rest/fbv/findmovie', views.find_movie),

    #8 new reservation  from rest FBV 
    path('rest/fbv/newreservation', views.new_reservation)
]
