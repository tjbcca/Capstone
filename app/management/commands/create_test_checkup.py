from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import *

class Command(BaseCommand):
    help = 'Create a test checkup with admin1 as the inspector'

    def handle(self, *args, **kwargs):
        try:
            inspector = User.objects.get(username='admin1')
            customer = User.objects.get(username='test_customer')
            checkup = Checkup.objects.create(customer=customer, status='Pending', inspector=inspector, startDT='2025-06-20 12:30', departDT='2025-06-20 16:00')
            self.stdout.write(self.style.SUCCESS(f'Successfully created checkup with ID {checkup.id}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User with username "admin1" does not exist'))