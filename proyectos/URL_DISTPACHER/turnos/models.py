from django.db import models

# Create your models here.


class Especialidad(models.Model):  # para la lista desplegable
    nombre = models.CharField(max_length=50, verbose_name='Nombre')

    def __str__(self):
        return self.nombre


class Appointment(models.Model):  # esto es para el calendario
    date = models.DateField()
    time = models.TimeField()
    especialidad = models.CharField(max_length=100)


class Persona(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=150, verbose_name='Apellido')
    email = models.EmailField(max_length=150, null=True)
    dni = models.IntegerField(verbose_name="DNI")
    genero = models.CharField(max_length=10, verbose_name='Genero')
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de nacimiento', null=True, default=None)
    telefono = models.CharField(max_length=30, verbose_name='Telefono')
    domicilio = models.CharField(max_length=150, verbose_name='Domicilio')
    usuario = models.CharField(max_length=30, verbose_name='Usuario')
    clave = models.CharField(max_length=30, verbose_name='Clave')


class Medico(Persona):
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)


class Paciente(Persona):
    obrasocial = models.CharField(max_length=100, verbose_name='obrasocial')


class Turno(models.Model):
    fecha = models.DateField(verbose_name='fecha', null=True, default=None)
    hora = models.TimeField(verbose_name='hora', null=True, default=None)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)


class Estado(models.TextChoices):
    Pendiente = 'pen', 'Pendiente'
    Cancelado = 'can', 'Cancelado'
    Cumplido = 'cum', 'Cumplido'
    Reprogramado = 'rep', 'Reprogramado'

    estado = models.CharField(
        max_length=3, choices=Estado.choices, default=Estado.Pendiente)
