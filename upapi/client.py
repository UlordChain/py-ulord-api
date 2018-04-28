# coding=utf-8
# @File  : client.py
# @Author: PuJi
# @Date  : 2018/4/17 0017

from uuid import uuid1
import inspect

import ipfsapi

from upapi.src.db.tett import app, db, User, Resource, Billing, Tag, Ads, Content
from upapi.src.utils.errcode import _errcodes

# class Client(object):
#
#     def __init__(self):
#         self.ipfs = ipfsapi.connect()
#
#     def start_daemon(self):
#         pass
default_wallet = "Default"
default_pay_password = "123"


class DBhelper():

    # add object into the DB
    def add_user(self, username, password, id=str(uuid1), email=None, cellphone=None, wallet=default_wallet, pay_password=default_pay_password):
        if User.query.filter_by(username=username).first() is not None:
            return _errcodes.get(60000)
        user = User()
        user.username = username
        user.hash_password(password)
        user.id = id
        user.email = email
        user.cellphone = cellphone
        user.wallet = wallet
        user.pay_password = pay_password
        db.session.commit()

    def add_resource(self, title, userid, body, amount, description, id=str(uuid1), tags=None):
        if tags is None or isinstance(tags, list):
            return _errcodes.get(60100)
        resource = Resource()
        resource.title = title
        resource.userid = userid
        resource.body = body
        resource.amount = amount
        resource.description = description
        resource.id = id
        for tag in tags:
            if Tag.query.filter_by(tagname=tag).first() is None:
                resource.tags.append(Tag(tag))
            else:
                resource.tags.append()

    def modify_user(self, userid, **kwargs):
        # user = User.filter_by(id=userid)
        user= User()
        user_list_bak = dir(user)
        for kwarge in kwargs:
            if kwarge in user_list_bak:
                print(kwargs[kwarge])

        print(user_list_bak)

# dbhelper = DBhelper()
# dbhelper.modify_user("id",username="tet", password="ddd")

from src.db.tett import User

print(User.add(username="test2",password='123'))
print(User.modify(userid='e97cd6e1-4abc-11e8-956a-f48e388c65be',email="155748264@qq.com", cellphone="15555", ttt='ds'))


