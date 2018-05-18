# coding=utf-8
# Copyright (c) 2016-2018 The Ulord Core Developers
# @File  : user.py
# @Author: Ulord_PuJi
# @Date  : 2018/5/18 0018

import inspect, logging

from ulordapi.config import config
import utils


class Developer():
    """
    basic develoer class to execute some functions
    """
    def config_edit(self, args=None):
        """
        config operations

        :param args: a list or a dict.Update config
        :type args: list/dict
        :return: args dict
        """
        # args is a list or a dict
        if isinstance(args, list):
            args = utils.ListToDict(args)
        if not isinstance(args, dict):
            return None
        if args:
            utils.Update(config, args)
            # write to the config file
            config.save()
        return args

    def config_show(self, args=None):
        """
        show config.Default show all.
        :param args: keys
        :type args: list/dict
        :return: config according to the keys
        """
        result = config
        if args and isinstance(args, list):
            for arg in args:
                if result is None:
                    return None
                result = result.get(arg)
        return result

    def config_init(self):
        """
        init config
        """

    # udfs operations
    def udfs_download(self, udfshashs):
        # download file from ulord.udfses is a udfs list
        result = {}
        for udfshash in udfshashs:
            # TODO multi threading
            if utils.isUdfsHash(udfshash):
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
        # TODO achieve
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