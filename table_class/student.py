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





class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), )
    group_id =  Column(Integer(), )
    num_zach = Column(Integer(),)

    def __init__(self,user_id , group_id, num_zach):
        self.user_id = user_id
        self.group_id = group_id
        self.num_zach = num_zach

    def __repr__(self):
        return f"<Student('$s','$s','$s')>".format(self.user_id, self.group_id, self.num_zach)


def student_serializer(obj):
    return {
        'id': obj.id,
        'user_id': obj.user_id,
        'group_id': obj.group_id,
        'num_zach': obj.num_zach
    }



class StudentIndexEndpoint(Endpoint, GetListMixin, CreateMixin):

    name = 'list'
    many = True
    response_handler = DBResponseHandler


    def get_response_handler_params(self, **params):
        params['serializer'] = student_serializer
        return params

    def get_objects(self):

        students = session.query(Student).all()
        return students

    def save_object(self, obj):

        users = Student(**obj)
        Base.session.add(Student)
        session.commit()
        return users


class StudentObjectEndpoint(Endpoint, GetObjectMixin,
                              PutObjectMixin, DeleteObjectMixin):

    name = 'object'
    url = '/<string:obj_id>'
    response_handler = DBResponseHandler

    def get_response_handler_params(self, **params):

        params['serializer'] = student_serializer
        return params

    def get_object(self):

        obj_id = self.kwargs['obj_id']
        obj = session.query(Student).filter(Student.id == obj_id).one_or_none()
        if not obj:
            payload = {
                "message": "Students object not found.",
            }
            self.return_error(404, payload=payload)

        return obj

    def update_object(self, obj):

        data = self.request.data
        allowed_fields = ['group_id', 'num_zach']

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