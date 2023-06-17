from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime
from msilib.schema import ListView
#from urllib import request
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from decouple import config
import psycopg2
from .forms import ContactoForm  # Formulario de Clase Contacto
# from .models import Profile #podria ser paciente, este se necesita para visuaisar cual es el paciente que hizo el log-in
from .models import Especialidad  # para la lista desplegable
from .models import Persona
from .models import Medico
from .models import Appointment
from .forms import EspecialidadForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import ListView


# Create your views here.


def index(request):
    return render(request, "index.html")


# def turnos(request):
#     return render(request, "turnos.html")


@login_required
def ingreso(request):
    return render(request, "index.html")

def exit(request):
    logout(request)
    return redirect('inicio')

def registro(request):
    return render(request, "reg_usuario.html")


# def misturnos(request):
#    return render(request, "reg_usuario.html")


def turnostodos(request):
    return HttpResponse("Todos los turnos")


def turnosporprofesional(request):
    return HttpResponse("Turnos por profesional")


def turnosporespecialidad(request):
    return HttpResponse("Turnos por especialidad")


def turnospordni(request, dni):
    return HttpResponse(f"<h1>Listado de turnos para el dni n° {dni}</h1>")


def contact(request):  # este aun no se ha usado
    return HttpResponse("Formulario de registro")


def contacto(request):
    data = {
        'contacto_formulario': ContactoForm()
    }

    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Contacto guardado"
        else:
            data['contacto_formulario'] = formulario

    return render(request,'contacto.html', data)


def paciente(request, nombre):
    context = {"nombre": nombre}
    return render(request, "paciente.html", {"context": context})
    # return HttpResponse("hola")


# --------------------------------------------------------------------

# def my_view(request): #para que se visualicen esos datos en la parte de turnos
#     user = request.user
#     profile = profile.objects.get(user=user)
#     context = {
#         'username': user.username,
#         'dni': profile.dni,
#     }
#     return render(request, 'turnos.html', context)

# def especialidad(request): #ESTO E PARA QUE SE VISUALICE LA ESPECIALIDAD
#     especialidad = Especialidad.objects.all()
#     return render(request, 'turnos.html', {'especialidad': especialidad})


def turnos(request):

    especialidades = Especialidad.objects.all()
    med = Medico.objects.all()
    return render(request, 'turnos.html', {"especialidades": especialidades, "medicos": med})

    

def medicos(request):

    med = Medico.objects.all()
    return render(request, 'turnos.html', {"medicos": med})


def persona(request):

    personas = Persona.objects.all()
    return render(request, 'turnos.html', {"persona": personas})

@login_required
def especialidades_index(request):
    # queryset
    especialidades = Especialidad.objects.all
    return render(request, 'especialidad/index.html', {'especialidades': especialidades})


def especialidad_nuevo(request):
    if (request.method == 'POST'):
        formulario = EspecialidadForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('abm')
    else:
        formulario = EspecialidadForm()
    return render(request, 'especialidad/nuevo.html', {'form': formulario})


def especialidad_editar(request, id_especialidad):
    try:
        especialidad = Especialidad.objects.get(pk=id_especialidad)
    except Especialidad.DoesNotExist:
        return render(request, 'index.html')

    if (request.method == 'POST'):
        formulario = EspecialidadForm(request.POST, instance=especialidad)
        if formulario.is_valid():
            formulario.save()
            return redirect('abm')
    else:
        formulario = EspecialidadForm(instance=especialidad)
    return render(request, 'especialidad/editar.html', {'form': formulario})


def especialidad_eliminar(request, id_especialidad):
    try:
        especialidad = Especialidad.objects.get(pk=id_especialidad)
    except especialidad.DoesNotExist:
        return render(request, 'index.html')
    especialidad.delete()
    return redirect('abm')

def get_especialidades(_request):
    especialidades = list(Especialidad.objects.values())

    if (len(especialidades) > 0):
        data = {'message': "Success", 'especialidades': especialidades}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)

def get_medicos(_request, especialidad_id):
    medicos = list(Medico.objects.filter(especialidad=especialidad_id).values())

    if (len(medicos) > 0):
        data = {'message': "Success", 'medicos': medicos}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)


class MedicoListView(ListView):
    model = Medico
    context_object_name = 'medicos'
    template_name = 'medico/index.html'
    queryset = Medico.objects.all
  #  ordering = ['nombre']