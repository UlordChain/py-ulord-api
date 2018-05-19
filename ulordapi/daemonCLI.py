# coding=utf-8
# @File  : daemonCLI.py
# @Author: PuJi
# @Date  : 2018/5/4 0004

# init to start three APIs.


import pprint, argparse, sys, os, textwrap, json


from .config import config,ulordconfig
from .manage import create
from . import  user


senior = user.Senior(ulordconfig.get('ulord_appkey'), ulordconfig.get('ulord_secret'))

udfs = senior.udfs
# develop2 = user.Junior(ulordconfig.get('ulord_appkey'), ulordconfig.get('ulord_secret'))

try:
    config_path = config.get('baseconfig').get('config_file')
except:
    config_path = "basic config"


def main():
    parser = argparse.ArgumentParser(
        prog='ulordapi',
        description='ulordapi ---- SDK for the Ulord APIs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
        Use 'ulordapi <command> --help' to learn more about each command.

        EXIT STATUS

        The CLI will exit with one of the following values:

        0   Successful execution.
        1   Failed executions.
        '''),
        usage='%(prog)s [options|sub-command] [-h]'
    )
    # main command
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1')
    # parser.add_argument('daemon', action='store_true')

    # subcommand
    subparsers = parser.add_subparsers(
        title="ulordapi sub-command",
        description="ulordapi sub-command,reading API documents ",
        help='using basic config - {}'.format(config_path))

    # basic group
    # group_basic = parser.add_argument_group('BASIC COMMANDS')


    # subcommand - up commands
    parser_daemon = subparsers.add_parser(
        'daemon',
        help='Daemon process,including web server and udfs daemon.',
        prog='ulordapi daemon'
        # type=udfs.udfs.start
    )
    parser_daemon.set_defaults(func=udfs.udfs.start)
    # subparsers_daemon = parser_up.add_subparsers(
    #     title='DAEMON COMMANDS',
    #     description='Daemon process,including web server and udfs daemon',
    # )
    # subparsers_daemon.set_default(func=udfs.udfs.start())
    # parser.add_argument('daemon', help='Daemon process,including web server and udfs daemon')
    # parser.set_defaults(func=udfs.udfs.start())

    # subcommand - up commands
    parser_up = subparsers.add_parser(
        'UP',
        help='main functions',
        prog='ulordapi UP <actions> [<value>]'
    )
    subparsers_up = parser_up.add_subparsers(
        title='UP COMMANDS',
        description='packing ulord-platform HTTP APIs and some transmission functions',
        metavar='',
        help='just for the Senior programmer functions.'
    )
    parser_up_wallet_create = subparsers_up.add_parser('create', help='create wallet')
    parser_up_wallet_create.set_defaults(func=senior.ulord.ulord_createwallet)

    parser_basic_publish = subparsers_up.add_parser('publish', help='publish data to the ulord')
    parser_basic_publish.set_defaults(func=senior.ulord.publish)

    parser_basic_transaction = subparsers_up.add_parser('transaction', help='transaction on the ulord')
    parser_basic_transaction.set_defaults(func=senior.ulord.transaction)

    parser_basic_paytouser = subparsers_up.add_parser('paytouser', help='activity send ulord to the user')
    parser_basic_paytouser.set_defaults(func=senior.ulord.paytouser)

    parser_basic_queryblog = subparsers_up.add_parser('resourceslist', help='list all resources')
    parser_basic_queryblog.set_defaults(func=senior.ulord.queryblog)

    parser_basic_querybalance = subparsers_up.add_parser('querybalance', help="query user's balance")
    parser_basic_querybalance.set_defaults(func=senior.ulord.querybalance)

    parser_basic_checkisbought = subparsers_up.add_parser('checkisbought', help="check the resource if bought")
    parser_basic_checkisbought.set_defaults(func=senior.ulord.checkisbought)

    parser_basic_queryuserpublished = subparsers_up.add_parser('queryuserpublished', help="query user's published")
    parser_basic_queryuserpublished.set_defaults(func=senior.ulord.queryuserpublished)

    parser_basic_queryuserbought = subparsers_up.add_parser('queryuserbought', help="query user's bought")
    parser_basic_queryuserbought.set_defaults(func=senior.ulord.queryuserbought)

    parser_basic_queryincomebillings = subparsers_up.add_parser('queryincomebillings', help="query user's income billings")
    parser_basic_queryincomebillings.set_defaults(func=senior.ulord.queryincomebillings)

    parser_basic_queryoutgobillings = subparsers_up.add_parser('queryoutgobillings', help="query user's outgo billings")
    parser_basic_queryoutgobillings.set_defaults(func=senior.ulord.queryoutgobillings)

    parser_basic_querybillingsdetail = subparsers_up.add_parser('querybillingsdetail', help="query the detail of user's billings")
    parser_basic_querybillingsdetail.set_defaults(func=senior.ulord.querybillingsdetail)

    parser_basic_querybillings = subparsers_up.add_parser('querybillings', help="query user's billings")
    parser_basic_querybillings.set_defaults(func=senior.ulord.querybillings)

    parser_basic_querypublishnum = subparsers_up.add_parser('querypublishnum', help="query the num of user's published")
    parser_basic_querypublishnum.set_defaults(func=senior.ulord.querypublishnum)

    # parser_basic_addpurchases = subparsers_up.add_parser('addpurchases', help="add resources's purchases")
    # parser_basic_addpurchases.set_defaults(func=develop1.addpurchases)

    # subcommand - udfs commands
    parser_udfs = subparsers.add_parser(
        'udfs',
        help='transfer resources to the platform',
        prog='ulordapi udfs [upload <file>] | [download|cat <udfs-hash>]'
    )
    subparsers_udfs = parser_udfs.add_subparsers(
        title='UDFS COMMANDS',
        description='udfs is a high speed transmitter base on the ulord-platform',
        # metavar='ulordapi udfs [upload <file>] | [download|cat <udfs-hash>]',
        metavar='',
        help='upload resources,download/cat resources from the ulord-platform'
    )

    parser_db_upload = subparsers_udfs.add_parser('upload', help='upload resources to udfs')
    parser_db_upload.set_defaults(func=udfs.udfshelper.upload_file)

    parser_db_download = subparsers_udfs.add_parser('download', help='download resources from udfs')
    parser_db_download.set_defaults(func=udfs.udfshelper.downloadhash)

    parser_db_cat = subparsers_udfs.add_parser('cat', help='look up resources from udfs')
    parser_db_cat.set_defaults(func=udfs.udfshelper.cat)

    # subcommand - DB commands
    parser_DB = subparsers.add_parser(
        'DB',
        help='Manage database',
        prog='ulordapi DB <actions>'
    )
    subparsers_DB = parser_DB.add_subparsers(
        title='DB COMMANDS',
        description='create simple database and some simple APIs',
        metavar='',
        help='Manage database'
    )
    parser_db_create = subparsers_DB.add_parser('create', help='create database')
    parser_db_create.set_defaults(func=create)

    # subcommand - config commands
    parser_config = subparsers.add_parser(
        'config',
        help='Manage configuration',
        prog='ulordapi config <key> [<value>]'
    )
    subparsers_config = parser_config.add_subparsers(
        title='config commands',
        description=textwrap.dedent('''
        Config Management.It controls configuration variables.
        
        The configuration values are stored in a config file inside your ulord repository({0}).
        '''.format(config_path)),
        prog='config',
        metavar='',
        help='Get and set ulordapi config values.'
    )
    parser_config_show = subparsers_config.add_parser('show', help='show config.Output config file contents.')
    parser_config_show.add_argument('key', metavar='[key]', nargs='*', help='show config.Output config file contents.')
    parser_config_show.set_defaults(func=show_config)

    parser_config_edit = subparsers_config.add_parser('edit', help='edit config')
    parser_config_edit.add_argument('key', metavar='[key]', nargs='*',
                                    help='edit config.Open the config file for editing.')
    parser_config_edit.set_defaults(func=edit_config)

    args = parser.parse_args()

    if hasattr(args, 'daemon'):
        args.func()
    else:
        args.func(args)


class client():
    def __init__(self):
        pass


def formatResult(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result

    return wrapper


@formatResult
def edit_config(args):
    if args and args.key:
        args = args.key
    return senior.config_edit(args)


@formatResult
def show_config(args):
    if args and args.key:
        args = args.key
    return senior.config_show(args)


if __name__ == '__main__':
    # print show_config(['ulordconfigs','password'])
    # print show_config(['ulordconfigs'])
    main()

