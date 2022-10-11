from django.db import models
from apps.empresas.models import Empresa

# Create your models here.
class Articulo(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    stock = models.IntegerField()
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="articulos_empresa")

    def __str__(self):
        return self.nombre