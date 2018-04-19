# coding=utf-8
# @File  : client.py
# @Author: PuJi
# @Date  : 2018/4/17 0017
import ipfsapi


class Client(object):

    def __init__(self):
        self.ipfs = ipfsapi.connect()

    def start_daemon(self):
        pass


