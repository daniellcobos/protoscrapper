import pandas as pd
from fastapi import FastAPI
from importer import importer
from models import Estate
from database import SessionLocal
from sqlalchemy import desc

app = FastAPI()


@app.get("/")
async def root():

    return {"message": "Hello World"}


@app.get("/importer/{ciudad}/{inmueble}/{transaccion}")
async def filldatabase(ciudad: str, inmueble:str, transaccion:str):
    importer(ciudad,inmueble,transaccion)
    return {"message": f"Hello {ciudad}"}

@app.get("/absoluteimporter")
async def filldatabase():
    for ciudad in ["Bogota","Medellin","Cali","Barranqilla"]:
        for inmueble in ["casa","apartamento"]:
            for transaccion in ["venta","arriendo"]:
                importer(ciudad,inmueble,transaccion)
    return {"message": f"Hello {ciudad}"}




@app.get("/query/{ciudad}")
async def querydatabase(ciudad: str):
    results = []
    ciudadq = ciudad
    if ciudad == 'Bogota':
        ciudadq = 'Bogotá'
    if ciudad == 'Medellin':
        ciudadq = 'Medellín'
    with SessionLocal.begin() as session:
        print('e')
        for i in session.query(Estate).filter_by(city=ciudadq):
            ijson = {'area': i.area,
                'rooms': i.rooms,
                'bath':i.bath,
                'price':i.price,
                'property_type':i.property_type,
                'pid':i.pid,
                'city':i.city,
                'barrio':i.barrio,
                'url':i.url,
                'fuente':i.fuente,
                'm2price':i.m2price,
                'fecha': i.fecha,
                'tipo' : i.tipo
                      }
            results.append(ijson)
    return results

@app.get("/query/{ciudad}/muestra")
async def databaseSample(ciudad:str):
    results = []
    ciudadq = ciudad
    if ciudad == 'Bogota':
        ciudadq = 'Bogotá'
    if ciudad == 'Medellin':
        ciudadq = 'Medellín'
    with SessionLocal.begin() as session:
        print('e')
        query = session.query(Estate).filter(Estate.city == ciudadq,Estate.area >= 100).order_by(desc('fecha')).limit(2000).statement
        df = pd.read_sql_query(query,session.bind)
        dfs = df.sample(n=100)
        dfs.to_excel(ciudad + 'sample.xlsx')


    return {"answer":"respuestas mostradas"}

