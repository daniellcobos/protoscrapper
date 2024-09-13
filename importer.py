import requests
import pandas as pd
import time
from datetime import date
from database import SessionLocal
from models import Estate
from unidecode import unidecode
import json
from bs4 import BeautifulSoup

def importer(ciudad,inmueble,transaccion):
    queries = 2000
    if transaccion == "venta":
        optype = 1
        tslug = 'sell'
    if transaccion == "arriendo":
        optype = 2
        tslug = 'rent'
    if inmueble == "apartamento":
        inslug = "apartment"
        propid = 2
    if inmueble == "casa":
        inslug = "house"
        propid = 1
    if ciudad == "Medellin":
        ciudadstr = "Medellín"
        estatestr = {
                        "name": "Antioquia",
                        "id": "2d63ee80-421b-488f-992a-0e07a3264c3e",
                        "slug": "state-colombia-05-antioquia"
                    }
        ciudadcoords = [[-75.5635900,6.2518400],[-75.5435900,6.2318400]]
        cityid= "183f0a11-9452-4160-9089-1b0e7ed45863"
        slug = "city-colombia-05-001"
        queries = 500
    elif ciudad == "Cali":
        ciudadstr = "Cali"
        ciudadcoords = [[-76.5225,3.43722],[-76.5425,3.45722]]
        queries = 400
    elif ciudad == "Barranquilla":
        ciudadstr = "Barranquilla"
        ciudadcoords = [[-74.5225,7.43722],[-74.5425,7.45722]]
        queries = 400
    else:
        ciudadstr = "Bogota"
        ciudadcoords =[[-74.0611609,4.6707751],[-74.0889301,4.5628634]]
        slug = "city-colombia-11-001"
        estatestr = {
                "name": "Bogotá, d.c.",
                "id": "2d9f0ad9-8b72-4364-a7dc-e161d7dddb4d",
                "slug": "state-colombia-11-bogota-dc"
            }
        cityid = "65d441f3-a239-4111-bc5b-01c5a268869f"

        queries = 1500
    hitlist = []
    homes = []
    homes2 = []
    now = date.today()

    k = 0
    for page in range(1,50):
        k = k + 1
        print(k)

        headers = {
           "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
           "referer": "https://fincaraiz.com.co/"
        }

        json_data = {
    "variables": {
        "rows": 21,
        "params": {
            "page": page,
            "order": 2,
            "operation_type_id": optype,
            "property_type_id": [
               propid
            ],
            "currencyID": 4,
            "m2Currency": 4,
            "locations": [
                {
                    "country": [
                        {
                            "name": "Colombia",
                            "id": "858656c1-bbb1-4b0d-b569-f61bbdebc8f0",
                            "slug": "country-48-colombia"
                        }
                    ],
                    "name": ciudadstr,
                    "location_point": {
                        "coordinates": ciudadcoords[0],
                        "type": "point"
                    },
                    "id": cityid,
                    "type": "CITY",
                    "slug": [
                        slug
                    ],
                    "estate": estatestr,
                }
            ]
        },
        "page": 1,
        "source": 10
    },
    "query": ""
}



        try:
            response = requests.post('https://search-service.fincaraiz.com.co/api/v1/properties/search',
            headers=headers, json=json_data)
            rooturl = "https://www.fincaraiz.com.co"
            data = response.json()
            hits = data["hits"]["hits"]

            for i,hit in enumerate(hits):

                subdata= (hit["_source"]["listing"])

                if "location_point" in subdata["locations"]:

                    lp = subdata["locations"]["location_point"]



                else:
                    lp = "POINT(0 0)"

                suborg = {}

                if 'neighbourhood' in subdata["locations"]:
                    suborg["barrio"] = subdata["locations"]['neighbourhood'][0]["name"]
                    suborg["barrio"] = suborg["barrio"]
                else:
                    suborg["barrio"] = "No Barrio"

                area = float(subdata["m2"])
                rooms = subdata["rooms"]
                bath = subdata["bathrooms"]
                city = subdata["locations"]["city"][0]["name"]

                try:
                    rooms = int(rooms)
                    bath = int(bath)
                except:
                    rooms = 0
                    bath = 0

                if area == 0:
                    area = 1
                url = str(rooturl) + str(subdata["link"])
                garage = subdata["garage"]
                estrato = subdata["stratum"]
                antiguedad = subdata["construction_year"]

                subestate = Estate(
                    area=area,
                    rooms=rooms,
                    bath=bath,
                    price=float(subdata["price"]["amount"]),
                    property_type=inmueble,
                    pid=subdata["id"],
                    city=city,
                    barrio=str(suborg["barrio"]).upper(),
                    url=url,
                    garage=garage,
                    estrato=estrato,
                    fuente="Finca Raiz",
                    m2price=float(subdata["price"]["amount"]) / area,
                    fecha=now,
                    tipo=transaccion,
                    lp=lp,
                    antiguedad=antiguedad,
                    cons="No aplica"
                )
                homes.append(subestate)
        except Exception as e:
            print(e)
        time.sleep(2)








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
    k = 0
    for offset in range(0,1000,50):
        try:
            k = k + 1
            print("Metrocuadrado",k)
            ult = "https://www.metrocuadrado.com/rest-search/search?realEstateBusinessList=venta&realEstateStatusList=nuevo&city=Bogot%C3%A1&from=0&size=50"
            response = requests.get('https://www.metrocuadrado.com/rest-search/search?realEstateBusinessList='+transaccion+'&city='+ciudadstr+'&realEstateTypeList='+ inmueble+'&from='+str(offset) +'&size=50',headers=headers)
            data = response.json()
            hits = data["results"]
            print(k)

            for hit2 in hits:
                price = 0
                if transaccion == 'arriendo':
                    price = float(hit2["mvalorarriendo"])
                else:
                    price = float(hit2["mvalorventa"])
                suborg = {}
                try:
                    area = float(hit2["marea"])
                except:
                    area = 1

                url = "https://www.metrocuadrado.com" + hit2["link"]
                garage,estrato,antiguedad = MetroCuadradoComp(url)
                rooms = hit2["mnrocuartos"]
                bath = hit2["mnrobanos"]
                suborg["property_type"] = inmueble
                suborg["id"] = hit2['midinmueble']

                suborg["city"] = hit2["mciudad"]["nombre"]
                suborg["barrio"] = hit2["mbarrio"]
                suborg["fuente"] = "Metro Cuadrado"
                suborg["link"] = url
                suborg["idven"] = hit2['midempresa']

                try:
                    rooms = int(rooms)
                    bath = int(bath)
                except:
                    rooms = 0
                    bath = 0

                if area == 0:
                    area = 1
                subestate = Estate(
                    area=area,
                    rooms=rooms,
                    bath=bath,
                    price=price,
                    property_type="Apartamento",
                    pid=hit2['midinmueble'],
                    city=hit2["mciudad"]["nombre"],
                    barrio=hit2["mbarrio"].upper(),
                    url="https://www.metrocuadrado.com" + hit2["link"],
                    fuente="Metro Cuadrado",
                    m2price=price / area,
                    fecha=now,
                    tipo = transaccion,
                    lp = "POINT(0 0)",
                    cons = suborg["idven"],
                    garage = garage,
                    estrato = estrato,
                    antiguedad = antiguedad,
                )
                print(subestate)
                homes2.append(subestate)
        except Exception as e:
            print(e)



    print(len(homes))
    with SessionLocal.begin() as session:
        session.add_all(homes)
        session.commit()
    with SessionLocal.begin() as session:
        session.add_all(homes2)
        session.commit()





def fincaraizindComp(url):
    try:
        headers = {
            "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
            "referer": "https://fincaraiz.com.co/"
        }

        response = requests.get(url,headers=headers)
        data = response.text

        # parse the HTML
        soup = BeautifulSoup(data, "html.parser")

        # print the HTML as text
        script = soup.find("script", id="__NEXT_DATA__")
        hdict = json.loads(script.text)["props"]["pageProps"]
        hdictseo = json.loads(script.text)["props"]["pageProps"]["seo"]["description"]
        hdictseo = hdictseo.split(",")

        antiguedad = hdictseo[3][12:]
        return hdict["garages"]['name'], hdict['stratum']['name'],antiguedad

    except:
        return "Sin especificar", "Sin especificar","Sin especificar "

def MetroCuadradoComp(url):
    try:
        headers = {
            "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
            "referer": "https://fincaraiz.com.co/"
        }

        response = requests.get(url,headers=headers)
        data = response.text

        # parse the HTML
        soup = BeautifulSoup(data, "html.parser")

        # print the HTML as text
        script = soup.find("script", id="__NEXT_DATA__")
        hdict = json.loads(script.text)
        if hdict['props']['initialState']['realestate']['basic']['builtTime']:
            builtime = (hdict['props']['initialState']['realestate']['basic']['builtTime'])
        else:
            builtime = 'sin especificar'
        garage = (hdict['props']['initialState']['realestate']['basic']['garages'])
        stratum = (hdict['props']['initialState']['realestate']['basic']['stratum'])

        return (garage,stratum,builtime)

    except Exception as e:
        print(e)
        return "sin especificar","sin especificar","sin especificar"
