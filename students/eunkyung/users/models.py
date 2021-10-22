from django.db import models

# Create your models here.

class User(models.Model):
    name         = models.CharField(max_length=45)
    email        = models.CharField(max_length=45, unique=True)
    password     = models.CharField(max_length=45)
    phone_number = models.PositiveIntegerField(default=0)
    address      = models.TextField ()

    class Meta:
        db_table = 'users'