# coding=utf-8
# @File  : user.py
# @Author: PuJi
# @Date  : 2018/5/9 0009
import logging, inspect

from ..utils import ListToDict, Update
from ..config import config
from ..up.udfs import udfshelper
from ..utils.Checker import checker
from ..up.up import ulord_helper


class Developer():
    # basic class to execute some functions
    # init base config and udfs
    # def __init__(self):
    #     self.log = logging.getLogger("User:")
    #     self.log.info("Basic")

    # config operations
    def config_edit(self, args=None):
        # args is a list or a dict
        if isinstance(args, list):
            args = ListToDict(args)
        if not isinstance(args, dict):
            return None
        if args:
            Update(config,args)
            # write to the config file
            config.save()
            # return return_result(0, result={
            #     'config': config
            # })
        return args

    def config_show(self, args=None):
        result = config
        if args and isinstance(args, list):
            for arg in args:
                if result is None:
                    return None
                result = result.get(arg)
        # return return_result(0, result={
        #     'config':result
        # })
        return result

    def config_init(self):
        # init config
        pass

    # udfs operations
    def udfs_download(self, udfshashs):
        # download file from ulord.udfses is a udfs list
        result = {}
        for udfshash in udfshashs:
            # TODO multi threading
            if checker.isUdfsHash(udfshash):
                filehash = udfshelper.downloadhash(udfshash)
                result.update({
                    udfshash: filehash
                })
            else:
                result.update({
                    udfshash: "not a udfshash"
                })
        # return return_result(0, result=result)
        return result

    def udfs_upload(self, fileinfos):
        # upload file into ulord.fileinfo is a file list
        result = {}
        if isinstance(fileinfos, list):
            for fileinfo in fileinfos:
                # TODO multi threading
                filehash = udfshelper.upload_file(fileinfo)
                result.update({
                    fileinfo: filehash
                })
        else:
            filehash = udfshelper.upload_file(fileinfos)
            result.update({
                fileinfos: filehash
            })
        # return return_result(0, result=result)
        return result

    def udfs_cat(self, udfshashs):
        result = {}
        for udfshash in udfshashs:
            if checker.isUdfsHash(udfshash):
                file_context = udfshelper.cat(udfshash)
                result.update({
                    udfshash: file_context
                })
            else:
                result.update({
                    udfshash: "not a udfshash"
                })
        return result

    def start(self):
        # start udfs daemon
        #TODO achieve
        pass

    def stop(self):
        # stop udfs daemon
        # TODO achieve
        pass

    # Advanced command
    def request(self, method, url, data=None):
        if method == 'post':
            return ulord_helper.post(url=url, data=data)
        if method == 'get':
            return ulord_helper.get(url=url)

    def help(self):
        return inspect.getmembers(self, predicate=inspect.ismethod)


if __name__ == '__main__':
    develop = Developer()
    result = develop.help()
    try:
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except:
        # print(type(result))
        print(result)