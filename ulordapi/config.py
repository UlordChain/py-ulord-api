# coding=utf-8
# Copyright (c) 2016-2018 The Ulord Core Developers
# @File  : config.py
# @Author: PuJi
# @Date  : 2018/5/16 0016
# @Description : Second import.Just after utils
import os, json, logging, io, time

from ulordapi import utils


PROJECT_ROOTPATH = os.path.dirname(os.path.realpath(__file__))
ROOTPATH = os.getcwd()
level='INFO'
log_format='[%(asctime)s] %(levelname)-8s %(name)s %(message)s'
log_file_path=os.path.join(ROOTPATH, 'upapi.log')


class Config(dict):
    """
    config class.Based on the dict.Update key-value,including subdict.
    """
    def __init__(self, *args, **kwargs):
        """
        config init

        :param key-value: config key and it's value
        :type key-value : str
        """
        dict.__init__(self, *args, **kwargs)
        self._ensure_subconfig()
        self.log = logging.getLogger('Config:')

    def _ensure_subconfig(self):
        """
        set sub dict as config class
        """
        for key in self:
            obj = self[key]
            if isinstance(obj, dict) and not isinstance(obj, Config):
                setattr(self, key, Config(obj))

    def save(self):
        """
        save config to the config file.Just for the config,not support for it's sub config.

        """
        # data ={k: unicode(v).encode("utf-8") for k,v in self.iteritems()}
        # Just think about config.maybe need to think about other instance.
        if self.has_key('baseconfig') and self['baseconfig'].has_key('config_file'):
            # print(json.dumps(self, ensure_ascii=False, indent=2, sort_keys=True))
            with open(self['baseconfig']['config_file'], 'w') as target:
                json.dump(self, target, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)
        else:
            self.log.error("cann't find config.Please check if has config_file in config.It will using original path {}".format(os.path.join(ROOTPATH, 'config')))
            # self.update({
            #     "baseconfig":{
            #         "version":"0.0.1",
            #         "config_file":unicode(os.path.join(ROOTPATH, 'config')).encode('utf-8')
            #     }
            # })
            utils.Update(self, {
                    "baseconfig": {
                            "version":"0.0.1",
                            "config_file":unicode(os.path.join(ROOTPATH, 'config')).encode('utf-8')
                    }
                })
            with open(os.path.join(ROOTPATH, 'config'), 'w') as target:
                json.dump(self, target, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)

    def read(self, init=True):
        """
        read config from config file and update config.

        :param init: check if the config is first save.Default is True, will save the config file.
        :type init: bool
        """
        # read and config from self['baseconfig']['config_file']
        if self.has_key('baseconfig') and self['baseconfig'].has_key('config_file') and \
                os.path.isfile(self.get('baseconfig').get('config_file')):
            # with io.open(self['baseconfig']['config_file'], 'r', encoding='utf8') as target:
            with io.open(self['baseconfig']['config_file'], encoding='utf-8') as target:
                # self.update(utils.json_load_byteified(target))
                utils.Update(self, utils.json_load_byteified((target)))
        elif init:
            # first init
            self.save()
        else:
            self.log.error("cann't find config.Please restart...")
            os._exit(-1)

    def edit(self, data):
        self.update(data)
        self.save()


baseconfig = Config(
    version="0.0.1",
    Debug=True,
    config_file=os.path.join(ROOTPATH, 'config')
)


udfsconfig = Config(
    udfs_host = '127.0.0.1',
    udfs_port = 5001,
)


logconfig = Config(
    level=level,
    format=log_format,
    log_file_path=log_file_path
)


ulordconfig = Config(
    ulord_url = "http://192.168.14.67:5000/v1",
    ulord_secret = "5d42b27f581c11e8bf63f48e3889c8ab",
    ulord_appkey = '5d42b27e581c11e88b12f48e3889c8ab',
    ulord_curtime = int(time.time()),
    # ulord_head = {
    #     "U-AppKey": "",
    #     "U-CurTime": int(time.time())
    #         # "appkey": "2b111d70452f11e89c2774e6e2f53324"
    #     },
    ulord_publish = "/transactions/publish",
    # ulord_publish_data = {
    #         "author": "justin",
    #         "title": "第一篇技术博客",
    #         "tags": ["blockchain", "IPFS"],
    #         "udfs_hash": "QmVcVaHhMeWNNetSLTZArmqaHMpu5ycqntx7mFZaci63VF",
    #         "price": 0.1,
    #         "content_type": ".txt",
    #         "pay_password": "123",
    #         "description": "这是使用IPFS和区块链生成的第一篇博客的描述信息"
    #     },
    ulord_createwallet = "/transactions/createwallet",
    ulord_transaction = "/transactions/consume",
    ulord_paytouser = "/transactions/paytouser",
    ulord_queryblog = "/content/list",
    ulord_querybalance = "/transactions/balance",
    ulord_checkbought = "/transactions/check",
    ulord_userpublished = "/content/publish/list",
    ulord_userbought = "/content/consume/list",
    ulord_in = "/transactions/account/in",
    ulord_out = "/transactions/account/out",
    ulord_billings = "/transactions/publish/account",
    ulord_publish_num = "/transactions/publish/count",
    ulord_view = "/content/view",
    ulord_billings_detail = "/transactions/account/inout",
    #TODO ulord other URL,
    # password = "123",
    # username = "shuxudong",
    # password = "123"
    # username = "cln"
)


webconfig = Config(
    start=True,
    port= 5000,
    host='0.0.0.0',
    token_expired=86400, # Token expiration time. /s
    # activity
    activity=True,
    amount=10,

    # encryption
    # utilspath = os.path.join(ROOTPATH, 'utils'),
    pubkeypath=os.path.join(ROOTPATH, 'public.pem'),
    privkeypath=os.path.join(ROOTPATH, 'private.pem'),
)


dbconfig = Config(
    IsCreated=False,
    SECRET_KEY="ulord platform is good",
    SQLALCHEMY_DATABASE_URI='sqlite:///sqlite.db',
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
    JSON_AS_ASCII=False, # support chinese
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SQLALCHEMY_COMMIT_TEARDOWN=True
)


config = Config(
    baseconfig=baseconfig,
    udfsconfig=udfsconfig,
    logconfig=logconfig,
    ulordconfig=ulordconfig,
    webconfig=webconfig,
    dbconfig=dbconfig
)


config.read()
baseconfig = config.get('baseconfig')
udfsconfig = config.get('udfsconfig')
logconfig = config.get('logconfig')
ulordconfig = config.get('ulordconfig')
webconfig=config.get('webconfig')
dbconfig = config.get('dbconfig')
# TODO need to init some actions according to the config
level=logconfig.get('level')
log_format=logconfig.get('format')
log_file_path=logconfig.get('log_file_path')


if level in logging._levelNames.keys():
    level = logging._levelNames.get(level)
else:
    level = logging.INFO


logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    format=log_format)


# if __name__ == '__main__':
#     import pprint
#     pprint.pprint(config)
