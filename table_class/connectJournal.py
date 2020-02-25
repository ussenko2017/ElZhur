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


class connectJournal(Base):
    __tablename__ = 'connectjournal'
    id = Column(Integer(), primary_key=True)
    id_predmet = Column(Integer(),)
    id_room = Column(Integer(),)
    id_teacher = Column(Integer(),)


    def __init__(self,id_predmet,id_room,id_teacher):
        self.id_predmet = id_predmet
        self.id_room = id_room
        self.id_teacher = id_teacher


    def __repr__(self):
            return "<connectJournal('%s','%s', '%s')>" % (self.id_predmet, self.id_room,
                                                                        self.id_teacher)

def connectJournal_serializer(obj):
    return {
        'id': obj.id,
        'id_predmet': obj.id_predmet,
        'id_room': obj.id_room,
        'id_teacher': obj.id_teacher
    }


Base.metadata.create_all(engine)