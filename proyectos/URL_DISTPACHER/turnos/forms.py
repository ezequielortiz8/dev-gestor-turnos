from django import forms
    
class ContactoF(forms.Form):
    nombre = forms CharField(label='Nombre:', required = True)
    email = forms EmailField(required = True)
    asunto = forms CharField(label='Asunto:', required = True)
    mensaje = forms CharField(label='Mensaje:', required = True)