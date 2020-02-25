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





class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer(), primary_key=True)
    category = Column(String(100), )
    img =  Column(String(300), )
    text = Column(String(10000),)
    title = Column(String(700),)

    def __init__(self,category , img, text,title):
        self.category = category
        self.img = img
        self.text = text
        self.title = title

    def __repr__(self):
        return f"<Post('$s','$s','$s','$s')>".format(self.category, self.img, self.text,self.title)


def student_serializer(obj):
    return {
        'id': obj.id,
        'category': obj.category,
        'img': obj.img,
        'text': obj.text,
        'title':obj.title
    }


Base.metadata.create_all(engine)