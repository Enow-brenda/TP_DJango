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
from django.utils.dateparse import parse_datetime
from rest_framework.response import Response

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

    def get_queryset(self):
        reservations = Reservation.objects.all()
        salle = self.request.query_params.get("salle")
        date = self.request.query_params.get("date")
        if salle:
            reservations = reservations.filter(salle__nom=salle.nom)
        if date:
            reservations = reservations.filter(debut__date=date)
        return reservations

    @action(detail=True, methods=["get"])
    def occupation(self,request):
        salle = self.get_object()
        debut_str = request.query_params.get("debut")
        fin_str = request.query_params.get("fin")

        if not debut_str or not fin_str:
            return Response("debut and fin are required", status=400)

        debut = parse_datetime(debut_str)
        fin = parse_datetime(fin_str)

        if fin <= debut:
            return Response("start must be after debut", status=400)

        if not salle.exist():
            return Response("class doesnot exist", status=404)

        # now we get all confirmed reservations strictly inside the period
        reservations = Reservation.objects.filter(salle=salle,statut=Reservation.Statut.CONFIRMEE,debut__gte=debut,fin__lte=fin,)

        time_reserved = 0
        for r in reservations:
            time_reserved += (r.fin - r.debut)

        period_duration = fin - debut
        rate = time_reserved / period_duration

        return Response({"taux_occupation": rate})




