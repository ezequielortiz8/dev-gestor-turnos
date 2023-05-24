import re
from django import forms
from django.forms import ValidationError

from turnos.models import Especialidad


def solo_caracteres(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('El nombre no puede contener números. %(valor)s',
                              code='Invalid',
                              params={'valor': value})


def custom_validate_email(value):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError('Correo electrónico inválido')


class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        max_length=50,
        validators=(solo_caracteres,),
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Solo letras'}
        )
    )
    email = forms.EmailField(
        label='Email',
        max_length=100,
        error_messages={
            'required': 'Por favor completa el campo'
        },
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'ejemplo@dominio'})
        # widget=forms.TextInput(
        #     attrs={'class': 'form-control', 'type': 'email'})
    )
    asunto = forms.CharField(
        label='Asunto',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    mensaje = forms.CharField(
        label='Mensaje',
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'})
    )

    def clean_mensaje(self):
        data = self.cleaned_data['mensaje']
        if len(data) < 20:
            raise ValidationError(
                "Debes especificar mejor el mensaje que nos envias")
        return data

    def clean(self):
        cleaned_data = super().clean()
        asunto = cleaned_data.get("asunto")
        suscripcion = cleaned_data.get("suscripcion")

        if suscripcion and asunto and "suscripcion" not in asunto:
            msg = "Debe agregar la palabra 'suscripcion' al asunto."
            self.add_error('asunto', msg)


class EspecialidadForm(forms.ModelForm):
    # nombre = forms.CharField(error_messages={'required':'Hello! no te olvide de mi!'})

    class Meta:
        model = Especialidad
        # fields='__all__'
        fields = ['nombre']
        # exclude=('baja',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre de especialidad'})
        }
