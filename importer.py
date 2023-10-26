import requests
import pandas as pd
import time
from datetime import date
from database import SessionLocal
from models import Estate
from unidecode import unidecode

def importer(ciudad,inmueble,transaccion):
    if transaccion == "venta":
        tslug = 'sell'
    if transaccion == "arriendo":
        tslug = 'rent'
    if inmueble == "apartamento":
        inslug = "apartment"
    if inmueble == "casa":
        inslug = "house"
    if ciudad == "Medellin":
        ciudadstr = "Medellín"
        ciudadcoords = [[-75.5635900,6.2518400],[-75.5435900,6.2318400]]
    elif ciudad == "Cali":
        ciudadstr = "Cali"
        ciudadcoords = [[-76.5225,3.43722],[-76.5425,3.45722]]
    elif ciudad == "Barranquilla":
        ciudadstr = "Barranquilla"
        ciudadcoords = [[-74.5225,7.43722],[-74.5425,7.45722]]
    else:
        ciudadstr = "Bogota"
        ciudadcoords =[[-74.0611609,4.6707751],[-74.0889301,4.5628634]]
    hitlist = []
    homes = []
    now = date.today()

    for offset in range(0,5000,25):

        print(offset)
        headers = {
           "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
           "referer": "https://fincaraiz.com.co/"
        }

        json_data = {
         'filter': {
            'offer': {
                'slug': [
                    tslug,
                  ],
              },
            'property_type': {
                'slug': [
                    inslug,
                  ],
              },
            'locations': {
                'location_point': ciudadcoords,
            },

         },

         'fields': {
            'exclude': [],

            'include': [
                'area',
                'is_new',
                'baths.name',
                'locations.cities.name',
                'locations.cities.slug',

                'locations.countries.name',
                'locations.countries.slug',
                'locations.groups.name',
                'locations.groups.slug',
                'locations.groups.subgroups.name',
                'locations.groups.subgroups.slug',
                'locations.location_point',
                'locations.neighbourhoods.name',
                'locations.neighbourhoods.slug',
                'locations.states.name',
                'locations.states.slug',
                'locations.view_map.slug',
                'price',
                'products.configuration.tag_id',
                'products.configuration.tag_name',
                'products.label',
                'products.name',
                'products.slug',
                'property_id',
                'fr_property_id',
                'rooms.name',
                'title',
                'property_type.name',


            ],
            'limit': 25,
            'offset': offset, #set to 25 to get the second page, 50 for the 3rd page etc.
            'ordering': [],
            'platform': 40,
            'with_algorithm': False,
           },
        }
        try:
            response = requests.post('https://api.fincaraiz.com.co/document/api/1.0/listing/search',
            headers=headers, json=json_data)
            data = response.json()

            hits = data["hits"]["hits"]
            rooturl = "https://www.fincaraiz.com.co/inmueble/apartamento-en-venta/"
            for h in hits:

                subdata  = (h["_source"]["listing"])
                if "location_point" in subdata["locations"]:
                    lp = subdata["locations"]["location_point"]
                else:
                    lp = "0,0"

                suborg = {}
                if "neighbourhoods" in subdata["locations"]:
                    suborg["barrio"] = subdata["locations"]["neighbourhoods"][0]["name"]
                else:
                    suborg["barrio"] = "No Barrio"
                suborg["city"] =subdata["locations"]["cities"][0]["name"]
                area = float(subdata["area"])
                rooms = subdata["rooms"]["name"]
                bath = subdata["baths"]["name"]
                if type(rooms) is str:
                    rooms = 0
                if type(bath) is str:
                    bath = 0
                if area == 0:
                    area = 1
                subestate = Estate(
                    area=area,
                    rooms=rooms,
                    bath=bath,
                    price=float(subdata["price"]),
                    property_type=inmueble,
                    pid=subdata["property_id"],
                    city=suborg["city"],
                    barrio= suborg["barrio"],
                    url=rooturl+suborg["barrio"].replace(" ","-")+"/"+unidecode(suborg["city"])+"/"+str(subdata["fr_property_id"]),
                    fuente="Finca Raiz",
                    m2price=float(subdata["price"])/area,
                    fecha=now,
                    tipo = transaccion,
                    lp = lp
                )
                homes.append(subestate)
        except:
            pass






        time.sleep(0.025)


    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5,ca;q=0.4,pt;q=0.3",
        "sec-ch-ua": "\"Chromium\";v=\"112\", \"Microsoft Edge\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-api-key": "P1MfFHfQMOtL16Zpg36NcntJYCLFm8FqFfudnavl",
        "x-requested-with": "XMLHttpRequest",
        "referrer": "https://www.metrocuadrado.com/apartamento/venta/bogota/?search=form",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "credentials": "include",
    }

    for offset in range(0,5000,25):
        print(offset)
        response = requests.get('https://www.metrocuadrado.com/rest-search/search?realEstateBusinessList='+transaccion+'&city='+ciudadstr+'&realEstateTypeList='+inmueble+'&from='+str(offset) +'&size=100',headers=headers)
        data = response.json()
        hits = data["results"]

        for hit in hits:
            print(hit)
            price = 0
            if transaccion == 'arriendo':
                price = float(hit["mvalorarriendo"])
            else:
                price = float(hit["mvalorventa"])
            suborg = {}
            try:
                area = float(hit["marea"])
            except:
                area = 1
            rooms = hit["mnrocuartos"]
            bath = hit["mnrobanos"]
            suborg["property_type"] = inmueble
            suborg["id"] = hit['midinmueble']
            suborg["city"] = hit["mciudad"]["nombre"]
            suborg["barrio"] = hit["mbarrio"]
            suborg["fuente"] = "Metro Cuadrado"
            suborg["link"] = "https://www.metrocuadrado.com" + hit["link"]
            if type(rooms) is str:
                rooms = 0
            if type(bath) is str:
                bath = 0
            if area == 0:
                area = 1
            subestate = Estate(
                area=area,
                rooms=rooms,
                bath=bath,
                price=price,
                property_type="Apartamento",
                pid=hit['midinmueble'],
                city=hit["mciudad"]["nombre"],
                barrio=hit["mbarrio"],
                url="https://www.metrocuadrado.com" + hit["link"],
                fuente="Metro Cuadrado",
                m2price=price / area,
                fecha=now,
                tipo = transaccion,
                lp = "0,0"
            )

            homes.append(subestate)
        time.sleep(0.025)


    print(len(homes))
    with SessionLocal.begin() as session:
        session.add_all(homes)
        session.commit()

