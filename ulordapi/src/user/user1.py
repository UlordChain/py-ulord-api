# coding=utf-8
# @File  : user1.py
# @Author: PuJi
# @Date  : 2018/5/9 0009

import logging

from user import Developer
from ulordapi.src.ulordpaltform.up import UlordHelper
from ulordapi.src.udfs.udfs import UdfsHelper
from ulordapi import ulordconfig


class Developer1(Developer, UlordHelper, UdfsHelper):
    # ulord-platform API and some udfs API
    def __init__(self, appkey):
        ulordconfig.update({
            'ulord_head':{
                'appkey':appkey
            }
        })
        UlordHelper.__init__(self)
        UdfsHelper.__init__(self)
        self.log = logging.getLogger("Developer1:")
        self.log.info("Developer1 init")


