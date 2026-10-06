from django.db import models
from EntrepriseApp.models import Entreprise

# Create your models here.

class Vehicule(models.Model):
    immatriculation = models.charField(max_length=20, unique=True)
    type_vehicule = models.charField(max_length = 50, choices=[
        ('camionnette', 'Camionnette'),
        ('fourgon', 'Fourgon'),
        ('camion porteur', 'Camion Proteur'),
        ('semi-remorque', 'Semi-remorque')
    ], blank=False, null=False)
    capacite_kg = models.IntegerField()
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='vehicules'
    )   
