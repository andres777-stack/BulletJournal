from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class CustomUser(AbstractUser):
    dob = models.DateField(verbose_name='Date of Birth', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('my-account')

# Create your models here.
