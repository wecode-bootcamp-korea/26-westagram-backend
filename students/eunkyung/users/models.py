from django.db import models

# Create your models here.

class User(models.Model):
    name         = models.CharField(max_length=45)
    email        = models.CharField(max_length=45, unique=True)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=45)
    address      = models.CharField(max_length=200)

    class Meta:
        db_table = 'users'