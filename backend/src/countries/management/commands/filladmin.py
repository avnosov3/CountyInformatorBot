from django.contrib.auth.models import User as Admin
from django.core.management.base import BaseCommand

from core.settings import env


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.create_super_user()

    def create_super_user(self):
        username = env("DJANGO_ADMIN")
        email = env("DJANGO_ADMIN_EMAIL")
        password = env("DJAGO_ADMIN_PASSWORD")
        if Admin.objects.filter(username=username, email=email).exists():
            self.stdout.write(self.style.SUCCESS("Super Admin exists!"))
        else:
            Admin.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS("Super Admin created!"))
