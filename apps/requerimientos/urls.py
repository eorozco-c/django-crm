from django.urls import  path
from . import views

app_name = "requerimientos"

urlpatterns = [
    path('', views.ListRequerimientos.as_view(), name="index"),
    path('crear', views.CrearRequerimiento.as_view(), name="crear"),
    path('editar/<int:pk>', views.EditRequerimiento.as_view(), name="editar"),
    path('predestroy/<int:pk>', views.predestroy, name="predestroy"),
    path('destroy/<int:pk>', views.destroy, name="destroy"),
]