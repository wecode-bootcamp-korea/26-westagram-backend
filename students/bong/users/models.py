from django.db import models
from django.db import DatabaseError
from django.db.models.deletion import CASCADE

class Name(models.Model):
    user_name = models.CharField(max_length=45)

    class Meta:
        db_table = 'name'

class Email(models.Model):
    user_email = models.EmailField(max_length=200)

    class Meta:
        db_table = 'email'

class Password(models.Model):
    user_password = models.CharField(max_length=200)

    class Meta:
        db_table = 'password'

class Phone(models.Model):
    user_phone_num = models.CharField(max_length=11)

    class Meta:
        db_table = 'phone'

class etc(models.Model):
    user_etc = models.CharField(max_length=200)

    class Meta:
        db_table = 'etc'
        



