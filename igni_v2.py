# IGNI-15 V12.0.0 SUPREMA UNIFICADA
# Autor: Jair Olindino Bernardo Junior
# Licença: MIT
# PoW + Consenso + Alerta + SQLite + Flask + Interface Limiar

import hashlib
import json
import time
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any
from flask import Flask, request, jsonify, send_from_directory
import uuid

# ===== SISTEMA DE ALERTA =====
class SistemaAlerta:
    def __init__(self):
        self.logs = []
        self.niveis = {"INFO": "🟢", "ALERTA": "🟡", "CRITICO": "🔴", "CONSENSO": "👑"}
    def registrar(self, nivel, mensagem):
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log = f"{self.niveis.get(nivel, '⚪')} [{timestamp}] {nivel}: {mensagem}"
        self.logs.append(log)
        print(log)
    def exportar_logs(self):
        return "\n".join(self.logs)

# ===== BLOCK + BLOCKCHAIN + DATABASE =====
class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[Dict], previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index, "timestamp": self.timestamp, "transactions": self.transactions,
            "previous_hash": self.previous_hash, "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    def mine_block(self, difficulty: int):
        target = '0' * difficulty
        while self.hash[:difficulty]!= target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Database:
    def __init__(self, db_name='data/blockchain.db'):
        os.makedirs('data', exist_ok=True)
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS blocks (id INTEGER PRIMARY KEY AUTOINCREMENT, block_index INTEGER UNIQUE, timestamp REAL, hash TEXT UNIQUE, previous_hash TEXT, nonce INTEGER, data TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, recipient TEXT, amount REAL, timestamp REAL, block_index INTEGER)''')
        self.conn.commit()
    def save_block(self, block):
        self.cursor.execute('''INSERT OR REPLACE INTO blocks (block_index, timestamp, hash, previous_hash, nonce, data) VALUES (?,?,?,?,?,?)''',
            (block.index, block.timestamp, block.hash, block.previous_hash, block.nonce, json.dumps(block.transactions)))
        for tx in block.transactions:
            self.cursor.execute('''INSERT INTO transactions (sender, recipient, amount, timestamp, block_index) VALUES (?,?,?,?,?)''',
                (tx.get('sender'), tx.get('recipient'), tx.get('amount'), tx.get('timestamp'), block.index))
        self.conn.commit()

class IGNI15:
    def __init__(self):
        self.versao = "V12.0.0 SUPREMA"
        self.autor = "Jair Olindino Bernardo Junior"
        self.alerta = SistemaAlerta()
        self.db = Database()
        self.difficulty = 4
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict] = []
        self.saldos = {"Alice": 1000, "Bob": 1000, "Comandante": 10000}
        self.create_genesis_block()
        self.alerta.registrar("INFO", f"IGNI-15 {self.versao} inicializado")

    def create_genesis_block(self):
        genesis = Block(0, time.time(), [{"genesis": True, "sender": "IGNI", "recipient": "Genesis", "amount": 0}], "0")
        genesis.mine_block(self.difficulty)
        self.chain.append(genesis)
        self.db.save_block(genesis)

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, sender: str, recipient: str, amount: float):
        if sender!= "IGNI" and self.saldos.get(sender, 0) < amount:
            self.alerta.registrar("CRITICO", f"Saldo insuficiente: {sender}")
            return False
        self.pending_transactions.append({
            "sender": sender, "recipient": recipient, "amount": amount, "timestamp": time.time()
        })
        return True

    def mine_pending_transactions(self, miner_address: str):
        if not self.pending_transactions: return False
        block = Block(len(self.chain), time.time(), self.pending_transactions, self.get_last_block().hash)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.db.save_block(block)
        # Atualiza saldos
        for tx in self.pending_transactions:
            if tx['sender']!= "IGNI": self.saldos[tx['sender']] -= tx['amount']
            self.saldos[tx['recipient']] = self.saldos.get(tx['recipient'], 0) + tx['amount']
        self.pending_transactions = []
        self.alerta.registrar("INFO", f"Novo bloco minerado: {block.hash[:12]}...")
        return True

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            if self.chain[i].hash!= self.chain[i].calculate_hash(): return False
            if self.chain[i].previous_hash!= self.chain[i-1].hash: return False
        return True

# ===== API FLASK =====
app = Flask(__name__)
node_identifier = str(uuid.uuid4()).replace('-', '')
igni = IGNI15()

@app.route('/mine', methods=['GET'])
def mine():
    igni.mine_pending_transactions(node_identifier)
    last_block = igni.get_last_block()
    return jsonify({'message': "Novo bloco minerado", 'index': last_block.index, 'hash': last_block.hash}), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    if not all(k in values for k in ['sender', 'recipient', 'amount']):
        return 'Missing values', 400
    if igni.add_transaction(values['sender'], values['recipient'], float(values['amount'])):
        return jsonify({'message': f"Transação será adicionada ao Bloco {igni.get_last_block().index + 1}"}), 201
    return jsonify({'message': 'Saldo insuficiente'}), 400

@app.route('/chain', methods=['GET'])
def full_chain():
    chain_data = [{'index': b.index, 'timestamp': b.timestamp, 'transactions': b.transactions, 'hash': b.hash, 'previous_hash': b.previous_hash} for b in igni.chain]
    return jsonify({'chain': chain_data, 'length': len(chain_data), 'saldos': igni.saldos, 'logs': igni.alerta.exportar_logs()}), 200

@app.route('/valid', methods=['GET'])
def valid():
    return jsonify({'valid': igni.is_chain_valid()}), 200

@app.route('/')
def home():
    return send_from_directory('', 'templates/index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)