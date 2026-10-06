from django.db import models
from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule

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
        related_name='offres'
    )

    prix = models.DecimalField(max_digits=10, decimal_places=2)
    delai = models.CharField(max_length=100)
    
    statut = models.CharField(
        max_length=20, 
        choices=[
            ('en_attente', 'En attente'),
            ('acceptee', 'Acceptee'),
            ('refusee', 'Refusee'),
        ], 
        default='en_attente'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
