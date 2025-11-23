from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission, User
from .forms import LoginForm
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    MyTokenObtainPairSerializer, LogoutSerializer, RegisterSerializer, 
    ChangePasswordSerializer, PerfilSerializer, AprobarSolicitudSerializer, 
    SolicitudRegistroSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers, generics
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .models import SolicitudRegistro
from django.contrib.auth.hashers import make_password
from django.utils import timezone

def _get_user_perfil_data(user):
    """Función auxiliar para obtener datos del perfil del usuario.
    
    Retorna un diccionario con:
    - group: nombre del grupo
    - perfil: instancia del modelo (Paciente/Profesional)
    - perfil_dict: diccionario con los datos serializados
    - perfil_data: lista de tuplas (label, value) para mostrar en templates
    """
    group = user.groups.first().name if user.groups.exists() else None
    perfil = None
    perfil_dict = {}
    perfil_data = []
    
    # Mapeo de grupos a modelos y serializers
    GROUP_CONFIG = {
        "pacientes": {
            "model_attr": "paciente",
            "import_path": ("paciente.models", "Paciente"),
            "serializer_path": ("paciente.serializers", "PacienteSerializer"),
        },
        "profesionales": {
            "model_attr": "profesional",
            "import_path": ("profesional.models", "Profesional"),
            "serializer_path": ("profesional.serializers", "ProfesionalSerializer"),
        },
    }
    
    if group in GROUP_CONFIG:
        config = GROUP_CONFIG[group]
        # Importación dinámica del serializer
        from importlib import import_module
        serializer_module = import_module(config["serializer_path"][0])
        serializer_class = getattr(serializer_module, config["serializer_path"][1])
        
        # Obtener perfil
        perfil = getattr(user, config["model_attr"], None)
        if perfil:
            # Serializar datos
            serializer = serializer_class(perfil)
            perfil_dict = serializer.data
            
            # Convertir a lista de tuplas para template
            # Etiquetas amigables
            FIELD_LABELS = {
                'ci': 'Cédula',
                'nombre': 'Nombre',
                'apellido': 'Apellido',
                'fecha_nacimiento': 'Fecha de Nacimiento',
                'direccion': 'Dirección',
                'telefono': 'Teléfono',
                'otro_contacto': 'Otro Contacto',
                'especialidad': 'Especialidad',
                'registro_profesional': 'Registro Profesional',
                'cargo': 'Cargo',
            }
            
            # Excluir campos internos
            exclude_fields = {'id', 'user', 'created_at', 'updated_at'}
            
            perfil_data = [
                (FIELD_LABELS.get(key, key.replace('_', ' ').title()), value)
                for key, value in perfil_dict.items()
                if key not in exclude_fields and value is not None
            ]
    
    return {
        'group': group,
        'perfil': perfil,
        'perfil_dict': perfil_dict,
        'perfil_data': perfil_data
    }

@login_required
def perfil_view(request):
    user = request.user
    perfil_info = _get_user_perfil_data(user)
    
    return render(request, "perfil.html", {
        "user": user,
        "perfil": perfil_info['perfil'],
        "perfil_data": perfil_info['perfil_data'],
        "group": perfil_info['group']
    })

@login_required
def cambiar_contrasena_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
            return redirect("perfil")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "cambiar_contrasena.html", {"form": form})

class RegisterAPIView(generics.GenericAPIView):
    """API endpoint para solicitar registro de usuario.
    
    Uso:
      POST /auth/api/register/
      Body JSON: { "username": "...", "password": "...", "ci": "..." }
    
    Respuestas:
      201 Created - solicitud creada correctamente
      400 Bad Request - errores de validación
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            ci = serializer.validated_data["ci"]
            # Crear solicitud de registro
            SolicitudRegistro.objects.create(
                username=username,
                password_hash=make_password(password),
                ci=ci
            )
            return Response({
                "detail": "Solicitud de registro enviada correctamente. Un administrador la revisará pronto.",
                "username": username,
                "ci": ci,
                "estado": "pendiente"
            }, status=status.HTTP_201_CREATED)
        else:
            # Extraer solo los mensajes de error sin el nombre del campo
            errors = []
            for field, messages in serializer.errors.items():
                if isinstance(messages, list):
                    errors.extend(messages)
                else:
                    errors.append(str(messages))
            
            return Response({
                "detail": errors[0] if len(errors) == 1 else "\n".join(errors)
            }, status=status.HTTP_400_BAD_REQUEST)

def register_view(request):
    from .forms import RegisterForm
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            ci = form.cleaned_data["ci"]
            # Crear solicitud de registro
            SolicitudRegistro.objects.create(
                username=username,
                password_hash=make_password(password),
                ci=ci
            )
            return render(request, "registro_exitoso.html")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

@login_required
def listar_solicitudes_view(request):
    """Vista para que el administrador vea las solicitudes pendientes."""
    if not request.user.groups.filter(name__iexact="administradores").exists():
        return redirect("menu_principal")
    solicitudes = SolicitudRegistro.objects.filter(estado='pendiente')
    return render(request, "listar_solicitudes.html", {"solicitudes": solicitudes})

@login_required
def detalle_solicitud_view(request, solicitud_id):
    """Vista para ver el detalle de una solicitud y aprobar/rechazar."""
    if not request.user.groups.filter(name__iexact="administradores").exists():
        return redirect("menu_principal")
    from paciente.models import Paciente
    from profesional.models import Profesional
    from django.shortcuts import get_object_or_404
    
    solicitud = get_object_or_404(SolicitudRegistro, id=solicitud_id)
    perfil_existente = None
    
    # Buscar datos existentes del paciente/profesional con esta cédula
    paciente = Paciente.objects.filter(ci=solicitud.ci).first()
    profesional = Profesional.objects.filter(ci=solicitud.ci).first()
    
    if paciente:
        perfil_existente = {"tipo": "Paciente", "datos": paciente}
    elif profesional:
        perfil_existente = {"tipo": "Profesional", "datos": profesional}
    
    return render(request, "detalle_solicitud.html", {
        "solicitud": solicitud,
        "perfil_existente": perfil_existente
    })

@login_required
def procesar_solicitud_view(request, solicitud_id):
    """Vista para aprobar o rechazar una solicitud."""
    if not request.user.groups.filter(name__iexact="administradores").exists():
        return redirect("menu_principal")
    from paciente.models import Paciente
    from profesional.models import Profesional
    from django.shortcuts import get_object_or_404
    
    solicitud = get_object_or_404(SolicitudRegistro, id=solicitud_id)
    
    if request.method == "POST":
        accion = request.POST.get("accion")
        
        if accion == "aprobar":
            group_name = request.POST.get("group")
            if not group_name:
                return render(request, "detalle_solicitud.html", {
                    "solicitud": solicitud,
                    "error": "Debe seleccionar un grupo."
                })
            
            # Crear usuario
            user = User.objects.create_user(
                username=solicitud.username,
                password=None  # Password will be set to the hash below
            )
            user.password = solicitud.password_hash  # Assign only if this is a valid Django hash
            user.save()
            
            # Asignar grupo
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            
            # Buscar y enlazar con perfil existente
            if group_name == "pacientes":
                paciente = Paciente.objects.filter(ci=solicitud.ci).first()
                if paciente:
                    paciente.user = user
                    paciente.save()
            elif group_name == "profesionales":
                profesional = Profesional.objects.filter(ci=solicitud.ci).first()
                if profesional:
                    profesional.user = user
                    profesional.save()
            # elif group_name == "administradores": no requiere perfil adicional
            
            # Marcar solicitud como aprobada
            solicitud.estado = "aprobada"
            solicitud.fecha_procesada = timezone.now()
            solicitud.procesada_por = request.user
            solicitud.save()
            
            return redirect("autenticacion:listar_solicitudes")
        
        elif accion == "rechazar":
            # Eliminar la solicitud en lugar de marcarla como rechazada
            solicitud.delete()
            return redirect("autenticacion:listar_solicitudes")
    
    return redirect("autenticacion:detalle_solicitud", solicitud_id=solicitud_id)


def login_view(request):
    from django.contrib.auth.models import User
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data["username"].lower()
            p = form.cleaned_data["password"]
            user = authenticate(request, username=u, password=p)
            if user is not None:
                login(request, user)
                if user.groups.filter(name="administradores").exists():
                    return redirect("menu_principal")
                if user.groups.filter(name="profesionales").exists():
                    return redirect("profesional_dashboard")
                if user.groups.filter(name="pacientes").exists():
                    return redirect("paciente_dashboard")
                # default
                return redirect("menu_principal")
            else:
                return render(request, "login.html", {"form": form, "error": "Credenciales inválidas"})
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

@require_POST
def logout_view(request):
    """Logout seguro via POST.

    Requiere que el formulario envíe un POST con CSRF. Devuelve redirect al login.
    """
    logout(request)
    return redirect('autenticacion:login')


class MyTokenObtainPairView(TokenObtainPairView):
    """Vista basada en SimpleJWT que usa el serializador personalizado

    Devuelve access/refresh tokens con claims adicionales (username, email, roles).
    Soporta login case-insensitive y mensajes de error en español.
    """
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            # Extraer mensaje de error limpio
            if 'detail' in e.detail:
                return Response({
                    'detail': e.detail['detail']
                }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # Si es otro tipo de error de validación
                errors = []
                for field, messages in e.detail.items():
                    if isinstance(messages, list):
                        errors.extend(messages)
                    else:
                        errors.append(str(messages))
                
                return Response({
                    'detail': errors[0] if len(errors) == 1 else "\n".join(errors)
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Agregar espaciado para mejor visualización en Swagger
        data = serializer.validated_data
        formatted_data = {
            'refresh_token': data['refresh'],
            'access_token': data['access']

        }
        
        return Response(formatted_data, status=status.HTTP_200_OK)


@login_required
def home_view(request):
    """Vista protegida que muestra el menú principal.

    Si el usuario no está autenticado, `login_required` lo redirige a `LOGIN_URL`.
    """
    return render(request, 'menu_principal.html')


@login_required
def paciente_dashboard(request):
    """Dashboard para pacientes: muestra permisos y enlaces disponibles según permisos."""
    # Obtener permisos a través de los grupos del usuario para que sea dinámico
    groups = request.user.groups.all()
    perms_qs = Permission.objects.filter(group__in=groups).distinct()
    perms = []
    for p in perms_qs:
        perms.append({
            'name': p.name,
            'codename': p.codename,
            'app_label': p.content_type.app_label,
            'model': p.content_type.model,
        })
    group_names = [g.name for g in groups]
    return render(request, 'paciente_dashboard.html', {"group_permissions": perms, "groups": group_names})


@login_required
def profesional_dashboard(request):
    """Dashboard para profesionales: muestra permisos y enlaces disponibles según permisos."""
    # Obtener permisos a través de los grupos del usuario para que sea dinámico
    groups = request.user.groups.all()
    perms_qs = Permission.objects.filter(group__in=groups).distinct()
    perms = []
    for p in perms_qs:
        perms.append({
            'name': p.name,
            'codename': p.codename,
            'app_label': p.content_type.app_label,
            'model': p.content_type.model,
        })
    group_names = [g.name for g in groups]
    return render(request, 'profesional_dashboard.html', {"group_permissions": perms, "groups": group_names})


class PermissionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        groups = user.groups.all()
        roles = [g.name for g in groups]
        perms_qs = Permission.objects.filter(group__in=groups).distinct()
        permissions = set()
        modules = set()
        for p in perms_qs:
            model = p.content_type.model
            codename = p.codename
            # Map Django codename to expected format
            if codename.startswith('view_'):
                permissions.add(f"{model}.view")
            elif codename.startswith('add_'):
                permissions.add(f"{model}.create")
            elif codename.startswith('change_'):
                permissions.add(f"{model}.edit")
            elif codename.startswith('delete_'):
                permissions.add(f"{model}.delete")
            else:
                permissions.add(f"{model}.{codename}")
            modules.add(model)
        # Ejemplo: dashboard.view si el usuario tiene acceso al dashboard
        if 'dashboard' in [m.lower() for m in modules]:
            permissions.add('dashboard.view')
        return Response({
            "permissions": sorted(permissions),
            "modules": sorted(modules),
            "roles": sorted(roles)
        })

class LogoutView(generics.GenericAPIView):
    """API endpoint para invalidar (blacklist) un refresh token.

    Uso:
      POST /auth/api/logout/
      Body JSON: { "refresh": "<refresh_token>" }

    Respuestas:
      205 Reset Content - token blacklisteado correctamente
      400 Bad Request - payload inválido o token inválido
    """
    serializer_class = LogoutSerializer
    # Solo permite el acceso a usuarios que ya están autenticados (para invalidar su propio token)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data.get('refresh')
        # Blacklist refresh token
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except (ValueError, TypeError, KeyError) as e:
                return Response({'detail': f'Invalid refresh token: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'No refresh token provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Blacklist access token (if present in Authorization header)
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            access_raw = auth_header.split(' ', 1)[1].strip()
            try:
                access_token = AccessToken(access_raw)
                jti = access_token.get('jti')
                if jti:
                    # Buscar OutstandingToken por jti y usuario
                    try:
                        outstanding = OutstandingToken.objects.get(jti=jti, user=request.user)
                        BlacklistedToken.objects.get_or_create(token=outstanding)
                    except OutstandingToken.DoesNotExist:
                        # It's possible that the access token does not have a corresponding OutstandingToken.
                        # In this case, we can safely ignore and continue.
                        pass
            except (ValueError, TypeError, KeyError):
                pass

        return Response({"detail": "Sesión cerrada con éxito."}, status=status.HTTP_205_RESET_CONTENT)


class PerfilAPIView(generics.GenericAPIView):
    """API endpoint para obtener el perfil del usuario autenticado.
    
    Uso:
      GET /auth/api/perfil/
      Headers: Authorization: Bearer <access_token>
    
    Respuestas:
      200 OK - perfil del usuario con datos completos
      401 Unauthorized - token no válido o ausente
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PerfilSerializer
    
    def get(self, request):
        user = request.user
        perfil_info = _get_user_perfil_data(user)
        
        return Response({
            "username": user.username,
            "email": user.email or "",
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "group": perfil_info['group'] or "",
            "perfil_data": perfil_info['perfil_dict']
        }, status=status.HTTP_200_OK)


class ChangePasswordAPIView(generics.GenericAPIView):
    """API endpoint para cambiar contraseña del usuario autenticado.
    
    Uso:
      POST /auth/api/change-password/
      Headers: Authorization: Bearer <access_token>
      Body JSON: { "old_password": "...", "new_password": "...", "confirm_password": "..." }
    
    Respuestas:
      200 OK - contraseña cambiada exitosamente
      400 Bad Request - errores de validación
      401 Unauthorized - token no válido o ausente
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Cambiar contraseña
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({
                "detail": "Contraseña cambiada exitosamente."
            }, status=status.HTTP_200_OK)
        else:
            # Extraer solo los mensajes de error sin el nombre del campo
            errors = []
            for field, messages in serializer.errors.items():
                if isinstance(messages, list):
                    errors.extend(messages)
                else:
                    errors.append(str(messages))
            
            return Response({
                "detail": errors[0] if len(errors) == 1 else "\n".join(errors)
            }, status=status.HTTP_400_BAD_REQUEST)


class AprobarSolicitudAPIView(generics.GenericAPIView):
    """API endpoint para aprobar una solicitud de registro.
    
    Uso:
      POST /auth/api/solicitudes/<id>/aprobar/
      Headers: Authorization: Bearer <access_token>
      Body JSON: { "group": "pacientes|profesionales|administradores" }
    
    Respuestas:
      200 OK - solicitud aprobada exitosamente
      400 Bad Request - errores de validación
      401 Unauthorized - token no válido o ausente
      403 Forbidden - usuario no es administrador
      404 Not Found - solicitud no encontrada
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AprobarSolicitudSerializer
    
    def post(self, request, solicitud_id):
        # Verificar que el usuario sea administrador
        if not request.user.groups.filter(name__iexact="administradores").exists():
            return Response({
                "detail": "No tienes permisos para aprobar solicitudes."
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Buscar solicitud
        try:
            solicitud = SolicitudRegistro.objects.get(id=solicitud_id)
        except SolicitudRegistro.DoesNotExist:
            return Response({
                "detail": "Solicitud no encontrada."
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Validar que esté pendiente
        if solicitud.estado != 'pendiente':
            return Response({
                "detail": f"La solicitud ya fue {solicitud.estado}."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar datos
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Extraer solo los mensajes de error sin el nombre del campo
            errors = []
            for field, messages in serializer.errors.items():
                if isinstance(messages, list):
                    errors.extend(messages)
                else:
                    errors.append(str(messages))
            
            return Response({
                "detail": errors[0] if len(errors) == 1 else "\n".join(errors)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        group_name = serializer.validated_data['group']
        
        # Crear usuario
        from paciente.models import Paciente
        from profesional.models import Profesional
        
        user = User.objects.create_user(
            username=solicitud.username,
            password=None
        )
        user.password = solicitud.password_hash
        user.save()
        
        # Asignar grupo
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        
        # Buscar y enlazar con perfil existente
        if group_name == "pacientes":
            paciente = Paciente.objects.filter(ci=solicitud.ci).first()
            if paciente:
                paciente.user = user
                paciente.save()
        elif group_name == "profesionales":
            profesional = Profesional.objects.filter(ci=solicitud.ci).first()
            if profesional:
                profesional.user = user
                profesional.save()
        # elif group_name == "administradores": no requiere perfil adicional
        
        # Marcar solicitud como aprobada
        solicitud.estado = "aprobada"
        solicitud.fecha_procesada = timezone.now()
        solicitud.procesada_por = request.user
        solicitud.save()
        
        return Response({
            "detail": "Solicitud aprobada exitosamente.",
            "username": user.username,
            "group": group_name
        }, status=status.HTTP_200_OK)


class RechazarSolicitudAPIView(generics.GenericAPIView):
    """API endpoint para rechazar y eliminar una solicitud de registro.
    
    Uso:
      POST /auth/api/solicitudes/<id>/rechazar/
      Headers: Authorization: Bearer <access_token>
    
    Respuestas:
      200 OK - solicitud rechazada y eliminada exitosamente
      401 Unauthorized - token no válido o ausente
      403 Forbidden - usuario no es administrador
      404 Not Found - solicitud no encontrada
      400 Bad Request - solicitud ya fue procesada
    
    Nota: Al rechazar una solicitud, esta se ELIMINA completamente del sistema,
    permitiendo que el usuario pueda volver a intentar el registro con la misma cédula.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, solicitud_id):
        # Verificar que el usuario sea administrador
        if not request.user.groups.filter(name__iexact="administradores").exists():
            return Response({
                "detail": "No tienes permisos para rechazar solicitudes."
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Buscar solicitud
        try:
            solicitud = SolicitudRegistro.objects.get(id=solicitud_id)
        except SolicitudRegistro.DoesNotExist:
            return Response({
                "detail": "Solicitud no encontrada."
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Validar que esté pendiente
        if solicitud.estado != 'pendiente':
            return Response({
                "detail": f"La solicitud ya fue {solicitud.estado}."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Guardar datos antes de eliminar para la respuesta
        solicitud_id = solicitud.id
        username = solicitud.username
        
        # Eliminar la solicitud en lugar de marcarla como rechazada
        solicitud.delete()
        
        return Response({
            "detail": "Solicitud rechazada y eliminada exitosamente. El usuario puede volver a intentar el registro.",
            "solicitud_id": solicitud_id,
            "username": username
        }, status=status.HTTP_200_OK)


class ListarSolicitudesAPIView(generics.GenericAPIView):
    """API endpoint para listar solicitudes de registro.
    
    Uso:
      GET /auth/api/solicitudes/
      Headers: Authorization: Bearer <access_token>
      Query params (opcionales):
        - estado: filtrar por estado (pendiente|aprobada|rechazada)
    
    Respuestas:
      200 OK - lista de solicitudes
      401 Unauthorized - token no válido o ausente
      403 Forbidden - usuario no es administrador
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SolicitudRegistroSerializer
    
    def get(self, request):
        # Verificar que el usuario sea administrador
        if not request.user.groups.filter(name__iexact="administradores").exists():
            return Response({
                "detail": "No tienes permisos para ver solicitudes."
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Obtener solicitudes
        solicitudes = SolicitudRegistro.objects.all()
        
        # Filtrar por estado si se proporciona
        estado = request.query_params.get('estado', None)
        if estado and estado in ['pendiente', 'aprobada', 'rechazada']:
            solicitudes = solicitudes.filter(estado=estado)
        
        # Serializar datos
        data = []
        for solicitud in solicitudes:
            data.append({
                'id': solicitud.id,
                'username': solicitud.username,
                'ci': solicitud.ci,
                'estado': solicitud.estado,
                'fecha_solicitud': solicitud.fecha_solicitud,
                'fecha_procesada': solicitud.fecha_procesada,
                'procesada_por': solicitud.procesada_por.username if solicitud.procesada_por else None
            })
        
        return Response({
            "solicitudes": data,
            "total": len(data)
        }, status=status.HTTP_200_OK)
