from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SolicitudRegistro
from paciente.models import Paciente
from profesional.models import Profesional
from empleado.models import Empleado


class ChangePasswordSerializer(serializers.Serializer):
	"""Serializer para cambiar contraseña del usuario autenticado."""
	old_password = serializers.CharField(required=True, write_only=True)
	new_password = serializers.CharField(required=True, write_only=True)
	confirm_password = serializers.CharField(required=True, write_only=True)
	
	def validate_old_password(self, value):
		user = self.context['request'].user
		if not user.check_password(value):
			raise serializers.ValidationError("La contraseña actual es incorrecta.")
		return value
	
	def validate(self, data):
		if data['new_password'] != data['confirm_password']:
			raise serializers.ValidationError({"confirm_password": "Las contraseñas no coinciden."})
		if len(data['new_password']) < 8:
			raise serializers.ValidationError({"new_password": "La nueva contraseña debe tener al menos 8 caracteres."})
		return data


class PerfilSerializer(serializers.Serializer):
	"""Serializer para mostrar el perfil del usuario autenticado."""
	username = serializers.CharField()
	email = serializers.EmailField()
	first_name = serializers.CharField()
	last_name = serializers.CharField()
	group = serializers.CharField()
	perfil_data = serializers.DictField()


class AprobarSolicitudSerializer(serializers.Serializer):
	"""Serializer para aprobar una solicitud de registro."""
	group = serializers.ChoiceField(
		choices=['pacientes', 'profesionales', 'empleados', 'administradores'],
		required=True,
		help_text="Grupo al que se asignará el usuario"
	)


class SolicitudRegistroSerializer(serializers.Serializer):
	"""Serializer para listar solicitudes de registro."""
	id = serializers.IntegerField()
	username = serializers.CharField()
	ci = serializers.CharField()
	estado = serializers.CharField()
	fecha_solicitud = serializers.DateTimeField()
	fecha_procesada = serializers.DateTimeField(allow_null=True)
	procesada_por = serializers.CharField(allow_null=True)


class RegisterSerializer(serializers.Serializer):
	"""Serializer para el endpoint de registro."""
	username = serializers.CharField(max_length=150)
	password = serializers.CharField(write_only=True, style={'input_type': 'password'})
	ci = serializers.CharField(max_length=20)
	
	def validate_username(self, value):
		username = value.lower()
		if User.objects.filter(username__iexact=username).exists():
			raise serializers.ValidationError("El nombre de usuario ya existe.")
		if SolicitudRegistro.objects.filter(username__iexact=username).exists():
			raise serializers.ValidationError("Ya existe una solicitud con este nombre de usuario.")
		return username
	
	def validate_ci(self, value):
		# Verificar que no haya una solicitud existente para esta cédula
		solicitud_existente = SolicitudRegistro.objects.filter(ci=value).first()
		if solicitud_existente:
			if solicitud_existente.estado == 'pendiente':
				raise serializers.ValidationError("Ya existe una solicitud pendiente con esta cédula.")
			elif solicitud_existente.estado == 'aprobada':
				raise serializers.ValidationError("Esta cédula ya tiene un usuario registrado (solicitud aprobada previamente).")
		
		# Verificar que la cédula exista en la base de datos
		paciente = Paciente.objects.filter(ci=value).first()
		profesional = Profesional.objects.filter(ci=value).first()
		empleado = Empleado.objects.filter(ci=value).first()
		
		if not (paciente or profesional or empleado):
			raise serializers.ValidationError("No existe ningún registro con esta cédula. Debe ser registrado como paciente, profesional o empleado primero.")
		
		# Verificar que la cédula no tenga ya un usuario asignado
		if paciente and paciente.user:
			raise serializers.ValidationError("Esta cédula ya tiene un usuario asignado.")
		if profesional and profesional.user:
			raise serializers.ValidationError("Esta cédula ya tiene un usuario asignado.")
		if empleado and empleado.user:
			raise serializers.ValidationError("Esta cédula ya tiene un usuario asignado.")
		
		return value


class LogoutSerializer(serializers.Serializer):
	"""Serializer para el endpoint de logout que recibe el refresh token.

	Ejemplo de payload esperado:
		{ "refresh": "<refresh_token>" }
	"""
	# refresh token opcional: si se envía, lo validamos y blacklisteamos; si no,
	# la vista puede optar por invalidar todos los tokens del usuario (requiere auth).
	refresh = serializers.CharField(write_only=True, required=False)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	"""Extiende el token para incluir información adicional del usuario.

	Agrega username, email y roles (grupos) al payload del token.
	Soporta login case-insensitive y mensajes en español.
	"""

	def validate(self, attrs):
		# Convertir username a minúsculas para login case-insensitive
		username = attrs.get('username', '').lower()
		password = attrs.get('password', '')
		
		# Autenticar con username en minúsculas
		from django.contrib.auth import authenticate
		user = authenticate(username=username, password=password)
		
		if user is None:
			raise serializers.ValidationError({
				'detail': 'Credenciales inválidas. Por favor, verifica tu usuario y contraseña.'
			})
		
		if not user.is_active:
			raise serializers.ValidationError({
				'detail': 'Esta cuenta está desactivada.'
			})
		
		# Llamar al método padre con las credenciales correctas
		attrs['username'] = username
		refresh = self.get_token(user)
		
		data = {
			'refresh': str(refresh),
			'access': str(refresh.access_token),
			'username': user.username,
			'email': user.email or "",
			'roles': [g.name for g in user.groups.all()],
			'first_name': user.first_name or "",
			'last_name': user.last_name or ""
		}
		
		return data

	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		# Claims personalizados
		token['username'] = user.username
		token['email'] = user.email or ""
		token['roles'] = [g.name for g in user.groups.all()]
		return token
