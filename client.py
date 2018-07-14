# -*- coding:utf-8 -*-
'''
File: client.py
File Created: Saturday, 7th July 2018
Author: Hongzoeng Ng (kenecho@hku.hk)
-----
Last Modified: Saturday, 14th July 2018
Modified By: Hongzoeng Ng (kenecho@hku.hk>)
-----
Copyright @ 2018 KenEcho
'''

import requests

from params import ADDRESS, DEFAULT_PORT


class Client(object):
    def __init__(self, address=ADDRESS, port=DEFAULT_PORT):
        self._base_url = "http://{}:{}".format(
            address, port
        )

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

    def register_node(self, address):
        """
        :params:
        address, list of string
        """
        url = self._base_url + "/nodes_register"
        params = {
            "nodes": address
        }
        response = requests.post(url, json=params)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(
                "Error code: {}\n".format(response.status_code)
            )

    def update_chain(self):
        url = self._base_url + "/nodes/resolve"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                "Http service error.\nURL: {}".format(url)
            )

    def registerNode_and_updateChain(self, address):
        url = self._base_url + "/nodes_register"
        params = {
            "nodes": address
        }
        response = requests.post(url, json=params)
        if response.status_code == 201:
            print(response.json()['message'])
            print("Total nodes:\n")
            for node in response.json()['total_nodes']:
                print(node)
            self.update_chain()
        else:
            raise Exception(
                response
            )
