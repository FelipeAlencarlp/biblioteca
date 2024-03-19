from django import forms
from .models import Livros

class CadastroLivro(forms.ModelForm):
    class Meta:
        model = Livros
        fields = "__all__"

    # sobrescrevendo o método __init__()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # campos que não serão exibidos para o usuário
        self.fields['usuario'].widget = forms.HiddenInput()
        self.fields['slug'].widget = forms.HiddenInput()