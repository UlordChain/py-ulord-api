# coding=utf-8
# @File  : client.py
# @Author: PuJi
# @Date  : 2018/4/17 0017
import ipfsapi
from uuid import uuid1

from upapi.src.db.tett import app, db, User, Resource, Billing, Tag, Ads, Content

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
            pass
        user = User()
        user.username = username
        user.hash_password(password)


