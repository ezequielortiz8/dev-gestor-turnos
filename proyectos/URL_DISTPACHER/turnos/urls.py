from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='turnos-index'),
    path('misturnos/', views.misturnos),
    path('turnostodos/', views.turnostodos),
    path('turnosporespecialidad/', views.turnosporespecialidad),
    path('turnosporprofesional/', views.turnosporprofesional),
    path('turnospordni/<int:dni>', views.turnospordni),
  #  path('turnoscancelados/', views.turnoscancelados),

]