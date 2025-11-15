from django import forms
from django.contrib.auth.models import User, Group
from paciente.models import Paciente
from profesional.models import Profesional
from empleado.models import Empleado
from .models import SolicitudRegistro

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    ci = forms.CharField(max_length=20, label="Cédula")

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("El nombre de usuario ya existe.")
        if SolicitudRegistro.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Ya existe una solicitud con este nombre de usuario.")
        return username
    
    def clean_ci(self):
        ci = self.cleaned_data["ci"]
        # Verificar que la cédula exista en la base de datos
        paciente = Paciente.objects.filter(ci=ci).first()
        profesional = Profesional.objects.filter(ci=ci).first()
        empleado = Empleado.objects.filter(ci=ci).first()
        
        if not (paciente or profesional or empleado):
            raise forms.ValidationError("No existe ningún registro con esta cédula. Debe ser registrado como paciente, profesional o empleado primero.")
        
        # Verificar que la cédula no tenga ya un usuario asignado
        if paciente and paciente.user:
            raise forms.ValidationError("Esta cédula ya tiene un usuario asignado.")
        if profesional and profesional.user:
            raise forms.ValidationError("Esta cédula ya tiene un usuario asignado.")
        if empleado and empleado.user:
            raise forms.ValidationError("Esta cédula ya tiene un usuario asignado.")
        
        # Verificar que no haya una solicitud pendiente para esta cédula
        if SolicitudRegistro.objects.filter(ci=ci, estado='pendiente').exists():
            raise forms.ValidationError("Ya existe una solicitud pendiente con esta cédula.")
        
        return ci
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        return username
