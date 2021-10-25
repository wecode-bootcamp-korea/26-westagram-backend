from django.db import models

# Create your models here.

class User(models.Model):
    name         = models.CharField(max_length=45)
    email        = models.CharField(max_length=45, unique=True)
    password     = models.CharField(max_length=200)
    number       = models.CharField(max_length=45, default='')
    nickname     = models.CharField(max_length=45, default='')

    class Meta:
        db_table = 'users'