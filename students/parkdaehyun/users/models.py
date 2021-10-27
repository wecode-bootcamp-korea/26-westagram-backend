from django.db import models

# Create your models here.

class User(models.Model):
    name                 = models.CharField(max_length=100, null=True)
    email                = models.EmailField(max_length=100, unique=True)
    password             = models.CharField(max_length=100)
    telephone            = models.CharField(max_length=100, null=True)
    personal_information = models.TextField(max_length=2000, null=True)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'users'