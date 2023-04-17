from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, "index.html")

def misturnos(request):
    return HttpResponse("mis turnos")

def turnostodos(request):
    return HttpResponse("Todos los turnos")

def turnosporprofesional(request):
    return HttpResponse("Turnos por profesional")

def turnosporespecialidad(request):
    return HttpResponse("Turnos por especialidad")

def turnospordni(request, dni):
    return HttpResponse(f"<h1>Listado de turnos para el dni n° {dni}</h1>")

def contact(request):
    return HttpResponse("Formulario de registro")
