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





class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer(),  primary_key=True)
    otdel_id =  Column(Integer(), )
    user_id =  Column(Integer(),unique=True )
    def __init__(self, otdel_id, user_id):
        self.otdel_id = otdel_id
        self.user_id = user_id

    def __repr__(self):
        return "<Teacher('$s','$s')>" % (self.otdel_id, self.user_id)


def teacher_serializer(obj):
    return {
        'id': obj.id,
        'otdel_id': obj.otdel_id,
        'user_id': obj.user_id
    }



class TeachersIndexEndpoint(Endpoint, GetListMixin, CreateMixin):

    name = 'list'
    many = True
    response_handler = DBResponseHandler


    def get_response_handler_params(self, **params):
        params['serializer'] = teacher_serializer
        return params

    def get_objects(self):

        teachers = session.query(Teacher).all()
        return teachers

    def save_object(self, obj):

        users = Teacher(**obj)
        Base.session.add(Teacher)
        session.commit()
        return users


class TeachersObjectEndpoint(Endpoint, GetObjectMixin,
                              PutObjectMixin, DeleteObjectMixin):

    name = 'object'
    url = '/<string:obj_id>'
    response_handler = DBResponseHandler

    def get_response_handler_params(self, **params):

        params['serializer'] = teacher_serializer
        return params

    def get_object(self):

        obj_id = self.kwargs['obj_id']
        obj = session.query(Teacher).filter(Teacher.id == obj_id).one_or_none()
        if not obj:
            payload = {
                "message": "Teachers object not found.",
            }
            self.return_error(404, payload=payload)

        return obj

    def update_object(self, obj):

        data = self.request.data
        allowed_fields = ['otdel_id','user_id']

        for key, val in data.items():
            if key in allowed_fields:
                setattr(obj, key, val)

        session.add(obj)
        session.commit()

        return obj

    def delete_object(self, obj):

        session.delete(obj)
        session.commit()


Base.metadata.create_all(engine)