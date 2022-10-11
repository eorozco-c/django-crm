from django.urls import  path
from . import views

app_name = "articulos"

urlpatterns = [
    path('', views.ListArticulos.as_view(), name="index"),
    path('crear', views.CrearArticulo.as_view(), name="crear"),
    path('editar/<int:pk>', views.EditArticulo.as_view(), name="editar"),
    path('predestroy/<int:pk>', views.predestroy, name="predestroy"),
    path('destroy/<int:pk>', views.destroy, name="destroy"),
    path('importar', views.importar, name="importar"),
]