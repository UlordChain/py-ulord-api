# coding=utf-8
# @File  : client.py
# @Author: PuJi
# @Date  : 2018/4/17 0017

import pprint, sys, os
path = os.path.split(os.getcwd())[0]
sys.path.append(path)

from uuid import uuid1
import inspect, logging, time

import ipfsapi

from upapi.src.db.manage import app, db, User, Resource, Billing, Tag, Ads, Content
from upapi.src.utils.errcode import return_result
from upapi.src.utils.encryption import rsahelper
from upapi.src.utils.Checker import checker
from upapi.src.ulordpaltform.up import ulord_helper
from upapi.config import baseconfig


class Client(object):
    # developer has to init a client to call command
    def __init__(self):
        # init base config and udfs
        self.log = logging.getLogger("Client:")
        self.log.info("init client")

    def get_purearg(self, arg):
        result = None
        try:
            result = rsahelper.decrypt(rsahelper.privkey, arg)
        except:
            self.log.info("{0} cann't decrypt,using {0}".format(arg))
        if result:
            return result
        else:
            return arg

    # user command
    def user_regist(self, username, password, cellphone=None, email=None, wallet=None, pay_password=None, *encryption):
        # encrypt
        if encryption:
            if encryption[0]:
                username = self.get_purearg(username)
            if encryption[1]:
                password = self.get_purearg(password)
            if cellphone and encryption[2]:
                cellphone = self.get_purearg(cellphone)
            if email and encryption[3]:
                email = self.get_purearg(email)
            if wallet and encryption[4]:
                wallet = self.get_purearg(wallet)
            if pay_password and encryption[5]:
                pay_password = self.get_purearg(pay_password)
        # check arg
        if User.query.filter_by(username=username).first() is not None:
            return return_result(60000)
        if email and checker.isMail(email):
            return return_result(60105)
        if cellphone and checker.isCellphone(cellphone):
            return return_result(60106)

        user = User(username=username)
        user.hash_password(password)
        if pay_password:
            user.pay_password = pay_password
        else:
            user.pay_password = user.password_hash
        if wallet:
            user.wallet = wallet
        else:
            user.wallet = username
        user.cellphone = cellphone
        user.email = email
        regist_result = ulord_helper.regist(user.wallet, user.pay_password)
        if regist_result.get("errcode") != 0:
            return regist_result
        user.token = str(uuid1())
        user.timestamp = int(time.time()) + baseconfig.token_expired
        user.id = str(uuid1())
        db.session.add(user)
        db.session.commit()
        return return_result(0, reason={"token": user.token})

    def user_login(self, username, password, *encryption):
        if encryption:
            if encryption[0]:
                username = self.get_purearg(username)
            if encryption[1]:
                password = self.get_purearg(password)
        login_user = User.query.filter_by(username=username).first()
        if not login_user:
            return return_result(60002)
        if not login_user.verify_password(password):
            return return_result(60003)
        login_user.token = str(uuid1())
        login_user.timestamp = int(time.time()) + baseconfig.token_expired
        db.session.commit()
        return return_result(0, reason={"token": login_user.token})

    def user_logout(self, token=None, username=None):
        # change user's timestamp
        login_user = None
        if token:
            login_user = User.query.filter_by(token=token).first()
            if int(login_user.timestamp) < time.time():
                return return_result(60104)
        elif username:
            login_user = User.query.filter_by(username=username).first()
        if login_user:
            login_user.timestamp = int(time.time()) - 1
            return return_result(0, reason={'username':login_user.username})
        else:
            return return_result(60002)

    def user_publish(self, title, udfshash, amount, tags, description, userid):
        # body is a file
        # check udfshash
        if len(udfshash) != 46 or (not udfshash.startwith('Qm')):
            return return_result(60107) # TODO need other check
        current_user =  User.query.filter_by(id=userid).first()
        data = ulord_helper.ulord_publish_data
        data['author'] = current_user.wallet
        data['title'] = title
        data['tag'] = tags
        data['ipfs_hash'] = udfshash
        data['price'] = amount
        data['pay_password'] = current_user.pay_password
        data['description'] = description
        result = ulord_helper.publish(data)
        return result

    def user_consume(self):
        pass

    def user_query(self):
        pass

    # edit config
    def config_edit(self, **kwargs):
        baseconfig.__dict__.update(kwargs)
        # TODO write to the config file

    def config_show(self):
        return return_result(0, reason={
            'config': baseconfig.__dict__
        })

    # UDFS command
    def udfs_download(self, udfses):
        # download file from ulord.udfses is a udfs list
        result = {}
        for udfs in udfses:
            # TODO multi threading
            filehash = ulord_helper.upload(udfs)
            result.update({
                udfs: filehash
            })
        return return_result(0, reason=result)

    def udfs_upload(self, fileinfos):
        # upload file into ulord.fileinfo is a file list
        result = {}
        for fileinfo in fileinfos:
            # TODO multi threading
            filehash = ulord_helper.upload(fileinfo)
            result.update({
                fileinfo: filehash
            })
        return return_result(0, reason=result)

    def udfs_cat(self):
        pass

    # Advanced command
    def request(self, method, url, data=None):
        if method == 'post':
            return ulord_helper.post(url=url, data=data)
        if method == 'get':
            return ulord_helper.get(url=url)


if __name__ == '__main__':
    log_file_path = "debug.log"
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)-8s %(name)s %(message)s',stream=open(log_file_path, "a"))
    client = Client()

    pprint.pprint(client.config_show().get('reason'))
    # print client.user_regist(username="test7", password="123")