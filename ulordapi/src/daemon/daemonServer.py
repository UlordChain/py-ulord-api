# coding=utf-8
# @File  : daemonServer.py
# @Author: PuJi
# @Date  : 2018/5/3 0003

class DaemonServer(object):
    def __init__(self):
        self.daemon = None
        self.webserver = None


import pprint, argparse, sys, os, textwrap, json

path = os.path.split(os.getcwd())[0]
sys.path.append("E:\ulord\py-ulord-api")

from ulordapi import config,ulordconfig
from ulordapi.src.db.manage import create
from ulordapi.src.user import user1, user2
from ulordapi.src.udfs import udfs

develop1 = user1.Developer1(ulordconfig.get('ulord_head').get('appkey'))

develop2 = user2.Developer2(ulordconfig.get('username'), ulordconfig.get('password'))


def methods_of(obj):
    result = []
    for i in dir(obj):
        if callable(getattr(obj, i)) and i.startswith('cli_'):
            result.append((i.split('cli_')[-1], getattr(obj, i)))
    return result


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

    )
    # for category in CATEGORIES:
    #     command_object = CATEGORIES[category]()
    #
    #     category_parser = subparsers.add_parser(category)
    #     category_parser.set_defaults(command_object=command_object)


class client():
    def __init__(self):
        pass


def formatResult(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result

    return wrapper


class test():
    def cli_test(self):
        print('cli_test')

    def cli_start(self):
        print('cli_start')


class daemon():
    def cli_init(self):
        print("cli_init")

    def cli_stop(self):
        print('cli_stop')


@formatResult
def edit_config(args):
    if args and args.key:
        args = args.key
    return develop2.config_edit(args)


@formatResult
def show_config(args):
    if args and args.key:
        args = args.key
    return develop2.config_show(args)


def fetch_func_args(func,matchargs):
    fn_args = []
    for args,kwargs in getattr(func, 'args', []):
        arg = args[0]
        fn_args.append(getattr(matchargs, arg))


CATEGORIES = {
    'test' : {
        'help':"This is test help",
        'class':test
    },
    'daemon': {
        'help':'This is daemon help',
        'class':daemon
    }
}


def help_description(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


if __name__ == '__main__':
    # print show_config(['ulordconfigs','password'])
    # print show_config(['ulordconfigs'])
    top_parser = argparse.ArgumentParser(
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

    )
    top_parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1')

    subparsers = top_parser.add_subparsers(title="ulordapi sub-command",description="ulordapi sub-command",  help='subcommand help')

    for category in CATEGORIES:
        command_helper = CATEGORIES.get(category)
        command_object = command_helper.get('class')
        command_help = command_helper.get('help')
        category_parser = subparsers.add_parser(category, help=command_help)
        category_parser.set_defaults(command_object=command_object)
        category_subparsers = category_parser.add_subparsers(dest='action')
        for (action, action_fn) in  methods_of(command_object):

            # print(action)
            # print(action_fn)

            parser = category_subparsers.add_parser(action)

            action_kwargs = []
            for args, kwargs in getattr(action_fn, 'args', []):
                parser.add_argument(*args, **kwargs)

            parser.set_defaults(action_fn=action_fn)
            parser.set_defaults(action_kwargs=action_kwargs)

    match_args = top_parser.parse_args()

    fn = match_args.action_fn
    fn_args = fetch_func_args(fn, match_args)
    print(fn_args)
    fn(*fn_args)