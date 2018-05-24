# coding=utf-8
# Copyright (c) 2016-2018 The Ulord Core Developers
# @File  : up.py
# @Author: Ulord_PuJi
# @Date  : 2018/5/18 0018
import logging, copy, time

import requests

import utils
from config import ulordconfig, config, webconfig
from errcode import return_result


class UlordHelper(object):
    """
    a helper to request the ulord paltform
    """
    def __init__(self, appkey=None, ulord_secret=None):
        """
        using appkey and secret to init the helper

        :param appkey: registing from the ulord-platfrom will create application
        :type appkey: str
        :param ulord_secret: registing from the ulord-platfrom will create secret
        :type ulord_secret: str
        """
        self.log = logging.getLogger("UlordHelper:")
        # base URL
        self.ulord_url = ulordconfig.get('ulord_url')
        # self.ulord_head = ulordconfig.get('ulord_head')
        # if not self.ulord_head:
        #     self.log.error("cann't find the request head! Exit...")
        #     exit(1)
        if appkey and ulord_secret:
            self.appkey = appkey
            self.ulord_secret = ulord_secret
        else:
            self.appkey = ulordconfig.get('ulord_appkey')
            self.ulord_secret = ulordconfig.get('ulord_secret')
        self.curtime = ulordconfig.get('ulord_curtime')
        # regist URL
        self.ulord_createwallet = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_createwallet') # ulord regist webURL
        self.ulord_paytouser = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_paytouser') # ulord transfer webURL
        # publish URL
        self.ulord_publish = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_publish')  # ulord publish webURL
        self.ulord_publish_data =  {
            "author": "justin",
            "title": "第一篇技术博客",
            "tags": ["blockchain", "IPFS"],
            "udfs_hash": "QmVcVaHhMeWNNetSLTZArmqaHMpu5ycqntx7mFZaci63VF",
            "price": 0.1,
            "content_type": ".txt",
            "pay_password": "123",
            "description": "这是使用IPFS和区块链生成的第一篇博客的描述信息"
        }  # ulord publish data
        # query URL
        self.ulord_queryblog = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_queryblog') # query blog list webURL
        self.ulord_checkbought = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_checkbought') # query if the blog has bought
        self.ulord_transaction = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_transaction')  # ulord transaction webURL

        self.ulord_querybalance = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_querybalance')  # qurey balance webURL
        self.ulord_userbought = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_userbought') # query the blog that user has bought
        self.ulord_userpublished = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_userpublished') # query the blog that user has published
        self.ulord_in = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_in') # query income billings
        self.ulord_out = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_out') # query outcome billings
        self.ulord_billings = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_billings') # query the user's billings
        self.ulord_billings_detail = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_billings_detail') # query the detail billings
        self.ulord_published_num = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_publish_num') # query the number of the blog that author has published.
        self.ulord_view = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_view') # add blog's view
        # TODO ulord other URL

    def calculate_sign(self, dt=None):
        """
        encrypt the request data according to the secret

        :param dt: data need to be encrypted, Default is None
        :type dt: dict
        :return: Usign
        """
        # deepcopy dt
        datas = copy.deepcopy(dt)
        # sign request data
        if not datas:
            datas = ""
        result = ''
        for index in sorted(datas):
            if isinstance(datas[index], list):
                # if data is list need to change a string
                temp = ''
                for data in datas[index]:
                    if isinstance(data, bool):
                        if data:
                            data='true'
                        else:
                            data='false'
                    else:
                        data = str(data)
                    temp += data
                datas[index] = temp
            if isinstance(datas[index], bool):
                if datas[index]:
                    datas[index]='true'
                else:
                    datas[index]='false'
            result = result + str(index) + str(datas[index])
        del datas
        if (self.curtime + (5 * 60 - 1)) < int(time.time()):
            self.curtime = int(time.time())
            ulordconfig.update({
                'ulord_curtime':self.curtime
            })
        USign = self.appkey + result + self.ulord_secret + str(self.curtime)

        self.USign = utils.generateMD5(USign).upper()
        ulordconfig.update({
            'ulord_head':{
                'U-AppKey':self.appkey,
                'U-CurTime':str(self.curtime),
                'U-Sign':self.USign
            }
        })
        config.save()
        self.ulord_head = ulordconfig.get('ulord_head')
        return self.USign

    def post(self, url, data):
        """
        post to the ulord-platform

        :param url: request's url
        :type url: str
        :param data: post data
        :type data: dict
        :return: return result.you can query the errcode
        """
        self.log.debug(url)
        self.log.debug(data)

        # deal with unicode and utf-8
        from utils import _byteify
        data = _byteify(data=data)

        # calculate  U-Sign
        self.calculate_sign(data)
        # self.ulord_head = ulordconfig.get('ulord_head')
        try:
            r = requests.post(url=url, json=data, headers=self.ulord_head)
        except Exception, e:
            self.log.error("Failed request from the ulord-platform: {}".format(e))
            return return_result(50000)
        self.log.debug(r.status_code)
        if r.status_code == requests.codes.ok:
            self.log.debug(r.json())
            return r.json()
        else:
            return return_result(60400)

    def get(self, url):
        """
        get from the ulord-platform

        :param url: request's url
        :type url: str
        :return: return result.You can query the errcode.
        """
        self.calculate_sign()
        self.ulord_head = ulordconfig.get('ulord_head')
        try:
            r = requests.get(url=url, headers=self.ulord_head)
        except Exception, e:
            self.log.error("Failed request from the ulord-platform: {}".format(e))
            return return_result(50000)
        self.log.debug(url)
        self.log.debug(r.status_code)
        if (r.status_code == requests.codes.ok):
            self.log.debug(r.json())
            return r.json()
        else:
            return return_result(50000)

    def regist(self, username, password):
        """
        regist wallet address from the ulord platform

        :param username: wallet name
        :type username: str
        :param password: wallet password
        :type password: str
        :return: errcode.You can query from the errcode dict
        """
        data = {
            "username": username,
            "pay_password": password
        }
        return self.post(self.ulord_createwallet, data)

    def publish(self, data):
        """
        publish data to the ulord platform

        :param data: data needed to be published
        :type data: dict
        :return: errcode.You can query from the errcode dict.
        """
        return self.post(self.ulord_publish, data)

    def transaction(self, payer, claim_id, pay_password, isads=False):
        """
        record the transaction to the ulord platform

        :param payer: payer wallet name
        :type payer: str
        :param claim_id: resource claim id
        :type claim_id: str
        :param pay_password: payer wallet password
        :type pay_password: str
        :param isads: check the resource if a Ad.
        :type isads: bool
        :return: errcode.You can query from the errcode dict.
        """

        data = {
            'customer': payer,
            'claim_id': claim_id
        }
        if isads:
            data.update({
                'author_pay_password': pay_password
            })
        else:
            data.update({
                'customer_pay_password': pay_password
            })
        return self.post(self.ulord_transaction, data)

    def paytouser(self, username):
        """
        activity send some ulords to the user

        :param username: user wallet name
        :type username: str
        :return: errcode.You can query from the errcode dict.
        """
        if webconfig.get('activity'):
            data = {
                'is_developer': True,
                'recv_user': username,
                'amount': webconfig.get('amount')
            }
            return self.post(self.ulord_paytouser, data)
        else:
            return return_result(60300)

    def queryblog(self, page=1, num=10):
        """
        query the blog list from the ulord platform.method is get

        :param page: which page do you want to view?Default is 1.
        :type page: int
        :param num: how many pieces of datas in one page?.Default is 10.
        :type num: int
        :return: errcode.You can query from the errcode dict.
        """
        temp_url = self.ulord_queryblog + "/{0}/{1}".format(page, num)
        return self.get(temp_url)

    def querybalance(self, payer, pay_password):
        """
        query the personal balance from the ulord platform

        :param payer: payer wallet name
        :type payer: str
        :param pay_password: payer wallet password
        :type pay_password: str
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'username': payer,
            'pay_password':pay_password
        }
        return self.post(self.ulord_querybalance, data)

    def checkisbought(self, payer, claim_ids):
        """
        query the personal balance from the ulord platform

        :param payer: payer wallet name
        :type payer: str
        :param claim_ids: resource claim id
        :type claim_ids: list
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'customer': payer,
            'claim_ids': claim_ids
        }
        return self.post(self.ulord_checkbought, data)

    def queryuserpublished(self, wallet_username, page=1, num=10, category=2):
        """
        query user published from ulort platform

        :param wallet_username: current user wallet name
        :type wallet_username: str
        :param page: which page of result do you want to view?Default is 1.
        :type page: int
        :param num: how many pieces of data of result do you want to view?Default is 10.
        :type num: int
        :param category: 0-resource,1-ads,2-all
        :type category: todo need to be thinking
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'author': wallet_username,
        }
        if category != 2:
            data.update({
                'category':category
            })
        temp_url = self.ulord_userpublished + "/{0}/{1}".format(page, num)
        return self.post(temp_url, data)

    def queryuserbought(self, wallet_username, page=1, num=10, category=2):
        """
        query user published from ulort platform

        :param wallet_username: current user wallet name
        :type wallet_username: str
        :param page: which page of result do you want to view?Default is 1.
        :type page: int
        :param num: how many pieces of data of result do you want to view?Default is 10.
        :type num: int
        :param category: 0-resource,1-ads,2-all
        :type category: todo need to be thinking
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'customer': wallet_username,
        }
        if category != 2:
            data.update({
                'category':category
            })
        temp_url = self.ulord_userbought + "/{0}/{1}".format(page, num)
        return self.post(temp_url, data)

    def queryincomebillings(self, author, page=1, num=10):
        """
        get billings info

        :param author: current user wallet name
        :type author: str
        :param page: which page of result do you want to view?Default is 1.
        :type page: int
        :param num: how many pieces of data of result do you want to view?Default is 10.
        :type num: int
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'username': author,
        }
        temp_url = self.ulord_in + "/{0}/{1}".format(page, num)
        return self.post(temp_url, data)

    def queryoutgobillings(self, author, page=1, num=10):
        """
        get billings info

        :param author: current user wallet name
        :type author: str
        :param page: which page of result do you want to view?Default is 1.
        :type page: int
        :param num: how many pieces of data of result do you want to view?Default is 10.
        :type num: int
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'username': author,
        }
        temp_url = self.ulord_out + "/{0}/{1}".format(page, num)
        return self.post(temp_url, data)

    def querybillingsdetail(self, author, page=1, num=10):
        """
        query the billings detail.Union the income and outgo

        :param author: current user wallet name
        :type author: str
        :param page: which page of result do you want to view?Default is 1.
        :type page: int
        :param num: how many pieces of data of result do you want to view?Default is 10.
        :type num: int
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'username':author,
        }
        temp_url = self.ulord_billings_detail + '/{0}/{1}'.format(page, num)
        return self.post(temp_url, data)

    def querybillings(self, username):
        """
        get billings info

        :param username: current user wallet name
        :type username: str
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'username': username,
        }
        return self.post(self.ulord_billings, data)

    def querypublishnum(self, author):
        """
        query the number of resourced which has published

        :param author: current user wallet name
        :type author: str
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'author': author
        }
        return self.post(self.ulord_published_num, data)


ulord_helper = UlordHelper()


if __name__ == '__main__':
    author = "test"
    data = {
        'author':author
    }
    print(ulord_helper.regist(username='x'*12,password='123'))