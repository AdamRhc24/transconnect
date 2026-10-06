from django.db import models
from EntrepriseApp.models import Entreprise
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from datetime import timezone

class Expedition(models.Model):
    reference = models.CharField(max_length=50, editable=False, unique=True, blank=True)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100,)
    poids_kg = models.DecimalField(max_digits=10, decimal_places=2, validators = [MinValueValidator(0.001, message="Le poids doit etre superieur a 0")])
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


    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError({
                'entreprise': "Une expedition ne peut etre cree par une entreprise de type chargeur"
            })

    @classmethod
    def _generate_ref(cls):
        annee = timezone.now().strftime('%y')
        prefix = f"EXP_{annee}_"


        compteur = cls.objects.filter(reference_startswith=prefix).order_by('-reference').last()