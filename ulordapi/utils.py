# coding=utf-8
# Copyright (c) 2016-2018 The Ulord Core Developers
# @File  : utils.py
# @Author: Ulord_PuJi
# @Date  : 2018/5/18 0018
# @Description: project import first.Alone.

import re, os, hashlib, base64, logging, json, codecs, collections

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random


RANDOM_GENERATOR=Random.new().read


def isCellphone(number):
    """
    check if a cellphone

    :param number: cellphone
    :type number: str
    :return: True of False
    """
    if re.compile(r'[1][^1269]\d{9}').match(number):
        return True
    else:
        return False


def isMail(mail):
    """
    check if a mail

    :param mail: mail
    :type mail: str
    :return: True of False
    """
    if re.compile(r'[^\._][\w\._-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$').match(mail):
        return True
    else:
        return False


def isUdfsHash(udfshash):
    """
    check the string if a udfs hash
    simple check, TODO advanced check

    :param udfshash: a string
    :type udfshash: str
    :return: True or False
    """
    if isinstance(udfshash, unicode):
        udfshash = udfshash.encode('utf-8')
    if len(udfshash) == 46 and udfshash.startswith('Qm'):
        return True
    else:
        return False


def generateMD5(value):
    """
    generate value's md5
    :param value: need to encrypt
    :type value: str
    :return: value's md5 or ""
    """
    if isinstance(value, str):
        m = hashlib.md5()
        m.update(value)
        return m.hexdigest()
    else:
        return ""


class RSAHelper(object):
    """
    rsa helper.Create private key and public key.
    """
    def __init__(self, public_path, private_path):
        """
        Init a rsa helper.If is not a file will generate them.

        :param public_path: public key path.
        :type public_path: str
        :param private_path: private key path
        :type private_path: str
        """
        self._pubkeypath=public_path
        self._privkeypath = private_path
        # check the dir
        if os.path.isfile(self._pubkeypath):
            with open(self._pubkeypath) as publickfile:
                p = publickfile.read()
                self.pubkeybytes = p
                self.pubkey = RSA.import_key(p)
            with open(self._privkeypath) as privatefile:
                p = privatefile.read()
                self.privkeybytes = p
                self.privkey = RSA.import_key(p)
        else:
            self.generate()
            self.load()
        # update public pem path and private pem path

    def generate(self):
        """
        generate public key and private key
        """
        self.key = RSA.generate(1024, Random.new().read)
        self.privkeybytes = self.key.export_key()
        with open(self._privkeypath, 'wb') as prifile:
            prifile.write(self.privkeybytes)

        self.pubkeybytes = self.key.publickey().export_key()
        with open(self._pubkeypath, 'wb') as pubfile:
            pubfile.write(self.pubkeybytes)

    def load(self):
        """
        read key from the path
        """
        with open(self._pubkeypath) as publickfile:
            p = publickfile.read()
            self.pubkey = RSA.import_key(p)
        with open(self._privkeypath) as privatefile:
            p = privatefile.read()
            self.privkey = RSA.import_key(p)

    def _encry(self, comment):
        """
        encrypt comment

        :param comment: information
        :type comment: str
        :return: encrypted information
        """
        pass

    def encry(self, pubkey, comment):
        # cipher = PKCS1_v1_5.new(pubkey)
        # return (cipher.decrypt(base64.b64decode(comment), RANDOM_GENERATOR))
        pass

    def _decrypt(self, message):
        """
        decrypt message

        :param message: need to be decrypted
        :type message: str
        :return: decrypted message
        """
        cipher = PKCS1_v1_5.new(self.privkey)
        return (cipher.decrypt(base64.b64decode(message), RANDOM_GENERATOR))

    def decrypt(self, prikey, message):
        """
        using private key to decrypt message

        :param prikey: private key
        :type prikey: str
        :param message: need to be decrypted
        :type message: str
        :return: decrypted message
        """
        cipher = PKCS1_v1_5.new(prikey)
        return (cipher.decrypt(base64.b64decode(message), RANDOM_GENERATOR))


class FileHelper():
    """
    file helper to operate the files
    """
    def __init__(self):
        """
        init a file helper.Add a logger.
        """
        self.log = logging.getLogger("FileHelper")

    def getSize(self, filename):
        """
        get file size

        :param filename: a file path
        :type filename: str
        :return: file size
        """
        fsize = os.path.getsize(filename)
        return fsize

    def getType(self, filename):
        """
        get file type

        :param filename: a file path
        :type filename: str
        :return: file type
        """
        # TODO get file type from file header
        if '.' in filename:
            return filename.split('.')[-1]
        else:
            return 'NoType'

    def getPureName(self, filename):
        """
        get file name.Doesn't contain type.

        :param filename: a file path
        :type filename: str
        :return: file name
        """
        if '.' in filename:
            filename = filename.split('.')[0]
        if '/' in filename:
            return filename.split('/')[-1]
        elif '\\' in filename:
            return filename.split('\\')[-1]
        else:
            return filename

    def getName(self, filename):
        """
        get file name,including type

        :param filename: a file path
        :type filename: str
        :return: file name
        """
        return os.path.split(filename)[-1]

    def changeName(self, originalname, newname):
        """
        change file name from a hash to filename

        :param originalname: a file path, old file name.
        :type originalname: str
        :param newname: a file path, new file name.
        :type newname: str
        :return: True or False
        """
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
        """
        save source into a filepath. Create path if dir is not existed.

        :param filepath: a file path
        :type filepath: str
        :param source: message
        :type source: str
        :return: True or False
        """
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
        """
        merge chunks into a file.Used for the multi-threading download

        :param filepath: a file path.Final file.
        :type filepath: str
        :param chunks: chunk path list
        :type chunks: list
        :return: True or False
        """
        try:
            with open(filepath, 'wb') as target_file:
                for chunk in chunks:
                    with open(chunk, 'rb') as source_file:
                        for line in source_file:
                            target_file.write(line)
                    try:
                        os.remove(chunk)  # delete chunk,save space
                    except Exception, e:
                        self.log.error("{0}:{1} remove failed:{2}".format(chunk, os.path.isfile(chunk), e))
            return True
        except Exception,e:
            self.log.error("Error mergeFile:{}".format(e))
            return False

    def readFile(self, filepath):
        """
        read file comment

        :param filepath: a file path
        :type filepath: str
        :return: file comment
        """
        result = None
        try:
            with open(filepath, 'rb') as target_file:
                result = target_file
        except Exception, e:
            self.log.error("Error: read file{0}:{1}".format(filepath, e))
        return result

    def getRootPath(self):
        """
        get project root path
        :return: project root path
        """
        return os.path.split(os.getcwd())[0]


fileHelper = FileHelper()


def _byteify(data, ignore_dicts=False):
    """
    encode json to utf-8

    :param data: json
    :type data: dict
    :param ignore_dicts: if ignore sub-dict
    :type ignore_dicts: bool
    :return: encoded json(utf-8)
    """
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data


def json_load_byteified( file_handle):
    """
    encode a json file handle
    :param file_handle: a json file handle
    :type file_handle: handle
    :return: encoded json(utf-8)
    """
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )


def Update(d, u):
    """
    update dict u to dict d
    :param d: base dict
    :type d: dict
    :param u: need to update
    :type u: dict
    :return: dict d which updates d
    """
    for k, v in u.iteritems():
        if isinstance(d.get(k, None), collections.Mapping) and isinstance(v, collections.Mapping):
            d[k] = Update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def ListToDict(args):
    """
    change a list to dict

    :param args: a list
    :type args: list
    :return: dict

    .. code-block:: python

            >>> a = [1,2,3,4]
            >>> print(ListToDict(a))
            {1: {2: {3: 4}}}

    """
    if not isinstance(args, list):
        return None
    if len(args) == 1:
        return args[0]
    else:
        return {
            args[0]:ListToDict(args[1:])
        }


def require(required, tag):
    """
    a decorator function.current function need required function.Tag is a marker which mark the required function is running.

    :param required: required function
    :type required: function
    :param tag: mark the required function if has been running.
    :type tag: bool
    :return: decorator
    """
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
    while True:
        cellphone = raw_input("cellphone:")
        print isCellphone(cellphone)
        mail = raw_input("email:")
        print isMail(mail)

