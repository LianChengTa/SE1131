from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class user_account(AbstractUser):
    studentid = models.CharField(max_length=20, unique=True, verbose_name="學號")
    def __str__(self):
        return self.username