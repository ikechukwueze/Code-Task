from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

 
class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.exists():
            User.objects.create_superuser(username="admin", password="admin")
            self.stdout.write(
                "Admin user with username: 'admin' and password: 'admin' created."
            )
        else:
            self.stdout.write("Super user already exists.")
        
