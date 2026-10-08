"""Taches 3, 4, 5 (et bonus) : vues de l'API.

A FAIRE :
  - SalleViewSet (ModelViewSet), avec l'action `occupation` (tache 5)
  - ReservationViewSet (ModelViewSet), avec perform_create (tache 3)
"""
from rest_framework import viewsets  # noqa: F401  (a utiliser)
from rest_framework.permissions import IsAdminUser

from .models import Reservation, Salle  # noqa: F401  (a utiliser)
from rest_framework.decorators import action
from .serializers import *
from .permissions import *
from .pagination import *

# TODO : votre code ici

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related("user")
    serializer_class = ReservationSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)


class SalleViewSet(viewsets.ModelViewSet):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer
    pagination_class = ReservationPagination
    permission_classes = [IsAdminOrReadOnly] # assuming that the staff here is an admin user

    @action(detail=True, methods=["get"])
    def occupation(self,request):
        queryset = Reservation.objects.select_related("salle")
        classId = self.kwargs["nom"]
        start = self.request.query_params.get("debut")
        end = self.request.query_params.get("fin")
        if start and end:
            queryset = queryset.filter(salle__nom=classId)
        return queryset




