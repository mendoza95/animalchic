from django.contrib import admin
from .models import Propietario, Paciente, Vacuna, Enfermedad

#Register your models here.
admin.site.register(Propietario)
admin.site.register(Paciente)
admin.site.register(Vacuna)
admin.site.register(Enfermedad)