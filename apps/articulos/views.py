from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Articulo
from .forms import FormularioArticulo
import pandas as pd


# Create your views here.
@method_decorator(login_required, name='dispatch')
class ListArticulos(ListView):
    model = Articulo
    template_name = "articulos/articulos_list.html"

    def get_queryset(self):
        return Articulo.objects.filter(empresa=self.request.user.empresa)

    def get_context_data(self, **kwargs):
        context = super(ListArticulos, self).get_context_data(**kwargs)
        context["appname"] = "Articulos"
        return context

    def get(self, request):
        return super(ListArticulos, self).get(request)

@method_decorator(login_required, name='dispatch')
class CrearArticulo(CreateView):
    model = Articulo
    template_name = "formularios/generico.html"
    form_class = FormularioArticulo

    def get_context_data(self, **kwargs):
        context = super(CrearArticulo, self).get_context_data(**kwargs)
        context["appname"] = "Articulos"
        return context

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super(CrearArticulo, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("articulos:index")

@method_decorator(login_required, name='dispatch')
class EditArticulo(UpdateView):
    model = Articulo
    template_name = "formularios/generico.html"
    form_class = FormularioArticulo

    def get_context_data(self, **kwargs):
        context = super(EditArticulo, self).get_context_data(**kwargs)
        context["appname"] = "Articulos"
        return context

    def get_success_url(self):
        return reverse_lazy("articulos:index")

@login_required(login_url="/")
def predestroy(request, pk):
    if request.method == "GET":
        try:
            articulo = Articulo.objects.get(id=pk)
        except:
            return redirect("articulos:index")
        context={
            'id' : articulo.id,
            'nombre': articulo.nombre,
        }
        return JsonResponse(context)
    return redirect("articulos:index")

@login_required(login_url="/")
def destroy(request, pk):
    if request.method == "GET":
        try:
            articulo = Articulo.objects.get(id=pk)
            articulo.delete()
        except:
            return redirect("articulos:index")
        return redirect("articulos:index")
    return redirect("articulos:index")

@login_required(login_url="/")
def importar(request):
    if request.method == "POST":
        archivo = request.FILES["archivo"]
        df = pd.read_excel(archivo)
        #update or create if same nombre
        # try:
        for index, row in df.iterrows():
            Articulo.objects.update_or_create(
                nombre = row["id"],
                defaults={
                    "descripcion": row["nombre"],
                    "stock": row["cantidad"],
                    "ubicacion": row["ubicacion"],
                    "visible_bodega": row["visible bodega"],
                    "empresa": request.user.empresa,
                    "articulo_estado_id": 1,
                }
            )
        # except:
        #     return redirect("articulos:index")    
        return redirect("articulos:index")
    return redirect("articulos:index")