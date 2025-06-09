from django.db import models

class rawdatacity(models.Model):
    rawcity_name=models.TextField()

class correctedcity(models.Model):
    correctedcity_name=models.CharField(max_length=35)