# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_manager= models.BooleanField(default=False)
    is_warteam = models.BooleanField(default=False)
    is_opsteam = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)
    image=models.ImageField(upload_to='profile',blank=True)