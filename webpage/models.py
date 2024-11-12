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

    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.title, self.description, self.venue, self.event_date.strftime('%d/%m/%Y'),
                                       self.registration_deadline.strftime('%d/%m/%Y'))