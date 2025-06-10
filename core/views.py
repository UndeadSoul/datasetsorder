import unicodedata
from django.shortcuts import redirect, render
from .forms import TextFileForm
from .models import rawdatacity,ciudades_norm
import re

# Create your views here.

def home(request):
        return render(request, 'core/home.html')
 
def upload_file(request):
        if request.method == 'POST':
                form = TextFileForm(request.POST, request.FILES)
                if form.is_valid():
                        #Antes de cargar el archivo con las ciudades, vamos a borrar los datos ya existentes
                        rawdatacity.objects.all().delete()
                        ciudades_norm.objects.all().delete()
                        #Se procesa el archivo y se guarda linea por linea
                        file = form.cleaned_data['file']
                        for line in file:
                                rawdatacity.objects.create(rawcity_name=line.decode('utf-8').strip())
                        return redirect("success")
        else:
                form = TextFileForm()
        return render(request, 'core/upload_file.html', {'form':form})

def success(request):
        rawdata=rawdatacity.objects.all()
        return render(request, 'core/success.html',{'rawdata':rawdata})

def clean_data(request):
        #obtener datos y ordenarlos
        rawdata=rawdatacity.objects.all()
        ciudades_norm.objects.all().delete()
        #Aplicar limpieza
        cities = set()
        for city in range(len(rawdata)):
                #quitar los numeros del inicio
                text=rawdata[city].rawcity_name #obtener cada uno de las ciudades
                pos=text.find(". ")             #encontrar los caracteres que van despues de los numeros
                if pos != -1:
                        text=text[pos+2:]       #hacer un slice sin los caracteres ("<numero>. ")
                else:
                        text=text
                #quitar los tildes
                text = clean_accent(text)
                #quitar los que no sea letras o espacios
                text = re.sub(r'[^a-zA-Z\s]', '', text)
                #quitar espacios extra
                text = re.sub(r'\s+', ' ', text).strip()
                #transformar las mayusculas a minusculas
                text = text.lower()
                #capitalizar
                text = text.capitalize()
                #comparar con otros para saber si se repite
                if text not in cities:
                        cities.add(text)
                        #guardar en base de datos
                        ciudades_norm.objects.create(correctedcity_name=text)
        #obtener los objetos de los datos limpios en la bdd
        clean_data=ciudades_norm.objects.all().order_by('correctedcity_name')
        return render(request, 'core/clean_data.html', {'clean_data':clean_data, 'rawdata':rawdata})


def clean_accent(texto):
    texto_normalizado = unicodedata.normalize('NFD', texto)
    texto_sin_acentos = ''.join(
        c for c in texto_normalizado if unicodedata.category(c) != 'Mn'
    )
    return texto_sin_acentos