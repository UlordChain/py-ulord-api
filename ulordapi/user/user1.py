# coding=utf-8
# @File  : user1.py
# @Author: PuJi
# @Date  : 2018/5/9 0009

import logging

from user import Developer
from ..up.up import UlordHelper
from ..up.udfs import UdfsHelper
from ..config import ulordconfig, config


class Developer1(Developer, UlordHelper, UdfsHelper):
    # ulord-platform API and some udfs API
    def __init__(self, appkey, secret):
        ulordconfig.update({
            'ulord_appkey': appkey,
            'ulord_secret': secret
        })
        config.save()
        UlordHelper.__init__(self)
        UdfsHelper.__init__(self)
        self.log = logging.getLogger("Developer1:")
        self.log.info("Developer1 init")


