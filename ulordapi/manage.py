# coding=utf-8
# Copyright (c) 2016-2018 The Ulord Core Developers
# @File  : manage.py
# @Author: Ulord_PuJi
# @Date  : 2018/5/18 0018

from uuid import uuid1
import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context

from ulordapi.config import dbconfig
from ulordapi.errcode import _errcodes
from ulordapi.utils import isMail, isCellphone

# initialization
app = Flask(__name__)

app.config.update(dbconfig)

db = SQLAlchemy(app)


resource_tags = db.Table('resource_tags',
                        db.Column('resource_id', db.String(45), db.ForeignKey('resource.id')),
                        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


users_resource = db.Table('users_resource',
                        db.Column('user_id',db.Integer, db.ForeignKey('users.id')),
                        db.Column('resource_id', db.Integer, db.ForeignKey('resource.id')))


# class Base(db.Model):
# TODO:Extracting public methods
#     @classmethod
#     def add(cls, **kwargs):
#         pass


class User(db.Model):
    """
    User table: create user database.

    :Column id: Table id.Default is a uuid.
    :Column username: Needed
    :Column password_hash: Ciphertext password
    :Column email: email
    :Column cellphone: cellphone
    :Column token: user's token,a uuid
    :Column timestamp: token's effective time
    :Column balance: user's balance.# todo need to think about time
    :Column wallet: user's wallet name.Default is username.
    :Column pay_password: user's wallet password.Default is password_hash.It won't change if password has changed.
    :Column boughts: realtion table resource.
    """
    __tablename__ = 'users'
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(32))
    cellphone = db.Column(db.String(12))
    token = db.Column(db.String(128), index=True)
    timestamp = db.Column(db.String(10))
    balance = db.Column(db.Float)
    wallet = db.Column(db.String(34))
    pay_password = db.Column(db.String(128))
    boughts = db.relationship(
        'Resource',
        secondary=users_resource,
        backref=db.backref('resource', lazy='dynamic')
    )

    def hash_password(self, password):
        """
        Hash user's password and save hash result.

        :param password: user's password
        :type password: str
        """
        self.password_hash = pwd_context.encrypt(password)

    @classmethod
    def verify_password(self, password):
        """
        verify password

        :param password: user's password
        :type password: str
        :return: True or False.
        """
        return pwd_context.verify(password, self.password_hash)

    # @classmethod
    # def add(self, username, password, id=str(uuid1()), email=None, cellphone=None, wallet=None, pay_password=None):
    #     """
    #     add user
    #
    #     :param username: username
    #     :type username: str
    #     :param password: password
    #     :type password: str
    #     :param id:user table id ,primary key.Default is uuid.
    #     :type id: str
    #     :param email:user's email.Default is None.
    #     :type email: str
    #     :param cellphone:user's cellphone.Default is None.
    #     :type cellphone:str
    #     :param wallet:user's wallet name.Default is username
    #     :type wallet: str
    #     :param pay_password:user's wallet password.Default is password.
    #     :type pay_password:str
    #     :return:user module
    #     """
    #     if self.query.filter_by(username=username).first() is not None:
    #         return _errcodes.get(60000)
    #     if email and not isMail(email):
    #         return _errcodes.get(60105)
    #     if cellphone and not isCellphone(cellphone):
    #         return _errcodes.get(60106)
    #     user = User()
    #     user.username = username
    #     user.hash_password(password)
    #     user.id = id
    #     user.email = email
    #     user.cellphone = cellphone
    #     if wallet:
    #         user.wallet = wallet
    #     else:
    #         user.wallet = username
    #     if pay_password:
    #         user.pay_password = pay_password
    #     else:
    #         user.pay_password = self.password_hash
    #     db.session.add(user)
    #     db.session.commit()
    #     return user
    #
    # @classmethod
    # def modify(self, userid, **kwargs):
    #     """
    #     modify user's attribute
    #
    #     :param userid: user id.query conditions
    #     :type userid: str
    #     :param kwargs: key-value
    #     :type kwargs: user's attribute and value
    #     """
    #     user = self.query.filter_by(id=userid).first()
    #     for kwarg in kwargs:
    #         if kwarg in self.__dict__.keys():
    #             setattr(user, kwarg, kwargs[kwarg])
    #             # user[kwarg] = kwargs[kwarg]
    #             # print("{0}:{1}".format(kwarg, kwargs[kwarg]))
    #         else:
    #             print("{} doesn's in user's attributes".format(kwarg))
    #     db.session.commit()
    #
    # @classmethod
    # def delete(self, userid):
    #     """
    #
    #     :param userid:
    #     :return:
    #     """
    #     user = self.query.filter_by(id=userid).first()
    #     if user is not None:
    #         db.session.delete(user)
    #         db.session.commit()
    #     else:
    #         print("current user(userid={0}) hasn't found.".format(userid))
    #
    # def generateToken(self, expired=86400):
    #
    #     # generate token,expired is Token expiration time. /s
    #     self.token = str(uuid1())
    #     self.timestamp = int(time.time()) + expired
    #     db.session.conmmmit()


class Resource(db.Model):
    """
    Resource table: create resource table

    :column id: table id,primay key
    :co
    """
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(32), index=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.String(46))
    amount = db.Column(db.Float, index=True)
    tags = db.relationship(
        'Tag',
        secondary=resource_tags,
        backref=db.backref('resource', lazy='dynamic'))
    description = db.Column(db.String(128))
    views = db.Column(db.Integer)
    date = db.Column(db.Integer)
    claimID = db.Column(db.String(40))
    resource_type = db.Column(db.String(10))

    __mapper_args__ = {
        'polymorphic_on': resource_type
    }

    @classmethod
    def add(self, title, userid, body, amount=None, tags=None, description=None):
        if self.query.filter_by(title=title).first() is not None:
            return _errcodes.get(60000)
        resource = Resource()
        resource.title = title
        resource.userid = userid
        resource.body = body
        resource.amount = amount
        resource.tags = tags
        resource.description = description
        db.session.add(resource)
        db.session.commit()
        return _errcodes.update()


class Content(Resource):
    __mapper_args__ = {
        'polymorphic_identity': 'content'
    }


class Ads(Resource):
    __mapper_args__ = {
        'polymorphic_identity': 'ad'
    }


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(32), index=True)
    # Reserved field
    pre1 = db.Column(db.String())
    pre2 = db.Column(db.String())

    def __init__(self, name):
        self.tagname = name



def create():
    """
    Create database.
    """
    # check if existed
    if dbconfig.get('IsCreated'):
        print("Database has created!")
    else:
        db.create_all()


if __name__ == '__main__':
    # db.create_all(bind=['resources_tags', 'users_resources', 'User', 'Resource', 'Ads', 'Tag', 'Billing'])
    create()