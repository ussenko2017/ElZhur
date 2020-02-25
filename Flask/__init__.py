
# -*- coding: utf-8 -*-
"""
The flask application package.
"""
from urllib.parse import urlencode

from flask import Flask
from jinja2 import environment, filters

from table_class.user import UsersIndexEndpoint, UsersObjectEndpoint
from table_class.teacher import TeachersIndexEndpoint, TeachersObjectEndpoint
from table_class.student import StudentIndexEndpoint, StudentObjectEndpoint
from table_class.special import SpecialsIndexEndpoint, SpecialsObjectEndpoint
from table_class.room import RoomsIndexEndpoint, RoomsObjectEndpoint
from table_class.otdel import OtdelsIndexEndpoint, OtdelsObjectEndpoint
from table_class.group import GroupsIndexEndpoint, GroupsObjectEndpoint
from table_class.predmet import PredmetsIndexEndpoint, PredmetsObjectEndpoint

app = Flask(__name__)

import Flask.views

from arrested import (
    ArrestedAPI, Resource, Endpoint, GetListMixin, CreateMixin,
    GetObjectMixin, PutObjectMixin, DeleteObjectMixin, ResponseHandler
)

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, DateTime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
#from kim import field
from table_class import group,otdel,room,special,student,teacher,user,connectJournal, journalToDay,journalToWeek, ball, post

from config import SQLALCHEMY_DB_URI
#                <option value="{{ conJ.id }}" >{{ predmet.name + ' | '+ room.name + ' | '+ userr.lastname + ' ' + userr.firstname + ' ' + userr.patr}}</option>

#curl  -X DELETE localhost:5000/v1/users/1

api_v1 = ArrestedAPI(app,url_prefix="/v1")
app.config["SQLALCHEMY_DB_URI"] = SQLALCHEMY_DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

engine = create_engine(app.config['SQLALCHEMY_DB_URI'], echo=True)
metadata = MetaData()

Base = declarative_base()


Session = sessionmaker(bind=engine)
session = Session()

"""
user = Users('admin','admin@mail.ru','admin')
session.add(user)
session.commit()
"""




otdels_resource = Resource('otdel', __name__, url_prefix='/otdel')
users_resource = Resource('user', __name__, url_prefix='/user')
specials_resource = Resource('special', __name__, url_prefix='/special')
groups_resource = Resource('group', __name__, url_prefix='/group')
students_resource = Resource('student', __name__, url_prefix='/student')
teachers_resource = Resource('teacher', __name__, url_prefix='/teacher')
rooms_resource = Resource('room', __name__, url_prefix='/room')
predmets_resource = Resource('predmet', __name__, url_prefix='/predmet')
posts_resource = Resource('post',__name__,url_prefix='/post')




users_resource.add_endpoint(UsersIndexEndpoint)
users_resource.add_endpoint(UsersObjectEndpoint)
otdels_resource.add_endpoint(OtdelsIndexEndpoint)
otdels_resource.add_endpoint(OtdelsObjectEndpoint)
specials_resource.add_endpoint(SpecialsIndexEndpoint)
specials_resource.add_endpoint(SpecialsObjectEndpoint)
rooms_resource.add_endpoint(RoomsIndexEndpoint)
rooms_resource.add_endpoint(RoomsObjectEndpoint)
groups_resource.add_endpoint(GroupsIndexEndpoint)
groups_resource.add_endpoint(GroupsObjectEndpoint)
students_resource.add_endpoint(StudentIndexEndpoint)
students_resource.add_endpoint(StudentObjectEndpoint)
teachers_resource.add_endpoint(TeachersIndexEndpoint)
teachers_resource.add_endpoint(TeachersObjectEndpoint)
predmets_resource.add_endpoint(PredmetsIndexEndpoint)
predmets_resource.add_endpoint(PredmetsObjectEndpoint)




api_v1.register_resource(users_resource)
api_v1.register_resource(otdels_resource)
api_v1.register_resource(specials_resource)
api_v1.register_resource(groups_resource)
api_v1.register_resource(rooms_resource)
api_v1.register_resource(students_resource)
api_v1.register_resource(teachers_resource)
api_v1.register_resource(predmets_resource)
api_v1.register_resource(posts_resource)

