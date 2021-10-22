from django.db import models

class User(models.Model):
	name      = models.CharField(max_length=100)
	email     = models.CharField(max_length=100)
	password  = models.CharField(max_length=200)
	contact   = models.CharField(max_length=100)

	class Meta:
		db_table = 'users'