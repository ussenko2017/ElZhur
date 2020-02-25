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





class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer(), primary_key=True)
    name = Column(String(70),)
    special_id = Column(Integer(),)
    date_begin = Column(DateTime(50),)
    date_end = Column(DateTime(50),)
    def __init__(self, name, special_id, date_begin, date_end):
        self.name = name
        self.special_id = special_id
        self.date_begin = date_begin
        self.date_end = date_end

    def __repr__(self):
        return f"<Group('$s', '$s','$s', '$s')>" .format(self.name, self.special_id, self.date_end, self.date_begin)

def groups_serializer(obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'special_id': obj.special_id,
            'date_begin': obj.date_begin,
            'date_end': obj.date_end
        }

class GroupsIndexEndpoint(Endpoint, GetListMixin, CreateMixin):

        name = 'list'
        many = True
        response_handler = DBResponseHandler

        def get_response_handler_params(self, **params):
            params['serializer'] = groups_serializer
            return params

        def get_objects(self):
            groups = session.query(Group).all()
            return groups

        def save_object(self, obj):
            users = Group(**obj)
            Base.session.add(Group)
            session.commit()
            return users

class GroupsObjectEndpoint(Endpoint, GetObjectMixin,
                              PutObjectMixin, DeleteObjectMixin):

        name = 'object'
        url = '/<string:obj_id>'
        response_handler = DBResponseHandler

        def get_response_handler_params(self, **params):

            params['serializer'] = groups_serializer
            return params

        def get_object(self):

            obj_id = self.kwargs['obj_id']
            obj = session.query(Group).filter(Group.id == obj_id).one_or_none()
            if not obj:
                payload = {
                    "message": "Users object not found.",
                }
                self.return_error(404, payload=payload)

            return obj

        def update_object(self, obj):

            data = self.request.data
            allowed_fields = ['name', 'special_id', 'date_begin', 'date_end']

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