from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, Date, Numeric, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db_core.base import Base as db

class Address(db): # має бути базою для данних по відділеням та адрес
    id = Column(Integer, primary_key=True)
    uuid = Column(String(50))
    city_name = Column(String(50))
    city_ref = Column(String(50))
    region = Column(String(50))
    area = Column(String(50))
    warehouse_option = Column(String(50))
    warehouse_text = Column(String(50))
    warehouse_ref = Column(String(50))
    description_delivery = Column(String(50))
    warehouse_text = Column(String(50))
    place_street = Column(String(50))
    place_number = Column(String(50))
    place_house = Column(String(50))
    place_flat = Column(String(50))
    street_ref = Column(String(50))
    title_city = Column(String(50))
    