from django.db import models
from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone


class Offre(models.Model):
    expedition = models.ForeignKey(
        'ExpeditionApp.Expedition',
        on_delete=models.CASCADE,
        related_name='offres'
    )

    transporteur = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='offres'
    )

    vehicule = models.ForeignKey(
        Vehicule,
        on_delete=models.CASCADE,
        related_name='offres',
        null=True,
        blank=True
    )

    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01, message="Le prix doit etre superieur a 0")])
    delai_jours = models.PositiveIntegerField(validators=[MinValueValidator(1, message="Le delai doit etre un nombre positif")])

    statut = models.CharField(
        max_length=20,
        choices=[
            ('proposee', 'Proposee'),
            ('acceptee', 'Acceptee'),
            ('refusee', 'Refusee'),
            ('retiree', 'Retiree'),
        ],
        default='proposee'
    )

    date_proposition = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        # Regle 1: Une offre ne peut être créée que par une entreprise dont type_entreprise = transporteur
        if self.transporteur_id and self.transporteur.type_entreprise != "transporteur":
            raise ValidationError({'transporteur': "Une offre ne peut etre faite que par une entreprise de type transporteur"})

        # Regle 2: Le véhicule associé à une offre doit appartenir à la même entreprise que le transporteur de l'offre
        if self.vehicule and self.vehicule.entreprise_id != self.transporteur_id:
            raise ValidationError({'vehicule': "Le vehicule doit appartenir a l'entreprise transporteur de l'offre"})

        # Regle 3: Une expédition ne peut recevoir de nouvelles offres que si son statut est publiee
        if self.pk is None and self.expedition_id and self.expedition.statut != 'publiee':
            raise ValidationError({'expedition': "Une expedition ne peut recevoir d'offres que si son statut est publiee"})

        # Regle 4: Une entreprise ne peut pas avoir deux offres au statut proposee actives simultanément sur la même expédition
        if self.statut == 'proposee' and Offre.objects.filter(expedition_id=self.expedition_id, transporteur_id=self.transporteur_id, statut="proposee").exclude(pk=self.pk).exists():
            raise ValidationError({'transporteur': "Cette entreprise a déjà une offre proposee sur cette expédition"})
        # Regle 6: Un véhicule dont disponible = False ne peut pas être proposé sur une nouvelle offre.
        if self.vehicule and self.vehicule.disponible == False:
            raise ValidationError({'vehicule': "Le vehicule n'est pas disponible pour une nouvelle offre"})
        # Regle 7
        if self.vehicule_id and self.expedition_id:
            poids = self.expedition.poids_kg
            type_vehicule = self.vehicule.type_vehicule
            if type_vehicule == 'camionnette' and poids > 1500:
                raise ValidationError({'vehicule': "Le poids de l'expedition dépasse la capacité maximale d'une camionnette (1 500 kg)"})
            if type_vehicule == 'fourgon' and poids > 3500:
                raise ValidationError({'vehicule': "Le poids de l'expedition dépasse la capacité maximale d'un fourgon (3 500 kg)"})
            if type_vehicule == 'camion_porteur' and (poids < 3500 or poids > 19000):
                raise ValidationError({'vehicule': "Le poids de l'expedition n'est pas compatible avec un camion porteur (3 500 à 19 000 kg)"})
            if type_vehicule == 'semi_remorque' and (poids < 1900 or poids > 26000):
                raise ValidationError({'vehicule': "Le poids de l'expedition n'est pas compatible avec une semi-remorque (1 900 à 26 000 kg)"})

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.statut == 'acceptee' and self.pk:
            original = Offre.objects.get(pk=self.pk)
            if original.statut != 'acceptee':
                self.expedition.statut = 'attribuee'
                self.expedition.save()
                Offre.objects.filter(expedition_id=self.expedition_id, statut='proposee').exclude(pk=self.pk).update(statut='refusee')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Offre {self.id} - {self.expedition.reference} - {self.transporteur.raison_sociale}"