# coding=utf-8
# @File  : user3.py
# @Author: PuJi
# @Date  : 2018/5/9 0009

from user import Developer
import logging

class Developer3(Developer):

    def __init__(self):
        # init base config and udfs
        self.log = logging.getLogger("Developer3:")
        self.log.info("Developer3 init")

