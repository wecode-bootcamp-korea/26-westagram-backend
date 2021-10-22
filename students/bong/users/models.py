from django.db import models
from django.db import DatabaseError
from django.db.models.deletion import CASCADE

class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    phone_num = models.CharField(max_length=13)
    related_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'

