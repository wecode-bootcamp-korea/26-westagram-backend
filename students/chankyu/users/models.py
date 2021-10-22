from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    age = models.PositiveIntegerField() 
    
    class Meta:
        db_table = 'users'