from django.db              import models

class User(models.Model):
    name        = models.CharField(max_length=30)
    password    = models.CharField(max_length=300)
    birth       = models.DateField(auto_now=False, auto_now_add=False)
    email       = models.EmailField(max_length=254, unique=True)
    mobile      = models.CharField(max_length=100)
    sns_address = models.URLField(max_length=200, blank=True)
    sign_up     = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'