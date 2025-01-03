# Generated by Django 5.0.7 on 2024-11-12 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0002_alter_user_account_studentid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='add_event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Event Title')),
                ('description', models.TextField(verbose_name='Event Description')),
                ('venue', models.CharField(max_length=100, verbose_name='Event Venue')),
                ('event_date', models.DateTimeField(verbose_name='Event Date')),
                ('registration_deadline', models.DateTimeField(verbose_name='Registration Deadline')),
            ],
        ),
    ]
