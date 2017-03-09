from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Propietario, Paciente, Vacuna, Enfermedad, Antiparasitario
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import VacunaForm, EnfermedadForm, AntiparasitarioForm, PacienteForm
from django.contrib.auth.decorators import login_required
from .django_datatables_view_modificado.base_datatable_view import BaseDatatableView

# Create your views here.

@login_required(login_url="login/")
def home(request):
    return render(request, 'animalchic/main.html')

############################# Vistas Genericas para el modelo Propietario #############################



class PropietarioList(LoginRequiredMixin, TemplateView):
    model = Propietario
    template_name = 'animalchic/listing/propietario_list.html'

class PropietarioListJson(LoginRequiredMixin, BaseDatatableView):
    model = Propietario
    columns = ['propietario_nombre', 'direccion', 'telefono', 'observacion', 'show_url']
    order_columns = ['propietario_nombre', 'direccion', 'telefono', 'observacion']

    def get_initial_queryset(self):
        qs = super(PropietarioListJson, self).get_initial_queryset()
        return qs.filter(usuario=self.request.user.id)


    #
    # def get_initial_queryset(self):
    #     qs = super(PropietarioList, self).get_initial_queryset()
    #     return qs

    # def get_context_data(self, **kwargs):
    #     context = super(PropietarioList, self).get_context_data(**kwargs)
    #     table = PropietarioTable()
    #     context['propietarios'] = table
    #     return context

class PropietarioDetail(LoginRequiredMixin, DetailView):
    model = Propietario
    template_name = 'animalchic/details/propietario_detail.html'

class PropietarioCreation(LoginRequiredMixin, CreateView):
    model = Propietario
    template_name = 'animalchic/forms/propietario_form.html'
    success_url = reverse_lazy('animalchic:list_propietarios')
    fields = ['propietario_nombre', 'direccion', 'telefono', 'observacion']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario = self.request.user
        self.object.save()
        return super(PropietarioCreation, self).form_valid(form)

class PropietarioUpdate(LoginRequiredMixin, UpdateView):
    model = Propietario
    template_name = 'animalchic/forms/propietario_form.html'
    success_url = reverse_lazy('animalchic:list_propietarios')
    fields = ['propietario_nombre', 'direccion', 'telefono', 'observacion']

    def get_context_data(self, **kwargs):
        context = super(PropietarioUpdate, self).get_context_data(**kwargs)
        context['edit'] = True
        context['propietario_id'] = self.kwargs['pk']
        return context



############################# Vistas Genericas para el modelo Paciente ###############################

class PacienteList(LoginRequiredMixin, TemplateView):
    model = Paciente
    template_name = 'animalchic/listing/paciente_list.html'

    # def get_queryset(self):
    #     if 'pk_propietario' in self.kwargs.keys():
    #         return Paciente.objects.filter(propietario__id=self.kwargs['pk_propietario'])
    #     else:
    #         return Paciente.objects.all()
    #
    # def get_context_data(self, **kwargs):
    #     context = super(PacienteList, self).get_context_data(**kwargs)
    #     if 'pk_propietario' in self.kwargs.keys():
    #         context['nuevo_propietario_paciente'] = True
    #         context['propietario_id'] = self.kwargs['pk_propietario']
    #     return context

class PacienteListJson(BaseDatatableView):
    model = Paciente
    columns = ['propietario.propietario_nombre', 'paciente_nombre', 'especie', 'raza', 'sexo', 'show_url']
    order_columns = ['propietario.propietario_nombre', 'paciente_nombre', 'especie', 'raza', 'sexo']

    def get_initial_queryset(self):
        qs = super(PacienteListJson, self).get_initial_queryset()
        return qs.filter(usuario=self.request.user.id)

    # def get_initial_queryset(self):
    #     qs = super(PacienteListJson, self).get_initial_queryset()
    #     if 'pk_propietario' in self.kwargs.keys():
    #         return qs.filter(propietario__id=self.kwargs['pk_propietario'])
    #     else:
    #         return qs

class PacienteDetail(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = 'animalchic/details/paciente_detail.html'

    #def get_context_data(self, **kwargs):
        #context = super(PacienteDetail, self).get_context_data(**kwargs)

class PacienteCreation(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'animalchic/forms/paciente_form.html'
    nuevo_paciente_propietario = False
    pk_propietario = None

    def get_propietario_nombre(self, pk_propietario):
        return Propietario.objects.get(pk=pk_propietario).propietario_nombre

    def get_context_data(self, **kwargs):
        context = super(PacienteCreation, self).get_context_data(**kwargs)
        if 'pk_propietario' in self.kwargs.keys():
            context['nuevo_propietario_paciente'] = True
            context['propietario_id'] = self.kwargs['pk_propietario']
            context['propietario_nombre'] = self.get_propietario_nombre(self.kwargs['pk_propietario'])
            self.nuevo_paciente_propietario = True
            self.pk_propietario = self.kwargs['pk_propietario']
        return context


    def get_success_url(self):
        context = self.get_context_data(**self.kwargs)
        if 'nuevo_propietario_paciente' in context.keys():
            return reverse_lazy('animalchic:list_propietario_pacientes', kwargs={'pk_propietario':context['propietario_id']})
        else:
            return reverse_lazy('animalchic:list_pacientes')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario = self.request.user
        self.object.save()
        return super(PacienteCreation, self).form_valid(form)

class PacienteUpdate(LoginRequiredMixin, UpdateView):
    model = Paciente
    template_name = 'animalchic/forms/paciente_form.html'
    form_class = PacienteForm

    def get_context_data(self, **kwargs):
        context = super(PacienteUpdate, self).get_context_data(**kwargs)
        context['paciente_id'] = self.kwargs['pk']
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('animalchic:detail_paciente', kwargs={'pk_paciente':self.kwargs['pk']})



############################# Vistas Genericas para el modelo Vacuna ###############################

class VacunaList(LoginRequiredMixin, ListView):
    model = Vacuna
    template_name = 'animalchic/listing/vacuna_list.html'

    def get_paciente_nombre(self, pk_paciente):
        return Paciente.objects.get(pk=pk_paciente).paciente_nombre

    def get_queryset(self):
        qs = super(VacunaList, self).get_queryset()
        return qs.filter(paciente__id=self.kwargs['pk_paciente'])

    def get_context_data(self, **kwargs):
        context = super(VacunaList, self).get_context_data(**kwargs)
        context['paciente_id'] = self.kwargs['pk_paciente']
        context['paciente_nombre'] = self.get_paciente_nombre(self.kwargs['pk_paciente'])
        return context

class VacunaListJson(BaseDatatableView):
    model = Vacuna
    columns = ['descripcion', 'fecha', 'proxima_vacuna', 'show_url']
    order_columns = ['descripcion', 'fecha', 'proxima_vacuna']

    def get_initial_queryset(self):
        qs = super(VacunaListJson, self).get_initial_queryset()
        return qs.filter(paciente__id=self.kwargs['pk_paciente'], usuario=self.request.user.id)

class VacunaDetail(LoginRequiredMixin, DetailView):
    model = Vacuna
    template_name = 'animalchic/details/vacuna_detail.html'

    def get_object(self, queryset=None):
        return Vacuna.objects.get(pk=self.kwargs['pk_vacuna'])

    def get_context_data(self, **kwargs):
        context = super(VacunaDetail, self).get_context_data(**kwargs)
        context['paciente_id'] = self.kwargs['pk_paciente']
        return context

class VacunaCreation(LoginRequiredMixin, CreateView):
    model = Vacuna
    form_class = VacunaForm
    template_name = 'animalchic/forms/vacuna_form.html'
    paciente = object = None

    def get_paciente(self):
        if not self.paciente:
            self.paciente = get_object_or_404(Paciente, id=self.kwargs['pk_paciente'])
        return self.paciente

    def get_context_data(self, **kwargs):
        context = super(VacunaCreation, self).get_context_data(**kwargs)
        context['paciente_nombre'] = Paciente.objects.get(pk=self.kwargs['pk_paciente'])
        context['paciente_id'] = self.kwargs['pk_paciente']
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.paciente = self.get_paciente()
        self.object.usuario = self.request.user
        self.object.save()
        return super(VacunaCreation, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('animalchic:list_vacunas', kwargs={'pk_paciente': self.get_paciente().id})

class VacunaUpdate(LoginRequiredMixin, UpdateView):
    model = Vacuna
    template_name = 'animalchic/forms/vacuna_form.html'
    form_class = VacunaForm
    paciente = object = None

    def get_paciente(self):
        if not self.paciente:
            self.paciente = get_object_or_404(Paciente, id=self.kwargs['pk_paciente'])
        return self.paciente

    def get_object(self, queryset=None):
        return Vacuna.objects.get(pk=self.kwargs['pk_vacuna'])

    def get_context_data(self, **kwargs):
        context = super(VacunaUpdate, self).get_context_data(**kwargs)
        context['paciente_nombre'] = Paciente.objects.get(pk=self.kwargs['pk_paciente'])
        context['paciente_id'] = self.kwargs['pk_paciente']
        context['edit'] = True
        context['vacuna_id'] = self.kwargs['pk_vacuna']
        return context

    def get_success_url(self):
        return reverse_lazy('animalchic:list_vacunas', kwargs={'pk_paciente': self.get_paciente().id})


############################# Vistas Genericas para el modelo Enfermedad ###############################

class EnfermedadList(LoginRequiredMixin, ListView):
    model = Enfermedad
    template_name = 'animalchic/listing/enfermedad_list.html'

    def get_paciente_nombre(self, pk_paciente):
        return Paciente.objects.get(pk=pk_paciente).paciente_nombre

    def get_queryset(self):
        qs = super(EnfermedadList, self).get_queryset()
        return qs.filter(paciente__id=self.kwargs['pk_paciente'])

    def get_context_data(self, **kwargs):
        context = super(EnfermedadList, self).get_context_data(**kwargs)
        context['paciente_id'] = self.kwargs['pk_paciente']
        context['paciente_nombre'] = self.get_paciente_nombre(self.kwargs['pk_paciente'])
        return context

class EnfermedadListJson(BaseDatatableView):
    model = Enfermedad
    columns = ['descripcion', 'fecha', 'tratamiento','show_url']
    order_columns = ['descripcion', 'fecha', 'tratamiento']

    def get_initial_queryset(self):
        qs = super(EnfermedadListJson, self).get_initial_queryset()
        return qs.filter(paciente__id=self.kwargs['pk_paciente'], usuario=self.request.user.id)

class EnfermedadDetail(LoginRequiredMixin, DetailView):
    model = Enfermedad
    template_name = 'animalchic/details/enfermedad_detail.html'

    def get_object(self, queryset=None):
        return Enfermedad.objects.get(pk=self.kwargs['pk_enfermedad'])

    def get_context_data(self, **kwargs):
        context = super(EnfermedadDetail, self).get_context_data(**kwargs)
        context['paciente_id'] = self.kwargs['pk_paciente']
        return context

class EnfermedadCreation(LoginRequiredMixin, CreateView):
    model = Enfermedad
    template_name = 'animalchic/forms/enfermedad_form.html'
    form_class = EnfermedadForm
    paciente = object = None

    def get_paciente(self):
        if not self.paciente:
            self.paciente = Paciente.objects.get(pk=self.kwargs['pk_paciente'])
        return self.paciente

    def get_context_data(self, **kwargs):
        context = super(EnfermedadCreation, self).get_context_data(**kwargs)
        context['paciente_nombre'] = Paciente.objects.get(pk=self.kwargs['pk_paciente'])
        context['paciente_id'] = self.kwargs['pk_paciente']
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.paciente = self.get_paciente()
        self.object.usuario = self.request.user
        self.object.save()
        return super(EnfermedadCreation, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('animalchic:list_enfermedades', kwargs={'pk_paciente':self.get_paciente().id})

class EnfermedadUpdate(LoginRequiredMixin, UpdateView):
    model = Enfermedad
    template_name = 'animalchic/forms/enfermedad_form.html'
    form_class = EnfermedadForm
    paciente = object = None

    def get_paciente(self):
        if not self.paciente:
            self.paciente = Paciente.objects.get(pk=self.kwargs['pk_paciente'])
        return self.paciente

    def get_context_data(self, **kwargs):
        context = super(EnfermedadUpdate, self).get_context_data(**kwargs)
        context['paciente_nombre'] = Paciente.objects.get(pk=self.kwargs['pk_paciente'])
        context['paciente_id'] = self.kwargs['pk_paciente']
        context['edit'] = True
        context['enfermedad_id'] = self.kwargs['pk_enfermedad']
        return context

    def get_object(self, queryset=None):
        return Enfermedad.objects.get(pk=self.kwargs['pk_enfermedad'])

    def get_success_url(self):
        return reverse_lazy('animalchic:list_enfermedades', kwargs={'pk_paciente': self.get_paciente().id})


############################# Vistas Genericas para el modelo Antiparasitarios ###############################

class AntiparasitarioList(LoginRequiredMixin, ListView):
    model = Antiparasitario
    template_name = 'animalchic/listing/antiparasitario_list.html'

    def get_paciente_nombre(self, pk_paciente):
        return Paciente.objects.get(pk=pk_paciente).paciente_nombre

    def get_queryset(self):
        qs = super(AntiparasitarioList, self).get_queryset()
        return qs.filter(paciente__id=self.kwargs['pk_paciente'])

    def get_context_data(self, **kwargs):
        context = super(AntiparasitarioList, self).get_context_data(**kwargs)
        context['paciente_id'] = self.kwargs['pk_paciente']
        context['paciente_nombre'] = self.get_paciente_nombre(self.kwargs['pk_paciente'])
        return context

class AntiparasitarioListJson(BaseDatatableView):
    model = Antiparasitario
    columns = ['fecha', 'vermifugos', 'proxima_aplicacion','show_url']
    order_columns = ['fecha', 'vermifugos', 'proxima_aplicacion']

    def get_initial_queryset(self):
        qs = super(AntiparasitarioListJson, self).get_initial_queryset()
        return qs.filter(paciente__id=self.kwargs['pk_paciente'], usuario=self.request.user.id)

class AntiparasitarioDetail(LoginRequiredMixin, DetailView):
    model = Antiparasitario
    template_name = 'animalchic/details/antiparasitario_detail.html'



    def get_object(self, queryset=None):
        return Antiparasitario.objects.get(pk=self.kwargs['pk_antiparasitario'])

    def get_context_data(self, **kwargs):
        context = super(AntiparasitarioDetail, self).get_context_data(**kwargs)
        context['paciente_id'] = self.kwargs['pk_paciente']
        return context

class AntiparasitarioCreation(LoginRequiredMixin, CreateView):
    model = Antiparasitario
    template_name = 'animalchic/forms/antiparasitario_form.html'
    form_class = AntiparasitarioForm
    paciente = object = None

    def get_paciente(self):
        if not self.paciente:
            self.paciente = Paciente.objects.get(pk=self.kwargs['pk_paciente'])
        return self.paciente

    def get_context_data(self, **kwargs):
        context = super(AntiparasitarioCreation, self).get_context_data(**kwargs)
        context['paciente_nombre'] = Paciente.objects.get(pk=self.kwargs['pk_paciente'])
        context['paciente_id'] = self.kwargs['pk_paciente']
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.paciente = self.get_paciente()
        self.object.usuario = self.request.user
        self.object.save()
        return super(AntiparasitarioCreation, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('animalchic:list_antiparasitarios', kwargs={'pk_paciente': self.get_paciente().id})

class AntiparasitarioUpdate(LoginRequiredMixin, UpdateView):
    model = Antiparasitario
    template_name = 'animalchic/forms/antiparasitario_form.html'
    form_class = AntiparasitarioForm
    paciente = object = None

    def get_paciente(self):
        if not self.paciente:
            self.paciente = Paciente.objects.get(pk=self.kwargs['pk_paciente'])
        return self.paciente

    def get_context_data(self, **kwargs):
        context = super(AntiparasitarioUpdate, self).get_context_data(**kwargs)
        context['paciente_nombre'] = Paciente.objects.get(pk=self.kwargs['pk_paciente'])
        context['paciente_id'] = self.kwargs['pk_paciente']
        context['edit'] = True
        context['antiparasitario_id'] = self.kwargs['pk_antiparasitario']
        return context

    def get_object(self, queryset=None):
        return Antiparasitario.objects.get(pk=self.kwargs['pk_antiparasitario'])

    def get_success_url(self):
        return reverse_lazy('animalchic:list_antiparasitarios', kwargs={'pk_paciente': self.get_paciente().id})


#Funciones para eliminar objetos
@login_required
def delete_antiparasitario(request, pk_paciente, pk_antiparasitario):
    antiparasitario = Antiparasitario.objects.get(pk=pk_antiparasitario)
    if antiparasitario:
        antiparasitario.delete()
    return HttpResponseRedirect (reverse('animalchic:list_antiparasitarios', kwargs={'pk_paciente':pk_paciente}))

@login_required
def delete_enfermedad(request, pk_paciente, pk_enfermedad):
    enfermedad = Enfermedad.objects.get(pk=pk_enfermedad)
    if enfermedad:
        enfermedad.delete()
    return HttpResponseRedirect(reverse('animalchic:list_enfermedades', kwargs={'pk_paciente': pk_paciente}))

@login_required
def delete_vacuna(request, pk_paciente, pk_vacuna):
    vacuna = Vacuna.objects.get(pk=pk_vacuna)
    if vacuna:
        vacuna.delete()
    return HttpResponseRedirect(reverse('animalchic:list_vacunas', kwargs={'pk_paciente': pk_paciente}))

@login_required
def delete_paciente(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    if paciente:
        paciente.delete()
    return HttpResponseRedirect(reverse('animalchic:list_pacientes'))

@login_required
def delete_propietario(request, pk):
    propietario = Propietario.objects.get(pk=pk)
    if propietario:
        propietario.delete()
    return HttpResponseRedirect(reverse('animalchic:list_propietarios'))