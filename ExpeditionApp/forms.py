
from django import forms
from ExpeditionApp.models import Expedition

class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = Expedition
        fields = "__all__"
        exclude = ['reference', 'id', 'created_at', 'update_at']
        widgets = {"date_souhaitee":forms.DateInput(attrs={'type':'date'}, format="%Y-%m-%d")}