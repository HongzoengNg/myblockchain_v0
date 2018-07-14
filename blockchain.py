# -*- coding: utf-8 -*-
"""
@Author: Ken Ng
@Date: 2018-07-04 17:16:17
@Last Modified by:   Ken Ng
@Last Modified time: 2018-07-04 17:16:17
"""
import json
import time
import hashlib
from urllib.parse import urlparse
import requests


BLOCK_FORMAT_FILE = 'block.json'
with open(BLOCK_FORMAT_FILE, 'r') as load_json:
    CONST_BLOCK = json.load(load_json)


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

        self.nodes = set()

    def new_block(self, proof, previous_hash=None):
        # Creates a new Block and adds it to the chain
        """
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block = CONST_BLOCK.copy()
        block['index'] = len(self.chain) + 1
        block['timestamp'] = time.time()
        block['transactions'] = self.current_transactions,
        block['proof'] = proof,
        block['previous_hash'] = previous_hash or self.hash(self.chain[-1])
        # reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        generate the new transaction information and add in next pending block

        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.current_transactions.append(transaction)
        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
        simply POW:
        - seek a `p'` to let hash(pp') starting with 4 zeros
        - p is the last proof and  p' is the current proof

        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, current_proof):
        """
        Validation: if hash(last_proof, proof) starting with 4 '0'
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = "{}{}".format(last_proof, current_proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        """
        generate the SHA-256 hash value of the block

        :param block: <dict> Block
        :return: <str>
        """
        block_str = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        for i in range(1, len(chain)):
            block = chain[i]
            previous_block = chain[i-1]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            if not self.valid_proof(
                previous_block["proof"], block["proof"]
            ):
                return False
        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None

        max_chain_length = len(self.chain)
        for node in neighbours:
            response = requests.get(
                "http://{}/full_chain".format(node)
            )
            if response.status_code == 200:
                node_chain = response.json()
                length = node_chain['length']
                chain = node_chain['chain']
                # TODO
                if length > max_chain_length:
                    max_chain_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False
