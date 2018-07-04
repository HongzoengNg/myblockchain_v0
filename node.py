# -*- coding: utf-8 -*-
"""
@Author: Ken Ng
@Date: 2018-07-04 18:38:14
@Last Modified by:   Ken Ng
@Last Modified time: 2018-07-04 18:38:14
"""
import requests
import json

from textwrap import dedent
from flask import (
    Flask,
    jsonify,
    request
)
from blockchain import Blockchain
from uuid import uuid4

# Initiate our node
app = Flask(__name__)

# Generate a globally unique address for this node
node_id = str(uuid4()).replace('-', '')

# Initiate the blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # award
    # sender is 0 referring a new coin
    blockchain.new_transaction(
        sender="0",
        recipient=node_id,
        amount=1
    )

    # forge the new block into the chain
    new_block = blockchain.new_block(proof)
    response = {
        'message': 'New Block Forged',
        'index': new_block['index'],
        'transactions': new_block['transactions'],
        'proof': new_block['proof'],
        'previous_hash': new_block['previous_hash']
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    transaction = request.get_json()

    # checking
    required_field = ['sender', 'recipient', 'amount']
    if not all(k in transaction for k in required_field):
        return 'Missing values', 400
    
    # create a new transaction
    index = blockchain.new_transaction(
        transaction['sender'],
        transaction['recipient'],
        transaction['amount']
    )
    response = {
        'message': f'Transaction will be added to Block {index}'
    }
    return jsonify(response), 201


@app.route('/full_chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


def main():
    app.run(host='')

if __name__ == '__main__':
    main()
