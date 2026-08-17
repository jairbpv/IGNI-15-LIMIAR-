from flask import Flask, jsonify, request, render_template 
import hashlib 
import json 
from time import time 

app = Flask(__name__) 

class Blockchain: 
    def __init__(self): 
        self.chain = [] 
        self.current_transactions = [] 
        self.new_block(previous_hash='1', proof=100) 

    def new_block(self, proof, previous_hash=None): 
        block = { 
            'index': len(self.chain) + 1, 
            'timestamp': time(), 
            'transactions': self.current_transactions, 
            'proof': proof, 
            'previous_hash': previous_hash or self.hash(self.chain[-1]), 
        } 
        self.chain.append(block)              # <- PRIMEIRO SALVA
        self.current_transactions = []        # <- DEPOIS LIMPA
        return block 

    def new_transaction(self, sender, recipient, amount): 
        self.current_transactions.append({ 
            'sender': sender, 
            'recipient': recipient, 
            'amount': amount, 
        }) 
        return self.last_block['index'] + 1 

    @property 
    def last_block(self): 
        return self.chain[-1] 

    @staticmethod 
    def hash(block): 
        block_string = json.dumps(block, sort_keys=True).encode() 
        return hashlib.sha256(block_string).hexdigest() 

blockchain = Blockchain() 

@app.route('/') 
def home(): 
    return render_template('index.html') 

@app.route('/mine', methods=['GET']) 
def mine(): 
    last_block = blockchain.last_block 
    proof = 123 
    previous_hash = blockchain.hash(last_block) 
    block = blockchain.new_block(proof, previous_hash) 
    response = { 
        'message': "BLOCO MINERADO!", 
        'index': block['index'], 
        'transactions': block['transactions'], 
        'proof': block['proof'], 
        'previous_hash': block['previous_hash'] 
    } 
    return jsonify(response), 200 

@app.route('/transaction', methods=['POST']) 
def new_transaction(): 
    values = request.form 
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount']) 
    response = {'message': f'Transação será adicionada ao Bloco {index}'} 
    return jsonify(response), 201 

@app.route('/chain', methods=['GET']) 
def full_chain(): 
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)} 
    return jsonify(response), 200 

@app.route('/verify', methods=['GET']) 
def verify(): 
    response = {'valid': True} 
    return jsonify(response), 200 

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=10000)