from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(default=None)
    bio = models.CharField(max_length=200, blank=True, null=True)
    notes = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
class Checkup(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.TextField()
    inspector = models.ForeignKey(User, related_name='inspector', on_delete=models.CASCADE, default=1)
    def save(self, *args, **kwargs):
        super(Checkup, self).save(*args, **kwargs)
        if not self.items.exists():
            interior_checks = [
                "Check Dishwasher", "Check Refrigerator", "Check Ice Maker", "Check Oven",
                "Check Washer & Dryer", "Check HVAC", "Check Security System", "Check Smoke Alarms",
                "Check Sinks", "Check All Toilets", "Check All Showers", "Check for Water Damage",
                "Check for Signs of Pests", "Check Outlets", "Check Switches/Lights/Fans",
                "Reset Breakers After Outages", "Check All Doors/Windows", "Pickup/Secure Packages"
            ]
            exterior_checks = [
                "360 Visual Inspection of Property", "Check Window Screens", "Check Lawn Care",
                "Check for Proper Drainage", "Inspect Garage", "Visual Inspection of Roof (Ground Level)",
                "Test & Check Security System", "Inspect for Vandalism or Theft", "Remove Ads, Newspapers, or Flyers",
                "Check Deck & Patio Areas", "Visual Inspection HVAC Equipment", "Check for Damaged Landscaping",
                "Check Pest Control Issues", "Ensure Pool Area is Secured", "Check Switches/Lighting/Fans",
                "Test Start Vehicles (If Requested)"
            ]
            for check in interior_checks + exterior_checks:
                ChecklistItem.objects.create(checklist=self, description=check)
class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checkup, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    

def Context(request, extra=None):
    BasicContext = {'user':request.user}
    return {k: v for d in (BasicContext, extra) for k, v in d.items()}