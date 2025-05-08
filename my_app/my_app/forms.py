from django import forms
from .models import StockAliment, Aliment

class StockAlimentForm(forms.ModelForm):
    class Meta:
        model = StockAliment
        fields = ['id_aliment', 'fournisseur_aliment', 'stock_entree', 'date_reception', 'prix_aliment']

    id_aliment = forms.ModelChoiceField(queryset=Aliment.objects.all(), label="Id Aliment")

# forms.py
from django import forms
from .models import Maladie

class MaladieForm(forms.ModelForm):
    class Meta:
        model = Maladie
        fields = ['nom_maladie', 'description_maladie']
        widgets = {
            'nom_maladie': forms.TextInput(attrs={
                'placeholder': 'Entrez le nom de la maladie',
                'class': 'form-control'
            }),
            'description_maladie': forms.Textarea(attrs={
                'placeholder': 'Entrez la description de la maladie',
                'class': 'form-control',
                'rows': 3
            }),
        }