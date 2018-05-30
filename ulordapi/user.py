# coding=utf-8
# Copyright (c) 2016-2018 The Ulord Core Developers
# @File  : user.py
# @Author: Ulord_PuJi
# @Date  : 2018/5/18 0018

import inspect, logging, os, time
from uuid import uuid1

import utils, up
from ulordapi.udfs import udfs
from ulordapi.config import config, ulordconfig, webconfig, dbconfig, ROOTPATH
from ulordapi.manage import db, User, Resource, Tag, create
from ulordapi.errcode import _errcodes, return_result


class Developer(up.UlordHelper):
    """
    basic develoer class to execute some functions
    """
    def __init__(self, appkey, secret):
        """
        init the developer. create a udfs helper, a ulord-helper, add a logger

        :param appkey: application key
        :type appkey: str
        :param secret: application secret
        :type secret: str
        """
        up.UlordHelper.__init__(self, appkey, secret)
        utils.Update(ulordconfig,
                     utils._byteify({
                        'ulord_appkey': appkey,
                        'ulord_secret': secret
                        })
                     )
        config.save()
        self.udfs = udfs.UdfsHelper()
        self.ulord = up.UlordHelper()
        if webconfig.get('privkeypath'):
            self.pripath = webconfig.get('privkeypath')
        else:
            self.pripath = os.path.join(ROOTPATH, 'private.pem')
        if webconfig.get('pubkeypath'):
            self.pubpath = webconfig.get('pubkeypath')
        else:
            self.pubpath = os.path.join(ROOTPATH, 'public.pem')
        self.rsahelper = utils.RSAHelper(self.pubpath, self.pripath)

    def get_purearg(self, args):
        """
        check if the arg is encrypted.If encrypted return decrypted arg,else return None.

        :param args: arg need to be checked,
        :type args: str/str list
        :return: decrypted arg or arg(unicode)
        """
        result = None
        try:
            if isinstance(args, list):
                result = []
                for arg in args:
                    temp_arg = self.rsahelper._decrypt(arg)
                    if not isinstance(temp_arg, unicode):
                        temp_arg = temp_arg.decode('utf-8')
                    result.append(temp_arg)
            else:
                result = self.rsahelper._decrypt(args)
                if not isinstance(result, unicode):
                    result = result.decode('utf-8')
        except:
            # todo need to think twice
            try:
                self.log.info("{0} cann't decrypt,using {0}".format(str(args)))
            except:
                self.log.info("args is unicode")
        if result:
            return result
        else:
            return None

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
            utils.Update(config, utils._byteify(args))
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
        """
        download file from ulord.udfses is a udfs list

        :param udfshashs: udfs hashes
        :type udfshashs: list
        :return: udfshash - True/False
        """
        result = {}
        for udfshash in udfshashs:
            # TODO multi threading
            if utils.isUdfsHash(udfshash):
                filehash = self.udfs.downloadhash(udfshash)
                result.update({
                    udfshash: filehash
                })
            else:
                result.update({
                    udfshash: 0 # "not a udfshash"
                })
        return result

    def udfs_upload(self, fileinfos):
        """
        upload file into ulord.fileinfo is a file list

        :param fileinfos: file need to upload to the ulord-platform
        :type fileinfos: list
        :return: dict fileinfo - True/False
        """
        result = {}
        if isinstance(fileinfos, list):
            for fileinfo in fileinfos:
                # TODO multi threading
                if os.path.isfile(fileinfo):
                    filehash = self.udfs.upload_file(fileinfo)
                else:
                    filehash = self.udfs.upload_stream(fileinfo)
                result.update({
                    fileinfo: filehash
                })
        else:
            if os.path.isfile(fileinfos):
                filehash = self.udfs.upload_file(fileinfos)
            else:
                filehash = self.udfs.upload_stream(fileinfos)
            result.update({
                fileinfos: filehash
            })
        return result

    def udfs_cat(self, udfshashs):
        """
        view the udfs hash comment

        :param udfshashs: udfs hashes
        :type udfshashs: list
        :return: dict udfshash - True/False
        """
        result = {}
        for udfshash in udfshashs:
            if utils.isUdfsHash(udfshash):
                file_context = self.udfs.cat(udfshash)
                result.update({
                    udfshash: file_context
                })
            else:
                result.update({
                    udfshash: 0 # "not a udfshash"
                })
        return result

    def start(self):
        """
        start udfs daemon
        """
        # TODO achieve

    def stop(self):
        """
        stop udfs daemon
        """
        # TODO achieve

    # Advanced command
    def request(self, method, url, data=None):
        """
        advanced command. request to the ulord-platform

        :param method: request method,like post,get and so on.
        :type method: str
        :param url: request url
        :type url: str
        :param data: request data
        :type data: dict
        :return: return result.you can query the errcode
        """
        if method.lower() == 'post':
            return self.ulord.post(url=url, data=data)
        if method.lower() == 'get':
            return self.ulord.get(url=url)

    def help(self):
        """
        :return: dict.self method
        """
        # todo create self help
        return inspect.getmembers(self, predicate=inspect.ismethod)


class Senior(Developer):
    """
    Senior programmer to develop his application.
    """
    def __init__(self, appkey, secret):
        """

        :param appkey:application app key, you can get it when you regist from the ulord-platform.
        :type appkey: str
        :param secret: application app secret, you can get it when you regist from the ulord-platform.
        :type secret: str
        """
        Developer.__init__(self, appkey, secret)
        self.log = logging.getLogger("Senior:")
        self.log.info("Senior init")


class Junior(Developer):
    """
    Junior programmer to develop his application.Using default database.
    """
    def __init__(self, appkey, secret):
        """
        init a junior programmer to use functions
        :param appkey: application app key, you can get it when you regist from the ulord-platform.
        :type appkey: str
        :param secret: application app secret, you can get it when you regist from the ulord-platform.
        :type secret: str
        """
        Developer.__init__(self, appkey, secret)
        self.log = logging.getLogger("Junior:")
        self.log.info("Junior init")

    # up functions
    def user_regist(self, username, password, cellphone=None, email=None, wallet=None, pay_password=None, encrypted=False):
        """
        user regist

        :param username: user name
        :type username: str
        :param password: user password
        :type password: str
        :param cellphone: user cellphone.Default is None.
        :type cellphone: str
        :param email: user email.Default is None.
        :type email: str
        :param wallet: user wallet name.Default is username.
        :type wallet: str
        :param pay_password: user wallet password.Default is hash password.
        :type pay_password: str
        :param encrypted: check if the password encrypted
        :type encrypted: bool
        :return: user token
        """
        # encrypt
        if encrypted:
            password = self.get_purearg(password)
        # check arg
        if User.query.filter_by(username=username).first() is not None:
            return _errcodes.get(60000)
        if email and utils.isMail(email):
            return _errcodes.get(60105)
        if cellphone and utils.isCellphone(cellphone):
            return _errcodes.get(60106)

        user = User(username=username)
        user.hash_password(password)
        if pay_password:
            if encrypted:
                pay_password = self.get_purearg(pay_password)
            user.pay_password = pay_password
        else:
            user.pay_password = user.password_hash
        if wallet:
            user.wallet = wallet
        else:
            user.wallet = username
        user.cellphone = cellphone
        user.email = email
        regist_result = self.ulord.regist(user.wallet, user.pay_password)
        if regist_result.get("errcode") != 0:
            return regist_result
        user.token = str(uuid1())
        user.timestamp = int(time.time()) + webconfig.get('token_expired')
        user.id = str(uuid1())
        db.session.add(user)
        db.session.commit()
        return return_result(0, result={"token": user.token})
        # return user.token

    def user_login(self, username, password, encrypted=False):
        """
        user login

        :param username: user name
        :type username: str
        :param password: user password
        :type password: str
        :param encrypted: check if the password is encrypted
        :type encrypted: bool
        :return: user token
        """
        if encrypted:
            password = self.get_purearg(password)
        login_user = User.query.filter_by(username=username).first()
        if not login_user:
            return _errcodes.get(60002)
        if not login_user.verify_password(password):
            return _errcodes.get(60003)
        login_user.token = str(uuid1())
        login_user.timestamp = int(time.time()) + webconfig.get('token_expired')
        db.session.commit()
        return return_result(0, result={"token": login_user.token})
        # return login_user.token

    def user_logout(self, token=None, username=None):
        """
        user logout.Change user's timestamp

        :param token: user token
        :type token: str
        :param username: user name
        :type username: str
        :return: username or errcode.You can query the errcode dict.
        """
        login_user = None
        if token:
            login_user = User.query.filter_by(token=token).first()
            if int(login_user.timestamp) < time.time():
                return _errcodes.get(60104)
        elif username:
            login_user = User.query.filter_by(username=username).first()
        if login_user:
            login_user.timestamp = int(time.time()) - 1
            return return_result(0, result={username:login_user.username})
        else:
            return _errcodes.get(60002)

    def user_activity(self, token=None, username=None):
        """
        activity.App developer send some ulords to the user.

        :param token: user token
        :type token: str
        :param username: user name
        :type username: str
        :return: True or False.
        """
        login_user = None
        if token:
            login_user = User.query.filter_by(token=token).first()
            if int(login_user.timestamp) < time.time():
                return _errcodes.get(60104)
        elif username:
            login_user = User.query.filter_by(username=username).first()
        if login_user:
            credit_result = self.ulord.paytouser(login_user.wallet)
            if credit_result.get('errcode') != 0:
                return credit_result
            else:
                login_user.activity = webconfig.get('amount')
                return return_result(0,result={"amount": webconfig.get('amount')})
        else:
            return _errcodes.get(60002)

    def user_publish(self, title, udfshash, amount, tags, description, usercondition):
        """
        user publish resource

        :param title: resource title
        :type title: str
        :param udfshash: resource uplorded to the UDFS hash
        :type udfshash: str
        :param amount: resource price
        :type amount: float
        :param tags: resource tag
        :type tags: list
        :param description: resource description
        :type description: str
        :param usercondition: a condition which need to query user
        :type usercondition: dict
        :return: errcode.You can query from the errcode.
        """
        # body is a file
        # check udfshash
        if not utils.isUdfsHash(udfshash):
            return _errcodes.get(60107)
        if 'userid' in usercondition:
            userid = usercondition.get('userid')
            current_user = User.query.filter_by(id=userid).first()
        elif 'username' in usercondition:
            username = usercondition.get('username')
            current_user = User.query.filter_by(name=username).first()
        elif 'usertoken' in usercondition:
            token = usercondition.get('usertoken')
            current_user = User.query.filter_by(token=token).first()
        else:
            return return_result(60100)  # missing user info argument
        # save to the localDB
        # change demand:title can be repeatedly.
        # if Resource.query.filter_by(title=title, userid=current_user.id).first() is not None:
        #     # existing title
        #     return _errcodes.get(60007)
        # TODO check balance
        if not isinstance(amount, float):
            try:
                amount = float(amount)
            except:
                amount = 0
        # publish to the ulord-platform
        data = self.ulord.ulord_publish_data
        data['author'] = current_user.wallet
        data['title'] = title
        data['tags'] = tags
        data['udfs_hash'] = udfshash
        data['price'] = amount
        data['pay_password'] = current_user.pay_password
        data['description'] = description
        publish_result = self.ulord.publish(data)
        if publish_result.get('errcode') == 0:
            new_resource = Resource(id=str(uuid1()), title=title, amount=amount, views=0)
            if tags:
                for tag in tags:
                    if Tag.query.filter_by(tagname=tag).first() is None:
                        new_resource.tags.append(Tag(tag))
            new_resource.description = description
            new_resource.body = udfshash
            new_resource.date = int(time.time())
            new_resource.userid = current_user.id
            new_resource.claimID = publish_result.get('result').get('claim_id')
            db.session.add(new_resource)
            db.session.commit()
        #     return new_resource.claimID
        # else:
        #     return publish_result
        return publish_result

    def user_resouce_views(self, title):
        """
        add resource view

        :param title: resource title
        :type title: str
        :return: resource current view
        """
        resources = Resource.query.filter_by(title=title).first()
        resources.views += 1
        db.commit()
        return resources.views

    def user_pay_resources(self, payer, claim_id, password, encrypted=False):
        """
        user pay resource

        :param payer: payer
        :type payer: User
        :param claim_id: resource claim id
        :type claim_id: str
        :param password: payer password
        :type password: str
        :return: errcode.You can query from the errcode.
        """
        if encrypted:
            password = self.get_purearg(password)
        # check password
        if not payer.verify_password(password):
            return return_result(60003)
        return self.ulord.transaction(payer.wallet, claim_id, payer.pay_password)

    def user_pay_ads(self, wallet, claim_id, authername):
        """
        user view ads

        :param wallet: user wallet name
        :type wallet: str
        :param claim_id: resource claim id
        :type claim_id: str
        :param authername: resource auther name
        :type authername: str
        :return: errcode.You can query from the errcode.
        """
        auther = User.query.filter_by(username=authername).first()
        if not auther:
            return return_result(60108)
        return self.ulord.transaction(wallet, claim_id, auther.pay_password, isads=True)

    def user_info_query(self, username=None, token=None):
        """
        user information

        :param username: username.Default is none.
        :type username: str
        :param token: user token.Default is none.
        :type token: str
        :return: dict.User info
        """
        login_user = None
        if token:
            login_user = User.query.filter_by(token=token).first()
            if int(login_user.timestamp) < time.time():
                return return_result(60104)
        elif username:
            login_user = User.query.filter_by(username=username).first()
        if login_user:
            result = {
                'username': login_user.username,
                "cellphone": login_user.cellphone,
                "Email": login_user.email
            }
            return return_result(result=result)
        else:
            return return_result(60002)

    def user_infor_modify(self, username=None, token=None, encrypted=False, password=None, cellphone=None, email=None, new_password=None):
        """
         user information

        :param username: username.Default is none.
        :type username: str
        :param token: user token.Default is none.
        :type token: str
        :param encrypted: if encrypted password.If ture,all password will be decrypted.
        :type encrypted: bool
        :param password: user passowrd to confirm account
        :type password: str
        :param cellphone: user new cellphone
        :type cellphone: str
        :param email: user new email
        ;:type email: str
        :param new_password: user new password
        :type new_password: str
        :return: dict.User info
        """
        login_user = None
        if token:
            login_user = User.query.filter_by(token=token).first()
            if int(login_user.timestamp) < time.time():
                return return_result(60104)
        elif username:
            login_user = User.query.filter_by(username=username).first()
        if login_user:
            if password:
                if encrypted:
                    password = self.get_purearg(password)
                # check password .It's maybe a none.
                if password and login_user.verify_password(password):
                    pass
                else:
                    return _errcodes.get(60003)
            else:
                return return_result(60100)
            if email:
                if utils.isMail(email):
                    login_user.email = email
                else:
                    return return_result(60105)
            if cellphone:
                if utils.isCellphone(cellphone):
                    login_user.cellphone = cellphone
                else:
                    return return_result(60106)
            if new_password:
                if encrypted:
                    new_password = self.get_purearg(new_password)
                if new_password:
                    login_user.hash_password(new_password)
            db.session.commit()
            result = {
                'username': login_user.username,
                "cellphone": login_user.cellphone,
                "Email": login_user.email
            }
            return return_result(result=result)
        else:
            return return_result(60002)

    def create_database(self, path=None):
        """
        create database

        :param path: database path.Warining:It'a a dir
        :type path: str
        :return: True/False
        """
        # check if the database is exited
        if dbconfig.get('IsCreated'):
            self.log.info("DB has created!")
        else:
            self.log.info("Creating DB...")
            if path:
                try:
                    os.stat(path)
                except:
                    os.mkdir(path)
                utils.Update(dbconfig,
                             utils._byteify({
                                 'SQLALCHEMY_DATABASE_URI':'sqlite:///{}'.format(os.path.join(path,'sqlite.db'))
                                })
                             )
                config.save()
            create()
            dbconfig.update({
                'IsCreated': True
            })
            config.save()

    # web command
    def start_web(self):
        """
        start web server
        """
        import webServer
        webServer.start()
        webconfig.update({
            "start": True
        })

    # advanced command
    def query(self, sql):
        """
        advanced command self query

        :param sql: sql sentence
        :type sql: str
        :return: query result
        """
        try:
            result = db.engine.execute(sql)
        except Exception, e:
            self.log.error("Execute sql({0}) failed! Exception is{1}".format(sql, e))
            result = None
        return result


if __name__ == '__main__':
    develop = Developer()
    result = develop.help()
    try:
        import json

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except:
        # print(type(result))
        print(result)