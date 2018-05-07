# coding=utf-8
# @File  : client.py
# @Author: PuJi
# @Date  : 2018/4/17 0017

# init to start three APIs.


import pprint, argparse, sys, os, textwrap

path = os.path.split(os.getcwd())[0]
sys.path.append(path)
from ulordapi import config
from ulordapi.src.daemon.daemonCLI import commands
from ulordapi.src.db.manage import test


def main():
    parser = argparse.ArgumentParser(
        prog='ulordapi',
        description='ulord - SDK for the Ulord APIs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog = textwrap.dedent('''
        Use 'ulordapi <command> --help' to learn more about each command.
                
        EXIT STATUS
                
        The CLI will exit with one of the following values:
                
        0   Successful execution.
        1   Failed executions.
        '''),

        )
    # main command
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1')

    # subcommand
    subparsers = parser.add_subparsers(title="ulordapi sub-command", help='subcommand help')

    # basic group
    # group_basic = parser.add_argument_group('BASIC COMMANDS')

    # subcommand - basic commands
    parser_basic = subparsers.add_parser(
        'user',
        help='basic'
    )
    subparsers_basic = parser_basic.add_subparsers(
        title='BASIC COMMANDS',
        description='packing ulord-platform HTTP APIs and come transmission functions',
    )
    parser_basic_user = subparsers_basic.add_parser('regist', help='user regist')
    parser_basic_user.set_defaults(func=commands.user_regist)

    parser_basic_user = subparsers_basic.add_parser('login', help='user login')
    parser_basic_user.set_defaults(func=commands.user_login)

    # subcommand - DB commands
    parser_DB = subparsers.add_parser(
        'DB',
        help='DB'
    )
    subparsers_DB = parser_DB.add_subparsers(
        title='DB COMMANDS',
        description='create simple database and some simple API for Junior programmer',
        help='DB'
    )
    parser_db_create = subparsers_DB.add_parser('create', help='create database')
    parser_db_create.set_defaults(func=test.main)

    # subcommand - config commands
    parser_config = subparsers.add_parser(
        'config',
        help='config'
    )
    subparsers_config = parser_config.add_subparsers(
        title='CONFIG COMMANDS',
        description='config management',
        help='config'
    )
    parser_config_show = subparsers_config.add_parser('show', help='show config')
    parser_config_show.set_defaults(func=show_config)

    parser_config_edit = subparsers_config.add_parser('edit', help='edit config')
    parser_config_edit.set_defaults(func=edit_config)

    args = parser.parse_args()

    args.func(args)


class client():
    def __init__(self):
        pass


def edit_config():
    pass


def show_config(args=None):
    print(args)
    if not args:
        return config
    else:
        result = config
        for arg in args:
            if result is None:
                return None
            result = result.get(arg)
        return result


if __name__ == '__main__':
    # print show_config(['ulordconfigs','password'])
    # print show_config(['ulordconfigs'])
    main()

