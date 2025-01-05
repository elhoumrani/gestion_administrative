from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Utlisateur(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_dg = models.BooleanField(default=False)
    is_rh = models.BooleanField(default=False)
    is_chef = models.BooleanField(default=False)
    is_employe = models.BooleanField(default=True)
    matricule = models.CharField(default=' ', max_length=100)