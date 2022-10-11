from django import forms
from .models import Articulo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class FormularioArticulo(forms.ModelForm):
    
        class Meta:
            model = Articulo
            fields = ["nombre","descripcion","stock"]
    
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            #all fields
            self.helper.layout = Layout(
                 *self.fields,
            Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto mt-2')
            )