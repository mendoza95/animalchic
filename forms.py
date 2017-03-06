from .models import Paciente, Vacuna, Enfermedad, Antiparasitario
from django.forms import ModelForm, TextInput, DateInput


class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = ['propietario', 'paciente_nombre', 'especie', 'raza', 'sexo', 'fecha_de_nacimiento',
                  'pelaje', 'foto']

        widgets = {
            'fecha_de_nacimiento':DateInput(attrs={'class':'datepicker'})
        }



class VacunaForm(ModelForm):
    class Meta:
        model = Vacuna
        fields = ['fecha', 'descripcion', 'proxima_vacuna', 'veterinario']

        widgets = {
            'fecha':DateInput(attrs={'class':'datepicker'}),
            'proxima_vacuna': DateInput(attrs={'class': 'datepicker'}),
        }


class EnfermedadForm(ModelForm):
    class Meta:
        model = Enfermedad
        fields = ['descripcion', 'fecha', 'tratamiento', 'enfermedad_archivo']
        widgets = {
            'fecha': DateInput(attrs={'class': 'datepicker'}),
        }

class AntiparasitarioForm(ModelForm):
    class Meta:
        model = Antiparasitario
        fields = ['fecha', 'vermifugos', 'proxima_aplicacion']
        widgets = {
            'fecha': DateInput(attrs={'class': 'datepicker'}),
            'proxima_aplicacion': DateInput(attrs={'class': 'datepicker'})
        }