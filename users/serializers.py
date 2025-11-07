from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# --- Serializer para registro (darse de alta) ---
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # Definimos los campos requeridos para el registro
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    # Sobreescribimos el método create para hashear la contraseña
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

# --- Serializer para Cierre de Sesión (Blacklist del Refresh Token) ---
class LogoutSerializer(serializers.Serializer):
    """
    Serializador para recibir el token de refresco y ponerlo en la lista negra.
    """
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('El token es inválido o expiró')
    }

    def validate(self, attrs):
        # Almacenamos el token para usarlo en el método save()
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            # Pone el token de refresco en la "lista negra"
            RefreshToken(self.token).blacklist()
        except TokenError:
            # Si el token ya está expirado o en la lista negra, no hacemos nada y devolvemos éxito.
            pass
# --- Serializer para listado de usuarios ---
class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para listar los detalles básicos del usuario.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = fields # Solo lectura, no se usa para crear/actualizar