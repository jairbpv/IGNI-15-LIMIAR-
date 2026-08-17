
from flask import Flask, render_template_string, request
import hashlib
import time
import json
import os

app = Flask(__name__)

ARQUIVO_CHAIN = "igni_chain.json"

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
    
    def create_genesis_block(self):
        return Block(0, ["Genesis Block"], time.time(), "0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, transactions):
        new_block = Block(len(self.chain), transactions, time.time(), self.get_latest_block().hash)
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash!= current.calculate_hash(): 
                return False
            if current.previous_hash!= previous.hash: 
                return False
        return True

def salvar_chain():
    data = []
    for block in igni_chain.chain:
        data.append({
            'index': block.index,
            'transactions': block.transactions,
            'timestamp': block.timestamp,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce,
            'hash': block.hash
        })
    with open(ARQUIVO_CHAIN, 'w') as f:
        json.dump(data, f)

def carregar_chain():
    global igni_chain
    if os.path.exists(ARQUIVO_CHAIN):
        with open(ARQUIVO_CHAIN, 'r') as f:
            data = json.load(f)
            igni_chain.chain = []
            for b in data:
                block = Block(b['index'], b['transactions'], b['timestamp'], b['previous_hash'])
                block.nonce = b['nonce']
                block.hash = b['hash']
                igni_chain.chain.append(block)

igni_chain = Blockchain()
carregar_chain()

def get_balance(address):
    balance = 0
    for block in igni_chain.chain:
        for tx in block.transactions:
            if isinstance(tx, str) and ">" in tx:
                parts = tx.split(" > ")
                if len(parts) == 3:
                    sender, receiver, amount = parts
                    amount = int(amount)
                    if sender == address: 
                        balance -= amount
                    if receiver == address: 
                        balance += amount
    return balance

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>IGNI-15 V9.8.0 MEMORIA ETERNA</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body{background:#0a0a0a;color:#fff;font-family:Arial;text-align:center;padding:20px}
       .card{background:#1a1a1a;border:2px solid #FFD700;border-radius:15px;padding:20px;margin:10px auto;max-width:300px}
        h1{color:#FFD700;text-shadow:0 0 10px #FFD700}
        input,button{padding:10px;margin:5px;border-radius:8px;border:none;font-size:16px}
        input{background:#333;color:#fff;width:200px}
        button{background:#FFD700;color:#000;font-weight:bold;cursor:pointer}
        button:hover{background:#FFA500}
        a{text-decoration:none;color:#FFD700}
    </style>
</head>
<body>
    <h1>💎 IGNI-15 V9.8.0 MEMORIA ETERNA</h1>
    
    <div class="card">
        <h2>ALICE</h2>
        <h1>{{saldo_alice}} IGNI</h1>
    </div>
    
    <div class="card">
        <h2>BOB</h2>
        <h1>{{saldo_bob}} IGNI</h1>
    </div>
    
    <div class="card">
        <h2>COMANDANTE</h2>
        <h1>{{saldo_comandante}} IGNI</h1>
    </div>
    
    <div class="card">
        <h3>ENVIAR TRANSAÇÃO</h3>
        <form action="/transaction" method="post">
            <input name="sender" placeholder="DE: Alice/Bob/Comandante"><br>
            <input name="receiver" placeholder="PARA: Alice/Bob/Comandante"><br>
            <input name="amount" placeholder="QUANTIDADE" type="number"><br>
            <button type="submit">ENVIAR TX</button>
        </form>
    </div>
    
    <br>
    <a href="/mine"><button>MINERAR BLOCO</button></a>
    <a href="/chain"><button>VER CORRENTE</button></a>
    <a href="/verify"><button>VERIFICAR</button></a>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML, 
        saldo_alice=get_balance("Alice"), 
        saldo_bob=get_balance("Bob"), 
        saldo_comandante=get_balance("Comandante")
    )

@app.route('/mine')
def mine():
    igni_chain.add_block(igni_chain.pending_transactions)
    igni_chain.pending_transactions = []
    salvar_chain()
    return '<h1 style="color:gold">BLOCO MINERADO E SALVO!</h1><a href="/">VOLTAR</a>'

@app.route('/transaction', methods=['POST'])
def transaction():
    tx = f"{request.form['sender']} > {request.form['receiver']} > {request.form['amount']}"
    igni_chain.pending_transactions.append(tx)
    salvar_chain()
    return '<h1 style="color:gold">TX ENVIADA E SALVA!</h1><a href="/">VOLTAR</a>'

@app.route('/chain')
def chain():
    blocks = "<br>".join([f"Bloco {b.index}: {b.transactions}" for b in igni_chain.chain])
    return f"<h1 style='color:gold'>CORRENTE IGNI</h1>{blocks}<br><br><a href='/'>VOLTAR</a>"

@app.route('/verify')
def verify():
    valid = "100% VALIDA" if igni_chain.is_chain_valid() else "INVALIDA"
    return f"<h1 style='color:gold'>CHAIN {valid}</h1><a href='/'>VOLTAR</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)