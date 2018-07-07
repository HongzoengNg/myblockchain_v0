# -*- coding:utf-8 -*-
'''
File: client.py
File Created: Saturday, 7th July 2018
Author: Hongzoeng Ng (kenecho@hku.hk)
-----
Last Modified: Saturday, 7th July 2018
Modified By: Hongzoeng Ng (kenecho@hku.hk>)
-----
Copyright @ 2018 KenEcho
'''

import requests


class Client(object):
    def __init__(self):
        self._base_url = "http://127.0.0.1:5000"

    def get_full_chain(self):
        url = self._base_url + "/full_chain"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                "Http service error.\nURL: {}".format(url)
            )

    def mine(self):
        url = self._base_url + "/mine"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                "Http service error.\nURL: {}".format(url)
            )

    def add_transaction(self, sender, recipient, amount):
        url = self._base_url + "/transactions/new"
        trans = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        }
        response = requests.post(url, json=trans)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(
                "Error code: {}\n".format(response.status_code)
            )
