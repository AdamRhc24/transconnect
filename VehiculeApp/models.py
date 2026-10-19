from django.db import models
from EntrepriseApp.models import Entreprise
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Vehicule(models.Model):
    TYPE_VEHICULE_CHOICES = [
        ('camionnette', 'Camionnette / utilitaire léger'),
        ('fourgon', 'Fourgon'),
        ('camion_porteur', 'Camion porteur'),
        ('semi_remorque', 'Semi-remorque'),
    ]

    immatriculation = models.CharField(max_length=20, unique=True)
    type_vehicule = models.CharField(max_length=20, choices=TYPE_VEHICULE_CHOICES, default='camionnette')
    capacite_kg = models.PositiveIntegerField(validators=[MinValueValidator(1, message="La capacité doit être supérieure à 0")])
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='vehicules'
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.entreprise and self.entreprise.type_entreprise != 'transporteur':
            raise ValidationError({'entreprise': "Le véhicule doit appartenir à une entreprise de type transporteur"})
        
    def __str__(self):
        return self.immatriculation