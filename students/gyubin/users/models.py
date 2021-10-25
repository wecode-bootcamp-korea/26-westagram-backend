from django.db import models

class User(models.Model):
    name      = models.CharField(max_length=100)
    email     = models.CharField(max_length=100, unique=True)
    password  = models.CharField(max_length=200)
    contact   = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'users'