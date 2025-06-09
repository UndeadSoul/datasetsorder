from django.db import models

class rawdatacity(models.Model):
    rawcity_name=models.TextField()

class ciudades_norm(models.Model):
    correctedcity_name=models.CharField(max_length=35)