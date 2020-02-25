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


class journalToWeek(Base):
    __tablename__ = 'journaltoweek'
    id = Column(Integer(), primary_key=True)
    day_1 = Column(Integer(),nullable=True)
    day_2 = Column(Integer(),nullable=True)
    day_3 = Column(Integer(),nullable=True)
    day_4 = Column(Integer(),nullable=True)
    day_5 = Column(Integer(),nullable=True)
    day_6 = Column(Integer(),nullable=True)
    day_7 = Column(Integer(),nullable=True)
    id_group = Column(Integer(),nullable=True)



    def __init__(self,day_1,day_2,day_3, day_4,day_5,day_6,day_7,id_group):
        self.day_1 = day_1
        self.day_2 = day_2
        self.day_3 = day_3
        self.day_4 = day_4
        self.day_5 = day_5
        self.day_6 = day_6
        self.day_7 = day_7
        self.id_group = id_group


    def __repr__(self):
            return "<journalToWeek('%s','%s', '%s', '%s', '%s', '%s', '%s','%s)>" % (self.day_1, self.day_2,
                                                self.day_3,self.day_4,
                                                self.day_5,self.day_6,
                                                self.day_7,self.id_group)

def journalToWeek_serializer(obj):
    return {
        'day_1': obj.day_1,
        'day_2': obj.day_2,
        'day_3': obj.day_3,
        'day_4': obj.day_4,
        'day_5': obj.day_5,
        'day_6': obj.day_6,
        'day_7': obj.day_7,
        'id_group': obj.id_group

    }


Base.metadata.create_all(engine)