from django import forms
from .models import (Director,Writer,ProductionCompany)

# class ActForm(forms.ModelForm):
#     class Meta:
#         model = Actor
#         fields = '__all__'

class WriterForm(forms.ModelForm):
    class Meta:
        model = Writer
        fields = '__all__'

class DirecForm(forms.ModelForm):
    class Meta:
        model = Director
        fields='__all__'

class ProdForm(forms.ModelForm):
    class Meta:
        model = ProductionCompany
        fields = '__all__'