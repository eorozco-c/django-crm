from django.db import models
from apps.empresas.models import Empresa
from apps.usuarios.models import Usuario

class TipoRequerimiento(models.Model):
    nombre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


# Create your models here.
class Requerimiento(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50, null=True, blank=True)
    estado = models.BooleanField(default=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="requerimientos_empresa")
    created_by = models.CharField(max_length=255)
    tipo = models.ForeignKey(TipoRequerimiento, on_delete=models.CASCADE, related_name="requerimientos_tipo", null=True, blank=True)
    cumple = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    comentario = models.TextField()
    requerimiento = models.ForeignKey(Requerimiento, on_delete=models.CASCADE, related_name="comentarios_requerimiento")
    created_by = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="comentarios_usuario")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comentario