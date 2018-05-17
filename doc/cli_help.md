# py-ulord-api cli reference

created on 2018-05-16

------

## Table of Contents

- [ulordapi](#ulordapi)
- [ulordapi -v](#ulordapi--v)
- [ulordapi daemon](#ulordapi-daemon)
- [ulordapi UP](#ulordapi-up)
- [ulordapi UP create](#ulordapi-up-create)
- [ulordapi UP publish](#ulordapi-up-publish)
- [ulordapi UP transaction](#ulordapi-up-transaction)
- [ulordapi UP paytouser](#ulordapi-up-paytouser)
- [ulordapi UP resourceslist](#ulordapi-up-resourceslist)
- [ulordapi UP querybalance](#ulordapi-up-querybalance)
- [ulordapi UP checkisbought](#ulordapi-up-checkisbought)
- [ulordapi UP queryuserpublished](#ulordapi-up-queryuserpublished)
- [ulordapi UP queryuserbought](#ulordapi-up-queryuserbought)
- [ulordapi UP queryincomebillings](#ulordapi-up-queryincomebillings)
- [ulordapi UP queryoutgobillings](#ulordapi-up-queryoutgobillings)
- [ulordapi UP querybillingsdetail](#ulordapi-up-querybillingsdetail)
- [ulordapi UP querybillings](#ulordapi-up-querybillings)
- [ulordapi UP querypublishnum](#ulordapi-up-querypublishnum)
- [ulordapi udfs](#ulordapi-udfs)
- [ulordapi udfs upload](#ulordapi-udfs-upload)
- [ulordapi udfs download](#ulordapi-udfs-download)
- [ulordapi udfs cat](#ulordapi-udfs-cat)
- [ulordapi DB](#ulordapi-db)
- [ulordapi DB create](#ulordapi-db-create)
- [ulordapi config](#ulordapi-config)
- [ulordapi config show](#ulordapi-config-show)
- [ulordapi config edit](#ulordapi-config-edit)


## ulordapi
```sh
usage: ulordapi [options|sub-command] [-h]

ulordapi ---- SDK for the Ulord APIs

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

ulordapi sub-command:
  ulordapi sub-command,reading API documents

  {daemon,UP,udfs,DB,config}
                        using basic config - E:\ulord\ulord-blog-demo\venv\lib
                        \site-
                        packages\ulordapi-0.0.1-py2.7.egg\ulordapi\config
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

## ulordapi -v
This will show the version of the ulordapi
```sh
ulordapi 0.0.1
```

## ulordapi daemon

Start a daemon for download, upload and webserver.It will start in the program when it was needed.

```sh
usage: ulordapi daemon [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi UP
```sh
usage: ulordapi UP <actions> [<value>] [-h]  ...

optional arguments:
  -h, --help           show this help message and exit

UP COMMANDS:
  packing ulord-platform HTTP APIs and some transmission functions

                       just for the Senior programmer functions.
    create             create wallet
    publish            publish data to the ulord
    transaction        transaction on the ulord
    paytouser          activity send ulord to the user
    resourceslist      list all resources
    querybalance       query user's balance
    checkisbought      check the resource if bought
    queryuserpublished
                       query user's published
    queryuserbought    query user's bought
    queryincomebillings
                       query user's income billings
    queryoutgobillings
                       query user's outgo billings
    querybillingsdetail
                       query the detail of user's billings
    querybillings      query user's billings
    querypublishnum    query the num of user's published

```

## ulordapi UP create

Create wallet for the user.

```sh
usage: ulordapi UP <actions> [<value>] create [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi UP publish

Publish data to the ulord-platform.

```sh
usage: ulordapi UP <actions> [<value>] publish [-h]

optional arguments:
  -h, --help  show this help message and exit
```
## ulordapi UP transaction

Make a transaction in the ulord accroding to the ulord-platform.

```sh

usage: ulordapi UP <actions> [<value>] transaction [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi UP paytouser

Pay develop's amount to the user.This is a web activity.You can edit the config to change the amount.(Default amount=10)

```sh
usage: ulordapi UP <actions> [<value>] paytouser [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi UP resourceslist

List all the resources in the app from the ulord-platform.

```sh
usage: ulordapi UP <actions> [<value>] resourceslist [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi UP querybalance

Query the user's balance.

```sh
usage: ulordapi UP <actions> [<value>] querybalance [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi UP checkisbought

Check the resource if bought or not.

```sh
usage: ulordapi UP <actions> [<value>] checkisbought [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi UP queryuserpublished

Query the resources list which the user has published.

```sh
usage: ulordapi UP <actions> [<value>] queryuserpublished [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi UP queryuserbought

Query the resources list which the user has bought.

```sh
usage: ulordapi UP <actions> [<value>] queryuserbought [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi UP queryincomebillings

Query the user's income list.

```sh
usage: ulordapi UP <actions> [<value>] queryincomebillings [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi UP queryoutgobillings

Query the user's outgo list.

```sh
usage: ulordapi UP <actions> [<value>] queryoutgobillings [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi UP querybillingsdetail

Query the user billings detail list.

```sh
usage: ulordapi UP <actions> [<value>] querybillingsdetail [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi UP querybillings

Query the user billings detail list.

```sh
usage: ulordapi UP <actions> [<value>] querybillings [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi UP querypublishnum

Query the num of the user published resources.

```sh
usage: ulordapi UP <actions> [<value>] querypublishnum [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi udfs
```sh
usage: ulordapi udfs [upload <file>] | [download|cat <udfs-hash>] [-h]  ...

optional arguments:
  -h, --help  show this help message and exit

UDFS COMMANDS:
  udfs is a high speed transmitter base on the ulord-platform

              upload resources,download/cat resources from the ulord-platform
    upload    upload resources to udfs
    download  download resources from udfs
    cat       look up resources from udfs
```

## ulordapi udfs upload
```sh
usage: ulordapi udfs [upload <file>] | [download|cat <udfs-hash>] upload [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi udfs download
```sh
usage: ulordapi udfs [upload <file>] | [download|cat <udfs-hash>] download
       [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi udfs cat
```sh
usage: ulordapi udfs [upload <file>] | [download|cat <udfs-hash>] cat [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi DB
```sh
usage: ulordapi DB <actions> [-h]  ...

optional arguments:
  -h, --help  show this help message and exit

DB COMMANDS:
  create simple database and some simple APIs

              Manage database
    create    create database
```

## ulordapi DB create
```sh
usage: ulordapi DB <actions> create [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi config
```sh
usage: ulordapi config <key> [<value>] [-h]  ...

optional arguments:
  -h, --help  show this help message and exit

config commands:
  Config Management.It controls configuration variables. The configuration
  values are stored in a config file inside your ulord repository(E:\ulord
  \ulord-blog-demo\venv\lib\site-
  packages\ulordapi-0.0.1-py2.7.egg\ulordapi\config).

              Get and set ulordapi config values.
    show      show config.Output config file contents.
    edit      edit config
```

## ulordapi config show
```sh
usage: config show [-h] [[key] [[key] ...]]

positional arguments:
  [key]       show config.Output config file contents.

optional arguments:
  -h, --help  show this help message and exit
```

## ulordapi config edit
```sh
usage: config edit [-h] [[key] [[key] ...]]

positional arguments:
  [key]       edit config.Open the config file for editing.

optional arguments:
  -h, --help  show this help message and exit
```
