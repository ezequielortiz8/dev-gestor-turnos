from django.db import models

# Create your models here.

class Especialidad(models.Model): #para la lista desplegable
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Appointment(models.Model): #esto es para el calendario
    date = models.DateField()
    time = models.TimeField()
    especilidad = models.CharField(max_length=100)
