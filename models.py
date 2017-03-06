from django.db import models
from datetime import date
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

class Propietario(models.Model):
    propietario_nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    observacion = models.CharField(max_length=100)
    usuario = models.ForeignKey(User)

    def __str__(self):
        return self.propietario_nombre

    '''  '''
    @property
    def show_url(self):
        url = "/animalchic/propietarios/"+ str(self.id)  +"/"
        return " <a href=' " + url + " ', class='btn btn-info'>Detalle</a> "

class Paciente(models.Model):
    SEXO = (
        ('M','Macho'),
        ('H', 'Hembra'),
    )
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    paciente_nombre = models.CharField(max_length=30)
    especie = models.CharField(max_length=20)
    raza = models.CharField(max_length=20)
    sexo = models.CharField(max_length=1, choices=SEXO)
    fecha_de_nacimiento  = models.DateField('Fecha de Nacimiento')
    pelaje = models.CharField(max_length=15)
    foto = models.ImageField(blank=True, upload_to='pet_images/')
    # usuario = models.ForeignKey(User)

    def __str__(self):
        return self.paciente_nombre

    def get_edad(self):
        hoy = date.today()
        return str((hoy - self.fecha_de_nacimiento).days)+" dias"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.fecha_de_nacimiento <= date.today():
            super(Paciente, self).save()

    @property
    def show_url(self):
        url = "/animalchic/pacientes/" + str(self.id) + "/"
        return " <a href=' " + url + " ', class='btn btn-info'>Detalle</a> "

class Vacuna(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField('fecha de vacunacion')
    descripcion = models.CharField(max_length=30)
    proxima_vacuna = models.DateField('fecha de proxima vacunacion')
    veterinario = models.CharField(max_length=30)
    # usuario = models.ForeignKey(User)

    def __str__(self):
        return self.descripcion
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.fecha <= date.today() and self.fecha < self.proxima_vacuna:
            super(Vacuna, self).save()

    @property
    def show_url(self):
        url = "/animalchic/pacientes/" + str(self.paciente.id) + "/vacunas/"+ str(self.id)+"/"
        return " <a href=' " + url + " ', class='btn btn-info'>Detalle</a> "

class Enfermedad(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=50)
    fecha = models.DateField('Fecha de Deteccion')
    tratamiento = models.CharField(max_length=50)
    enfermedad_archivo = models.FileField(blank=True, upload_to='enfermedades_archivos/')
    # usuario = models.ForeignKey(User)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.fecha <= date.today():
            super(Enfermedad, self).save()

    def __str__(self):
        return self.descripcion

    @property
    def show_url(self):
        url = "/animalchic/pacientes/" + str(self.paciente.id) + "/enfermedades/" + str(self.id) + "/"
        return " <a href=' " + url + " ', class='btn btn-info'>Detalle</a> "

class Antiparasitario(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField('Fecha de aplicacion')
    vermifugos = models.CharField(max_length=20)
    proxima_aplicacion = models.DateField('Proxima aplicacion')
    # usuario = models.ForeignKey(User)

    def __str__(self):
        return self.vermifugos

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.fecha <= date.today() and self.fecha < self.proxima_aplicacion:
            super(Antiparasitario, self).save()

    @property
    def show_url(self):
        url = "/animalchic/pacientes/" + str(self.paciente.id) + "/antiparasitarios/" + str(self.id) + "/"
        return " <a href=' " + url + " ', class='btn btn-info'>Detalle</a> "

@receiver(post_delete, sender=Paciente)
def photo_post_delete_handler(sender, **kwargs):
    paciente = kwargs['instance']
    if len(paciente.foto.name) > 0:
        storage, path = paciente.foto.storage, paciente.foto.path
        storage.delete(path)

@receiver(post_delete, sender=Enfermedad)
def archivo_post_delete_handler(sender, **kwargs):
    enfermedad = kwargs['instance']
    if len(enfermedad.enfermedad_archivo.name) > 0:
        storage, path = enfermedad.enfermedad_archivo.storage, enfermedad.enfermedad_archivo.path
        storage.delete(path)