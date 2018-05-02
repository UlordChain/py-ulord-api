# coding=utf-8
# @File  : client.py
# @Author: PuJi
# @Date  : 2018/4/17 0017

from uuid import uuid1
import inspect

import ipfsapi

from upapi.src.db.manage import app, db, User, Resource, Billing, Tag, Ads, Content
from upapi.src.utils.errcode import _errcodes


class Client(object):
    # developer has to init a client to call command
    def __init__(self):
        # init base config and udfs
        pass

    # user command
    def user_regist(self, username, password, cellphone=None, email= None):
        pass

    def user_login(self):
        pass

    def user_publish(self):
        pass

    def user_consume(self):
        pass

    def user_query(self):
        pass

    # edit config
    def config_edit(self):
        pass

    def config_show(self):
        pass

    # UDFS command
    def udfs_download(self):
        pass

    def udfs_upload(self):
        pass

    def udfs_cat(self):
        pass

    # Advanced command
    def request(self):
        pass
