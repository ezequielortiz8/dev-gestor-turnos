from django.contrib import admin
from turnos.models import Persona, Medico, Paciente, Turno, Especialidad, Contacto, Usuario
from django.contrib.auth import views as auth_views

# Register your models here.
admin.site.register(Persona)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Turno)
admin.site.register(Especialidad)
admin.site.register(Contacto)
admin.site.register(Usuario)