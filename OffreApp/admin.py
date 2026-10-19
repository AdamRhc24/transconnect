from django.contrib import admin
from .models import Offre



# Register your models here.


admin.site.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('expedition', 'delai_jours', 'statut')
    list_filter = ('statut')
    search_fields = ('expedition__reference', 'transporteur__raison_sociale', 'vehicule__id')
    ordering = ('statut', 'vehicule')