from django.db import models
from django.db import DatabaseError
from django.db.models.deletion import CASCADE

class User(models.Model):
    user_name = models.CharField(max_length=45)
    user_email = models.EmailField(max_length=200, unique=True)
    user_password = models.CharField(max_length=200)
    user_phone_num = models.CharField(max_length=11)
    
    class Meta:
        db_table = 'users'

