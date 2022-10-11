from django import forms
from .models import Empresa
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from apps.validaciones import validarLongitud
class FormularioEmpresa(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = ["nombre","logo"]

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        validarLongitud(nombre,"nombre",2,15)
        return nombre

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                'nombre', css_class='form-group col-md-12 mb-3'
            ),
            Row(
                'logo', css_class='form-group col-md-12 mb-3'
            ),  
            Submit('submit', 'Enviar', css_class='btn btn-primary')
    )
