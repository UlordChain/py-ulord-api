# coding=utf-8
# @File  : __init__.py
# @Author: PuJi
# @Date  : 2018/4/26 0026

import collections

def Update(d, u):
    for k, v in u.iteritems():
        if isinstance(d.get(k, None), collections.Mapping) and isinstance(v, collections.Mapping):
            d[k] = Update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def ListToDict(args):
    if not isinstance(args, list):
        return None
    if len(args) == 1:
        return args[0]
    else:
        return {
            args[0]:ListToDict(args[1:])
        }


def require(required, tag):
    def decorate(func):
        def wrapper(*args, **kwargs):
            global tag
            if tag:
                func(*args, **kwargs)
                # print("will run {0} {1}".format(str(func), func))
            else:
                # print("need {0} {1}".format(str(required), required))
                required()
                func(*args, **kwargs)
        return wrapper
    return decorate


if __name__ == '__main__':
    # a = [1,2,3,4]
    # print(ListToDict(a))
    tag = None

    def connect():
        global tag
        print("connect ... ")
        tag = True

    @require(connect, tag)
    def start():
        print("start init...")


    start()
    import time
    time.sleep(2)
    start()




