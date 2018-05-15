# coding=utf-8
# @File  : user2.py
# @Author: PuJi
# @Date  : 2018/5/9 0009

import logging,time
from uuid import uuid1

from user import Developer
from ulordapi.src.db.manage import create,db, User,Tag,Resource
from ulordapi import config, dbconfig, webconfig, ulordconfig
from ulordapi.src.utils.encryption import rsahelper
from ulordapi.src.utils.errcode import _errcodes
from ulordapi.src.utils.Checker import checker
from ulordapi.src.ulordpaltform.up import ulord_helper
from ulordapi.src.daemon import webServer


class Developer2(Developer):

    # using database
    # def __init__(self, username, password):
    #     ulordconfig.update({
    #         'username':username,
    #         'password':password,
    #         'ulord_head':{
    #             'appkey':self.get_appkey(username, password)
    #         }
    #     })
    #     self.log = logging.getLogger("Developer2:")
    #     self.log.info("Developer2 init")
    def __init__(self, appkey, secert):
        ulordconfig.update({
            'ulord_appkey':appkey,
            'ulord_secert':secert
        })
        config.save()
        self.log = logging.getLogger("Developer2:")
        self.log.info("Developer2 init")

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

    # up functions
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
            current_user = User.query.filter_by(id=userid).first()
        elif 'username' in usercondition:
            username = usercondition.get('username')
            current_user = User.query.filter_by(name=username).first()
        elif 'usertoken' in usercondition:
            token = usercondition.get('token')
            current_user = User.query.filter_by(token=token).first()
        else:
            return _errcodes.get(60100)  # missing user info argument
        # save to the localDB
        if Resource.query.filter_by(title=title, userid=current_user.id).first() is not None:
            # existing title
            return _errcodes.get(60007)
        # TODO check balance

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

    def user_resouce_purchases(self, dbID):
        return ulord_helper.addpurchases(dbID)

    def user_resouce_views(self, title):
        resources = Resource.query.filter_by(title=title)
        resources.views += 1
        db.commit()
        return resources.views

    def user_pay_resources(self, payer, claim_id, pay_password):
        return ulord_helper.transaction(payer, claim_id, pay_password)

    def user_pay_ads(self, wallet, claim_id, pay_password):
        return ulord_helper.transaction(wallet, claim_id, pay_password, True)

    def create_database(self):
        # check if the database is exited
        if dbconfig.get('IsCreated'):
            self.log.info("DB has created!")
        else:
            self.log.info("Creating DB...")
            create()
            dbconfig.update({
                'IsCreated': True
            })
            config.save()

    # web command
    def start_web(self):
        webServer.start()
        webconfig.update({
            "start": True
        })

    # advanced command
    def query(self, sql):
        try:
            result = db.engine.execute(sql)
        except Exception, e:
            self.log.error("Execute sql({0}) failed! Exception is{1}".format(sql, e))
            result = None
        return result


if __name__ == '__main__':
    # user = Developer2(ulordconfig.get('username'),ulordconfig.get('password'))
    if ulordconfig.get('ulord_head'):
        user = Developer2(ulordconfig.get('ulord_appkey'), ulordconfig.get('ulord_secert'))
        user.create_database()
    else:
        print("Failed! Doesn't have appkey")
