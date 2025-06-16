import unicodedata
from django.shortcuts import redirect, render
from datetime import datetime
from .forms import TextFileForm
from .models import rawdatacity,ciudades_norm,fnac_famosos,fnac_famosos_norm
import re

# Create your views here.

def home(request):
        return render(request, 'core/home.html')

########################################################### 
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
###########################################################

###########################################################
def upload_file_date(request):
        if request.method == 'POST':
                form = TextFileForm(request.POST, request.FILES)
                if form.is_valid():
                        #Antes de cargar el archivo con las fechas, vamos a borrar los datos ya existentes
                        fnac_famosos.objects.all().delete()
                        fnac_famosos_norm.objects.all().delete()
                        #Se procesa el archivo y se guarda linea por linea
                        file = form.cleaned_data['file']
                        for line in file:
                                fnac_famosos.objects.create(raw_fnac=line.decode('utf-8').strip())
                        return redirect("success_date")
        else:
                form = TextFileForm()
        return render(request, 'core/upload_file_date.html', {'form':form})

def success_date(request):
        rawdata=fnac_famosos.objects.all()
        return render(request, 'core/success_date.html',{'rawdata':rawdata})

def clean_data_date(request):
        #obtener datos y ordenarlos
        rawdata=fnac_famosos.objects.all()
        fnac_famosos_norm.objects.all().delete()
        #Aplicar limpieza
        names = set()
        for line in range(len(rawdata)):
                #quitar los numeros del inicio
                data=rawdata[line].raw_fnac
                pos1=data.find(". ")    #encontrar los caracteres que van despues de los numeros
                pos2=data.find(" - ")   #encontrar los caracteres que dividen el nombre de la fecha        
                substring_name=data[pos1+2:pos2]
                substring_date=data[pos2+3:]
                #comparar con otros para saber si se repite
                if substring_name not in names:
                        names.add(substring_name)
                        #limpiar y formatear fecha
                        ##verificar si es una fecha tradicional
                        ###si es que la fecha posee - o /
                        substring_date=substring_date.replace("/","-")
                        if substring_date.find("-")!=-1:
                                #si es que la fecha tiene 4>= caracteres al inicio, va a ser el año
                                if substring_date.find("-")>=3:
                                        day=substring_date[-2:]
                                        month=substring_date[-5:-3:]
                                        year=substring_date[:-6]
                                        str_year=day+"-"+month+"-"+year
                                        #extraer dia mes y año actual
                                        today = datetime.today()
                                        this_year = today.year
                                        #calcular edad y cumplaños
                                        if "a.C." in year:
                                                year=year.replace(" a.C.", "")
                                                year=-int(year)
                                        else:
                                                year=int(year)
                                        amount_of_years=this_year-year
                                        if (today.month, today.day) < (int(month), int(day)):
                                                amount_of_years -= 1
                                        fnac_famosos_norm.objects.create(fnac_name=substring_name, fnac_date=str_year,fnac_age=amount_of_years,fnac_birthday="")
                        else:
                                #guardar en base de datos
                                fnac_famosos_norm.objects.create(fnac_name=substring_name, fnac_date=substring_date,fnac_age="",fnac_birthday="")
        #obtener los objetos de los datos limpios en la bdd
        clean_data=fnac_famosos_norm.objects.all().order_by('fnac_name')
        return render(request, 'core/clean_data_date.html', {'clean_data':clean_data, 'rawdata':rawdata})
###########################################################


###########################################################
def clean_accent(texto):
    texto_normalizado = unicodedata.normalize('NFD', texto)
    texto_sin_acentos = ''.join(
        c for c in texto_normalizado if unicodedata.category(c) != 'Mn'
    )
    return texto_sin_acentos