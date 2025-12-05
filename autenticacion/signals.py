from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver

GROUPS = ["administradores", "profesionales", "pacientes"]

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    # crea los grupos si no existen
    for g in GROUPS:
        Group.objects.get_or_create(name=g)



