from django import forms
from OffreApp.models import Offre


class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = "__all__"
        exclude = ['id', 'date_proposition', 'created_at', 'updated_at']
        widgets = {
            'prix': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01', 'placeholder': 'Ex: 1250.00'}),
            'delai_jours': forms.NumberInput(attrs={'min': '1', 'placeholder': 'Ex: 3'}),
            'expedition': forms.Select(attrs={}),
            'transporteur': forms.Select(attrs={}),
            'vehicule': forms.Select(attrs={}),
        }
