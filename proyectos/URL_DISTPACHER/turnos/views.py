from datetime import datetime
from msilib.schema import ListView
from urllib import request
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from turnos.forms import ContactoForm  # Formulario de Clase Contacto

# from .models import Profile #podria ser paciente, este se necesita para visuaisar cual es el paciente que hizo el log-in
import psycopg2
from .models import Especialidad  # para la lista desplegable
from .models import Appointment
from .forms import EspecialidadForm
from decouple import config


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
    if request.method == "POST":
        mi_formulario = ContactoForm(request.POST)
        # mensaje ='Hemos recibido tus datos'
        # acción para tomar los datos del formulario
        if mi_formulario.is_valid():
            messages.success(request, "Hemos recibido tus datos")
            mensaje = f"De: {mi_formulario.cleaned_data['nombre']} <{mi_formulario.cleaned_data['email']}>\n Asunto: {mi_formulario.cleaned_data['asunto']}\n Mensaje: {mi_formulario.cleaned_data['mensaje']}"
            mensaje_html = f"""
                <p>De: {mi_formulario.cleaned_data['nombre']} <a href="mailto:{mi_formulario.cleaned_data['email']}">{mi_formulario.cleaned_data['email']}</a></p>
                <p>Asunto:  {mi_formulario.cleaned_data['asunto']}</p>
                <p>Mensaje: {mi_formulario.cleaned_data['mensaje']}</p>
            """
            asunto = (
                "CONSULTA DESDE LA PAGINA - " + mi_formulario.cleaned_data["asunto"]
            )
            send_mail(
                asunto,
                mensaje,
                settings.EMAIL_HOST_USER,
                [settings.RECIPIENT_ADDRESS],
                fail_silently=False,
                html_message=mensaje_html,
            )
        # acción para tomar los datos del formulario
        else:
            messages.error(request, "Por favor revisa los errores en el formulario")
    elif request.method == "GET":
        mi_formulario = ContactoForm()
    else:
        return HttpResponseNotAllowed(f"Método {request.method} no soportado")

    context = {"contacto_formulario": mi_formulario}
    return render(request, "contacto.html", context)


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


def turnos(request):  # ESTO E PARA QUE SE VISUALICE LA ESPECIALIDAD

    # Establecer conexión a la base de datos
    conn = psycopg2.connect(
        host=config("DATABASE_HOST"),
        port=config("DATABASE_PORT"),
        dbname=config("DATABASE_NAME"),
        user=config("DATABASE_USER"),
        password=config("DATABASE_PASSWORD"),
    )

    # Crear un cursor para ejecutar consultas
    cursor = conn.cursor()

    # Ejecutar la consulta SQL
    cursor.execute("SELECT nombre FROM public.turnos_especialidad")

    # Obtener los resultados de la consulta
    results = cursor.fetchall()
    especialidades = [result[0] for result in results]

    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    conn.close()

    # Renderizar la vista con el contexto
    return render(request, "turnos.html", {"especialidades": especialidades})


def especialidades_index(request):
    # queryset
    especialidades = Especialidad.objects.all
    return render(
        request, "especialidad/index.html", {"especialidades": especialidades}
    )


def especialidad_nuevo(request):
    if request.method == "POST":
        formulario = EspecialidadForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect("abm")
    else:
        formulario = EspecialidadForm()
    return render(request, "especialidad/nuevo.html", {"form": formulario})


def especialidad_editar(request, id_especialidad):
    try:
        especialidad = Especialidad.objects.get(pk=id_especialidad)
    except Especialidad.DoesNotExist:
        return render(request, "index.html")

    if request.method == "POST":
        formulario = EspecialidadForm(request.POST, instance=especialidad)
        if formulario.is_valid():
            formulario.save()
            return redirect("abm")
    else:
        formulario = EspecialidadForm(instance=especialidad)
    return render(request, "especialidad/editar.html", {"form": formulario})


def especialidad_eliminar(request, id_especialidad):
    try:
        especialidad = Especialidad.objects.get(pk=id_especialidad)
    except especialidad.DoesNotExist:
        return render(request, "index.html")
    especialidad.delete()
    return redirect("abm")

def medicos(request):

    # medicos = Medico.objects.all()
    # return render(request, 'turnos.html', {"medico": medicos})

    result = Persona.objects.filter(medico__persona_ptr_id=Persona.id) \
                .filter(medico__persona_ptr_id=Especialidad.id) \
                .filter(Especialidad__nombre='Cardiologia') \
                .values('nombre')
    return render(request, 'turnos.html', {"medico": result})


# def appointment_calendar(request, especialidad): #esto e para el calendar
#     appointments = Appointment.objects.filter(especialidad=especialidad)
#     context = {'appointments': appointments}
#     return render(request, 'turnos.html', context)
