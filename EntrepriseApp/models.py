from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


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
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.user_id:
            annee = timezone.now().strftime('%y')
            prefix = f"{annee}user"
            last_user = Utilisateur.objects.filter(user_id__startswith=prefix).order_by('-user_id').first()
            if last_user:
                try:
                    last_num = int(last_user.user_id[-2:])
                    next_num = (last_num + 1) % 100
                except ValueError:
                    next_num = 1
            else:
                next_num = 1
            self.user_id = f"{prefix}{next_num:02d}"
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

    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='entreprise')

    def __str__(self):
        return self.raison_sociale