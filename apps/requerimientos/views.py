from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Comentario, Requerimiento
from .forms import FormularioRequerimiento, FormularioComentario

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
            'nombre': requerimiento.nombre,
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
        return Requerimiento.objects.filter(empresa=self.request.user.empresa, estado=False)

    def get_context_data(self, **kwargs):
        context = super(ListHistorial, self).get_context_data(**kwargs)
        context["appname"] = "requerimientos_historial"
        return context

    def get(self, request):
        return super(ListHistorial, self).get(request)

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

@LoginRequiredMixin(login_url="/")
def list_comentarios(request, pk):
    if request.method == "GET":
        try:
            requerimiento = Requerimiento.objects.get(id=pk)
            comentarios = Comentario.objects.filter(requerimiento=requerimiento)
        except:
            return redirect("requerimientos:index")
        context={
            'comentarios' : comentarios,
        }
        return JsonResponse(context)
    return redirect("requerimientos:index")