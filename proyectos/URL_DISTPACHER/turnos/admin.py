from django.contrib import admin
from turnos.models import Persona, Medico, Paciente, Turno, Especialidad

# Register your models here.
admin.site.register(Persona)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Turno)
admin.site.register(Especialidad)