# coding=utf-8
# @File  : __init__.py
# @Author: PuJi
# @Date  : 2018/4/26 0026

import collections

def update(d, u):
    for k, v in u.iteritems():
        if isinstance(d.get(k, None), collections.Mapping) and isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
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

if __name__ == '__main__':
    a = [1,2,3,4]
    print(ListToDict(a))



