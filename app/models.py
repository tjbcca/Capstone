from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(default=None, upload_to='profile_pics')
#     bio = models.CharField(max_length=200, blank=True, null=True)
#     notes = models.CharField(max_length=1000, blank=True, null=True)

#     def __str__(self):
#         return f'{self.user.username} Profile'
    
# class Checkup(models.Model):
#     customer = models.OneToOneField(User, on_delete=models.CASCADE)
#     status = models.TextField()

# class ChecklistItem(models.Model):
#     checklist = models.ForeignKey(Checkup, related_name='items', on_delete=models.CASCADE)
#     description = models.CharField(max_length=255)
#     is_completed = models.BooleanField(default=False)