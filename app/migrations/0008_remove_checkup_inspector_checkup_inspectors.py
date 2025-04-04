# Generated by Django 5.1.2 on 2025-04-04 14:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_alter_checkup_name_alter_checkup_status"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="checkup",
            name="inspector",
        ),
        migrations.AddField(
            model_name="checkup",
            name="inspectors",
            field=models.ManyToManyField(
                default=1, related_name="inspector", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
