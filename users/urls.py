from django.urls import path
from .views import RegisterView, LogoutView, ProtectedTestView, UserListView

# Definimos el namespace para evitar conflictos de nombres
app_name = 'users'

urlpatterns = [
    # 1. Darse de alta de usuario
    path('register/', RegisterView.as_view(), name='register'),

    # Cerrar sesión
    path('logout/', LogoutView.as_view(), name='logout'),

    # Endpoint de prueba protegido
    path('test-auth/', ProtectedTestView.as_view(), name='test-auth'),

    path('list/', UserListView.as_view(), name='user-list'),
]
