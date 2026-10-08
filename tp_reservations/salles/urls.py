"""Tache 3 : brancher les ViewSets sur un DefaultRouter.

Les routes attendues sont (prefixe /api/ deja fourni par config/urls.py) :
  /api/salles/            /api/salles/{id}/
  /api/reservations/      /api/reservations/{id}/
  /api/salles/{id}/occupation/
"""
# TODO : votre code ici
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import *

router = DefaultRouter()
router.register("salles", SalleViewSet, basename="salle")
router.register("reservations", ReservationViewSet, basename="reservations")

urlpatterns = [
    path("", include(router.urls)),
]
