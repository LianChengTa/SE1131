from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class user_account(AbstractUser):
    studentid = models.CharField(max_length=20, unique=True, verbose_name="學號")
    def __str__(self):
        return self.username

class add_event(models.Model):
    title = models.CharField(max_length=100, verbose_name="Event Title")
    description = models.TextField(verbose_name="Event Description")
    venue = models.CharField(max_length=100, verbose_name="Event Venue")
    event_date = models.DateTimeField(verbose_name="Event Date")
    registration_deadline = models.DateTimeField(verbose_name="Registration Deadline")
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    participants = models.ManyToManyField(user_account, related_name='participated_events', blank=True)
    user = models.ForeignKey(user_account, on_delete=models.CASCADE, related_name='events', null=True, blank=True)


    def __str__(self):
        return self.title