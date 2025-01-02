# Generated by Django 5.0.7 on 2024-12-21 19:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0007_add_event_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_event',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participated_events', to=settings.AUTH_USER_MODEL),
        ),
    ]