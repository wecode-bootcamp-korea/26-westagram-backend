from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    OtherPersonalInf = models.CharField(max_length=200)

    class Meta:
        db_table = "users"