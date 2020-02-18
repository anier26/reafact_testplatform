from django import forms
from model_app.models import Module



class ModelForm(forms.ModelForm):
    class Meta:
        model=Module
        fields=['project','name','describe']