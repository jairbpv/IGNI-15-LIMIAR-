from flask import Flask, render_template_string, request
import hashlib
import time

app = Flask(__name__)

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
            if current.hash!= current.calculate_hash(): return False
            if current.previous_hash!= previous.hash: return False
        return True

igni_chain = Blockchain()

def get_balance(address):
    balance = 0
    for block in igni_chain.chain:
        for tx in block.transactions:
            if isinstance(tx, str) and ">" in tx:
                parts = tx.split(" > ")
                if len(parts) == 3:
                    sender, receiver, amount = parts
                    amount = int(amount)
                    if sender == address: balance -= amount
                    if receiver == address: balance += amount
    return balance

@app.route('/')
def home():
    saldo = get_balance("Comandante")
    total_blocos = len(igni_chain.chain)
    total_tx = len(igni_chain.pending_transactions) + sum(len(b.transactions) for b in igni_chain.chain) - 1
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>IGNI-15 V9.6.6 ULTRA</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <style>
            @keyframes pulse { 0%, 100% { text-shadow: 0 0 10px #ffdd00, 0 0 20px #ffdd00; } 50% { text-shadow: 0 0 30px #ffdd00, 0 0 60px #ffdd00; } }
            @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }
            body {background: #050505; color: #e0e0e0; font-family: 'Courier New', monospace; padding: 20px; text-align: center; overflow-x: hidden;}
            body::before {content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, rgba(255,221,0,0.1) 0%, transparent 50%); pointer-events: none; z-index: 0;}
           .container { max-width: 700px; margin: auto; position: relative; z-index: 1; }
            h1 {color: #ffdd00; animation: pulse 2s infinite, float 3s ease-in-out infinite; font-size: 36px; margin-bottom: 30px;}
            h1 i {font-size: 40px;}
           .stats {display: flex; gap: 15px; justify-content: center; margin: 25px 0; flex-wrap: wrap;}
           .stat-card {background: linear-gradient(145deg, #1a1a1a, #111); border: 1px solid #ffdd00; border-radius: 12px; padding: 15px 20px; min-width: 120px; box-shadow: 0 0 20px rgba(255,221,0,0.2);}
           .stat-card i {font-size: 24px; color: #ffdd00; margin-bottom: 8px;}
           .stat-num {font-size: 28px; color: #ffdd00; font-weight: bold;}
           .saldo-box {background: linear-gradient(145deg, #1a1a1a, #111); border: 2px solid #ffdd00; border-radius: 15px; padding: 25px; margin: 25px 0; box-shadow: 0 0 30px rgba(255, 221, 0, 0.5); animation: float 4s ease-in-out infinite;}
           .saldo-valor {font-size: 42px; color: #ffdd00; font-weight: bold; text-shadow: 0 0 20px #ffdd00;}
            button {background: linear-gradient(145deg, #ffdd00, #ffcc00); color: #0a0a0a; border: none; padding: 14px 28px; border-radius: 8px; font-weight: bold; cursor: pointer; margin: 10px; font-size: 17px; display: inline-flex; align-items: center; gap: 10px; transition: all 0.3s; box-shadow: 0 0 15px rgba(255,221,0,0.3);}
            button:hover {transform: scale(1.05); box-shadow: 0 0 25px #ffdd00, 0 0 40px #ffdd00;}
           .tx-form { background: linear-gradient(145deg, #111, #0a0a0a); padding: 20px; border-radius: 15px; margin: 25px 0; border: 1px solid #333;}
            input {background: #1a1a1a; color: #ffdd00; border: 1px solid #ffdd00; padding: 12px; border-radius: 6px; margin: 8px; font-size: 16px; width: 85%;}
        </style>
    </head>
    <body>
        <div class="container">
            <h1><i class="fa-solid fa-cube"></i> IGNI-15 V9.6.6 ULTRA <i class="fa-solid fa-cube"></i></h1>
            <div class="stats">
                <div class="stat-card"><i class="fa-solid fa-link"></i><div class="stat-num">{{ total_blocos }}</div><div>BLOCOS</div></div>
                <div class="stat-card"><i class="fa-solid fa-paper-plane"></i><div class="stat-num">{{ total_tx }}</div><div>TRANSAÇÕES</div></div>
                <div class="stat-card"><i class="fa-solid fa-shield-halved"></i><div class="stat-num">100%</div><div>VÁLIDA</div></div>
            </div>
            <div class="saldo-box">
                <h2><i class="fa-solid fa-wallet"></i> CARTEIRA DO COMANDANTE</h2>
                <div class="saldo-valor">{{ saldo }} IGNI</div>
            </div>
            <button onclick="window.location.href='/mine'"><i class="fa-solid fa-hammer"></i> MINERAR</button>
            <button onclick="window.location.href='/chain'"><i class="fa-solid fa-link"></i> VER CHAIN</button>
            <button onclick="window.location.href='/verify'"><i class="fa-solid fa-shield-halved"></i> VERIFICAR</button>
            <div class="tx-form">
                <h2><i class="fa-solid fa-rocket"></i> ENVIAR TRANSAÇÃO</h2>
                <form action="/transaction" method="post">
                    <input type="text" name="sender" placeholder="De: Gênesis" required><br>
                    <input type="text" name="receiver" placeholder="Para: Comandante" required><br>
                    <input type="number" name="amount" placeholder="Quantidade" required><br>
                    <button type="submit"><i class="fa-solid fa-paper-plane"></i> ENVIAR</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    ''', saldo=saldo, total_blocos=total_blocos, total_tx=total_tx)

@app.route('/mine')
def mine():
    igni_chain.add_block(igni_chain.pending_transactions)
    igni_chain.pending_transactions = []
    return render_template_string('<style>body{background:#050505;color:#ffdd00;font-family:"Courier New";text-align:center;padding:50px;}h1{font-size:40px;animation:pulse 2s infinite;text-shadow:0 0 20px #ffdd00;}@keyframes pulse{0%,100%{text-shadow:0 0 10px #ffdd00}50%{text-shadow:0 0 40px #ffdd00}}</style><h1><i class="fa-solid fa-hammer"></i> BLOCO MINERADO! <i class="fa-solid fa-hammer"></i></h1><a href="/" style="color:#ffdd00">VOLTAR</a>')

@app.route('/chain')
def chain():
    chain_data = []
    for block in igni_chain.chain:
        chain_data.append({"index": block.index, "hash": block.hash, "prev": block.previous_hash, "tx": block.transactions})
    return render_template_string('<style>body{background:#050505;color:#e0e0e0;font-family:"Courier New";padding:20px;}h1{color:#ffdd00;text-align:center;text-shadow:0 0 10px #ffdd00;}.bloco{background:linear-gradient(145deg,#1a1a1a,#111);border:2px solid #ffdd00;border-radius:12px;padding:18px;margin:15px 0;box-shadow:0 0 20px rgba(255,221,0,0.3);position:relative;}.elo{color:#ffdd00;text-align:center;font-size:30px;margin:-10px 0;}</style><h1><i class="fa-solid fa-link"></i> CORRENTE IGNI</h1>{% for b in data %}<div class="bloco"><b>Bloco #{{ b.index }}</b><br><small>Hash: {{ b.hash[:25] }}...</small><br><small>TX: {{ b.tx }}</small></div>{% if not loop.last %}<div class="elo"><i class="fa-solid fa-arrow-down"></i></div>{% endif %}{% endfor %}<a href="/" style="color:#ffdd00;display:block;text-align:center;margin-top:20px;">VOLTAR</a>', data=chain_data)

@app.route('/verify')
def verify():
    status = igni_chain.is_chain_valid()
    cor = "#00ff88" if status else "#ff0000"
    return render_template_string('<style>body{background:#050505;color:{{cor}};font-family:"Courier New";text-align:center;padding:50px;}h1{font-size:40px;text-shadow:0 0 20px {{cor}};}</style><h1><i class="fa-solid fa-shield-halved"></i> CHAIN VÁLIDA: {{status}} <i class="fa-solid fa-shield-halved"></i></h1><a href="/" style="color:#ffdd00">VOLTAR</a>', status=status, cor=cor)

@app.route('/transaction', methods=['POST'])
def transaction():
    tx = f"{request.form['sender']} > {request.form['receiver']} > {request.form['amount']}"
    igni_chain.pending_transactions.append(tx)
    return render_template_string('<style>body{background:#050505;color:#ffdd00;font-family:"Courier New";text-align:center;padding:50px;}h1{font-size:40px;animation:pulse 2s infinite;text-shadow:0 0 20px #ffdd00;}@keyframes pulse{0%,100%{text-shadow:0 0 10px #ffdd00}50%{text-shadow:0 0 40px #ffdd00}}</style><h1><i class="fa-solid fa-rocket"></i> TRANSAÇÃO ADICIONADA! <i class="fa-solid fa-rocket"></i></h1><a href="/" style="color:#ffdd00">VOLTAR</a>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)