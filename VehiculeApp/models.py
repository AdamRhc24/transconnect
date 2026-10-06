from django.db import models
from EntrepriseApp.models import Entreprise
from django.core.validators import MinValueValidator

# Create your models here.

class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=20, unique=True)
    type_vehicule = models.CharField(max_length = 50, choices=[
        ('camionnette', 'Camionnette'),
        ('fourgon', 'Fourgon'),
        ('camion porteur', 'Camion Proteur'),
        ('semi-remorque', 'Semi-remorque')
    ], default = 'camionnette', blank=False, null=False)
    capacite_kg = models.IntegerField(validators=[MinValueValidator(100, message="La capacité doit être d'au moins 100 kg")])
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    proprietaire = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='vehicules'
    )
