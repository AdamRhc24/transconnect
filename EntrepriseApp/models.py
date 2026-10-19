from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

def validate_email(value):
    if not value:
        raise ValidationError("L'adresse e-mail ne peut pas être vide.")

    if not value.endswith("@gmail.com"):
        raise ValidationError("L'adresse e-mail doit se terminer par '@gmail.com'.")


matricule_fiscal_validator = RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
    message="Format Incorrect -(ex, 1234567AAM000 ou 1234567-A-A-M-000)."
)


class Utilisateur(AbstractUser):
    user_id = models.CharField(max_length=8, primary_key=True, editable=False)
    email = models.EmailField(unique=True, validators=[validate_email])
    telephone = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('chargeur', 'Chargeur'),
        ('transporteur', 'Transporteur')
    ], default='chargeur')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def _generate_entreprise_id(cls):
        annee = datetime.now().year
        prefix = f'{str(annee)[-2:]}entreprise'
        dernier_user = cls.objects.filter(user_id_startswith=prefix).order_by('user_id').last()
        compteur = int(dernier_user.user_id[-2:]) + 1 if dernier_user else 0
        if compteur > 99:
            raise ValidationError("Le nombre d'entreprises pour cette année a atteint la limite maximale de 99.")
        return f'{prefix}{compteur:02d}'
    @classmethod
    def _generate_user_id(cls):
        annee = datetime.now().year
        prefix = f'{str(annee)[-2:]}user'
        dernier_user = cls.objects.filter(user_id_startswith=prefix).order_by('user_id').last()
        compteur = int(dernier_user.user_id[-2:]) + 1 if dernier_user else 0
        if compteur > 99:
            raise ValidationError("Le nombre d'utilisateurs pour cette année a atteint la limite maximale de 99.")
        return f'{prefix}{compteur:02d}'
    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self._generate_user_id()
        self.full_clean()
        super().save(*args, **kwargs)


class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=255, null=False, blank=False)
    matricule_fiscale = models.CharField(max_length=17, unique=True, validators=[matricule_fiscal_validator])
    type_entreprise = models.CharField(max_length=100, choices=[
        ('chargeur', 'Chargeur'),
        ('transporteur', 'Transporteur')
    ], default='chargeur')
    adresse = models.TextField(validators=[
        MinLengthValidator(20, message="L'adresse doit contenir au moins 20 caractères"),
        MaxLengthValidator(300, message="L'adresse ne peut pas dépasser 300 caractères")
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    gerant = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='entreprise')

    def __str__(self):
        return self.raison_sociale