from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from sqlalchemy.orm import sessionmaker
from arrested import (
    ArrestedAPI, Resource, Endpoint, GetListMixin, CreateMixin,
    GetObjectMixin, PutObjectMixin, DeleteObjectMixin, ResponseHandler
)
from config import SQLALCHEMY_DB_URI
engine = create_engine(SQLALCHEMY_DB_URI, echo=True)

metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()


class journalToDay(Base):
    __tablename__ = 'journaltoday'
    id = Column(Integer(), primary_key=True)
    para_1 = Column(Integer(),nullable=True)
    para_2 = Column(Integer(),nullable=True)
    para_3 = Column(Integer(),nullable=True)
    para_4 = Column(Integer(),nullable=True)
    para_5 = Column(Integer(),nullable=True)
    para_6 = Column(Integer(),nullable=True)
    para_7 = Column(Integer(),nullable=True)



    def __init__(self,para_1,para_2,para_3, para_4,para_5,para_6,para_7):
        self.para_1 = para_1
        self.para_2 = para_2
        self.para_3 = para_3
        self.para_4 = para_4
        self.para_5 = para_5
        self.para_6 = para_6
        self.para_7 = para_7


    def __repr__(self):
            return "<journalToDay('%s','%s', '%s', '%s', '%s', '%s', '%s')>" % (self.para_1, self.para_2,
                                                self.para_3,self.para_4,
                                                self.para_5,self.para_6,
                                                self.para_7)

def journalToDay_serializer(obj):
    return {
        'para_1': obj.para_1,
        'para_2': obj.para_2,
        'para_3': obj.para_3,
        'para_4': obj.para_4,
        'para_5': obj.para_5,
        'para_6': obj.para_6,
        'para_7': obj.para_7,

    }


Base.metadata.create_all(engine)