from django.db import models

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "accounts"
