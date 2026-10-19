
from django.contrib import admin

from .models import Vehicule


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = (
        "immatriculation",
        "type_vehicule",
        "capacite_kg",
        "entreprise",
        "disponible",
        "created_at",
    )
    list_filter = ("type_vehicule", "disponible")
    search_fields = (
        "immatriculation",
        "entreprise__raison_sociale",
        "entreprise__matricule_fiscale",
    )
    list_editable = ("disponible",)
    ordering = ("immatriculation",)
    date_hierarchy = "created_at"
    list_per_page = 25

    autocomplete_fields = ("entreprise",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Identification", {
            "fields": ("immatriculation", "type_vehicule", "entreprise")
        }),
        ("Capacité et disponibilité", {
            "fields": ("capacite_kg", "disponible")
        }),
        ("Suivi", {
            "fields": ("created_at", "updated_at")
        }),
    )
