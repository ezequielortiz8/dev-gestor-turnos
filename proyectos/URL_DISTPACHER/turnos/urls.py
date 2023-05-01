from django.urls import path
from . import views
from .views import Especialidad
from .views import appointment_calendar

urlpatterns = [
    path('', views.index, name='turnos-index'),
    path('misturnos/', views.misturnos),
    path('turnostodos/', views.turnostodos),
    path('turnosporespecialidad/', views.turnosporespecialidad),
    path('turnosporprofesional/', views.turnosporprofesional),
    path('turnospordni/<int:dni>', views.turnospordni),
    path('especialidad/', Especialidad, name='especialidad'), #para la lista desplegable
  path('appointments/<str:especialidad>/', appointment_calendar, name='appointment_calendar'),
  #  path('turnoscancelados/', views.turnoscancelados),

]

