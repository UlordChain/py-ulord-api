# py-ulord-api

[![](https://img.shields.io/badge/py--ulord--api-incomplete-red.svg)](https://github.com/UlordChain/py-ulord-api#todo-list)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![](https://img.shields.io/badge/cli-completed-green.svg)](https://github.com/UlordChain/py-ulord-api#cli)

Ulord-platform HTTP Client Library

Check out [the client API reference](http://py-ulord-api.readthedocs.io/en/latest/) for the full command reference.

*Important*: The legacy py-ulord-api package/module will only work for Ulord-platform 0.0.1 and Python 2.7.

*Note*: This library constantly has to change to stay compatible with the Ulord-platform HTTP API. Currently, this library is tested against Ulord-platform v0.0.1. You may experience compatibility issues when attempting to use it with other versions of Ulord-platform.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Documentation](#documentation)
- [Featured Projects](#featured-projects)
- [TODO list](#todo-list)
- [Contribute](#contribute)
  - [Bug reports](#bug-reports)
  - [Pull requests](#pull-requests)
- [License](#license)

## Install
> *import*: haven't completed!

Install with pip:

```sh
pip install ulordapi
```

Or you can use this repository to set up
```sh
git clone https://github.com/UlordChain/py-ulord-api.git
cd py-ulord-api
python setup.py install
```

## Usage
This package has three functions,including cli, py-api and web-API.

### cli
You can use cli to print help and other functions:

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
### py-api:

waiting...

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

### web-api:

waiting document...

## Documentation

API:[here](https://github.com/UlordChain/py-ulord-api/blob/master/docs/API.md)

[more](http://py-ulord-api.readthedocs.io/en/latest/)

cli-help:[here](https://github.com/UlordChain/py-ulord-api/blob/master/docs/cli_help.md)

webServer-help:[here](https://github.com/UlordChain/py-ulord-api/blob/master/docs/web-server.md)

## Featured Projects

 waiting...

## TODO list
- [x] add TODO list
- [ ] some docs
- [ ] support python3
- [ ] more friendly expression
- [ ] add multi-threading download
- [ ] add unit test
- [ ] docker environment

## Contribute

### Bug reports

You can submit bug reports using the [GitHub issue tracker](https://github.com/UlordChain/py-ulord-api/issues).

### Pull requests

Pull requests are welcome.  Before submitting a new pull request, please waiting...

### Want to read this repository?

Some places to get you started. (WIP)

Senior programmer Main file: [ulordapi/user.py](https://github.com/UlordChain/py-ulord-api/blob/master/ulordapi/user.py#L174) <br>
Junior Programmer Main file: [ulordapi/user.py](https://github.com/UlordChain/py-ulord-api/blob/master/ulordapi/user.py#L191) <br>
CLI Commands: [ulordapi/daemonCLI.py](https://github.com/UlordChain/py-ulord-api/blob/master/ulordapi/daemonCLI.py) <br>
Web Server: [ulordapi/webServer.py](https://github.com/UlordChain/py-ulord-api/blob/master/ulordapi/webServer.py) <br>

## License

This code is distributed under the terms of the [MIT license](https://opensource.org/licenses/MIT).  Details can be found in the file
[LICENSE](LICENSE) in this repository.