# coding=utf-8
# @File  : up.py
# @Author: PuJi
# @Date  : 2018/4/26 0026
# from __future__ import unicode_literals
import logging

import requests

from upapi.config import ulordconfig
from upapi.src.utils.errcode import return_result

class UlordHelper(object):
    # a helper to help request the ulord paltform
    def __init__(self):
        self.log = logging.getLogger("UlordHelper:")
        # base URL
        self.ulord_url = ulordconfig.get('ulord_url')
        self.ulord_head = ulordconfig.get('ulord_head')
        # regist URL
        self.ulord_regist = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_regist') # ulord regist webURL
        self.ulord_paytouser = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_paytouser') # ulord transfer webURL
        # publish URL
        self.ulord_publish = ulordconfig.get('ulord_url') + ulordconfig.get('ulord_publish')  # ulord publish webURL
        self.ulord_publish_data = ulordconfig.get('ulord_publish_data')  # ulord publish data
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

    def post(self, url, data):
        self.log.debug(url)
        self.log.debug(data)
        r = requests.post(url=url, json=data, headers=self.ulord_head)
        self.log.debug(r.status_code)
        if r.status_code == requests.codes.ok:
            self.log.debug(r.json())
            return r.json()
        else:
            return return_result(50000)

    def get(self, url):
        r = requests.get(url=url, headers=self.ulord_head)
        self.log.debug(url)
        self.log.debug(r.status_code)
        if (r.status_code == requests.codes.ok):
            self.log.debug(r.json())
            return r.json()
        else:
            return return_result(50000)

    def regist(self, username, password):
        # regist wallet address from the ulord platform
        data = {
            "username": username,
            "pay_password": password
        }
        return self.post(self.ulord_regist, data)

    def publish(self, data):
        # publish data to the ulord platform
        return self.post(self.ulord_publish, data)

    def transaction(self, payer, claim_id, pay_password, isads=False):
        # record the transaction to the ulord platform

        data = {
            'username': payer,
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
        # activity send some ulords to the user
        if baseconfig.activity:
            data = {
                'is_developer': True,
                'recv_user': username,
                'amount': baseconfig.amount
            }
            return self.post(self.ulord_paytouser, data)
        else:
            return return_result(60300)

    def queryblog(self, page=1, num=10):
        # query the blog list from the ulord platform.method is get
        temp_url = self.ulord_queryblog + "{0}/{1}/".format(page, num)
        return self.get(temp_url)

    def querybalance(self, payer, pay_password):
        # query the personal balance from the ulord platform
        data = {
            'username': payer,
            'pay_password':pay_password
        }
        return self.post(self.ulord_querybalance, data)

    def checkisbought(self, payer, claim_ids):
        # query the personal balance from the ulord platform
        data = {
            'username': payer,
            'claim_ids': claim_ids
        }
        return self.post(self.ulord_checkbought, data)

    def queryuserpublished(self, wallet_username, page=1, num=10, category=2):
        # query user published from ulort platform
        data = {
            'author': wallet_username,
        }
        if category != 2:
            data.update({
                'category':category
            })
        temp_url = self.ulord_userpublished + "{0}/{1}/".format(page, num)
        return self.post(temp_url, data)

    def queryuserbought(self, wallet_username, page=1, num=10, category=2):
        # query user published from ulort platform
        data = {
            'customer': wallet_username,
        }
        if category != 2:
            data.update({
                'category':category
            })
        temp_url = self.ulord_userbought + "{0}/{1}/".format(page, num)
        return self.post(temp_url, data)

    def queryincomebillings(self, author, page=1, num=10):
        # get billings info
        data = {
            'username': author,
        }
        temp_url = self.ulord_in + "{0}/{1}/".format(page, num)
        return self.post(temp_url, data)

    def queryoutgobillings(self, author, page=1, num=10):
        # get billings info
        data = {
            'username': author,
        }
        temp_url = self.ulord_out + "{0}/{1}/".format(page, num)
        return self.post(temp_url, data)

    def querybillingsdetail(self, author, page=1, num=10):
        # query the billings detail.Union the income and outgo
        data = {
            'username':author,
        }
        temp_url = self.ulord_billings_detail + '{0}/{1}/'.format(page, num)
        return self.post(temp_url, data)

    def querybillings(self, username):
        # get billings info
        data = {
            'username': username,
        }
        return self.post(self.ulord_billings, data)

    def querypublishnum(self, author):
        data = {
            'author': author
        }
        return self.post(self.ulord_published_num, data)

    def addviews(self, dbID):
        data = {
            'id': dbID
        }
        return self.post(self.ulord_view, data)

ulord_helper = UlordHelper()
