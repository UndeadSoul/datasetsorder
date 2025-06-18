from django.contrib import admin
from .models import rawdatacity,ciudades_norm,fnac_famosos,fnac_famosos_norm,Place,Address,Georeference

admin.site.register(rawdatacity)
admin.site.register(ciudades_norm)

admin.site.register(fnac_famosos_norm)
admin.site.register(fnac_famosos)

admin.site.register(Place)
admin.site.register(Address)
admin.site.register(Georeference)
