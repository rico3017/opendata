from sqlalchemy import Column, BIGINT, Integer, Float, String, Date, \
     ForeignKey
from sqlalchemy.orm import backref, relationship 
from model.database import Model


class Network(Model):
    __tablename__ = "network"
    id = Column("id", Integer, primary_key = True)
    postcode = Column("postcode", String(20))
    avg_download = Column("avg_download", String(20))
    avg_upload = Column("avg_upload", String(20))

    def __init__(self, postcode = None, avg_download = None, avg_upload = None, id = None):
        self.id = id
        self.postcode = postcode
        self.avg_download = avg_download
        self.avg_upload = avg_upload