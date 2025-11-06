from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import BlacklistedAccessToken


class CustomJWTAuthentication(JWTAuthentication):
    """Extiende JWTAuthentication para comprobar que el jti del access token
    no esté blacklisteado en la tabla `BlacklistedAccessToken`.

    Si el jti está presente en la blacklist, se lanza AuthenticationFailed.
    """

    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None
        user, token = result
        try:
            token_jti = token.get('jti')
        except Exception:
            token_jti = None

        if token_jti:
            if BlacklistedAccessToken.objects.filter(jti=token_jti).exists():
                raise AuthenticationFailed('Token access ha sido invalidado (logout).')

        return (user, token)
