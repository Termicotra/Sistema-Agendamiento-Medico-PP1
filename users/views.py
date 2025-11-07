from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User

from .serializers import RegisterSerializer, LogoutSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    """
    Permite el registro de nuevos usuarios.
    """
    # Permitir el acceso a usuarios no autenticados
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LogoutView(generics.GenericAPIView):
    """
    Pone en lista negra el token de refresco provisto, cerrando la sesión.
    """
    serializer_class = LogoutSerializer
    # Solo permite el acceso a usuarios que ya están autenticados (para invalidar su propio token)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # HTTP 205 (Reset Content) es la respuesta estándar para la invalidación de tokens
        return Response({"detail": "Sesión cerrada con éxito."}, status=status.HTTP_205_RESET_CONTENT)

# --- Endpoint para listar usuarios ---
class UserListView(generics.ListAPIView):
    """
    Devuelve la lista de todos los usuarios registrados.
    Requiere autenticación (JWT) para acceder.
    Ruta: /api/auth/list/ (GET)
    """
    # Define la fuente de datos (todos los usuarios)
    queryset = User.objects.all().order_by('id')
    # Define el serializador para transformar los objetos User a JSON
    serializer_class = UserSerializer
    # Requiere que el usuario esté autenticado con un JWT válido
    permission_classes = (IsAuthenticated,)

class ProtectedTestView(APIView):
    """
    Ruta de prueba que requiere un JWT válido en el encabezado Authorization.
    """
    permission_classes = (IsAuthenticated,)  # Requiere un JWT válido

    def get(self, request):
        return Response({
            "message": "¡Acceso concedido! JWT funciona correctamente.",
            "user_id": request.user.id,
            "username": request.user.username
        }, status=status.HTTP_200_OK)
