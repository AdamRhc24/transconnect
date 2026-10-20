
from django.contrib import admin
from django.utils.html import format_html

from .models import Offre


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "expedition",
        "transporteur",
        "vehicule",
        "prix",
        "delai_jours",
        "statut",
        "statut_badge",
        "date_proposition",
    )
    list_filter = ("statut", "date_proposition")
    search_fields = (
        "expedition__reference",
        "transporteur__raison_sociale",
        "vehicule__immatriculation",
    )
    list_editable = ("statut",)
    ordering = ("-date_proposition",)
    date_hierarchy = "date_proposition"
    list_per_page = 25

    # autocomplete_fields = ("expedition", "transporteur", "vehicule")
    readonly_fields = ("date_proposition", "created_at", "updated_at")

    fieldsets = (
        ("Relations", {
            "fields": ("expedition", "transporteur", "vehicule")
        }),
        ("Conditions de l'offre", {
            "fields": ("prix", "delai_jours")
        }),
        ("Décision et suivi", {
            "fields": ("statut", "date_proposition", "created_at", "updated_at")
        }),
    )

    @admin.display(description="Statut", ordering="statut")
    def statut_badge(self, obj):
        colors = {
            "proposee": "#2563eb",
            "acceptee": "#15803d",
            "refusee": "#dc2626",
            "retiree": "#6b7280",
        }
        color = colors.get(obj.statut, "#6b7280")

        return format_html(
            '<span style="background-color:{}; color:white; '
            'padding:3px 9px; border-radius:10px; font-weight:bold;">{}</span>',
            color,
            obj.get_statut_display(),
        )
