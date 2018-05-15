# coding=utf-8
# @File  : __init__.py.py
# @Author: PuJi
# @Date  : 2018/4/17 0017

import os,json, logging,io,yaml,sys,time

import chardet
from ulordapi.src.utils import fileHelper
# reload(sys)
# sys.setdefaultencoding('utf8')

ROOTPATH = os.path.dirname(os.path.realpath(__file__))
level='INFO'
format='[%(asctime)s] %(levelname)-8s %(name)s %(message)s'
# format='%(levelname)-8s %(name)s %(message)s'
log_file_path=os.path.join(ROOTPATH, 'upapi.log')


class Config(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self._ensure_subconfig()
        self.log = logging.getLogger('Config:')

    def _ensure_subconfig(self):
        for key in self:
            obj = self[key]
            if isinstance(obj, dict) and not isinstance(obj, Config):
                setattr(self, key, Config(obj))

    def save(self):
        # data ={k: unicode(v).encode("utf-8") for k,v in self.iteritems()}
        # Just think about config.maybe need to think about other instance.
        if self.has_key('baseconfig') and self['baseconfig'].has_key('config_file'):
            # print(json.dumps(self, ensure_ascii=False, indent=2, sort_keys=True))
            with open(self['baseconfig']['config_file'], 'w') as target:
                json.dump(self, target, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)
        else:
            self.log.error("cann't find config.Please check if has config_file in config.It will using original path {}".format(os.path.join(ROOTPATH, 'config')))
            self.update({
                "baseconfig":{
                    "version":"0.0.1",
                    "config_file":unicode(os.path.join(ROOTPATH, 'config')).encode('utf-8')
                }
            })
            with open(os.path.join(ROOTPATH, 'config'), 'w') as target:
                json.dump(self, target, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)

    def read(self, init=True):
        # read and config from self['baseconfig']['config_file']
        if self.has_key('baseconfig') and self['baseconfig'].has_key('config_file') and \
                os.path.isfile(self.get('baseconfig').get('config_file')):
            # with io.open(self['baseconfig']['config_file'], 'r', encoding='utf8') as target:
            with io.open(self['baseconfig']['config_file'], encoding='utf-8') as target:
                self.update(fileHelper.json_load_byteified(target))
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
        config_file=os.path.join(ROOTPATH, 'config')
)


udfsconfig = Config(
    udfs_host = '127.0.0.1',
    udfs_port = 5001,
)


logconfig = Config(
    level=level,
    format=format,
    log_file_path=log_file_path
)


ulordconfig = Config(
    ulord_url = "http://192.168.14.67:5000/v1",
    ulord_secert = "5d42b27f581c11e8bf63f48e3889c8ab",
    ulord_appkey = '5d42b27e581c11e88b12f48e3889c8ab',
    ulord_curtime = int(time.time()),
    # ulord_head = {
    #     "U-AppKey": "",
    #     "U-CurTime": int(time.time())
    #         # "appkey": "2b111d70452f11e89c2774e6e2f53324"
    #     },
    ulord_publish = "/transactions/publish",
    ulord_publish_data = {
            "author": "justin",
            "title": "第一篇技术博客",
            "tag": ["blockchain", "IPFS"],
            "udfs_hash": "QmVcVaHhMeWNNetSLTZArmqaHMpu5ycqntx7mFZaci63VF",
            "price": 0.1,
            "content_type": ".txt",
            "pay_password": "123",
            "description": "这是使用IPFS和区块链生成的第一篇博客的描述信息"
        },
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
    # utilspath = os.path.join(os.getcwd(), 'utils'),
    pubkeypath=os.path.join(os.path.join(os.getcwd(), 'utils'), 'public.pem'),
    privkeypath=os.path.join(os.path.join(os.getcwd(), 'utils'), 'private.pem'),
)


dbconfig = Config(
    IsCreated=False,
    Debug=True,
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
format=logconfig.get('format')
log_file_path=logconfig.get('log_file_path')


if level in logging._levelNames.keys():
    level = logging._levelNames.get(level)
else:
    level = logging.INFO


logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    format=format)


# if __name__ == '__main__':
#     import pprint
#     pprint.pprint(config)