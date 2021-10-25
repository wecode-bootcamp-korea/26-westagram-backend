from django.db import models

class User(models.Model):
    name          = models.CharField(max_length=45)
    email         = models.CharField(max_length=255, unique=True)
    password      = models.CharField(max_length=200)
    phone_number  = models.CharField(max_length=13)
    personal_info = models.TextField()
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
