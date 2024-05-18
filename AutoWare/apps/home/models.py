# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from apps.authentication.models import User
# from django.conf import settings
from core.settings import AUTH_USER_MODEL

class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Manager(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class WareTeams(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)
    manager=models.ForeignKey(Manager, on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        return self.name

class OpTeam(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)
    manager=models.ForeignKey(Manager, on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        return self.name

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='created_by')
    title = models.CharField(max_length=120)
    message = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_warteam = models.BooleanField(default=False)
    is_opsteam = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name='assigned_to',null=True, blank=True)

    def __str__(self):
        return self.title
    
class Product(models.Model):
    name = models.CharField(max_length=256)
    batchno = models.BigIntegerField()
    productno = models.BigIntegerField()
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ProductDeleted(models.Model):
    name = models.CharField(max_length=256)
    batchno = models.BigIntegerField()
    productno = models.BigIntegerField()
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ProductLogs(models.Model):
    name = models.CharField(max_length=256)
    batchno = models.BigIntegerField()
    productno = models.BigIntegerField()
    action=models.CharField(max_length=256,blank=True)
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # product=models.ForeignKey(Product, on_delete=models.CASCADE,default=1)
    product=models.CharField(max_length=256)
    quantity = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)
    status = models.PositiveIntegerField(default=2)

    def __str__(self):
        return self.title

class VendorRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.CharField(max_length=256)
    quote = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    desp=models.TextField()
    created_date = models.DateField(auto_now_add=True)
    status = models.PositiveIntegerField(default=2)
    image=models.ImageField(upload_to='vendorrequest',blank=True)

    def __str__(self):
        return self.title


class VendorRequestImage(models.Model):
    request = models.ForeignKey('VendorRequest', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vendor_request_images')
    
class QR(models.Model):
    data = models.CharField(max_length=256)
    image=models.ImageField(upload_to='qr',blank=True)
    
    def __str__(self):
        return self.name
    
class ProductAddModels(models.Model):
    name = models.CharField(max_length=256)
    created_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
