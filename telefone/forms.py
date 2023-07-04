from django import forms
from telefone.models import Telefone

class TelefoneForms(forms.ModelForm):
    class Meta:
        model = Telefone
        fields = ('id',
                  'numero_telefone',
                  'apelido',
                  'nome_jovem',
                  'idade_jovem',
                  'escolaridade',
                  'turno',
                  'telefone_jovem',
                  'nome_responsavel',
                  'telefone_responsavel')

        widgets = {
            'numero_telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'apelido': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_jovem': forms.Textarea(attrs={'class': 'form-control'}),
            'idade_jovem': forms.Select(attrs={'class': 'form-control'}),
            'escolaridade': forms.TextInput(attrs={'class': 'form-control'}),
            'turno': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone_jovem': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone_responsavel': forms.TextInput(attrs={'class': 'form-control'}),
        }

