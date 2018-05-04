# coding=utf-8
# @File  : config.py
# @Author: PuJi
# @Date  : 2018/4/19 0019

import os,json
ROOTPATH = ''

class Config(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self._ensure_subconfig()

    def _ensure_subconfig(self):
        for key in self:
            obj = self[key]
            if isinstance(obj, dict) and not isinstance(obj, Config):
                setattr(self, key, Config(obj))

    def save(self):
        # just think about config.maybe need to think about other instance.
        if self.has_key('baseconfig') and self['baseconfig'].has_key('config_file'):
            with open(self['baseconfig']['config_file'], 'w') as target:
                json.dump(self, target, ensure_ascii=False, indent=2)
            # with open('config', 'w') as target:
            #     json.dump(self, target, ensure_ascii=False, indent=2)


baseconfig = Config(
        version="0.0.1",
        rev=13,
        config_file="conf"
)

udfsconfig = Config(
    udfs_host = '127.0.0.1',
    udfs_port = 5001,
)


ulordconfig = Config(

    token_expired = 86400, # Token expiration time. /s
    ulord_url = "http://192.168.14.67:5000/v1",
    ulord_head = {
            "appkey": "37fd0c5e3eeb11e8a12af48e3889c8ab"
            # "appkey": "2b111d70452f11e89c2774e6e2f53324"
        },
    ulord_publish = "/transactions/publish/",
    ulord_publish_data = {
            "author": "justin",
            "title": "第一篇技术博客",
            "tag": ["blockchain", "IPFS"],
            "ipfs_hash": "QmVcVaHhMeWNNetSLTZArmqaHMpu5ycqntx7mFZaci63VF",
            "price": 0.1,
            "content_type": ".txt",
            "pay_password": "123",
            "description": "这是使用IPFS和区块链生成的第一篇博客的描述信息"
        },
    ulord_regist = "/transactions/createwallet/",
    ulord_transaction = "/transactions/consume/",
    ulord_paytouser = "/transactions/paytouser/",
    ulord_queryblog = "/content/list/",
    ulord_querybalance = "/transactions/balance/",
    ulord_checkbought = "/transactions/check/",
    ulord_userpublished = "/content/publish/list/",
    ulord_userbought = "/content/consume/list/",
    ulord_in = "/transactions/account/in/",
    ulord_out = "/transactions/account/out/",
    ulord_billings = "/transactions/publish/account/",
    ulord_publish_num = "/transactions/publish/count/",
    ulord_view = "/content/view/",
    ulord_billings_detail = "/transactions/account/inout/",
    #TODO ulord other URL,
    password = "123",
    username = "shuxudong",
    # password = "123"
    # username = "cln"

    # activity
    activity = True,
    amount = 10,

    # encryption
    # utilspath = os.path.join(os.getcwd(), 'utils'),
    pubkeypath = os.path.join(os.path.join(os.getcwd(), 'utils'), 'public.pem'),
    privkeypath = os.path.join(os.path.join(os.getcwd(), 'utils'), 'private.pem'),
)


config = Config(
    baseconfig=baseconfig,
    udfsconfig=udfsconfig,
    ulordconfig=ulordconfig
)


class UPConfig(object):

    def __init__(self):
        self.udfs_host = '127.0.0.1'
        self.udfs_port = 5001
        self.token_expired = 86400 # Token expiration time. /s
        self.ulord_url = "http://192.168.14.67:5000/v1"
        # self.ulord_url = "http://127.0.0.1:5000/v1"
        self.ulord_head = {
            "appkey": "37fd0c5e3eeb11e8a12af48e3889c8ab"
            # "appkey": "2b111d70452f11e89c2774e6e2f53324"
        }
        self.ulord_publish = "/transactions/publish/"
        self.ulord_publish_data = {
            "author": "justin",
            "title": "第一篇技术博客",
            "tag": ["blockchain", "IPFS"],
            "ipfs_hash": "QmVcVaHhMeWNNetSLTZArmqaHMpu5ycqntx7mFZaci63VF",
            "price": 0.1,
            "content_type": ".txt",
            "pay_password": "123",
            "description": "这是使用IPFS和区块链生成的第一篇博客的描述信息"
        }
        self.ulord_regist = "/transactions/createwallet/"
        self.ulord_transaction = "/transactions/consume/"
        self.ulord_paytouser = "/transactions/paytouser/"
        self.ulord_queryblog = "/content/list/"
        self.ulord_querybalance = "/transactions/balance/"
        self.ulord_checkbought = "/transactions/check/"
        self.ulord_userpublished = "/content/publish/list/"
        self.ulord_userbought = "/content/consume/list/"
        self.ulord_in = "/transactions/account/in/"
        self.ulord_out = "/transactions/account/out/"
        self.ulord_billings = "/transactions/publish/account/"
        self.ulord_publish_num = "/transactions/publish/count/"
        self.ulord_view = "/content/view/"
        self.ulord_billings_detail = "/transactions/account/inout/"

        # TODO ulord other URL
        self.password = "123"
        self.username = "shuxudong"
        # self.password = "123"
        # self.username = "cln"

        # activity
        self.activity = True
        self.amount = 10

        # encryption
        self.utilspath = os.path.join(os.getcwd(), 'utils')
        self.pubkeypath = os.path.join(self.utilspath, 'public.pem')
        self.privkeypath = os.path.join(self.utilspath, 'private.pem')


class DevConfig():
    Debug = True
    SECRET_KEY = "ulord platform is good"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite.db'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    JSON_AS_ASCII = False # support chinese



if __name__ == '__main__':
    import pprint
    pprint.pprint(config)
    # config.update()
    config.save()