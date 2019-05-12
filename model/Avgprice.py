from sqlalchemy import Column, BIGINT, Integer, Float, String, Date, \
     ForeignKey, SMALLINT
from sqlalchemy.orm import backref, relationship 
from model.database import Model


class Avgprice(Model):
    __tablename__ = "avg_price"
    id = Column("id", Integer, primary_key = True)
    postcode = Column("postcode", String(10))
    price = Column("price", Float)
    type = Column("type", String(30))
    county = Column("county", String(50))
    year = Column("year", String(5))
    isnew = Column("isnew", SMALLINT)


    def __init__(self, postcode = None, price = None, type = None, city = None, county = None, year = None, isnew = None, id = None):
        self.id = id
        self.postcode = postcode
        self.price = price
        self.type = type