from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers


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
	"""

	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		# Claims personalizados
		token['username'] = user.username
		token['email'] = user.email or ""
		token['roles'] = [g.name for g in user.groups.all()]
		return token
