from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.empresas.models import Empresa
from apps.usuarios.models import Usuario
from apps.articulos.models import Articulo

import psutil

from apps.usuarios.models import Usuario
# Create your views here.
def index(request):
    if request.method == "GET":
        if Empresa.objects.count() == 0:
            return redirect("empresas:crear")
        if Usuario.objects.count() == 0:
            return redirect("usuarios:registrar")
        if request.user.is_authenticated:
            articulos = Articulo.objects.filter(empresa=request.user.empresa, stock__lte=5)
            if articulos.count() > 0:
                #save in session
                request.session["articulos"] = True
            return redirect("master:menu")
    return redirect("usuarios:login")

@login_required(login_url='/')
def menu(request):
    return redirect("usuarios:perfil" , pk=request.user.id)
