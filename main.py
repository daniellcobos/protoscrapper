import pandas as pd
from fastapi import FastAPI
from importer import importer
from models import Estate
from database import SessionLocal
from sqlalchemy import desc, and_
from rates import ratecalulator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():

    return {"message": "Hello World"}


@app.get("/importer/{ciudad}/{inmueble}/{transaccion}")
async def filldatabase(ciudad: str, inmueble:str, transaccion:str):
    importer(ciudad,inmueble,transaccion)
    return {"message": f"Hello {ciudad}"}

@app.get("/absoluteimporter")
async def filldatabase():
    for ciudad in ["Bogota","Medellin"]:
        for inmueble in ["casa","apartamento"]:
            for transaccion in ["venta","arriendo"]:
                importer(ciudad,inmueble,transaccion)
    return {"message": f"Hello {ciudad}"}




@app.get("/query/{ciudad}")
async def querydatabase(ciudad: str):
    results = []
    ciudadq = ciudad
    if ciudad == 'Bogota' or ciudad == 'bogota' :
        ciudadq = 'Bogotá'
    if ciudad == 'Medellin' or ciudad == 'medellin':
        ciudadq = 'Medellín'
    with SessionLocal.begin() as session:
        print('e')
        for i in session.query(Estate).filter_by(city=ciudadq).order_by(desc(Estate.fecha)):
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
                'tipo' : i.tipo,
                'imgurl': i.imgurl,
                      }
            results.append(ijson)
    return results[0:25]

@app.get("/query/{ciudad}/{tipo}/{transaccion}")
async def querydatabase2(ciudad: str,tipo:str,transaccion:str):
    results = []
    ciudadq = ciudad
    if ciudad == 'Bogota' or ciudad == 'bogota' :
        ciudadq = 'Bogotá'
    if ciudad == 'Medellin' or ciudad == 'medellin':
        ciudadq = 'Medellín'
    with SessionLocal.begin() as session:
        print('e')
        for i in session.query(Estate).filter(Estate.city==ciudadq,Estate.property_type==tipo,Estate.tipo==transaccion).order_by(desc(Estate.fecha)):
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
                'tipo' : i.tipo,
                'imgurl': i.imgurl,
                      }
            results.append(ijson)
    return results[0:25]
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
        query = session.query(Estate).filter(Estate.city == ciudadq,Estate.area >= 50, Estate.tipo == 'venta', Estate.garage != None).order_by(desc('fecha')).limit(5000).statement
        df = pd.read_sql_query(query,session.bind)
        df = df.drop(['lp'],axis=1)
        dfs = df.sample(n=200)
        dfs.to_excel(ciudad + 'sample.xlsx')


    return {"answer":"respuestas mostradas"}

@app.get("/rate/{ciudad}")
async def getrates(ciudad: str):
    if ciudad == 'Bogota':
        ciudadq = 'Bogotá'
    if ciudad == 'Medellin':
        ciudadq = 'Medellín'
    ratecalulator(ciudadq)
    return{"rates":"calculated"}

@app.get("/mongotest")
async def getmongo():
    data = getmongodata()
    print(data)
    return {"Exito":"Exito"}