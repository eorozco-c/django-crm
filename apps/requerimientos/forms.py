from django import forms
from .models import Requerimiento
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class FormularioRequerimiento(forms.ModelForm):
    
        class Meta:
            model = Requerimiento
            fields = ["titulo", "tipo","descripcion","created_by", "estado"]

            labels = {
                "titulo": "Titulo",
                "tipo": "Tipo Requerimiento",
                "descripcion": "Descripción",
                "estado": "Estado",
                "created_by": "Nombre de quien crea el requerimiento",
            }
    
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                 *self.fields,
            Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto mt-2')
            )