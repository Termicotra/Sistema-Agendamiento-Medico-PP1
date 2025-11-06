from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from .forms import LoginForm
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from drf_spectacular.utils import extend_schema
from .serializers import LogoutSerializer
from .models import BlacklistedAccessToken

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data["username"]
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
                if user.groups.filter(name="empleados").exists():
                    return redirect("menu_principal")
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
    """
    serializer_class = MyTokenObtainPairSerializer


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


class LogoutRefreshView(APIView):
    """API endpoint para invalidar (blacklist) un refresh token.

    Uso:
      POST /auth/api/logout/
      Body JSON: { "refresh": "<refresh_token>" }

    Respuestas:
      205 Reset Content - token blacklisteado correctamente
      400 Bad Request - payload inválido o token inválido

    Nota: la vista acepta cualquier cliente (AllowAny) para permitir que el frontend
    invalide su refresh incluso si el access expiró. Si prefieres, puedo cambiar a
    IsAuthenticated para requerir un access válido.
    """
    # Permitir dos modos:
    # - Si el cliente envía {"refresh": "<token>"} se blacklistea ese refresh (no requiere access).
    # - Si no se envía refresh, se invalidan todos los refresh tokens del usuario autenticado
    #   (requiere Authorization: Bearer <access>).
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        request=LogoutSerializer,
        responses={
            205: None,
            400: "Bad Request - payload inválido o token inválido",
            401: "Unauthorized - se requiere access token válido",
        },
        description=(
            "Invalidar (blacklist) refresh tokens para hacer logout seguro.\n"
            "Si el body incluye {\"refresh\": \"<token>\"} se invalidará ese token."
            " Si no se incluye, se invalidarán todos los refresh tokens asociados al usuario autenticado."
        ),
    )
    def post(self, request, *args, **kwargs):
        # si se envía refresh explícito, lo validamos y blacklisteamos (no requiere access)
        if 'refresh' in request.data and request.data.get('refresh'):
            serializer = LogoutSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            refresh_token = serializer.validated_data['refresh']
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                # si el cliente incluyó también un access en Authorization, invalidarlo
                auth_header = request.META.get('HTTP_AUTHORIZATION', '')
                if auth_header.startswith('Bearer '):
                    access_raw = auth_header.split(' ', 1)[1].strip()
                    try:
                        access = AccessToken(access_raw)
                        jti = access.get('jti')
                        # intentar asociar a usuario
                        user_id = access.get('user_id')
                        if jti:
                            try:
                                from django.contrib.auth import get_user_model
                                User = get_user_model()
                                user_obj = None
                                if request.user and request.user.is_authenticated:
                                    user_obj = request.user
                                elif user_id:
                                    try:
                                        user_obj = User.objects.get(pk=user_id)
                                    except User.DoesNotExist:
                                        user_obj = None
                                if user_obj:
                                    BlacklistedAccessToken.objects.get_or_create(jti=jti, user=user_obj)
                            except Exception:
                                pass
                    except Exception:
                        pass
                return Response(status=status.HTTP_205_RESET_CONTENT)
            except Exception:
                return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)

        # si no se envía refresh, requerimos que el usuario esté autenticado
        if not request.user or not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided or no refresh token sent.'}, status=status.HTTP_401_UNAUTHORIZED)

        # invalidamos todos los outstanding tokens del usuario autenticado
        tokens = OutstandingToken.objects.filter(user=request.user)
        if not tokens.exists():
            return Response({'detail': 'No outstanding tokens found for user.'}, status=status.HTTP_400_BAD_REQUEST)

        for t in tokens:
            try:
                BlacklistedToken.objects.get_or_create(token=t)
            except Exception:
                continue

        # invalidar también el access token actual (si llegó en Authorization)
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            access_raw = auth_header.split(' ', 1)[1].strip()
            try:
                access = AccessToken(access_raw)
                jti = access.get('jti')
                if jti:
                    try:
                        BlacklistedAccessToken.objects.get_or_create(jti=jti, user=request.user)
                    except Exception:
                        pass
            except Exception:
                pass

        return Response(status=status.HTTP_205_RESET_CONTENT)
