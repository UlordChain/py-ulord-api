# py-ulord-api

[![](https://img.shields.io/badge/py--ulord--api-incomplete-red.svg)](https://github.com/UlordChain/py-ulord-api#todo-list)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![](https://img.shields.io/badge/cli-completed-green.svg)](https://github.com/UlordChain/py-ulord-api#cli)

[English](https://github.com/UlordChain/py-ulord-api)

Ulord平台HTTP接口客户端

查阅[文档](http://py-ulord-api.readthedocs.io/en/latest/)查看所有API文档以及相关使用。

*重要*: 当前py-ulord-api项目只针对ulord平台层0.1版本，适用python2.7，暂不支持python3。

*注意*: 为了保持与ulord平台层保持同步状态，当前项目可能会更新的比较频繁。目前只针对平台层0.1版本进行了测试。讲当前库与其他版本的ulord平台共用时可能会出现兼容问题。

## 目录

- [安装](#安装)
- [教程](#教程)
- [使用](#使用)
- [文档](#文档)
- [特性](#特性)
- [待办事项](#待办事项)
- [贡献](#贡献)
  - [漏洞报告](#漏洞报告)
  - [拉取请求](#拉取请求)
- [版权](#版权)

## 安装
> *重要*: 还未完成！

安装pip:

```sh
pip install ulordapi
```

或者使用这个项目进行安装
```sh
git clone https://github.com/UlordChain/py-ulord-api.git
cd py-ulord-api
python setup.py install
```

## 教程

这是一个使用SDK并且以初级开发者身份去创建博客的[教程](https://github.com/UlordChain/py-ulord-api/blob/master/docs/%E6%95%99%E7%A8%8B.md)

## 使用
当前项目有三种方式，包含命令行，python接口以及web接口。

### 命令行
你可以使用命令行打印帮助和其他的一些方法:

```sh
usage: ulordapi [options|sub-command] [-h]

ulordapi ---- SDK for the Ulord APIs

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

ulordapi sub-command:
  ulordapi sub-command,reading API documents

  {daemon,UP,udfs,DB,config}
                        using basic config - E:\ulord\ulord-blog-demo\venv\lib\site-packages\ulordapi-0.0.1-py2.7.egg\ulordapi\config
    daemon              Daemon process,including web server and udfs daemon.
    UP                  main functions
    udfs                transfer resources to the platform
    DB                  Manage database
    config              Manage configuration

Use 'ulordapi <command> --help' to learn more about each command.

EXIT STATUS

The CLI will exit with one of the following values:

0   Successful execution.
1   Failed executions.
```
### python接口:

待更新...

```sh
In [1]: from ulordapi import Junior

In [2]: junior = Junior(appkey="5d42b27e581c11e88b12f48e3889c8ab",secret="5d42b27f581c11e8bf63f48e3889c8ab")

In [3]: junior.config_show()
Out[3]:
{'baseconfig': {'config_file': 'E:\\ulord\\py-ulord-api\\ulordapi\\config',
  'version': '0.0.1'},
 'dbconfig': {'Debug': True,
  'IsCreated': False,
  'JSON_AS_ASCII': False,
  'SECRET_KEY': 'ulord platform is good',
  'SQLALCHEMY_COMMIT_ON_TEARDOWN': True,
  'SQLALCHEMY_COMMIT_TEARDOWN': True,
  'SQLALCHEMY_DATABASE_URI': 'sqlite:///sqlite.db',
  'SQLALCHEMY_TRACK_MODIFICATIONS': True},
 'logconfig': {'format': '[%(asctime)s] %(levelname)-8s %(name)s %(message)s',
  'level': 'INFO',
  'log_file_path': 'E:\\ulord\\py-ulord-api\\ulordapi\\upapi.log'},
 'udfsconfig': {'udfs_host': '127.0.0.1', 'udfs_port': 5001},
 'ulordconfig': {'ulord_appkey': '5d42b27e581c11e88b12f48e3889c8ab',
  'ulord_billings': '/transactions/publish/account',
  'ulord_billings_detail': '/transactions/account/inout',
  'ulord_checkbought': '/transactions/check',
  'ulord_createwallet': '/transactions/createwallet',
  'ulord_curtime': 1526433796,
  'ulord_head': {'U-AppKey': '5d42b27e581c11e88b12f48e3889c8ab',
   'U-CurTime': '1526433796',
   'U-Sign': '65E98D476619939606D3438B535A07F0'},
  'ulord_in': '/transactions/account/in',
  'ulord_out': '/transactions/account/out',
  'ulord_paytouser': '/transactions/paytouser',
  'ulord_publish': '/transactions/publish',
  'ulord_publish_data': {'author': 'test3',
   'content_type': '.txt',
   'description': '\xe8\xbf\x99\xe6\x98\xaf\xe7\xac\xac\xe4\xb8\x80\xe7\xaf\x87UDFS\xe6\xb5\x8b\xe8\xaf\x95\xe6\x96\x87\xe4\xbb\xb6',
   'pay_password': '123',
   'price': 0.1,
   'tag': ['test', 'udfs'],
   'tags': ['test', 'udfs'],
   'title': '\xe7\xac\xac\xe4\xb8\x80\xe7\xaf\x87\xe6\x8a\x80\xe6\x9c\xaf\xe5\x8d\x9a\xe5\xae\xa2',
   'udfs_hash': 'QmQGSgwfMtLH291KmyVouvu1mCwNYvZ2FGmStfvRwLQEgV'},
  'ulord_publish_num': '/transactions/publish/count',
  'ulord_querybalance': '/transactions/balance',
  'ulord_queryblog': '/content/list',
  'ulord_secret': '5d42b27f581c11e8bf63f48e3889c8ab',
  'ulord_transaction': '/transactions/consume',
  'ulord_url': 'http://192.168.14.67:5000/v1',
  'ulord_userbought': '/content/consume/list',
  'ulord_userpublished': '/content/publish/list',
  'ulord_view': '/content/view'},
 'webconfig': {'activity': True,
  'amount': 10,
  'host': '0.0.0.0',
  'port': 5000,
  'privkeypath': 'E:\\ulord\\py-ulord-api\\utils\\private.pem',
  'pubkeypath': 'E:\\ulord\\py-ulord-api\\utils\\public.pem',
  'start': True,
  'token_expired': 86400}}
```

### web接口:

待更新...

## 文档

API文档:[这里](https://github.com/UlordChain/py-ulord-api/blob/master/docs/API.md)

[详情](http://py-ulord-api.readthedocs.io/en/latest/)

命令行文档:[这里](https://github.com/UlordChain/py-ulord-api/blob/master/docs/cli_help.md)

web接口文档:[这里](https://github.com/UlordChain/py-ulord-api/blob/master/docs/web-server.md)

## Featured Projects

 待更新...

## 待办事项
- [x] 添加代办事项
- [ ] 一些文档
- [ ] 支持 python3
- [ ] 更友善的表现接口
- [ ] 添加多线程下载
- [ ] 添加单元测试
- [ ] docker 环境

## 贡献

### 漏洞报告

你可以使用[GitHub issue tracker](https://github.com/UlordChain/py-ulord-api/issues)来提交发现的漏洞.

### 拉取请求

非常欢迎拉取请求。拉取之前, 有些标准暂时还未想好...

### 更好地阅读本项目?

一些你开始的地方。 (WIP)

初级开发者主文件: [ulordapi/user.py](https://github.com/UlordChain/py-ulord-api/blob/master/ulordapi/user.py#L174) <br>
中级开发者主文件: [ulordapi/user.py](https://github.com/UlordChain/py-ulord-api/blob/master/ulordapi/user.py#L191) <br>
命令行: [ulordapi/daemonCLI.py](https://github.com/UlordChain/py-ulord-api/blob/master/ulordapi/daemonCLI.py) <br>
web接口: [ulordapi/webServer.py](https://github.com/UlordChain/py-ulord-api/blob/master/ulordapi/webServer.py) <br>

## 版权

该项目代码遵循 [MIT 协议](https://opensource.org/licenses/MIT)。详情参阅项目中的[LICENSE](LICENSE)文档。