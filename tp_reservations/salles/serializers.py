"""Tache 1 et 2 : serializers et validation.

A FAIRE :
  - SalleSerializer (ModelSerializer)
  - ReservationSerializer (ModelSerializer) :
      * le champ `utilisateur` est en LECTURE SEULE (il sera renseigne par la vue)
      * validation : `fin` strictement apres `debut`
      * validation : pas de chevauchement avec une autre reservation CONFIRMEE
        de la meme salle
"""
from rest_framework import serializers
from datetime import  datetime

from .models import Reservation, Salle  # noqa: F401  (a utiliser)

# TODO : votre code ici

class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = ["nom", "capacite", "batiment"]


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ["id", "salle", "utilisateur", "debut", "fin", "motif", "statut", "cree_le"]
        read_only_fields = ["utilisateur"]


    def validate(self, data):
        if data["fin"] <= data["debut"]:
            raise serializers.ValidationError("The End date should be after the start date")

        # checking if they dont overlap
        # get all the reservations for that class that are still pending
        reservations = Reservation.objects.filter(salle=data["salle"], fin__gt=datetime.now(),
                                                      statut=Reservation.Statut.CONFIRMEE)
        for r in reservations:
            if data["debut"] < r.fin and data["fin"] > r.debut:
                raise serializers.ValidationError("This time slot overlaps with an existing confirmed reservation")

        return data

