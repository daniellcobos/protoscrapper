import requests
import pandas as pd
import time

hitlist = []

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
hitlist = []
for  offset in range(0,10000,100):

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
        hitlist.append(suborg)
    time.sleep(0.5)
df = pd.DataFrame(hitlist)
df = df.drop_duplicates()
df["preciom2"] = df["price"]/df["area"]
print(df)
df.to_excel("Lista2.xlsx")