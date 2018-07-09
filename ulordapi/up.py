# coding=utf-8
# Copyright (c) 2016-2018 The Ulord Core Developers
# @File  : up.py
# @Author: Ulord_PuJi
# @Date  : 2018/5/18 0018
import logging, copy, time

import requests

from ulordapi import utils
from ulordapi.config import ulordconfig, config, webconfig
from ulordapi.errcode import return_result


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
        self.ulord_createwallet = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_createwallet') # ulord regist webURL 1
        self.ulord_paytouser = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_paytouser') # ulord transfer webURL 2
        # publish URL
        self.ulord_publish = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_publish')  # ulord publish webURL 4
        self.ulord_update = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_update') # ulord update webURL 4.1
        self.ulord_delete = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_delete') # ulord delete webURL 4.2
        self.ulord_publish_data =  {
            "author": "justin",
            "title": "第一篇技术博客",
            "tags": ["blockchain", "UDFS"],
            "udfs_hash": "QmVcVaHhMeWNNetSLTZArmqaHMpu5ycqntx7mFZaci63VF",
            "price": 0.1,
            "content_type": ".txt",
            "des": "这是使用UDFS和区块链生成的第一篇博客的描述信息"
        }  # ulord publish data
        # query URL
        self.ulord_queryresource = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_queryresourcelist') # query resource list webURL #resource2
        self.ulord_checkbought = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_checkbought') # query if the blog has bought 5
        self.ulord_transaction = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_transaction')  # ulord transaction webURL 6

        self.ulord_querybalance = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_querybalance')  # qurey balance webURL 3
        self.ulord_userpublished = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_userpublished') # query the resource that user has published resource3
        self.ulord_in = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_in') # query income billings 7
        self.ulord_out = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_out') # query outcome billings 8
        self.ulord_billings = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_billings') # query the user's billings 10
        self.ulord_billings_detail = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_billings_detail') # query the detail billings 9
        self.ulord_published_num = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_publish_num') # query the number of the resource that author has published. 11
        self.ulord_reource_byID = ulordconfig.get('ulord_url') + ulordconfig.get(
            'ulord_querysingleresource')  # query the resource list according to the ID. resource1
        self.ulord_expenserecords_byID = ulordconfig.get('ulord_url') + ulordconfig.get(
            'ulord_querysinglebilling')  # query the blog that user has bought resource4
        self.ulord_statistics_byID = ulordconfig.get('ulord_url') + ulordconfig.get(
            'ulord_querysingleresourceaccount')  # query the blog that user has bought resource5
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
        self.log.info("url is {}".format(url))
        self.log.info("data is {}".format(data))

        # deal with unicode and utf-8
        from setup import py_version
        if py_version == 3:
            pass
        elif py_version == 2:
            from utils import _byteify
            data = _byteify(data=data)
        else:
            info = 'unknown python version'
            self.log.error(info)
            print(info)
        # calculate  U-Sign
        self.calculate_sign(data)
        # self.ulord_head = ulordconfig.get('ulord_head')
        try:
            r = requests.post(url=url, json=data, headers=self.ulord_head)
        except Exception as e:
            self.log.error("Failed request from the ulord-platform: {0}, URL is {1}".format(e, url))
            return return_result(60400)
        self.log.info(r.status_code)
        if r.status_code == requests.codes.ok:
            self.log.debug(r.json())
            return r.json()
        else:
            self.log.debug(r)
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
        except Exception as e:
            self.log.error("Failed request from the ulord-platform: {0}, URL is {1}".format(e, url))
            return return_result(60400)
        self.log.info(url)
        self.log.debug(self.ulord_head)
        self.log.info(r.status_code)
        if (r.status_code == requests.codes.ok):
            self.log.debug(r.json())
            return r.json()
        else:
            self.log.debug(r)
            return return_result(60400)

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

        :param data: data needed to be published.Key includes author,title,tags,udfs_hash,price,content_type,des，pay_password
        :type data: dict
        :return: errcode.You can query from the errcode dict.
        """
        return self.post(self.ulord_publish, data)

    def update(self, data):
        """
        update data from the ulord-platform

        :param data: data needed to be updated.Key includes id,pay_password,title,tags,udfs_hash,price,content_type,des，pay_password
        :type data: dict
        :return: errcode.You can query from the errcode dict.
        """
        return self.post(self.ulord_update, data)

    def delete(self, id, password):
        """
        delete resource on the ulord-platform

        :param id: resource ulord-platform DB ID
        :type id: int
        :param password: user wallet password
        :type password: str
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            "id": id,
            "pay_password": password
        }
        return self.post(self.ulord_delete, data)

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

    def queryresource(self, page=1, num=10, **kwargs):
        """
        query the resource list from the ulord platform.method is get

        :param page: which page do you want to view?Default is 1.
        :type page: int
        :param num: how many pieces of datas in one page?.Default is 10.
        :type num: int
        :param kwargs: key-value query
        :type kwargs: key-value
        :return: errcode.You can query from the errcode dict.
        """
        temp_url = self.ulord_queryresource + "/{0}/{1}".format(page, num)
        if kwargs:
            data = {}
            for key, value in kwargs.items():
                data.update({
                    key: value
                })
            return self.post(temp_url,data)
        else:
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

    def queryuserpublished(self, wallet_username, page=1, num=10):
        """
        query user published from ulort platform

        :param wallet_username: auther wallet name
        :type wallet_username: str
        :param page: which page of result do you want to view?Default is 1.
        :type page: int
        :param num: how many pieces of data of result do you want to view?Default is 10.
        :type num: int
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'author': wallet_username,
        }
        temp_url = self.ulord_userpublished + "/{0}/{1}".format(page, num)
        return self.post(temp_url, data)

    def query_resourc_by_ID(self, ids):
        """
        query resource list according to the id list

        :param ids: need to be query id list
        :type ids: list
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'ids': ids,
        }
        return self.post(self.ulord_reource_byID, data)

    def queryBillingDetailByID(self, claim_id):
        """
        query all billing details according to the claimID

        :param claim_id: resource on the ulord-chain ID
        :type claim_id: str
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'claim_id': claim_id,
        }
        return self.post(self.ulord_expenserecords_byID, data)

    def queryStatisticsByID(self, claim_ids):
        """
        query resource statistics information by ID

        :param claim_ids: need to be query ID list.
        :type claim_ids: list
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'claim_ids': claim_ids,
        }
        return self.post(self.ulord_statistics_byID, data)

    def queryincomebillings(self, author, start, end, page=1, num=10, category=2):
        """
        get income billings info

        :param author: current user wallet name
        :type author: str
        :param start: start time.2018-03-29
        :type start: str
        :param end: end time.2018-03-29
        :type end: str
        :param page: which page of result do you want to view?Default is 1.
        :type page: int
        :param num: how many pieces of data of result do you want to view?Default is 10.
        :type num: int
        :param category: resource type. 0----common resource,1----ads,2-----all
        :type category: int
        :return: errcode.You can query from the errcode dict.
        """

        data = {
            'username': author,
            'sdate': start,
            'edate': end
        }
        if category == 1 or category == 0:
            data.update({
                'category': category,
            })
        temp_url = self.ulord_in + "/{0}/{1}".format(page, num)
        return self.post(temp_url, data)

    def queryoutgobillings(self, author, start, end, page=1, num=10, category=2):
        """
        get outgo billings info

        :param author: current user wallet name
        :type author: str
        :param start: start time.2018-03-29
        :type start: str
        :param end: end time.2018-03-29
        :type end: str
        :param page: which page of result do you want to view?Default is 1.
        :type page: int
        :param num: how many pieces of data of result do you want to view?Default is 10.
        :type num: int
        :param category: resource type. 0----common resource,1----ads,2-----all
        :type category: int
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'username': author,
            'sdate': start,
            'edate': end
        }
        if category == 1 or category == 0:
            data.update({
                'category': category,
            })
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

    def querybillings(self, username, start, end):
        """
        get billings info

        :param username: current user wallet name
        :type username: str
        :param start: start time.2018-03-29
        :type start: str
        :param end: end time.2018-03-29
        :type end: str
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'username': username,
            'sdate': start,
            'edate': end
        }
        return self.post(self.ulord_billings, data)

    def querypublishnum(self, author, start, end):
        """
        query the number of resourced which has published

        :param author: current user wallet name
        :type author: str
        :param start: start time.2018-03-29
        :type start: str
        :param end: end time.2018-03-29
        :type end: str
        :return: errcode.You can query from the errcode dict.
        """
        data = {
            'author': author,
            'sdate': start,
            'edate':end
        }
        return self.post(self.ulord_published_num, data)


# ulord_helper = UlordHelper()


if __name__ == '__main__':
    author = "test"
    data = {
        'author':author
    }
    # print(ulord_helper.regist(username='x'*12,password='123'))