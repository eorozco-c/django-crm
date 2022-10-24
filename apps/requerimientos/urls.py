from django.urls import  path
from . import views

app_name = "requerimientos"

urlpatterns = [
    path('', views.ListRequerimientos.as_view(), name="index"),
    path('crear', views.CrearRequerimiento.as_view(), name="crear"),
    path('editar/<int:pk>', views.EditRequerimiento.as_view(), name="editar"),
    path('predestroy/<int:pk>', views.predestroy, name="predestroy"),
    path('destroy/<int:pk>', views.destroy, name="destroy"),
    path('historial', views.ListHistorial.as_view(), name="historial"),
    path('editar_historial/<int:pk>', views.EditRequerimientoHist.as_view(), name="editar_historial"),
    path('agregar_comentarios/<int:pk>', views.CrearComentario.as_view(), name="agregar_comentarios"),
    path('list_comentarios/<int:pk>', views.list_comentarios, name="list_comentarios"),
    path('importar', views.importar, name="importar"),
]