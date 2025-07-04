import unicodedata, chardet
from django.http import HttpResponse
from django.shortcuts import redirect, render
from datetime import datetime
from .forms import TextFileForm
from .models import rawdatacity,ciudades_norm,fnac_famosos,fnac_famosos_norm,Place, Address, Georeference
import re
import csv

# Create your views here.

def home(request):
        return render(request, 'core/home.html')

"""Ciudades""" 
def upload_file(request):
        if request.method == 'POST':
                form = TextFileForm(request.POST, request.FILES)
                if form.is_valid():
                        #Antes de cargar el archivo con las ciudades, se borran los datos ya existentes
                        rawdatacity.objects.all().delete()
                        ciudades_norm.objects.all().delete()
                        #Se lee el contenido bruto del archivo
                        file = form.cleaned_data['file']
                        raw_bytes = file.read()
                        #se detecta la codificacion
                        result = chardet.detect(raw_bytes)
                        encoding = result['encoding'] or 'utf-8'
                        print(f"codificacion detectada: {encoding}")
                        #decodificar contenido
                        text = raw_bytes.decode(encoding,errors='replace')
                        #guardar linea por linea
                        for line in text.splitlines():
                               rawdatacity.objects.create(rawcity_name=line.strip())
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
###########################################################

"""Fecha"""
def upload_file_date(request):
        if request.method == 'POST':
                form = TextFileForm(request.POST, request.FILES)
                if form.is_valid():
                        #Antes de cargar el archivo con las fechas, vamos a borrar los datos ya existentes
                        fnac_famosos.objects.all().delete()
                        fnac_famosos_norm.objects.all().delete()
                        #Se lee el contenido bruto del archivo
                        file = form.cleaned_data['file']
                        raw_bytes = file.read()
                        #se detecta la codificacion
                        result = chardet.detect(raw_bytes)
                        encoding = result['encoding'] or 'utf-8'
                        print(f"codificación detectada: {encoding}")
                        #decodificar contenido
                        text = raw_bytes.decode(encoding,errors='replace')
                        #guardar linea por linea
                        for line in text.splitlines():
                                fnac_famosos.objects.create(raw_fnac=line.strip())
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
        dataflag=False
        for line in range(len(rawdata)):
                #quitar los numeros del inicio
                data=rawdata[line].raw_fnac
                substring_name=""
                pos1=data.find(". ")    #encontrar los caracteres que van despues de los numeros
                pos2=data.find(" - ")   #encontrar los caracteres que dividen el nombre de la fecha        
                if pos2==-1:
                        pos2=data.find("\t")
                        substring_date=data[pos2+1:]
                else: 
                        substring_date=data[pos2+3:]
                if pos1>-1:
                        substring_name=data[pos1+2:pos2]      
                else:
                        substring_name=data[:pos2]
                
                print(f"nombre: {substring_name} - fecha: {substring_date}")
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
                                        year, month, day = substring_date.split("-")
                                else:
                                        day, month, year = substring_date.split("-")
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
                                fnac_famosos_norm.objects.create(fnac_name=substring_name, fnac_date=str_year,fnac_age=amount_of_years)
                        else:
                                #no guardar en base de datos
                                dataflag=True
                        
        #obtener los objetos de los datos limpios en la bdd
        clean_data=fnac_famosos_norm.objects.all().order_by('fnac_name')
        return render(request, 'core/clean_data_date.html', {'clean_data':clean_data, 'rawdata':rawdata, 'dataflag':dataflag})
###########################################################

"""Direccion"""
def upload_file_places(request):
    if request.method == 'POST':
        form = TextFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Limpiar todo antes de importar
            Place.objects.all().delete()
            Address.objects.all().delete()
            Georeference.objects.all().delete()

            file = form.cleaned_data['file']

            seen_places = set()
            seen_addresses = set()

            places_to_create = []
            addresses_to_create = []
            georefs_to_create = []

            for line in file:
                try:
                    line_str = line.decode('utf-8').strip()
                except UnicodeDecodeError:
                    line_str = line.decode('latin-1').strip()

                parts = line_str.split(';')
                if len(parts) != 3:
                    continue

                name = parts[0].strip()
                address_str = parts[1].strip()
                geo_str = parts[2].strip()

                # Skip duplicate places
                if name in seen_places:
                    continue
                seen_places.add(name)

                # Parse address
                addr_parts = [x.strip() for x in address_str.split(',')]
                street_name = addr_parts[0] if len(addr_parts) > 0 else ''
                street_number = addr_parts[1] if len(addr_parts) > 1 else ''
                city_state = addr_parts[2] if len(addr_parts) > 2 else ''
                country = addr_parts[3] if len(addr_parts) > 3 else ''

                address_key = (street_name.lower(), street_number.lower(), city_state.lower(), country.lower())
                if address_key in seen_addresses:
                    continue
                seen_addresses.add(address_key)

                # Crear instancia del lugar (no guardada aún)
                place = Place(name=name)
                places_to_create.append(place)

                # Guardamos datos para usar después (con el índice correspondiente)
                addresses_to_create.append((place, street_name, street_number, city_state, country))
                try:
                    lat, lon = map(float, geo_str.split(','))
                except Exception:
                    lat, lon = 0.0, 0.0
                georefs_to_create.append((place, lat, lon))

            # Guardar Places
            Place.objects.bulk_create(places_to_create)

            # Ahora que los places están guardados, agregamos Address y Georeference
            Address.objects.bulk_create([
                Address(
                    place=place,
                    street_name=street_name,
                    street_number=street_number,
                    city_state_province=city_state,
                    country=country
                )
                for place, street_name, street_number, city_state, country in addresses_to_create
            ])

            Georeference.objects.bulk_create([
                Georeference(place=place, latitude=lat, longitude=lon)
                for place, lat, lon in georefs_to_create
            ])

            return redirect('success_places')
    else:
        form = TextFileForm()

    return render(request, 'core/upload_file_places.html', {'form': form})


def success_places(request):
    places = Place.objects.prefetch_related('address', 'georeference').all()
    places_data = []

    for place in places:
        address = getattr(place, 'address', None)
        georef = getattr(place, 'georeference', None)
        places_data.append({
            'name': place.name,
            'address': address,
            'georef': georef,
        })

    return render(request, 'core/success_places.html', {'places_data': places_data})


def clean_data_address(request):
    # Direcciones únicas ordenadas por nombre y número de calle
    addresses = Address.objects.order_by('street_name', 'street_number')
    return render(request, 'core/clean_data_address.html', {'addresses': addresses})


###########################################################

"""Descargar registros"""
def export_csv(request):
        data_type = request.GET.get("data_type")
        models={
                'cities':{
                        'model':ciudades_norm,
                        'fields':['correctedcity_name'],
                        'headers':['Nombre ciudad']
                },
                'dates':{
                        'model':fnac_famosos_norm,
                        'fields':['fnac_name','fnac_date','fnac_age','fnac_birthday'],
                        'headers':['Nombre','Fecha','Edad','Cumpleaños']
                },
                'addresses':{
                        'model':[],
                        'fields':[],
                        'headers':['Nombre', 'Calle','Numero','C.S.P.','Pais','Latitud','Longitud']
                }
        }
        if data_type not in models:
                return HttpResponse("Tabla no válida", status=400)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition']= f'attachment; filename="{data_type}".csv'
        response.write(u'\ufeff'.encode('utf8'))
        writer=csv.writer(response)
        
        if data_type != "addresses":
                config = models[data_type]
                model = config['model']
                fields= config['fields']
                headers = config['headers']

                writer.writerow(headers)

                for obj in model.objects.all():
                        row = [getattr(obj,field) for field in fields]
                        writer.writerow(row)
        else:
                #caso en el que se necesitan las 3 tablas de direccion
                data1= list(Place.objects.all())
                data2= list(Address.objects.all())
                data3= list(Georeference.objects.all())
                writer.writerow([['Nombre', 'Calle','Numero','C.S.P.','País','Latitud','Longitud']])
                for i in range(len(data1)):
                        row = [
                              data1[i].name,
                              data2[i].street_name,
                              data2[i].street_number,
                              data2[i].city_state_province,
                              data2[i].country,
                              data3[i].latitude,
                              data3[i].longitude,
                        ]
                        writer.writerow(row)
        return response