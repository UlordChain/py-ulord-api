# py-ulord-api config help

The config contains six sections as below:

baseconfig:

dbconfig:

logconfig:

udfsconfig:

ulordconfig:

webconfig:

You can make your own configuration.And it will take effect during the program execution.

>waring:After your config,you need to restart the program.Then your config will update the basic config.

## baseconfig

Basic config

### config_file

The path of the config.

### version:

current version:0.0.1

## dbconfig

database config.It services for the Junior programmer.Junior programmer can change his favourite database.And the SDK
support most relational database becauseof [flask-sqlalchemy](http://flask-sqlalchemy.pocoo.org/2.3/).

Other config is used for the [flask config](http://flask.pocoo.org/docs/1.0/config/).

### IsCreated

Check if the database has been created.

### JSON_AS_ASCII

### SECRET_KEY

### SQLALCHEMY_COMMIT_ON_TEARDOWN

### SQLALCHEMY_COMMIT_TEARDOWN

### SQLALCHEMY_DATABASE_URI

### SQLALCHEMY_TRACK_MODIFICATIONS

## logconfig

Log config.It is compatible with python logging module.

## format

Log output format.Default is
Config your database.
{
  "baseconfig": {
    "config_file": "E:\\ulord\\py-ulord-api\\ulordapi\\config",
    "version": "0.0.1"
  },
  "dbconfig": {

    "IsCreated": false,
    "JSON_AS_ASCII": false,
    "SECRET_KEY": "ulord platform is good",
    "SQLALCHEMY_COMMIT_ON_TEARDOWN": true,
    "SQLALCHEMY_COMMIT_TEARDOWN": true,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///sqlite.db",
    "SQLALCHEMY_TRACK_MODIFICATIONS": true
  },
  "logconfig": {
    "format": "[%(asctime)s] %(levelname)-8s %(name)s %(message)s",
    "level": "INFO",
    "log_file_path": "E:\\ulord\\py-ulord-api\\ulordapi\\upapi.log"
  },
  "udfsconfig": {
    "udfs_host": "127.0.0.1",
    "udfs_port": 5001
  },
  "ulordconfig": {
    "ulord_appkey": "5d42b27e581c11e88b12f48e3889c8ab",
    "ulord_billings": "/transactions/publish/account",
    "ulord_billings_detail": "/transactions/account/inout",
    "ulord_checkbought": "/transactions/check",
    "ulord_createwallet": "/transactions/createwallet",
    "ulord_curtime": 1526433796,
    "ulord_head": {
      "U-AppKey": "5d42b27e581c11e88b12f48e3889c8ab",
      "U-CurTime": "1526433796",
      "U-Sign": "65E98D476619939606D3438B535A07F0"
    },
    "ulord_in": "/transactions/account/in",
    "ulord_out": "/transactions/account/out",
    "ulord_paytouser": "/transactions/paytouser",
    "ulord_publish": "/transactions/publish",
    "ulord_publish_data": {
      "author": "test3",
      "content_type": ".txt",
      "description": "这是第一篇UDFS测试文件",
      "pay_password": "123",
      "price": 0.1,
      "tag": [
        "test",
        "udfs"
      ],
      "tags": [
        "test",
        "udfs"
      ],
      "title": "第一篇技术博客",
      "udfs_hash": "QmQGSgwfMtLH291KmyVouvu1mCwNYvZ2FGmStfvRwLQEgV"
    },
    "ulord_publish_num": "/transactions/publish/count",
    "ulord_querybalance": "/transactions/balance",
    "ulord_queryblog": "/content/list",
    "ulord_secret": "5d42b27f581c11e8bf63f48e3889c8ab",
    "ulord_transaction": "/transactions/consume",
    "ulord_url": "http://192.168.14.67:5000/v1",
    "ulord_userbought": "/content/consume/list",
    "ulord_userpublished": "/content/publish/list",
    "ulord_view": "/content/view"
  },
  "webconfig": {
  "Debug": true,
    "activity": true,
    "amount": 10,
    "host": "0.0.0.0",
    "port": 5000,
    "privkeypath": "E:\\ulord\\py-ulord-api\\utils\\private.pem",
    "pubkeypath": "E:\\ulord\\py-ulord-api\\utils\\public.pem",
    "start": true,
    "token_expired": 86400
  }
}