from django.core.management import BaseCommand
from django.contrib.auth.models import User
from decouple import config

class Command(BaseCommand):
    help = "Helps to create the default admin to handle things"

    admin_username = "DEFAULT_ADMIN_USERNAME"
    admin_password = "DEFAULT_ADMIN_PASSWORD"

    def handle(self, *args, **kwargs):
        if not (self.admin_username and self.admin_password):
            self.stdout.write(self.style.ERROR("Admin credentials not added to env"))
            return
        if User.objects.filter(username=self.admin_username).exists():
            self.style.ERROR("Admin User created")

        else:
            admin_user = User.objects.create_superuser(
                username=self.admin_username, password=self.admin_password,email=None
            )
            self.stdout.write(
                self.style.SUCCESS(f"Admin with username{admin_user.username} has been created")
            )
            