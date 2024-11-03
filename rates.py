import requests
import pandas as pd
import time
from datetime import date
from database import SessionLocal
from models import Estate
from unidecode import unidecode
import json
from bs4 import BeautifulSoup
from sqlalchemy import text
def ratecalulator(ciudad):
  sqltext = text(
      "select t1.barrio, ((t2.averagearriendo / t1.averageventa)) as rate, t1.fecha from "
      "(SELECT barrio, avg(m2price) as averageventa, fecha from estate where city = '"+ciudad+"' and tipo = 'venta' group by barrio, fecha) as t1,"
      "(SELECT barrio, avg(m2price) as averagearriendo, fecha from estate where city = '"+ciudad+"' and tipo = 'arriendo' group by barrio, fecha) as t2 "
      "where t1.barrio = t2.barrio order by rate")
  with SessionLocal.begin() as session:
      df = pd.read_sql_query(sqltext,session.bind)
      df = df.sort_values('fecha').groupby('barrio').tail(1)
      df2 = df.mean(numeric_only=True)[0]
      sql = text("update estate set rate = :x where city = :c ")
      session.execute(sql, {"x": df2, "c": ciudad})
      session.commit
      for index,rows in df.iterrows():
          sql = text("update estate set rate = :x where barrio = :b and city = :c ")
          session.execute(sql,{"b": rows["barrio"],"x":rows["rate"],"c":ciudad})
          session.commit
      print(df,df2)