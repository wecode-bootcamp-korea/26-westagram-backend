from django.db import models

# Create your models here.

class User(models.Model):
    name                 = models.CharField(max_length=100)
    email                = models.EmailField(max_length=100)
    password             = models.CharField(max_length=100)
    telephone            = models.CharField(max_length=100)
    personal_information = models.TextField(max_length=2000)

    class Meta:
        db_table = 'users'