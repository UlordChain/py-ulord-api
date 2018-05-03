# coding=utf-8
# @File  : client.py
# @Author: PuJi
# @Date  : 2018/4/17 0017

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
            pay_password = user.password_hash
        if wallet:
            user.wallet = wallet
        else:
            wallet = username
        user.cellphone = cellphone
        user.email = email
        regist_result = ulord_helper.regist(wallet, pay_password)
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

    def user_publish(self, title, ipfshash, amount, tags, description, userid):
        # body is a file
        current_user =  User.query.filter_by(id=userid).first()
        data = ulord_helper.ulord_publish_data
        data['author'] = current_user.wallet
        data['title'] = title
        data['tag'] = tags
        data['ipfs_hash'] = ipfshash
        data['price'] = amount
        data['pay_password'] = current_user.pay_password
        data['description'] = description
        result = ulord_helper.publish(data)
        return result

    def user_upload(self, fileinfos):
        # upload file into ulord.fileinfo is a file list
        result = {}
        for fileinfo in fileinfos:
            # TODO multi threading
            filehash = ulord_helper.upload(fileinfo)
            result.update({
                fileinfo:filehash
            })
        return return_result(0, reason=result)

    def user_consume(self):
        pass

    def user_query(self):
        pass

    # edit config
    def config_edit(self):
        pass

    def config_show(self):
        pass

    # UDFS command
    def udfs_download(self):
        pass

    def udfs_upload(self):
        pass

    def udfs_cat(self):
        pass

    # Advanced command
    def request(self):
        pass


if __name__ == '__main__':
    client = Client()
    print client.user_regist(username="test6", password="123")