from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=120)

    class Meta:
        db_table = 'users'