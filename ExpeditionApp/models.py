from django.db import models
from EntrepriseApp.models import Entreprise

class Expedition(models.Model):
    reference = models.CharField(max_length=50, editable=False, unique=True, blank=True)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100,)
    poids_kg = models.DecimalField(max_digits=10, decimal_places=2)
    date_souhaitee = models.DateField()
    description = models.TextField(blank=True, null=True)
    
    statut = models.CharField(
        max_length=20, 
        choices=[
            ('publiee', 'Publiee'),
            ('attribuee', 'Attribuee'),
            ('en_cours', 'En cours'),
            ('livree', 'Livree'),
            ('annulee', 'Annulee'),
        ], 
        default='publiee',
        verbose_name="Statut"
    )
    
    entreprise_chargeur = models.ForeignKey(
        Entreprise, 
        on_delete=models.CASCADE, 
        related_name='expeditions',
    )

    def save(self, *args, **kwargs):
        if not self.reference:
            count = Expedition.objects.count() + 1
            self.reference = f"EXP-{count:04d}"
        
        super().save(*args, **kwargs)

