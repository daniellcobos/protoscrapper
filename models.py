from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date, BigInteger
from sqlalchemy.orm import relationship

from database import Base
from geoalchemy2 import Geometry

class Estate(Base):
    __tablename__ = "estate"
    id = Column(Integer, primary_key=True, index=True)
    area = Column(Float)
    rooms = Column(Integer)
    bath= Column(Integer)
    price = Column(BigInteger)
    property_type = Column(String)
    pid= Column(String)
    barrio = Column(String)
    url = Column(String)
    fuente = Column(String)
    city = Column(String)
    m2price = Column(Float)
    fecha = Column(Date)
    tipo = Column(String)
    lp = Column(Geometry('POINT'))
    cons = Column(String)
    garage = Column(String)
    antiguedad = Column(String)
    estrato = Column(String)
    rate = Column(Float)
    imgurl =  Column(String)

    def __repr__(self):
        return "<pid(name='%s', precio='%s', barrio='%s', tipo='%s')>" % (
            self.pid,
            self.price,
            self.barrio,
            self.tipo,
        )
