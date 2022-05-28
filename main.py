# -*- coding: utf8 -*-
import json

import sqlalchemy
from flask import jsonify
from flask_restful import Resource, abort
from sqlalchemy import *
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_marshmallow import Marshmallow

metadata = MetaData()
DB_URL = 'mysql+pymysql://root:2243@127.0.0.1:3306/blogdb?charset=utf8'
engine = create_engine(DB_URL)

# ПОДКЛЮЧЕНИЕ К ДБ MYSQL

def start() -> scoped_session:
    base.metadata.bind = engine
    base.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


base = declarative_base()
session = start()

# КЛАСС БЛОГА
class blogs(base):
    '''The model, a plain, ol python cl ass'''
    __tablename__ = 'blogs'
    BlogID = Column(Integer, primary_key=True, autoincrement=True)
    Author = Column(VARCHAR(95), nullable=False)
    Title = Column(VARCHAR(45), nullable=False)
    Content = Column(VARCHAR(245), nullable=False)
    DatePost = Column(DATETIME(), nullable=False)

    def __init__(self, Author, Title, Content, DatePost):
        self.Author = Author
        self.Title = Title
        self.Content = Content
        self.DatePost = DatePost

    def __repr__(self):
        return "<blogs(%r, %r, %r, %r)>" % (self.Author, self.Title, self.Content, self.DatePost)

    def make_dict(self):
        return {'Author': self.Author, 'Title': self.Title, 'Content': self.Content, 'DatePost': self.DatePost}


def abort_if_news_not_found(BlogID):
    news = session.query(blogs).get(BlogID)
    if not news:
        abort(404, message=f"blogs {BlogID} not found")


def get_blogs_():
    conns = engine.connect()
    with conns as conn:
        cur = conn.execute('SELECT * FROM blogs ORDER BY BlogID DESC')
        posts = cur.fetchall()
    return posts

# КЛАСС АВТОРОВ
class auhtor(base):
    __tablename__ = 'auhtor'
    AuthorID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(VARCHAR(45), nullable=False)
    LastName = Column(VARCHAR(45), nullable=False)
    Email = Column(VARCHAR(45), nullable=False)
    Phone = Column(VARCHAR(12), nullable=False)
    DateRegistration = Column(DATETIME(), nullable=False)

    def __init__(self, FirstName, LastName, Email, Phone, DateRegistration):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.Phone = Phone
        self.DateRegistration = DateRegistration

    def __repr__(self):
        return "<auhtor(%r, %r, %r, %r, %r)>" % (self.FirstName, self.LastName, self.Email, self.Phone, self.DateRegistration)

    def make_dict(self):
        return {'FirstName': self.FirstName, 'LastName': self.LastName, 'Email': self.Email,
                'Phone': self.Phone, 'DateRegistration': self.DateRegistration}

def get_authors():
    conns = engine.connect()
    with conns as conn:
        cur = conn.execute('SELECT * FROM auhtor ORDER BY AuthorID DESC')
        posts = cur.fetchall()
        # print (json.dumps(posts))
    return posts


# КЛАСС КОММЕНТАРИЕВ
class comments(base):
    __tablename__ = 'comments'
    CommentID = Column(Integer, primary_key=True, autoincrement=True)
    BlogID = Column(Integer, nullable=False)
    Author = Column(VARCHAR(95), nullable=False)
    Content = Column(VARCHAR(100), nullable=False)
    DateComment = Column(DATETIME(), nullable=False)

    def __init__(self, BlogID, Author, Content, DateComment):
        self.BlogID = BlogID
        self.Author = Author
        self.Content = Content
        self.DateComment = DateComment

    def __repr__(self):
        return "<comments(%r, %r, %r, %r)>" % (self.BlogID, self.Author, self.Content, self.DateComment)

    def make_dict(self):
        return {'BlogID': self.BlogID, 'Author': self.Author, 'Content': self.Content,
                'DateComment': self.DateComment}

def get_comment():
    conns = engine.connect()
    with conns as conn:
        cur = conn.execute('SELECT * FROM comments ORDER BY CommentID DESC')
        posts = cur.fetchall()
        # print (json.dumps(posts))
    # base.metadata.create_all()
    return posts

def add_data():
    data2 = blogs(Author='Мария2', Title="Фокин323а", Content='r2ita@mail.ru', DatePost='2021-05-04 21:25:45')
    session.add_all([data2])
    session.commit()

def bl_delete():
    data = 'редактирование 28'
    conns = engine.connect()
    with conns as conn:
        cur = conn.execute("SELECT Title, Content FROM blogs WHERE Title = '%s'" % data)
        posts = cur.fetchall()
        data_2 =posts
    print(data_2)
    return "Guide was successfully deleted"
