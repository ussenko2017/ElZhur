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




class Special(Base):
    __tablename__ = 'special'
    id = Column(Integer(), primary_key=True)
    otdel_id = Column(Integer(), )
    name = Column(String(200),)
    def __init__(self, name, otdel_id):
        self.name = name
        self.otdel_id = otdel_id
    def __repr__(self):
        return f"<Special('$s', '$s')>".format(self.otdel_id, self.name)
def specials_serializer(obj):
    return {
        'id': obj.id,
        'name': obj.name,
        'otdel_id': obj.otdel_id

    }



class SpecialsIndexEndpoint(Endpoint, GetListMixin, CreateMixin):

    name = 'list'
    many = True
    response_handler = DBResponseHandler


    def get_response_handler_params(self, **params):
        params['serializer'] = specials_serializer
        return params

    def get_objects(self):

        specials = session.query(Special).all()
        return specials

    def save_object(self, obj):

        users = Special(**obj)
        Base.session.add(Special)
        session.commit()
        return users


class SpecialsObjectEndpoint(Endpoint, GetObjectMixin,
                              PutObjectMixin, DeleteObjectMixin):

    name = 'object'
    url = '/<string:obj_id>'
    response_handler = DBResponseHandler

    def get_response_handler_params(self, **params):

        params['serializer'] = specials_serializer
        return params

    def get_object(self):

        obj_id = self.kwargs['obj_id']
        obj = session.query(Special).filter(Special.id == obj_id).one_or_none()
        if not obj:
            payload = {
                "message": "Specials object not found.",
            }
            self.return_error(404, payload=payload)

        return obj

    def update_object(self, obj):

        data = self.request.data
        allowed_fields = ['name','otdel_id']

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