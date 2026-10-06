from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.


def validate_email(value):
    if not value:
        raise ValidationError("L'adresse e-mail ne peut pas être vide.")

    if not value.endswith("@gmail.com"):
        raise ValidationError("L'adresse e-mail doit se terminer par '@gmail.com'.")


class Utilisateur(AbstractUser):
    user_id = models.CharField(max_length=8, primary_key=True)
    email = models.EmailField(unique = True, validators=[validate_email])
    telephone = models.CharField(max_length = 15, null=True, blank=True)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('chargeur', 'Chargeur'),
        ('transporteur', 'Transporteur')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

matricule_fiscal_validator = RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
    message="Format Incorrect -(ex, 1234567AAM000 ou 1234567-A-A-M-000)."
)


class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=255, null=False, blank= False, validators=[matricule_fiscal_validator])
    matricule_fiscale = models.CharField(max_length=17, unique=True)
    type_entreprise = models.CharField(max_length=100, choices=[
        ('chargeur', 'Chargeur'),
        ('transporteur', 'Transporteur')
    ],  default='char')

    adresse = models.TextField(MinLengthValidator(20, message="L'adresse doit contenir au moins 20 caractères"),
                               MaxLengthValidator(300, message="L'adresse ne peut pas dépasser 300 caractères")
                               
                               )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    gerant = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='entreprise')



