from datetime import datetime
import re
from django.db import models

"""Ciudades"""
class rawdatacity(models.Model):
    rawcity_name=models.TextField()

class ciudades_norm(models.Model):
    correctedcity_name=models.CharField(max_length=35)

"""Fechas"""
class fnac_famosos(models.Model):
    raw_fnac=models.TextField()

class fnac_famosos_norm(models.Model):
    fnac_name=models.TextField()
    fnac_date=models.TextField()
    fnac_age=models.TextField()

    @property
    def fnac_birthday(self):
        """
        Devuelve True si hoy es el aniversario basado en la fecha del texto.
        """
        match = re.search(r'(\d{1,2})-(\d{1,2})', self.fnac_date)
        if match:
            dia, mes = int(match.group(1)), int(match.group(2))
            hoy = datetime.now()
            return dia == hoy.day and mes == hoy.month
        return False

"""Direcciones"""
class Place(models.Model):
    name = models.CharField(max_length=200)

class Address(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE)
    street_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=20)
    city_state_province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

class Georeference(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
