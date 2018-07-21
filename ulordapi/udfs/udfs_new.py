# coding=utf-8
# Copyright (c) 2016-2018 The Ulord Core Developers
# @File  : udfs.py
# @Author: Ulord_PuJi
# @Date  : 2018/7/19 0019
import logging
import os
import json
from uuid import uuid1

import ipfsapi

from ulordapi.config import ROOTPATH
# from ulordapi.utils import fileHelper


class Udfs():
    """udfs class"""
    def __init__(self, host='114.67.37.2', port='20418'):
        """add log and init a connection"""
        self.log = logging.getLogger("Udfs:")
        self.connect = ipfsapi.connect(host=host, port=port)
        self.downloadpath = os.path.join(ROOTPATH, 'download')

    def config(self, host, port):
        """update your connection"""
        self.connect = ipfsapi.connect(host=host, port=port)

    def upload_file(self, filepath):
        """upload file"""
        if os.path.isfile(filepath):
            return self.connect.add(filepath).get('Hash')
        else:
            self.log.error("Not a file:{}".format(filepath))
            return None

    def upload_stream(self, stream):
        """upload stream"""
        file_temp = os.path.join(ROOTPATH, 'temp', "{}.txt".format(uuid1()))
        if fileHelper.saveFile(file_temp, stream):
            result = self.connect.add(file_temp)
            try:
                os.remove(file_temp)
            except Exception as e:
                self.log.error("del temp file {0} error: {1}".format(file_temp, e))
                return result.get('Hash')

    def list(self, filehash):
        """list the udfs hash chunks"""
        links = []
        objects = self.connect.ls(filehash).get('Objects')
        if objects:
            for ob in objects:
                if 'Links' in ob.keys():
                    if ob.get('Links'):
                        for link in ob.get('Links'):
                            links.append(link.get('Hash'))
                    else:
                        links.append(ob.get('Hash'))
        return links

    def download(self, udfshash):
        """download the udfshash file"""
        self.connect.get(udfshash, self.downloadpath)

    def _get_chunks(self, filepath):
        """get chunks from the filepath(a json file)"""
        with open(filepath, 'r') as target:
            try:
                result = json.load(target)
            except Exception as e:
                self.log.error("Error read json file {0}:{1}".format(filepath, e))
                result = None
        return result

    # def resumableDownload(self, filehash):
    #     """resumable download"""
    #     filehash_path = os.path.join(self.downloadpath, filehash)
    #     tempjson = os.path.join(filehash_path, 'temp.json')
    #     filedict = None
    #     if os.path.isfile(filehash_path):
    #         # 已下载文件
    #         print('Successful download')
    #         return True
    #     if os.path.isdir(filehash_path):
    #         # 下载一半的情况
    #         if os.path.isfile(tempjson):
    #             # 存在临时json文件
    #             filedict = self._get_chunks(tempjson)
    #         else:
    #             filedict = {}
    #     else:
    #         # 第一次下载
    #         filelist = self.list(filehash)
    #
    #     # for file in filedict:
    #     #     if
    #     #     self.download(file)


if __name__ == '__main__':
    udfs = Udfs()
    print(udfs.list("QmT4kFS5gxzQZJwiDJQ66JLVGPpyTCF912bywYkpgyaPsD"))
    # udfs.download('QmQng3FX98mSe34z3jM1QFQ7XVsoEDWPbKg25ygPaWzgv4')
