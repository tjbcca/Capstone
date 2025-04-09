
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import CustomerProfile

class Command(BaseCommand):
    help = 'Create CustomerProfile instances for existing users'
    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            profile, created = CustomerProfile.objects.get_or_create(customer=user)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created profile for user: {user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Profile already exists for user: {user.username}'))
