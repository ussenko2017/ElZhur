# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, jsonify,request
from Flask import app
import json
import random
import requests
from table_class import group,otdel,room,special,student,teacher,user as clUser, predmet,connectJournal,journalToWeek,journalToDay, ball, post

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine, DateTime, inspect

# -*- coding: utf-8 -*-
"""
This script runs the Flask application using a development server.
"""

from datetime import datetime

import flask
import flask_login
from config import SQLALCHEMY_DB_URI
from flask import render_template, g
import config

#SQLALCHEMY_DB_URI = 'mysql+mysqlconnector://mylxru:Us2000Us2000@217.182.197.234/laratest'
login_manager = flask_login.LoginManager()

login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        user_cl = session.query(clUser.User).filter_by(email=email).all()[0]
    except:
        user_cl = None
    if user_cl == None:
        return
    user = User()
    user.id = email
    user.num = user_cl.id
    user.firstname = user_cl.firstname
    user.lastname = user_cl.lastname
    user.patr = user_cl.patr
    user.birthday = user_cl.birthday
    user.nickname = user_cl.nickname
    user.password = user_cl.password
    quer = 'SELECT COUNT(teacher.user_id) as num FROM teacher WHERE teacher.user_id = ' + str(user_cl.id)
    numb = session.execute(quer)
    access = False
    for i in numb:
        if i[0] == 1:
            access = True
    user.access = access


    return user


@login_manager.request_loader
def request_loader(request):
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    email = request.form.get('email')
    try:
        user_cl = session.query(clUser.User).filter_by(email=email).all()[0]
    except:
        user_cl = None
    if user_cl == None:
        return

    user = User()
    user.id = email
    user.num = user_cl.id
    user.firstname = user_cl.firstname
    user.lastname = user_cl.lastname
    user.patr = user_cl.patr
    user.birthday = user_cl.birthday
    user.nickname = user_cl.nickname
    user.password = user_cl.password
    quer = 'SELECT COUNT(teacher.user_id) as num FROM teacher WHERE teacher.user_id = ' + str(user_cl.id)
    numb = session.execute(quer)
    access = False
    for i in numb:
        if i[0] == 1:
            access = True
    user.access = access

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = flask.request.form['password'] == user_cl.password

    return user


# users = {'foo@bar.tld': {'password': 'secret'}}



@app.route('/')
def home():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    n = session.execute('SELECT * FROM `post`')
    news = []

    for id,category,img,text , title in n:
        news.append({'id':id,'category':category,'img':img,'title':title, 'text':text})
    news = reversed(news)
    try:
        user = flask_login.current_user.id
    except:
        user = 'null'
    return render_template('index.html', news=news, user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    email = request.form.get('email')
    try:
        user_cl = session.query(clUser.User).filter_by(email = email).all()[0]
        print(user_cl)

    except:
        user_cl = None
    if user_cl != None and flask.request.form['password'] == user_cl.password:
        user = User()
        user.id = email
        user.num = user_cl.id
        user.firstname = user_cl.firstname
        user.lastname = user_cl.lastname
        user.patr = user_cl.patr
        user.birthday = user_cl.birthday
        user.nickname = user_cl.nickname
        user.password = user_cl.password
        quer = 'SELECT COUNT(teacher.user_id) as num FROM teacher WHERE teacher.user_id = '+ str(user_cl.id)
        numb = session.execute(quer)
        access = False
        for i in numb:
            if i[0] == 1:
                access = True
        user.access = access
        flask_login.login_user(user)



        return flask.redirect(flask.url_for('home'))

    return flask.redirect(flask.url_for('home'))


@app.route('/profile')
@flask_login.login_required
def profile():
    return render_template('profile.html',user=flask_login.current_user)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    g.user = 'Гость'
    return flask.redirect(flask.url_for('home'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    email = flask.request.form['email']
    password = flask.request.form['password']


    try:
        user_cl = session.query(clUser.User).filter_by(email=email).all()[0]
    except:
        user_cl = None

    if user_cl == None:
        us = clUser.User('',email,password,'','','','')
        session.add(us)
        session.commit()
        g.user = email


        return flask.redirect(flask.url_for('home'))

    return flask.redirect(flask.url_for('home'))




@app.route('/autoadd', methods=['GET', 'POST'])
def autoadd():

    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    for i in range(100):
        us = clUser.User('nickname'+str(i),'email'+str(i),'password'+str(i),'lastname'+str(i),'firstname'+str(i),'patr'+str(i),str(datetime.now()))
        session.add(us)
        pred = predmet.Predmet('predmet'+str(i), i)
        session.add(pred)
        otd = otdel.Otdel('otdel'+ str(i))
        session.add(otd)
        spec = special.Special('spec'+str(i),i)
        session.add(spec)
        gr = group.Group('group'+ str(i), i,str(datetime.now()),str(datetime.now()))
        session.add(gr)
        rom = room.Room(100+i)
        session.add(rom)
        stud = student.Student(i,10000+i)
        session.add(stud)
        teach = teacher.Teacher(i)
        session.add(teach)
    session.commit()
    return 'done'

@app.route('/balls', methods=['GET', 'POST'])
def showball():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    quer = session.execute('SELECT ball.id as id, ball.ball as ball, `user`.`firstname` as fn, `user`.`lastname` as ln, `user`.`patr` as patr, predmet.name  as predmet_name , ball.date_add as date_add  FROM `ball` inner join `user` ON `user`.`id` = `ball`.`student_id` inner join predmet ON predmet.id = `ball`.`predmet_id`')
    print(quer)
    students = session.query(student.Student, clUser.User)
    students = students.join(clUser.User, clUser.User.id == student.Student.user_id).all()
    predmets = session.query(predmet.Predmet).all()
    return render_template(
        'data/ball.html', quer=quer,students=students,predmets=predmets,

    )




@app.route('/students', methods=['GET', 'POST'])
def showstudent():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    users = session.query(clUser.User).all()
    groups = session.query(group.Group).all()

    """
    SELECT * FROM student
    inner join `user` on 
    student.id = user.id
    inner join `group` on 
    `group`.id = student.group_id
    inner join special on 
    special.id = `group`.special_id
    inner JOIN otdel ON
    otdel.id = special.otdel_id
    """

    query = session.query(student.Student,clUser.User,  group.Group, special.Special, otdel.Otdel)
    query = query.join(clUser.User,student.Student.user_id == clUser.User.id )
    query = query.join(group.Group, group.Group.id == student.Student.group_id)
    query = query.join(special.Special, special.Special.id == group.Group.special_id)
    records = query.join(otdel.Otdel, otdel.Otdel.id == special.Special.otdel_id).all()
    print(records)
    return render_template(
        'data/student.html',
        records=records, groups = groups,users = users,
        year=datetime.now().year
    )


@app.route('/predmets', methods=['GET', 'POST'])
def showpredmet():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    records = session.query(predmet.Predmet).all()
    return render_template(
        'data/predmet.html',
        records=records,
        year=datetime.now().year
        #
    )


@app.route('/otdels', methods=['GET', 'POST'])
def showotdel():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    records = session.query(otdel.Otdel)

    return render_template(
        'data/otdel.html',
        records=records,
        year=datetime.now().year
    )


@app.route('/specials', methods=['GET', 'POST'])
def showspecial():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    que = session.execute('SELECT `special`.id as id, `special`.name as special_name, `otdel`.name as otdel_name FROM `special` inner join otdel ON `special`.`otdel_id` = otdel.id')
    print(que)
    otdels = session.query(otdel.Otdel).all()
    return render_template(
        'data/special.html',
        records=que,otdels=otdels,
        year=datetime.now().year
    )

@app.route('/groups', methods=['GET', 'POST'])
def showgroups():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    que = session.query(group.Group, special.Special)
    que = que.join(special.Special, special.Special.id == group.Group.special_id).all()
    specials = session.query(special.Special).all()
    return render_template(
        'data/group.html',
        specials=specials, que=que,
        year=datetime.now().year
    )
@app.route('/teachers', methods=['GET', 'POST'])
def showteachers():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    que = session.query(teacher.Teacher, clUser.User, otdel.Otdel)
    que = que.join(clUser.User, clUser.User.id == teacher.Teacher.user_id)
    que = que.join(otdel.Otdel, otdel.Otdel.id == teacher.Teacher.otdel_id)
    otdels = session.query(otdel.Otdel).all()
    users = session.query(clUser.User)
    return render_template(
        'data/teacher.html',
        otdels=otdels, que=que,users=users,
        year=datetime.now().year
    )

@app.route('/rooms', methods=['GET', 'POST'])
def showrooms():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    que = session.query(room.Room)

    return render_template(
        'data/room.html',
         que=que,
        year=datetime.now().year
    )

@app.route('/studfull', methods=['get','post'])
def showstudfull():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(student.Student, clUser.User, group.Group, special.Special, otdel.Otdel)
    query = query.join(clUser.User, student.Student.id == clUser.User.id)
    query = query.join(group.Group, group.Group.id == student.Student.group_id)
    query = query.join(special.Special, special.Special.id == group.Group.special_id)
    records = query.join(otdel.Otdel, otdel.Otdel.id == special.Special.otdel_id).all()
    print(records)
    return render_template(
        'data/studentfull.html',
        records=records,
        year=datetime.now().year
    )


@app.route('/updprofile', methods=['GET', 'POST'] )
def updprofile():

    newUser = clUser.User(flask.request.values['nickname'],
                          flask.request.values['email'],
                          flask.request.values['password'],
                          flask.request.values['lastname'],
                          flask.request.values['firstname'],
                          flask.request.values['patr'],
                          flask.request.values['birthday'])
    url = 'http://127.0.0.1:5000/v1/user/'

    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    oldEmail = flask.request.values['oldemail']
    user_cl = session.query(clUser.User).filter_by(email=oldEmail).all()[0]
    user_cl.email = flask.request.values['email']
    user_cl.nickname = flask.request.values['nickname']
    user_cl.password = flask.request.values['password']
    user_cl.lastname = flask.request.values['lastname']
    user_cl.firstname = flask.request.values['firstname']
    user_cl.patr = flask.request.values['patr']
    user_cl.birthday = flask.request.values['birthday']

    session.commit()
    #print(requests.put(url + str(flask_login.current_user.id)+'/',clUser.users_serializer(newUser)).text))
    return flask.redirect(flask.url_for('profile'))

@app.route('/editraspis',methods=['GET', 'POST'])
def editRaspis():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    rooms = session.query(room.Room).all()
    teachers = session.query(teacher.Teacher, clUser.User).join(clUser.User, clUser.User.id == teacher.Teacher.user_id).all()
    predmets = session.query(predmet.Predmet).all()
    connectJ = session.query(connectJournal.connectJournal, teacher.Teacher, clUser.User, predmet.Predmet, room.Room )
    connectJ = connectJ.join(teacher.Teacher, teacher.Teacher.user_id == connectJournal.connectJournal.id_teacher)
    connectJ = connectJ.join(clUser.User, clUser.User.id == teacher.Teacher.user_id)
    connectJ = connectJ.join(predmet.Predmet, predmet.Predmet.id == connectJournal.connectJournal.id_predmet)
    connectJ = connectJ.join(room.Room, room.Room.id == connectJournal.connectJournal.id_room).all()
    jourToDay = session.query(journalToDay.journalToDay).all()
    grp = session.query(group.Group).all()
    jourToDayFull = session.query(journalToDay.journalToDay ).all()
    allJourToDayList = []
    for i in jourToDayFull:
        journalToDayList = []
        for j in range(7):
            para_dict = {}
            queryes = session.execute('SELECT '
                                      'predmet.name as predmet_name, rooms.name as room_name, `user`.firstname as fn, `user`.lastname 	as ln, `user`.patr as patr '
                                      'FROM `connectjournal` '
                        'inner join predmet ON '
                        'predmet.id  = `connectjournal`.`id_predmet`'
                                      ' inner join `user` ON '
                        '`connectjournal`.`id_teacher` = `user`.`id` '
                        'inner join rooms ON '
                        'rooms.id = `connectjournal`.`id_room` '
                        'inner join journaltoday on '
                        'connectjournal.id = journaltoday.para_{0} '
                        'where journaltoday.id = {1}'.format(j+1, i.id))
            para_dict['predmet_name'] = '    -    '
            para_dict['room_name'] = '    -    '
            para_dict['fn'] = '    -    '
            para_dict['ln'] = '    -    '
            para_dict['patr'] = '    -    '
            para_dict['num'] = j
            para_dict['id'] = i.id
            for predmet_name, room_name, fn, ln, patr in queryes:
                para_dict['predmet_name'] = predmet_name
                para_dict['room_name'] = room_name
                para_dict['fn'] = fn
                para_dict['ln'] = ln
                para_dict['patr'] = patr
                para_dict['id'] = i.id
                para_dict['num'] = j
            journalToDayList.append(para_dict)
        allJourToDayList.append(journalToDayList)
    print(allJourToDayList)





    return render_template('data/editRaspis.html',rooms=rooms,teachers=teachers, predmets=predmets, connectJ=connectJ,jourToDay = jourToDay, grp=grp, allJourToDayList=allJourToDayList)




@app.route('/editraspis/add/connectjournal',methods=['GET', 'POST'])
def editRaspisAddConnectJournal():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(connectJournal.connectJournal(flask.request.values['predmet'],flask.request.values['room'],flask.request.values['teacher']))
    session.commit()
    return flask.redirect(flask.url_for('editRaspis'))


@app.route('/editraspis/add/journaltoday',methods=['GET', 'POST'])
def editRaspisJournalToDay():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        para_1 = flask.request.values['para_1']
    except:
        para_1 = None
    try:
        para_2 = flask.request.values['para_2']
    except:
        para_2 = None
    try:
        para_3 = flask.request.values['para_3']
    except:
        para_3 = None
    try:
        para_4 = flask.request.values['para_4']
    except:
        para_4 = None
    try:
        para_5 = flask.request.values['para_5']
    except:
        para_5 = None
    try:
        para_6 = flask.request.values['para_6']
    except:
        para_6 = None
    try:
        para_7 = flask.request.values['para_7']
    except:
        para_7 = None
    jourToDay = journalToDay.journalToDay(para_1, para_2, para_3, para_4, para_5, para_6, para_7)
    session.add(jourToDay)
    session.commit()
    return flask.redirect(flask.url_for('editRaspis'))

@app.route('/editraspis/add/journaltoweek',methods=['GET', 'POST'])
def editRaspisJournalToWeek():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        day_1 = flask.request.values['day_1']
    except:
        day_1 = None
    try:
        day_2 = flask.request.values['day_2']
    except:
        day_2 = None
    try:
        day_3 = flask.request.values['day_3']
    except:
        day_3 = None
    try:
        day_4 = flask.request.values['day_4']
    except:
        day_4 = None
    try:
        day_5 = flask.request.values['day_5']
    except:
        day_5 = None
    try:
        day_6 = flask.request.values['day_6']
    except:
        day_6 = None
    try:
        day_7 = flask.request.values['day_7']
    except:
        day_7 = None
    jourToWeek = journalToWeek.journalToWeek(day_1, day_2, day_3, day_4, day_5, day_6, day_7,flask.request.values['group_id'])
    session.add(jourToWeek)
    session.commit()
    return flask.redirect(flask.url_for('editRaspis'))


@app.route('/showraspis',methods=['GET', 'POST'])
def showRaspis():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    JourToWeek = session.query(journalToWeek.journalToWeek, group.Group)
    JourToWeek = JourToWeek.join(group.Group, group.Group.id == journalToWeek.journalToWeek.id_group)
    distListGroup = session.execute('SELECT DISTINCT `group`.id, `group`.`name` from journaltoweek inner join `group` ON `group`.id = journaltoweek.id_group')


    try:
        group_id = flask.request.values['group_id']
    except:
        group_id = JourToWeek.all()[0][0].id_group
    print(group_id)


    arrayToWeek = []
    for i in range(7):
        arrayToDay = []
        for j in range(7):
            query = session.execute(getQuery(j + 1, i + 1, group_id))
            slov = {}
            slov['predmet_name'] = '    -    '
            slov['room_name'] = '    -    '
            slov['fn'] = '    -    '
            slov['ln'] = '    -    '
            slov['patr'] = '    -    '
            for predmet_name, room_name, fn, ln ,patr in query:
                    slov['predmet_name'] = predmet_name
                    slov['room_name'] = room_name
                    slov['fn'] = fn
                    slov['ln'] = ln
                    slov['patr'] = patr
            arrayToDay.append(slov)

        arrayToWeek.append(arrayToDay)
    print(arrayToWeek)
    grp = session.query(group.Group).filter_by(id=group_id).all()[0].name









    return render_template('data/showraspis.html', distListGroup=distListGroup, grp=grp,seven = 7, arrayToWeek= arrayToWeek, none=None)

def getQuery(para, day, group):
    query = "SELECT predmet.name as predmet_name, rooms.name as room_name, `user`.firstname as fn, `user`.lastname 	as ln, `user`.patr as patr FROM connectjournal INNER JOIN predmet ON connectjournal.id_predmet = predmet.id INNER join rooms on connectjournal.id_room = rooms.id INNER JOIN journaltoday ON connectjournal.id = journaltoday.para_{0} INNER JOIN journaltoweek ON journaltoday.id = journaltoweek.day_{1} inner join teacher on connectjournal.id_teacher = teacher.user_id  inner join `user` on `user`.id = teacher.user_id WHERE journaltoweek.id_group = {2}".format(para,day,group)
    return query


@app.route('/add/<string:name>',methods=['GET', 'POST'])
def add(name):
    requesrTo = '/'

    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    if name == 'otdel':
        otdel_name = flask.request.values['name']
        newOtdel = otdel.Otdel(otdel_name)
        session.add(newOtdel)
        requesrTo = '/'+name+'s'
    elif name == 'student':
        student_id = flask.request.values['user_id']
        student_group_id = flask.request.values['group_id']
        student_num_zach = flask.request.values['num_zach']
        newStudent = student.Student(student_id, student_group_id, student_num_zach)
        session.add(newStudent)
        requesrTo = '/'+name+'s'

    elif name == 'predmet':
        predmet_name = flask.request.values['name']
        predmet_hours = flask.request.values['hours']
        newPredmet = predmet.Predmet(predmet_name, predmet_hours)
        session.add(newPredmet)
        requesrTo = '/'+name+'s'

    elif name == 'special':
        special_name = flask.request.values['name']
        special_otdel_id = flask.request.values['otdel_id']
        newSpecial = special.Special(special_name, special_otdel_id)
        session.add(newSpecial)
        requesrTo = '/'+name+'s'


    elif name == 'ball':
        ball_student_id = flask.request.values['student_id']
        ball_predmet_id = flask.request.values['predmet_id']
        ball_date_add = datetime.now()
        ball_ball = flask.request.values['ball']
        newBall = ball.Ball(ball_predmet_id,ball_student_id,ball_date_add, ball_ball)
        session.add(newBall)
        requesrTo = '/'+name+'s'

    elif name == 'group':
        group_name = flask.request.values['name']
        group_special_id = flask.request.values['special_id']
        date_begin = flask.request.values['date_begin']
        date_end = flask.request.values['date_end']
        newGroup = group.Group(group_name, group_special_id, date_begin, date_end)
        session.add(newGroup)
        requesrTo = '/'+name+'s'


    elif name == 'teacher':
        teacher_otdel_id =  flask.request.values['otdel_id']
        teacher_user_id = flask.request.values['user_id']
        newTeacher = teacher.Teacher(teacher_otdel_id, teacher_user_id)
        session.add(newTeacher)
        requesrTo = '/'+name+'s'

    elif name == 'rooms':
        rooms_name = flask.request.values['name']
        newRooms = room.Room(rooms_name)
        session.add(newRooms)
        requesrTo = '/'+name+''

    elif name == 'post':
        category = flask.request.values['category']
        img = flask.request.values['img']
        text = flask.request.values['text']
        title = flask.request.values['title']
        newPost = post.Post(category,img,text,title)
        session.add(newPost)

    session.commit()
    return flask.redirect(requesrTo)

@app.route('/showjournal',methods=['GET', 'POST'])
def showjournal():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    groups = session.query(group.Group)
    predmets = session.query(predmet.Predmet)

    try:
        group_id = flask.request.values['group_id']
        predmet_id = flask.request.values['predmet_id']
    except:
        group_id = groups[0].id
        predmet_id = predmets[0].id
    print(group_id)
    print(predmet_id)

    quer = session.execute('select predmet_id, student_id, ball,predmet.name as predmet_name, '
                           'lastname, firstname, patr, `group`.`name` as group_name, group_id, ball.date_add as date_add FROM ball '
                           'inner JOIN predmet ON '
                           'predmet.id = ball.predmet_id '
                           'inner join `student` ON '
                           '`student`.`user_id` = ball.student_id '
                           'INNER join `user` ON '
                           '`user`.`id` = `student`.`user_id` '
                           'inner join `group` ON '
                           '`group`.`id` = student.group_id '
                           'where student.group_id = {0} and ball.predmet_id = {1}'.format(group_id, predmet_id))


    return render_template('data/showjournal.html',groups=groups, predmets=predmets, predmet_id=predmet_id, group_id=group_id, quer=quer)
@app.route('/addpost',methods=['GET', 'POST'])
def addpost():

    return render_template('data/post.html')


@app.route('/del', methods=['GET', 'POST'])
def delete():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    id = flask.request.values['id']
    redirect = flask.request.values['redirect']
    tablename = flask.request.values['tablename']
    sql = "DELETE FROM `" + tablename + "` WHERE `" + tablename+"`.id = " + id
    session.execute(sql)
    session.commit()
    return flask.redirect(redirect)

@app.route('/autoball',  methods=['GET', 'POST'])
def autoball():
    engine = create_engine(SQLALCHEMY_DB_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}
    predmets = session.query(predmet.Predmet).all()
    students = session.query(student.Student, clUser.User).join(clUser.User, clUser.User.id == student.Student.user_id).all()
    for pred in predmets:
        for stud in students:
            session.add(ball.Ball(object_as_dict(pred)['id'], object_as_dict(stud)['id'] ,datetime.now(),  random.randint(2,5)))
    session.commit()