# coding=utf-8
# @File  : fileHelper.py
# @Author: PuJi
# @Date  : 2018/4/26 0026

import os, codecs, logging


class FileHelper():
    # file helper to operate the files
    def __init__(self):
        self.log = logging.getLogger("FileHelper")

    def getSize(self, filename):
        # get file size
        fsize = os.path.getsize(filename)
        return fsize

    def getType(self, filename):
        # get file type
        # TODO get file type from file header
        if '.' in filename:
            return filename.split('.')[-1]
        else:
            return 'NoType'

    def getPureName(self, filename):
        # get file name
        if '.' in filename:
            filename = filename.split('.')[0]
        if '/' in filename:
            return filename.split('/')[-1]
        elif '\\' in filename:
            return filename.split('\\')[-1]
        else:
            return filename

    def getName(self, filename):
        return os.path.split(filename)[-1]

    def changeName(self, originalname, newname):
        # change file name from a hash to filename
        if os.path.isfile(newname):
            self.log.error("Error: File {} has exited!".format(newname))
            return False
        if os.path.isfile(originalname):
            file_path, original_short_name = os.path.split(originalname)
            newname = os.path.join(file_path, newname)
            if os.path.isfile(newname):
                self.log.error("Error: File {} has exited!".format(newname))
                return False
            os.rename(originalname, newname)
            return True
        else:
            print("Error: File {} doesn't exist!".format(originalname))
            return False

    def saveFile(self, filepath, source):
        # save source into a filepath
        dirpath = os.path.split(filepath)[0]
        if os.path.isdir(dirpath):
            pass
        else:
            os.makedirs(dirpath)
        try:
            with codecs.open(filepath, 'wb', encoding='utf-8') as target_file:
                for line in source:
                    target_file.write(line)
                return True
        except Exception, e:
            self.log.error("saveFile error:{}".format(e))
            return False

    def mergeFile(self, filepath, chunks):
        # merge chunks into a file
        try:
            with open(filepath, 'wb') as target_file:
                for chunk in chunks:
                    with open(chunk, 'rb') as source_file:
                        for line in source_file:
                            target_file.write(line)
                    try:
                        os.remove(chunk)  # 删除该分片，节约空间
                    except Exception, e:
                        self.log.error("{0}:{1} remove failed:{2}".format(chunk, os.path.isfile(chunk), e))
            return True
        except Exception,e:
            self.log.error("Error mergeFile:{}".format(e))
            return False

    def readFile(self, filepath):
        # read file comment
        result = None
        try:
            with open(filepath, 'rb') as target_file:
                result = target_file
        except Exception, e:
            self.log.error("Error: read file{0}:{1}".format(filepath, e))
        return result

    def getRootPath(self):
        # get project root path
        return os.path.split(os.getcwd())[0]

    # def atomicWrite(self, dest, content, mode="w"):
    #     try:
    #         with open(dest+"-tmpnew", mode) as f:
    #             f.write(content)
    #             f.flush()
    #             os.fsync(f.fileno())

fileHelper = FileHelper()


if __name__ == '__main__':
    # print (getPureName('E:\ipfs\go-ipfs\ipfs.exe'))
    # print(getSize('E:\ipfs\go-ipfs\ipfs.exe'))
    # changeName(r'E:\ulord\app_server\sasas', 'testchange')
    print (fileHelper.getRootPath())