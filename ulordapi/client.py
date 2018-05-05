# coding=utf-8
# @File  : client.py
# @Author: PuJi
# @Date  : 2018/4/17 0017

# init to start three APIs.

from config import config
import pprint

class upapi():
    def __init__(self):
        pass

def edit_config(self):
    pass

def show_config(self, args=None):
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
    print show_config(['ulordconfigs','password'])
    print show_config(['ulordconfigs'])