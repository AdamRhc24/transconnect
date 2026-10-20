
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Utilisateur, Entreprise
from VehiculeApp.models import Vehicule


admin.site.site_header = 'TransConnect -- Administration'
admin.site.site_title = 'TransConnect'
admin.site.index_title = "Tableau de bord"


class VehiculeInline(admin.TabularInline):
    model = Vehicule
    extra = 1
    fields = (
        "immatriculation",
        "type_vehicule",
        "capacite_kg",
        "disponible",
    )
    show_change_link = True


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = (
        "user_id",
        "username",
        "email",
        "role",
        "telephone",
        "is_active",
        "created_at",
    )
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("user_id", "username", "email", "telephone")
    list_editable = ("role",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 25
    readonly_fields = ("user_id", "created_at", "updated_at", "last_login", "date_joined")

    fieldsets = (
        ("Identification", {
            "fields": ("user_id", "username", "email", "telephone")
        }),

        ("Permissions", {
            "fields": (
                "role",
                "password",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Dates", {
            "fields": ("last_login", "date_joined", "created_at", "updated_at")
        }),
    )

    add_fieldsets = (
        ("Création du compte", {
            "classes": ("wide",),
            "fields": (
                "username",
                "usable_password",
                "email",
                "telephone",
                "role",
                "password1",
                "password2",
            ),
        }),
    )


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = (
        "raison_sociale",
        "matricule_fiscale",
        "type_entreprise",
        "utilisateur",
        "created_at",
    )
    list_filter = ("type_entreprise",)
    search_fields = (
        "raison_sociale",
        "matricule_fiscale",
        "utilisateur__username",
        "utilisateur__email",
    )
    list_editable = ("type_entreprise",)
    ordering = ("raison_sociale",)
    date_hierarchy = "created_at"
    list_per_page = 25
    # autocomplete_fields = ("utilisateur",)
    readonly_fields = ("created_at", "updated_at")
    inlines = (VehiculeInline,)

    fieldsets = (
        ("Informations de l'entreprise", {
            "fields": (
                "raison_sociale",
                "matricule_fiscale",
                "type_entreprise",
                "adresse",
            )
        }),
        ("Responsable", {
            "fields": ("utilisateur",)
        }),
        ("Suivi", {
            "fields": ("created_at", "updated_at")
        }),
    )
