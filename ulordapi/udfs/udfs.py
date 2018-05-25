# coding=utf-8
# Copyright (c) 2016-2018 The Ulord Core Developers
# @File  : udfs.py
# @Author: Ulord_PuJi
# @Date  : 2018/5/18 0018

import sys, os, subprocess, platform, json, time, signal, logging, atexit
from uuid import uuid1

import ipfsapi

from ulordapi.utils import fileHelper
from ulordapi.config import ROOTPATH

class Udfs():
    """
    udfs class,including some operations about daemon program
    """
    def __init__(self):
        """
        add log and init daemon program
        """
        self.log = logging.getLogger("Udfs:")
        # get some paths
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.config = os.path.join(self.root_path, 'config')
        self.lock = os.path.join(self.config, 'repo.lock')
        self.udfs_path = self.get_udfs()
        self.udfs_daemon_pid = self.get_pid()
        if not os.path.isdir(self.config):
            self.start_init()
            if self.udfs_init:
                self.modify_config()
        # self.start()
        # self.connect = UdfsHelper() # TODO: multi helper to download faster

    def get_pid(self):
        """
        get daemon pid

        :return: daemon pid
        """
        if os.path.isfile(self.lock):
            self.log.debug('get udfs daemon pid')
            with open(self.lock, 'r') as target:
                return json.load(target).get("OwnerPID")
        else:
            self.log.debug("self.lock is {}.It doesn't exist".format(self.lock))
            return None

    def get_udfs(self):
        """
        get udfs path according to the os

        :return: udfs path
        """
        tools = os.path.join(self.root_path, 'tools')
        self.current_os = platform.system()
        self.log.info('Current os is {}'.format(self.current_os))

        if self.current_os in ["Windows", "Win32"]:
            udfs = os.path.join(tools, 'udfs.exe')
        elif self.current_os in ["Mac OSX", "Darwin"]:
            udfs = os.path.join(tools, 'udfs')
        elif self.current_os == "Linux":
            udfs = os.path.join(tools, 'udfs')
        else:
            self.log.critical("Unknow operating system")
            sys.exit(0)
        return udfs

    def start_command(self, cmd):
        """
        start external command

        :param cmd: shell command
        :type cmd: str
        :return: popen
        """
        self.log.debug("starting command,current command:{}".format(cmd))
        FNULL = open(os.devnull, 'w')
        try:
            pl = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=FNULL)
        except Exception, e:
            self.log.error("start command failed! Exception is {}".format(e))
            pl = None
        # self.log.info("end command,result is {}".format(pl.communicate()))
        return pl

    def start(self, daemon=None):
        """
        start udfs.if daemon is true, the udfs is a daemon,else the udfs is starting the current thread.

        :param daemon: if wait
        :type daemon: bool
        """
        atexit.register(self.stop)
        cmd = "{0} --config {1} daemon".format(self.udfs_path,self.config)
        self.udfs_daemon = self.start_command(cmd)
        info = "Udfs has started!\nNow you can use it to download or upload!"
        print(info)
        self.log.info(info)
        if daemon and self.udfs_daemon:
            self.udfs_daemon.wait()
        self.udfs_daemon_pid = self.udfs_daemon.pid

    def start_init(self):
        """
        init udfs, sleep 3 microsecond to wait the command finished.
        """
        cmd = "{0} --config {1} init".format(self.udfs_path, self.config)
        self.udfs_init = self.start_command(cmd)
        time.sleep(3)

    def modify_config(self):
        """
        modify udfs config
        """
        self.udfs_config = os.path.join(self.config, 'config')
        if os.path.isfile(self.udfs_config):
            # modify config file
            self.log.debug("starting modify udfs config")
            with open(self.udfs_config) as target:
                self.udfs_json = json.load(target)
            self.udfs_json['Bootstrap'] = ["/ip4/114.67.37.2/tcp/20515/ipfs/QmctwnuHwE8QzH4yxuAPtM469BiCPK5WuT9KaTK3ArwUHu"]
            self.udfs_json['Datastore']['StorageMax'] = '0MB'
            with open(self.udfs_config, 'w') as target:
                json.dump(self.udfs_json, target, indent=2)
            self.log.debug("end modify udfs config")
        else:
            self.log.error("error get udfs config.Restart init...")
            self.start_init()

    def stop(self):
        """
        kill the udfs daemon
        """
        if self.udfs_daemon_pid:
            self.log.info("stop daemon")
            if self.current_os in ["Windows", "Win32"]:
                self.log.debug("excute taskkill")
                try:
                    os.popen('taskkill.exe /pid:{0} /F'.format(self.udfs_daemon_pid))
                except Exception,e:
                    self.log.error("Kill task error!Exception is {}".format(e))
            elif self.current_os in ["Mac OSX", "Darwin"]:
                try:
                    os.killpg(self.udfs_daemon_pid, signal.SIGTERM)
                except:
                    self.log.error("Kill task error!Exception is {}".format(e))
            elif self.current_os == "Linux":
                try:
                    os.killpg(self.udfs_daemon_pid, signal.SIGTERM)
                except Exception, e:
                    self.log.error("Kill task error!Exception is {}".format(e))
            else:
                self.log.critical("Unknow operating system")
                sys.exit(1)
            # print(self.lock)
            # print(os.path.isfile(self.lock))
            if os.path.isfile(self.lock):
                try:
                    os.remove(self.lock)
                except Exception, e:
                    self.log.error('remove self.lock({0}) failed!'.format(e))


class UdfsHelper():
    """
    download and upload files from Ulord
    """
    def __init__(self, host='127.0.0.1', port='5001'):
        """
        create a connection to the udfs
        :param host: udfs daemon host
        :type host: str
        :param port: udfs daemon port
        :type port: str/int
        """
        self.udfs = Udfs()
        self.udfs_host = host
        self.udfs_port = port
        self.connect = None
        self.log = logging.getLogger("UdfsHelper:")
        self.chunks = {}
        self.objects = None
        self.links = []
        self.downloadpath = os.path.join(ROOTPATH, 'download')

    def update(self, host='127.0.0.1', port='5001'):
        """
        update udfs dameon connection
        :param host: udfs daemon host
        :type host: str
        :param port: udfs daemon port
        :type port: str/int
        """
        self.udfs_host = host
        self.udfs_port = port
        self.connect = None
        self.chunks = {}
        self.objects = None
        self.links = []

    def cat(self, udfshash):
        """
        Retrieves the contents of a file identified by hash.
        :param udfshash: udfs hash
        :type udfshash:str
        :return: str(File contents)
        """
        if not self.connect:
            self.udfs.start(False)
            self.connect = ipfsapi.connect(self.udfs_host, self.udfs_port)
        return self.connect.cat(udfshash)

    def upload_stream(self, stream):
        """
        upload the stream to the ulord
        :param stream:  stream data
        :type stream: file handle
        :return:
        """
        if not self.connect:
            self.udfs.start(False)
            self.connect = ipfsapi.connect(self.udfs_host, self.udfs_port)
        # TODO need fix
        try:
            # py-api doesn't support add stream.But the js-api supports.So sad.Maybe need to use HTTP-api.
            start = time.time()
            # TODO save stream to a file
            file_temp = "{}.txt".format(uuid1())
            if fileHelper.saveFile(file_temp, stream):
                result = self.connect.add(file_temp)
                # del temp file
                try:
                    os.remove(file_temp)
                except Exception, e:
                    self.log.error("del temp file {0} error: {1}".format(file_temp, e))
                end = time.time()
                self.log.info('upload stream cost:{}'.format(end - start))
                return result.get('Hash')
        except Exception, e:
            logging.error("Failed upload.{}".format(e))
            return None

    def upload_file(self, local_file):
        """
        upload the file to the udfs

        :param local_file: a local file path
        :type local_file: str
        :return: Hash or False
        """
        if not self.connect:
            self.udfs.start(False)
            # self.log.error("You need to ")
            self.connect = ipfsapi.connect(self.udfs_host, self.udfs_port)
        try:
            if os.path.isfile(local_file):
                # start = time.time()
                result = self.connect.add(local_file)
                # end = time.time()
                # print('upload {0} ,size is {1}, cost:{2}'.format(local_file, FileHelper.getSize(local_file), (end - start)))
                return result.get('Hash')
            else:
                return False
        except Exception, e:
            # save e in the log
            self.log.error("upload file failed!Exception is {}".format(e))
            return False

    def list(self, filehash):
        """
        list the udfshash chunks

        :param filehash: a udfs hash
        :type filehash: str
        :return: a list chunks of the udfs hash
        """
        if not self.connect:
            self.udfs.start(False)
            self.connect = ipfsapi.connect(self.udfs_host, self.udfs_port)
        try:
            self.objects = self.connect.ls(filehash).get('Objects')
            if self.objects:
                for object in self.objects:
                    if 'Links' in object.keys():
                        for link in object.get('Links'):
                            self.links.append(link)
            else:
                self.links = "test"
        except Exception, e:
            logging.error("ls fail:{}".format(e))

    def downloadfile(self, localfile):
        """
        query the localfile from DB and then download from the udfs

        :param localfile: a file path
        :type localfile: str
        :return: True os False
        """
        if not self.connect:
            self.udfs.start(False)
            self.connect = ipfsapi.connect(self.udfs_host, self.udfs_port)
        # TODO query the file hash from DB
        pass

    def downloadhash(self, filehash, filepath=None, Debug=False):
        """
        download file from the UDFS according to the udfs hash

        :param filehash: file udfs hash
        :type filehash: str
        :param filepath: the path to save the file
        :type filepath: str
        :param Debug: if Debug print the cost time
        :type Debug: bool
        :return: True or False
        """
        if not self.connect:
            self.udfs.start(False)
            self.connect = ipfsapi.connect(self.udfs_host, self.udfs_port)
        try:
            if Debug:
                start = time.time()
            self.connect.get(filehash, filepath=filepath)
            if Debug:
                end = time.time()
                self.log.debug('download {0} cost:{1}'.format(filehash, (end - start)))
                print('download {0} cost:{1}'.format(filehash, (end - start)))
            self.log.info("download {} successfully!".format(filehash))
            return True
        except Exception, e:
            logging.error("download fail:{}".format(e))
            return False

    def resumableDownload(self, filehash, filename=None):
        """
        resumable download

        :param filehash: file UDFS hash
        :type filehash: str
        :param filename: file path to save the file
        :type filename: str
        :return: True or False
        """
        if not self.connect:
            self.udfs.start(False)
            self.connect = ipfsapi.connect(self.udfs_host, self.udfs_port)
        # not thread safely.single thread
        filehash_path = os.path.join(self.downloadpath, filehash)
        tempjson = os.path.join(filehash_path, 'temp.json')
        if not os.path.isfile(tempjson):
            # save chunks result into the temp.json
            self.list(filehash)
            if self.links:
                i = 0
                for link in self.links:
                    if 'Hash' in link.keys():
                        self.chunks.update({
                            i: {
                                'filehash': link.get('Hash'),
                                'success': False
                            }
                        })
                    i += 1
                filehash.saveFile(tempjson, json.dumps(self.chunks))
            else:
                print("no chunks.Error get the {} chunks result".format(filehash))
        # download chunk
        with open(tempjson) as target_file:
            self.chunks = json.load(target_file)
        if self.chunks:
            for chunk, chunk_result in self.chunks.iteritems():
                if not chunk_result.get('success'):
                    chunk_result['success'] = self.downloadhash(chunk_result.get('filehash'),
                                                                filehash_path) or chunk_result.get('success')
                    fileHelper.saveFile(tempjson, json.dumps(self.chunks))
            # merge chunks
            if filename:
                localfile = os.path.join(filehash_path, filename)
            else:
                localfile = os.path.join(filehash_path, filehash)
            with open(localfile, 'wb') as target_file:
                for i in range(len(self.chunks)):
                    chunk = os.path.join(filehash_path, self.chunks.get(str(i)).get('filehash'))
                    with open(chunk, 'rb') as source_file:
                        for line in source_file:
                            target_file.write(line)
                    try:
                        os.remove(chunk)  # delete chunk to save the space
                    except Exception, e:
                        print("{0}:{1} remove failed:{2}".format(chunk, os.path.isfile(chunk), e))
                try:
                    os.remove(tempjson)
                except Exception, e:
                    print("{0}:{1} remove failed:{2}".format(tempjson, os.path.isfile(tempjson), e))


if __name__ == '__main__':
    udfs = Udfs()
    print(udfs.udfs_path)