# coding=utf-8
# @File  : udfs.py
# @Author: PuJi
# @Date  : 2018/4/21 0021
import sys, os, subprocess, platform, json, time


class Udfs():
    def __init__(self):
        # get some paths
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.config = os.path.join(self.root_path, 'config')
        self.udfs_path = self.get_ipfs()
        if not os.path.isfile(self.config):
            self.start_init()

    def get_ipfs(self):
        tools = os.path.join(self.root_path, 'tools')
        current_os = platform.system()
        print(current_os)

        if current_os in ["Windows", "Win32"]:
            udfs = os.path.join(tools, 'udfs.exe')
        elif current_os in ["Mac OSX", "Darwin"]:
            udfs = os.path.join(tools, 'udfs')
        elif current_os == "Linux":
            udfs = os.path.join(tools, 'udfs')
        else:
            print("Error:unknow operating system")
            sys.exit(0)
        return udfs

    def start_daemon(self, cmd):
        # start external command
        FNULL = open(os.devnull, 'w')
        pl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=FNULL)
        return pl

    def start_udps(self):
        cmd = "{0} --config {1} daemon".format(self.udfs_path,self.config)
        self.udfs_daemon = self.start_daemon(cmd)

    def start_init(self):
        cmd = "{0} --config {1} init".format(self.udfs_path, self.config)
        self.udfs_init = self.start_daemon(cmd)
        time.sleep(3)

    def modify_config(self):
        self.udfs_config = os.path.join(self.config, 'config')
        if os.path.isfile(self.udfs_config):
            # modify config file
            with open(self.udfs_config) as target:
                self.udfs_json = json.load(target)
            self.udfs_json['Bootstrap'] = ["/ip4/114.67.37.2/tcp/20515/ipfs/QmctwnuHwE8QzH4yxuAPtM469BiCPK5WuT9KaTK3ArwUHu"]
            self.udfs_json['Datastore']['StorageMax'] = '0MB'
            with open(self.udfs_config, 'w') as target:
                for line in json.dumps(self.udfs_json):
                    target.write(line)
        else:
            print(False)

if __name__ == '__main__':
    udfs = Udfs()
    print(udfs.config)
    print(udfs.udfs_path)
    udfs.modify_config()
    print udfs.udfs_config