from django.contrib import admin
from .models import Requerimiento, TipoRequerimiento

# Register your models here.

admin.site.register(Requerimiento)
admin.site.register(TipoRequerimiento)