# coding=utf-8
# @File  : udfs.py
# @Author: PuJi
# @Date  : 2018/4/21 0021
import sys, os, subprocess, platform, json, time, signal, logging, atexit

import ipfsapi

from upapi.src.utils.fileHelper import fileHelper as FileHelper


class Udfs():

    def __init__(self):
        self.log = logging.getLogger("Udfs:")
        # get some paths
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.config = os.path.join(self.root_path, 'config')
        self.lock = os.path.join(self.config, 'repo.lock')
        self.udfs_path = self.get_udfs()
        self.udfs_daemon_pid = self.get_pid()
        if not os.path.isfile(self.config):
            self.start_init()
        if self.udfs_init:
            self.modify_config()
        self.start()
        self.connect = UdfsHelper() # TODO: multi helper to download faster

    def get_pid(self):
        if os.path.isfile(self.lock):
            self.log.debug('get udfs daemon pid')
            with open(self.lock, 'r') as target:
                return json.load(target).get("OwnerPID")
        else:
            self.log.debug("self.lock is {}.It doesn't exist".format(self.lock))
            return None

    def get_udfs(self):
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
        # start external command
        self.log.info("starting command,current command:{}".format(cmd))
        FNULL = open(os.devnull, 'w')
        pl = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=FNULL)
        # self.log.info("end command,result is {}".format(pl.communicate()))
        return pl

    def start(self):
        # start udfs
        cmd = "{0} --config {1} daemon".format(self.udfs_path,self.config)
        self.udfs_daemon = self.start_command(cmd)
        self.udfs_daemon_pid = self.udfs_daemon.pid

    def start_init(self):
        # init udfs
        cmd = "{0} --config {1} init".format(self.udfs_path, self.config)
        self.udfs_init = self.start_command(cmd)
        time.sleep(3)

    def modify_config(self):
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
        # kill the udfs daemon
        if self.udfs_daemon_pid:
            self.log.info("stop daemon")
            print("stop daemon")
            if self.current_os in ["Windows", "Win32"]:
                self.log.debug("excute taskkill")
                os.popen('taskkill.exe /pid:{0} /F'.format(self.udfs_daemon_pid))
            elif self.current_os in ["Mac OSX", "Darwin"]:
                os.killpg(self.udfs_daemon_pid, signal.SIGTERM)
            elif self.current_os == "Linux":
                os.killpg(self.udfs_daemon_pid, signal.SIGTERM)
            else:
                self.log.critical("Unknow operating system")
                sys.exit(1)
            # print(self.lock)
            # print(os.path.isfile(self.lock))
            if os.path.isfile(self.lock):
                try:
                    os.remove(self.lock)
                except Exception, e:
                    self.log.error('remove self.lock({0}) failed!'.format(self.lock))
                    print("remove failed!", e)


class UdfsHelper():
    # download and upload files from Ulord
    def __init__(self, host='127.0.0.1', port='5001'):
        self.udfs_host = host
        self.udfs_port = port
        self.connect = ipfsapi.connect(self.udfs_host, self.udfs_port)
        self.log = logging.getLogger("UdfsHelper:")
        self.chunks = {}
        self.objects = None
        self.links = []
        self.downloadpath = os.path.join(FileHelper.getRootPath(), 'download')

    def update(self, host='127.0.0.1', port='5001'):
        self.udfs_host = host
        self.udfs_port = port
        self.connect = ipfsapi.connect(self.udfs_host, self.udfs_port)
        self.chunks = {}
        self.objects = None
        self.links = []

    def cat(self, udfshash):
        return self.connect.cat(udfshash)

    def upload_stream(self, stream):
        # TODO need fix
        try:
            start = time.time()
            result = self.connect.add(stream)
            end = time.time()
            self.log.info('upload stream cost:{}'.format(end - start))
            return result.get('Hash')
        except Exception, e:
            logging.error("Failed upload.{}".format(e))
            return None

    def upload(self, local_file):
        try:
            start = time.time()
            result = self.connect.add(local_file)
            end = time.time()
            print('upload {0} ,size is {1}, cost:{2}'.format(local_file, FileHelper.getSize(local_file), (end - start)))
            # TODO save filename in DB
            return result.get('Hash')
        except Exception, e:
            # TODO save e in the log
            return None

    def list(self, filehash):
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
        # TODO query the file hash from DB
        pass

    def downloadhash(self, filehash, filepath=None):
        try:
            start = time.time()
            self.connect.get(filehash, filepath=filepath)
            end = time.time()
            print('download {0} cost:{1}'.format(filehash, (end - start)))
            print("download {} successfully!".format(filehash))
            return True
        except Exception, e:
            logging.error("download fail:{}".format(e))
            return False

    def resumableDownload(self, filehash, filename=None):
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
                FileHelper.saveFile(tempjson, json.dumps(self.chunks))
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
                    FileHelper.saveFile(tempjson, json.dumps(self.chunks))
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
                        os.remove(chunk)  # 删除该分片，节约空间
                    except Exception, e:
                        print("{0}:{1} remove failed:{2}".format(chunk, os.path.isfile(chunk), e))
                try:
                    os.remove(tempjson)
                except Exception, e:
                    print("{0}:{1} remove failed:{2}".format(tempjson, os.path.isfile(tempjson), e))


udfs = Udfs()
atexit.register(udfs.stop)


if __name__ == '__main__':
    print(udfs.config)
    print(udfs.udfs_path)
    print udfs.udfs_config
    print(udfs.udfs_daemon_pid)
