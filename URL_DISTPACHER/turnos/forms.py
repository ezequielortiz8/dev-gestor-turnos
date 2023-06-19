import re
from django import forms
from django.forms import ValidationError
from turnos.models import Especialidad
from turnos.models import Contacto


def solo_caracteres(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('El nombre no puede contener números. %(valor)s',
                              code='Invalid',
                              params={'valor': value})


def custom_validate_email(value):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError('Correo electrónico inválido')


class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = '__all__'


class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        # fields='__all__'
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre de especialidad'})
        }
