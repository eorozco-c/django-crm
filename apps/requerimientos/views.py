from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Comentario, Requerimiento, TipoRequerimiento
from .forms import FormularioRequerimiento, FormularioComentario
import datetime
import pandas as pd

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ListRequerimientos(ListView):
    model = Requerimiento
    template_name = "requerimientos/requerimientos_list.html"

    def get_queryset(self):
        return Requerimiento.objects.filter(empresa=self.request.user.empresa, estado=True)

    def get_context_data(self, **kwargs):
        context = super(ListRequerimientos, self).get_context_data(**kwargs)
        context["appname"] = "requerimientos"
        return context

    def get(self, request):
        return super(ListRequerimientos, self).get(request)

@method_decorator(login_required, name='dispatch')
class CrearRequerimiento(CreateView):
    model = Requerimiento
    form_class = FormularioRequerimiento
    template_name = "formularios/generico.html"
    success_url = reverse_lazy("requerimientos:index")

    def get_context_data(self, **kwargs):
        context = super(CrearRequerimiento, self).get_context_data(**kwargs)
        context["appname"] = "requerimientos"
        return context

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super(CrearRequerimiento, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class EditRequerimiento(UpdateView):
    model = Requerimiento
    form_class = FormularioRequerimiento
    template_name = "formularios/generico.html"
    success_url = reverse_lazy("requerimientos:index")

    def get_context_data(self, **kwargs):
        context = super(EditRequerimiento, self).get_context_data(**kwargs)
        context["appname"] = "requerimientos"
        return context

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super(EditRequerimiento, self).form_valid(form)

@login_required(login_url="/")
def predestroy(request, pk):
    if request.method == "GET":
        try:
            requerimiento = Requerimiento.objects.get(id=pk)
        except:
            return redirect("requerimientos:index")
        context={
            'id' : requerimiento.id,
            'nombre': requerimiento.titulo,
            'descripcion': requerimiento.descripcion,
        }
        return JsonResponse(context)
    return redirect("articulos:index")

@login_required(login_url="/")
def destroy(request, pk):
    if request.method == "GET":
        try:
            requerimiento = Requerimiento.objects.get(id=pk)
            requerimiento.delete()
        except:
            return redirect("requerimientos:index")
        return redirect("requerimientos:index")
    return redirect("requerimientos:index")

@method_decorator(login_required, name='dispatch')
class ListHistorial(ListView):
    model = Requerimiento
    template_name = "requerimientos/requerimientos_historial.html"

    def get_queryset(self):
        fecha_ini = self.request.GET.get('fecha_ini')
        fecha_fin = self.request.GET.get('fecha_fin')
        if not fecha_ini or not fecha_fin:
            date_ini = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            date_end = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
        else:
            date_ini = datetime.datetime.strptime(fecha_ini, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
            date_end = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=0)
        return Requerimiento.objects.filter(empresa=self.request.user.empresa, estado=False, created_at__range=(date_ini, date_end))

    def get_context_data(self, **kwargs):
        context = super(ListHistorial, self).get_context_data(**kwargs)
        context["appname"] = "requerimientos_historial"
        fecha_ini = self.request.GET.get('fecha_ini')
        fecha_fin = self.request.GET.get('fecha_fin')
        if not fecha_ini or not fecha_fin:
            #date_ini for input type date
            date_ini = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            date_end = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
        else:
            date_ini = datetime.datetime.strptime(fecha_ini, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
            date_end = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=0)
        context["fecha_ini"] = date_ini
        context["fecha_fin"] = date_end
        return context


@method_decorator(login_required, name='dispatch')
class EditRequerimientoHist(UpdateView):
    model = Requerimiento
    form_class = FormularioRequerimiento
    template_name = "formularios/generico.html"
    success_url = reverse_lazy("requerimientos:historial")

    def get_context_data(self, **kwargs):
        context = super(EditRequerimientoHist, self).get_context_data(**kwargs)
        context["appname"] = "requerimientos"
        return context

    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super(EditRequerimientoHist, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class CrearComentario(CreateView):
    model = Comentario
    form_class = FormularioComentario
    template_name = "formularios/generico.html"
    success_url = reverse_lazy("requerimientos:index")

    #obtain pk requerimiento from url
    def get_initial(self):
        initial = super(CrearComentario, self).get_initial()
        initial['requerimiento'] = self.kwargs['pk']
        return initial

    def get_context_data(self, **kwargs):
        context = super(CrearComentario, self).get_context_data(**kwargs)
        context["appname"] = "comentarios"
        return context

    def form_valid(self, form):
        form.instance.requerimiento = Requerimiento.objects.get(id=self.kwargs['pk'])
        form.instance.created_by = self.request.user
        return super(CrearComentario, self).form_valid(form)

@login_required(login_url="/")
def list_comentarios(request, pk):
    if request.method == "GET":
        try:
            requerimiento = Requerimiento.objects.get(id=pk)
            comentarios = Comentario.objects.filter(requerimiento=requerimiento).values('id', 'comentario', 'created_by__username', 'created_at')
        except:
            return redirect("requerimientos:index")
        #obtain comentarios and created_by
        data = list(comentarios)
        context = {
            'comentarios': data,
        }
        return JsonResponse(data, safe=False)
    return redirect("requerimientos:index")

@login_required(login_url="/")
def importar(request):
    if request.method == "POST":
        try:
            archivo = request.FILES['archivo']
            if archivo:
                df = pd.read_excel(archivo)
                for index, row in df.iterrows():
                    requerimiento = Requerimiento()
                    requerimiento.titulo = row['titulo']
                    requerimiento.descripcion = row['descripcion']
                    requerimiento.created_by = row['creado por']
                    requerimiento.updated_at = row["fecha creacion"]
                    requerimiento.empresa = request.user.empresa
                    #tipo de requerimiento if not exist create
                    try:
                        tipo = TipoRequerimiento.objects.get(nombre__iexact=row['tipo'])
                    except:
                        tipo = TipoRequerimiento()
                        tipo.nombre = row['tipo']
                        tipo.save()
                    requerimiento.tipo = tipo
                    requerimiento.save()
        except:
            return redirect("requerimientos:index")
        return redirect("requerimientos:index")
    return redirect("requerimientos:index")