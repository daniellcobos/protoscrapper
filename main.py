import requests
import pandas as pd
import time
from datetime import date
hitlist = []
now = date.today()

for offset in range(0,10000,25):
    print(offset)
    headers = {
       "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
       "referer": "https://fincaraiz.com.co/"
    }

    json_data = {
     'filter': {
        'offer': {
            'slug': [
                'sell',
              ],
          },
        'property_type': {
            'slug': [
                'apartment',
              ],
          },
        'locations': {
            'location_point':[
                [
                 -74.0611609,
                4.6707751
                ],
                [
                -74.0889301,
                4.5628634
                ],
            ],
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

    response = requests.post('https://api.fincaraiz.com.co/document/api/1.0/listing/search',
    headers=headers, json=json_data)
    data = response.json()
    hits = data["hits"]["hits"]
    rooturl = "https://www.fincaraiz.com.co/inmueble/apartamento-en-venta/"
    for h in hits:
        subdata  = (h["_source"]["listing"])


        suborg = {}
        suborg["area"] = float(subdata["area"])
        suborg["rooms"] = subdata["rooms"]["name"]
        suborg["baths"] = subdata["baths"]["name"]
        suborg["price"] = float(subdata["price"])
        suborg["property_type"] = "Apartamento"
        suborg["id"] = subdata["property_id"]
        suborg["city"] = subdata["locations"]["cities"][0]["name"]
        if "neighbourhoods" in subdata["locations"]:
            suborg["barrio"] = subdata["locations"]["neighbourhoods"][0]["name"]
        else:
            suborg["barrio"] = "No Barrio"

        suborg["url"] = rooturl+suborg["barrio"].replace(" ","-")+"/"+suborg["city"]+"/"+str(subdata["fr_property_id"])
        suborg["fuente"] = "Finca Raiz"
        hitlist.append(suborg)
    time.sleep(1)


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

for offset in range(0,10000,100):
    print(offset)
    response = requests.get('https://www.metrocuadrado.com/rest-search/search?realEstateBusinessList=venta&city=Bogotá&realEstateTypeList=apartamento&from='+str(offset) +'&size=100',headers=headers)
    data = response.json()
    hits = data["results"]

    for hit in hits:

        suborg = {}
        suborg["area"] = float(hit["marea"])
        suborg["rooms"] = hit["mnrocuartos"]
        suborg["baths"] = hit["mnrobanos"]
        suborg["price"] = float(hit["mvalorventa"])
        suborg["property_type"] = "Apartamento"
        suborg["id"] = hit['midinmueble']
        suborg["city"] = hit["mciudad"]["nombre"]
        suborg["barrio"] = hit["mbarrio"]
        suborg["fuente"] = "Metro Cuadrado"
        suborg["link"] = "https://www.metrocuadrado.com" + hit["link"]

        hitlist.append(suborg)
    time.sleep(0.5)


df = pd.DataFrame(hitlist)
df = df.drop_duplicates()
df["preciom2"] = df["price"]/df["area"]
df["Fecha"] = now
print(df)
df.to_excel("Lista3.xlsx")

