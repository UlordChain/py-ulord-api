# coding=utf-8
# Copyright (c) 2016-2018 The Ulord Core Developers
# @File  : version.py
# @Author: Ulord_PuJi
# @Date  : 2018/5/18 0018

# todo: version description

__title__ = 'py-ulord-api'
__version__ = "0.0.1"
__copyright__ = 'Copyright (c) 2016-2018 The Ulord Core Developers'
__license__ = 'MIT'

import sys
__py_version__ = float(str(sys.version_info.major) + '.' + str(sys.version_info.minor))

__packagename__ = 'ulordapi-'+ __version__ + '-py' + str(__py_version__) + '.egg' # ulordapi-0.0.1-py2.7.egg



if __name__ == '__main__':
    print(__py_version__)
    print(type(__py_version__))


    print(__packagename__)