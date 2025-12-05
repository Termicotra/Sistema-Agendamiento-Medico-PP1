from django.urls import path
from .views import login_view, logout_view, MyTokenObtainPairView, LogoutView, register_view, RegisterAPIView, perfil_view, cambiar_contrasena_view, listar_solicitudes_view, detalle_solicitud_view, procesar_solicitud_view, PerfilAPIView, ChangePasswordAPIView, AprobarSolicitudAPIView, RechazarSolicitudAPIView, ListarSolicitudesAPIView
from .views import PermissionsAPIView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'autenticacion'

urlpatterns = [
    # Endpoints de autenticación tradicionales (templates)
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('perfil/', perfil_view, name='perfil'),
    path('cambiar-contrasena/', cambiar_contrasena_view, name='cambiar_contrasena'),
    
    # Gestión de solicitudes de registro (solo administradores)
    path('solicitudes/', listar_solicitudes_view, name='listar_solicitudes'),
    path('solicitudes/<int:solicitud_id>/', detalle_solicitud_view, name='detalle_solicitud'),
    path('solicitudes/<int:solicitud_id>/procesar/', procesar_solicitud_view, name='procesar_solicitud'),

    # Endpoints JWT
    # alias 'api/login/' usado como endpoint principal para obtener tokens
    path('api/login/', MyTokenObtainPairView.as_view(), name='api_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='token_logout'),
    path('api/permissions/', PermissionsAPIView.as_view(), name='api_permissions'),
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/perfil/', PerfilAPIView.as_view(), name='api_perfil'),
    path('api/change-password/', ChangePasswordAPIView.as_view(), name='api_change_password'),
    path('api/solicitudes/', ListarSolicitudesAPIView.as_view(), name='api_listar_solicitudes'),
    path('api/solicitudes/<int:solicitud_id>/aprobar/', AprobarSolicitudAPIView.as_view(), name='api_aprobar_solicitud'),
    path('api/solicitudes/<int:solicitud_id>/rechazar/', RechazarSolicitudAPIView.as_view(), name='api_rechazar_solicitud'),
]