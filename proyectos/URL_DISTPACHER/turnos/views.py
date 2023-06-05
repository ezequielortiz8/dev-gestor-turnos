from django.shortcuts import redirect, render
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


# Create your views here.


def index(request):
    return render(request, "index.html")


# def turnos(request):
#     return render(request, "turnos.html")


def ingreso(request):
    return render(request, "login.html", {})


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
    # return HttpResponse("Formulario de contacto")
    mensaje = None
    if request.method == 'POST':
        mi_formulario = ContactoForm(request.POST)
        # acción para tomar los datos del formulario
        if mi_formulario.is_valid():
            messages.success(request, 'Hemos recibido tus datos')
            mensaje = f"De: {mi_formulario.cleaned_data['nombre']} <{mi_formulario.cleaned_data['email']}>\n Asunto: {mi_formulario.cleaned_data['asunto']}\n Mensaje: {mi_formulario.cleaned_data['mensaje']}"
            mensaje_html = f"""
                <p>De: {mi_formulario.cleaned_data['nombre']} <a href="mailto:{mi_formulario.cleaned_data['email']}">{mi_formulario.cleaned_data['email']}</a></p>
                <p>Asunto:  {mi_formulario.cleaned_data['asunto']}</p>
                <p>Mensaje: {mi_formulario.cleaned_data['mensaje']}</p>
            """
            asunto = "CONSULTA DESDE LA PAGINA - " + \
                mi_formulario.cleaned_data['asunto']
            send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [
                      settings.RECIPIENT_ADDRESS], fail_silently=False, html_message=mensaje_html)
        # acción para tomar los datos del formulario
        else:
            messages.error(
                request, 'Por favor revisa los errores en el formulario')
    elif request.method == 'GET':
        mi_formulario = ContactoForm()
    else:
        return HttpResponseNotAllowed(f"Método {request.method} no soportado")

    context = {
        'contacto_formulario': mi_formulario
    }
    return render(request, 'contacto.html', context)

# --------------------------------------------------------------------


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
    return render(request, 'turnos.html', {"especialidades": especialidades})


def medicos(request):

    # medicos = Medico.objects.all()
    # return render(request, 'turnos.html', {"medico": medicos})

    #medic = Persona.objects.filter(persona_ptr_id__id__especialidad='Cardiologia')
    lista_medicos = Persona.objects.all().select_related('Cardiologia').values_list('id', 'persona_ptr_id__id').exists()
    for i in lista_medicos:
        print(i.nombre)
    return render(request, 'turnos.html', {"medico": lista_medicos})


def persona(request):

    personas = Persona.objects.all()
    return render(request, 'turnos.html', {"persona": personas})


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


# def appointment_calendar(request, especialidad): #esto e para el calendar
#     appointments = Appointment.objects.filter(especialidad=especialidad)
#     context = {'appointments': appointments}
#     return render(request, 'turnos.html', context)
