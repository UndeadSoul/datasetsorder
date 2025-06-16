from django.db import models

class rawdatacity(models.Model):
    rawcity_name=models.TextField()

class ciudades_norm(models.Model):
    correctedcity_name=models.CharField(max_length=35)

class fnac_famosos(models.Model):
    raw_fnac=models.TextField()

class fnac_famosos_norm(models.Model):
    fnac_name=models.TextField()
    fnac_date=models.TextField()
    fnac_age=models.TextField()
    fnac_birthday=models.TextField()