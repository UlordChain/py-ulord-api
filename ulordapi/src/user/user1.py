# coding=utf-8
# @File  : user1.py
# @Author: PuJi
# @Date  : 2018/5/9 0009
from user import User
import logging

class User1(User):

    def __init__(self):
        # init base config and udfs
        self.log = logging.getLogger("User:")
        self.log.info("Basic")