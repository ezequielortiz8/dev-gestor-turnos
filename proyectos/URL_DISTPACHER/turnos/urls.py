from django.urls import path
from . import views

# from .views import Especialidad
# from .views import appointment_calendar

urlpatterns = [
    path("", views.index, name="inicio"),
    #  path('misturnos/', views.misturnos, name="misturnos"),
    path("ingreso/", views.ingreso, name="ingreso"),
    path("turnostodos/", views.turnostodos),
    path("turnosporespecialidad/", views.turnosporespecialidad),
    path("turnosporprofesional/", views.turnosporprofesional),
    path("turnospordni/<int:dni>", views.turnospordni),
    path("registro/", views.registro, name="registro"),
    #  path('turnos/', views.turnos, name="turnos"),
    # para la lista desplegable
    path("especialidad/", views.turnos, name="especialidad"),
    #   path('appointments/<str:especialidad>/', appointment_calendar, name='appointment_calendar'),
    # --------------------------------------------------------------------
    path("paciente/<str:nombre>", views.paciente, name="paciente"),
    path("contacto/", views.contacto, name="contacto")
    # --------------------------------------------------------------------
]
