from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    hobby = models.TextField()

    class Meta : 
        db_table = 'users'