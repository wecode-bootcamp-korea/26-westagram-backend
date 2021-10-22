from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=45)
    email        = models.EmailField(max_length=45, unique=True)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=17, blank=True)
    url          = models.CharField(max_length=1000,blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
