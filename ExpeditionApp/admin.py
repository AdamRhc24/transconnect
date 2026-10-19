
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from django.utils import timezone

from .models import Expedition
from OffreApp.models import Offre



class EnRetardFilter(admin.SimpleListFilter):
    title = 'en retard'
    parameter_name = 'en_retard'
    def lookups(self, request, model_admin):
        return [('oui', 'Oui'), ('non', 'Non')]
    def queryset(self, request, queryset):
        if self.value() == 'oui':
            return queryset.filter(statut='publiee', date_souhaitee__lt=timezone.now().date())
        if self.value() == 'non':
            return queryset.exclude(statut='publiee', date_souhaitee__lt=timezone.now().date())
        return queryset



class OffreInline(admin.TabularInline):
    model = Offre
    extra = 0
    can_delete = False

    fields = (
        "transporteur",
        "vehicule",
        "prix",
        "delai_jours",
        "statut",
        "date_proposition",
    )
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False




@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "entreprise",
        "ville_depart",
        "ville_arrivee",
        "statut",
        "date_souhaitee"
    )
    list_filter = ("statut", "ville_depart", "ville_arrivee", EnRetardFilter)
    search_fields = (
        "reference",
        "entreprise__raison_sociale",
    )
    list_editable = ("statut",)
    ordering = ("-created_at",)
    date_hierarchy = "date_souhaitee"
    list_per_page = 25

    autocomplete_fields = ("entreprise",)
    readonly_fields = ("reference", "created_at", "updated_at")
    inlines = (OffreInline,)

    fieldsets = (
        ("Informations générales", {
            "fields": (
                "reference",
                "entreprise",
                "ville_depart",
                "ville_arrivee",
                "description",
            )
        }),
        ("Conditions de transport", {
            "fields": ("poids_kg", "date_souhaitee")
        }),
        ("Suivi", {
            "fields": ("statut", "created_at", "updated_at")
        }),
    )

    @admin.display(description="Statut", ordering="statut")
    def statut_badge(self, obj):
        colors = {
            "publiee": "#2563eb",
            "attribuee": "#7c3aed",
            "en_cours": "#d97706",
            "livree": "#15803d",
            "annulee": "#dc2626",
        }
        color = colors.get(obj.statut, "#6b7280")

        return format_html(
            '<span style="background-color:{}; color:white; '
            'padding:3px 9px; border-radius:10px; font-weight:bold;">{}</span>',
            color,
            obj.get_statut_display(),
        )

    @admin.action(description="Clôturer les expéditions sélectionnées")
    def cloturer_expeditions(self, request, queryset):
        traitees = 0
        erreurs = 0

        for expedition in queryset:
            if expedition.statut != "en_cours":
                continue

            expedition.statut = "livree"

            try:
                expedition.full_clean()
                expedition.save()
                traitees += 1
            except ValidationError:
                erreurs += 1

        self.message_user(
            request,
            f"{traitees} expédition(s) clôturée(s). "
            f"{erreurs} erreur(s) de validation.",
            level=messages.SUCCESS if erreurs == 0 else messages.WARNING,
        )

    actions = ("cloturer_expeditions",)
