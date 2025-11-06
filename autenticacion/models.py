from django.db import models
from django.conf import settings


class BlacklistedAccessToken(models.Model):
	"""Almacena el jti de access tokens que han sido invalidados (logout inmediato)."""
	jti = models.CharField(max_length=255, unique=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blacklisted_access_tokens')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Blacklisted access {self.jti} for {self.user}"

# Create your models here.
