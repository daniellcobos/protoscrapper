import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import json

hitlist = []


hitlist = []
tslug = 'sell'
inslug = "apartment"
ciudadstr = "Bogota"
ciudadcoords =[[-74.0611609,4.6707751],[-74.0889301,4.5628634]]
for  offset in range(0,1,1):
    headers = {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
        "referer": "https://fincaraiz.com.co/"
    }



    response = requests.get('https://www.metrocuadrado.com/inmueble/venta-apartamento-medellin-san-diego-3-habitaciones-2-banos-1-garajes/14473-M3501224',headers=headers)
    data = response.text


    # parse the HTML
    soup = BeautifulSoup(data, "html.parser")

    # print the HTML as text
    script = soup.find("script",id="__NEXT_DATA__")
    hdict = json.loads(script.text)
    print(hdict['props']['initialState']['realestate']['basic']['garages'])
    print(hdict['props']['initialState']['realestate']['basic']['stratum'])
    print(hdict['props']['initialState']['realestate']['basic']['builtTime'])
