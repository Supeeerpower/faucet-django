import os
import sys
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates the initial admin user'

    def handle(self, *args, **options):
        email = settings.DEFAULT_ADMIN_EMAIL
        password = settings.DEFAULT_ADMIN_PASS
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.SUCCESS(
                f'User: {email} already exists.'))
        else:
            superuser = User.objects.create_superuser(
                email=email, username=email, password=password)
            superuser.first_name = 'ADMIN'
            superuser.last_name = 'ADMIN'
            superuser.role = User.UserRole.ADMIN
            superuser.nda_signed = True
            superuser.kyc_status = 'verified'
            superuser.save()
            self.stdout.write(self.style.SUCCESS(
                f'User: {email} created successfully'))
            sys.exit()
