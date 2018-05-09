# coding=utf-8
# @File  : basic.py
# @Author: PuJi
# @Date  : 2018/5/9 0009

from uuid import uuid1
import inspect, logging, time

import ipfsapi
import os

from ulordapi.src.db.manage import app, db, User, Resource, Tag, Ads, Content
from ulordapi.src.utils.errcode import _errcodes
from ulordapi.src.utils.encryption import rsahelper
from ulordapi.src.utils.Checker import checker
from ulordapi.src.utils import update, ListToDict
from ulordapi.src.ulordpaltform.up import ulord_helper
from ulordapi.src.udfs.udfs import udfshelper
from ulordapi import webconfig, config


class Commands(object):
    # developer has to init a client to call command
    def __init__(self):
        # init base config and udfs
        self.log = logging.getLogger("Basic:")
        self.log.info("Basic")

    def get_purearg(self, arg):
        # check if the arg is encrypted.If encrypted return decrypted arg,else return arg.
        result = None
        try:
            result = rsahelper.decrypt(rsahelper.privkey, arg)
        except:
            self.log.info("{0} cann't decrypt,using {0}".format(arg))
        if result:
            return result
        else:
            return arg

    # basic command
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
            return _errcodes.get(60000)
        if email and checker.isMail(email):
            return _errcodes.get(60105)
        if cellphone and checker.isCellphone(cellphone):
            return _errcodes.get(60106)

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
        user.timestamp = int(time.time()) + webconfig.get('token_expired')
        user.id = str(uuid1())
        db.session.add(user)
        db.session.commit()
        # return return_result(0, result={"token": user.token})
        return user.token

    def user_login(self, username, password, *encryption):
        if encryption:
            if encryption[0]:
                username = self.get_purearg(username)
            if encryption[1]:
                password = self.get_purearg(password)
        login_user = User.query.filter_by(username=username).first()
        if not login_user:
            return _errcodes.get(60002)
        if not login_user.verify_password(password):
            return _errcodes.get(60003)
        login_user.token = str(uuid1())
        login_user.timestamp = int(time.time()) + webconfig.get('token_expired')
        db.session.commit()
        # return return_result(0, result={"token": login_user.token})
        return login_user.token

    def user_logout(self, token=None, username=None):
        # change user's timestamp
        login_user = None
        if token:
            login_user = User.query.filter_by(token=token).first()
            if int(login_user.timestamp) < time.time():
                return _errcodes.get(60104)
        elif username:
            login_user = User.query.filter_by(username=username).first()
        if login_user:
            login_user.timestamp = int(time.time()) - 1
            return login_user.username
        else:
            return _errcodes.get(60002)

    def user_publish(self, title, udfshash, amount, tags, description, **usercondition):
        # body is a file
        # check udfshash
        if not checker.isUdfsHash(udfshash):
            return _errcodes.get(60107)
        if 'userid' in usercondition:
            userid = usercondition.get('userid')
            current_user =  User.query.filter_by(id=userid).first()
        elif 'username' in usercondition:
            username = usercondition.get('username')
            current_user = User.query.filter_by(name=username).first()
        elif 'usertoken' in usercondition:
            token = usercondition.get('token')
            current_user = User.query.filter_by(token=token).first()
        else:
            return _errcodes.get(60100) # missing user info argument
        # save to the localDB
        if Resource.query.filter_by(title=title, userid=current_user.id).first() is not None:
            # existing title
            return _errcodes.get(60007)
        #TODO check balance

        # publish to the ulord-platform
        data = ulord_helper.ulord_publish_data
        data['author'] = current_user.wallet
        data['title'] = title
        data['tag'] = tags
        data['ipfs_hash'] = udfshash
        data['price'] = amount
        data['pay_password'] = current_user.pay_password
        data['description'] = description
        publish_result = ulord_helper.publish(data)
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

    def user_allresource(self, page=1, num=10):
        return ulord_helper.queryblog(page, num)

    def user_isbought(self, wallet, claim_ids):
        # TODO maybe need to check claim_id
        return ulord_helper.checkisbought(wallet, claim_ids)

    def user_resouce_views(self, dbID):
        return ulord_helper.addviews(dbID)

    def user_pay_resources(self, payer, claim_id, pay_password):
        return ulord_helper.transaction(payer, claim_id, pay_password)

    def user_pay_ads(self, wallet, claim_id, pay_password):
        return ulord_helper.transaction(wallet, claim_id, pay_password, True)

    # edit config


    # UDFS command
    def udfs_download(self, udfshashs):
        # download file from ulord.udfses is a udfs list
        result = {}
        for udfshash in udfshashs:
            # TODO multi threading
            if checker.isUdfsHash(udfshash):
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

    # Advanced command
    def request(self, method, url, data=None):
        if method == 'post':
            return ulord_helper.post(url=url, data=data)
        if method == 'get':
            return ulord_helper.get(url=url)

    def query(self, sql):
        return db.engine.execute(sql)


commands = Commands()