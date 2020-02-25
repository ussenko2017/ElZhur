from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import sessionmaker
from arrested import (
    ArrestedAPI, Resource, Endpoint, GetListMixin, CreateMixin,
    GetObjectMixin, PutObjectMixin, DeleteObjectMixin, ResponseHandler
)


from Flask import app
from config import SQLALCHEMY_DB_URI
engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()
class DBResponseHandler(ResponseHandler):

    def __init__(self, endpoint, *args, **params):
        super(DBResponseHandler, self).__init__(endpoint, *args, **params)

        self.serializer = params.pop('serializer', None)

    def handle(self, data, **kwargs):

        if isinstance(data, list):
            objs = []
            for obj in data:
                objs.append(self.serializer(obj))
            return objs
        else:
            return self.serializer(data)



class Ball(Base):
    __tablename__ = 'ball'
    id = Column(Integer(), primary_key=True)
    predmet_id = Column(Integer(),)
    student_id = Column(Integer(),)
    date_add = Column(String(50),)
    ball =  Column(Integer(),)

    def __init__(self,predmet_id, student_id, date_add, ball):
        self.predmet_id = predmet_id
        self.student_id = student_id
        self.date_add = date_add
        self.ball = ball


    def __repr__(self):
            return "<Ball('%s','%s', '%s', '%s')>" % (self.predmet_id, self.student_id, self.date_add, self.ball)

def users_serializer(obj):
    return {
        'id': obj.id,
        'student_id': obj.student_id,
        'predmet_id': obj.predmet_id,
        'date_add': obj.date_add,
        'ball': obj.ball
    }


Base.metadata.create_all(engine)