from django.conf.urls import url
from .views import (
    PropietarioCreation,
    PropietarioDetail,
    PropietarioList,
    PropietarioUpdate,
    PacienteList,
    PacienteCreation,
    PacienteUpdate,
    PacienteDetail,
    VacunaList,
    VacunaCreation,
    VacunaDetail,
    VacunaUpdate,
    EnfermedadList,
    EnfermedadCreation,
    EnfermedadDetail,
    EnfermedadUpdate,
    AntiparasitarioList,
    AntiparasitarioCreation,
    AntiparasitarioDetail,
    AntiparasitarioUpdate,
    index,
    delete_antiparasitario,
    delete_enfermedad,
    delete_vacuna,
    delete_paciente,
    delete_propietario,
    PropietarioListJson,
    PacienteListJson,
    VacunaListJson,
    EnfermedadListJson,
    AntiparasitarioListJson
)

app_name = 'animalchic'
urlpatterns = [
    url(r'^$', index, name='index'),
    ############ Urls para modelo Propietario ##############################
    url(r'^propietarios/$', PropietarioList.as_view(), name='list_propietarios'),
    url(r'^propietarios_json/$',PropietarioListJson.as_view(), name='list_propietarios_json'),
    url(r'^propietarios/(?P<pk>\d+)/$', PropietarioDetail.as_view(), name='detail_propietario'),
    url(r'^nuevo_propietario/$', PropietarioCreation.as_view(), name='new_propietario'),
    url(r'^editar_propietario/(?P<pk>\d+)/$', PropietarioUpdate.as_view(), name='edit_propietario'),
    url(r'^borrar_propietario/(?P<pk>\d+)/$', delete_propietario, name='delete_propietario'),
    #url(r'^propietarios/(?P<pk_propietario>\d+)/pacientes/$', PacienteList.as_view(), name='list_propietario_pacientes'),
    #url(r'^propietarios/(?P<pk_propietario>\d+)/pacientes_json/$', PacienteListJson.as_view(), name='list_propietario_pacientes_json'),
    url(r'^propietarios/(?P<pk_propietario>\d+)/pacientes/nuevo_paciente/$', PacienteCreation.as_view(),name='nuevo_propietario_paciente'),
    ############ Urls para modelo Paciente ##############################
    url(r'^pacientes/$', PacienteList.as_view(), name='list_pacientes'),
    url(r'^pacientes_json/$', PacienteListJson.as_view(), name='list_pacientes_json'),
    url(r'^pacientes/(?P<pk>\d+)/$', PacienteDetail.as_view(), name='detail_paciente'),
    url(r'^nuevo_paciente/$', PacienteCreation.as_view(), name='new_paciente'),
    url(r'^editar_paciente/(?P<pk>\d+)/$', PacienteUpdate.as_view(), name='edit_paciente'),
    url(r'^borrar_paciente/(?P<pk>\d+)/$', delete_paciente, name='delete_paciente'),
    ############ Urls para modelo Vacuna ##############################
    url(r'^pacientes/(?P<pk_paciente>\d+)/vacunas/$', VacunaList.as_view() , name='list_vacunas'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/vacunas_json/$', VacunaListJson.as_view(), name='list_vacunas_json'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/vacunas/(?P<pk_vacuna>\d+)/$', VacunaDetail.as_view(), name='detail_vacuna'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/nueva_vacuna/$', VacunaCreation.as_view(), name='new_vacuna'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/editar_vacuna/(?P<pk_vacuna>\d+)/$', VacunaUpdate.as_view(), name='edit_vacuna'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/borrar_vacuna/(?P<pk_vacuna>\d+)/$', delete_vacuna, name='delete_vacuna'),
    ############ Urls para modelo Enfermedad ##############################
    url(r'^pacientes/(?P<pk_paciente>\d+)/enfermedades/$', EnfermedadList.as_view() , name='list_enfermedades'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/enfermedades_json/$', EnfermedadListJson.as_view() , name='list_enfermedades_json'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/enfermedades/(?P<pk_enfermedad>\d+)/$', EnfermedadDetail.as_view(), name='detail_enfermedad'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/nueva_enfermedad/$', EnfermedadCreation.as_view(), name='new_enfermedad'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/editar_enfermedad/(?P<pk_enfermedad>\d+)/$', EnfermedadUpdate.as_view(), name='edit_enfermedad'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/borrar_enfermedad/(?P<pk_enfermedad>\d+)/$', delete_enfermedad, name='delete_enfermedad'),
    ############ Urls para modelo Antiparasitario ##########################
    url(r'^pacientes/(?P<pk_paciente>\d+)/antiparasitarios/$', AntiparasitarioList.as_view() , name='list_antiparasitarios'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/antiparasitarios_json/$', AntiparasitarioListJson.as_view() , name='list_antiparasitarios_json'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/antiparasitarios/(?P<pk_antiparasitario>\d+)/$', AntiparasitarioDetail.as_view(), name='detail_antiparasitario'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/nuevo_antiparasitario/$', AntiparasitarioCreation.as_view(), name='new_antiparasitario'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/editar_antiparasitario/(?P<pk_antiparasitario>\d+)/$', AntiparasitarioUpdate.as_view(), name='edit_antiparasitario'),
    url(r'^pacientes/(?P<pk_paciente>\d+)/borrar_antiparasitario/(?P<pk_antiparasitario>\d+)/$', delete_antiparasitario, name='delete_antiparasitario'),
]

