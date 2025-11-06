from django.urls import path
from .views import login_view, logout_view, MyTokenObtainPairView, LogoutRefreshView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'autenticacion'

urlpatterns = [
	# Endpoints de autenticación tradicionales (templates)
	path('login/', login_view, name='login'),
	path('logout/', logout_view, name='logout'),

	# Endpoints JWT
	# alias 'api/login/' usado como endpoint principal para obtener tokens
	path('api/login/', MyTokenObtainPairView.as_view(), name='api_login'),
	path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('api/logout/', LogoutRefreshView.as_view(), name='token_logout'),
]
