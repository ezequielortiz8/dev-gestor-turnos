from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
#from .models import Profile #podria ser paciente, este se necesita para visuaisar cual es el paciente que hizo el log-in
from .models import Especialidad #para la lista desplegable
from .models import Appointment
# Create your views here.

def index(request):
    return render(request, "index.html")

#def turnos(request):
#    return render(request, "turnos.html")

def ingreso(request):
    return render(request, "login.html",  {})

def registro(request):
    return render(request, "reg_usuario.html")

#def misturnos(request):
#    return render(request, "reg_usuario.html")

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

def turnos(request): #ESTO E PARA QUE SE VISUALICE LA ESPECIALIDAD
    especialidades = {
        'cardiologia': 'Cardiología',
        'dermatologia': 'Dermatología',
        'endocrinologia': 'Endocrinología',
        'gastroenterologia': 'Gastroenterología',
        'neurologia': 'Neurología',
        'oncologia': 'Oncología',
    }

    return render(request, 'turnos.html', {'especialidades': especialidades}) 



# def appointment_calendar(request, especialidad): #esto e para el calendar
#     appointments = Appointment.objects.filter(especialidad=especialidad)
#     context = {'appointments': appointments}
#     return render(request, 'turnos.html', context)

