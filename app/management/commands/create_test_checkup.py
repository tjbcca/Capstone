from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import *

class Command(BaseCommand):
    help = 'Create a test checkup with admin1 as the inspector'

    def handle(self, *args, **kwargs):
        try:
            inspector = User.objects.get(username='admin1')
            customer = User.objects.create_user(username='test_customer', password='password123')
            checkup = Checkup.objects.create(customer=customer, status='Pending', inspector=inspector, start_datetime='6-20-25', depart_datetime='6-20-25')
            self.stdout.write(self.style.SUCCESS(f'Successfully created checkup with ID {checkup.id}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User with username "admin1" does not exist'))