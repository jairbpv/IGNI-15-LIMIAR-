from flask import Flask, render_template_string, request, jsonify
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
            if current.hash!= current.calculate_hash():
                return False
            if current.previous_hash!= previous.hash:
                return False
        return True

igni_chain = Blockchain()

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>IGNI-15 V9.6.4 GOLD</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        body {background: #0a0a0a; color: #e0e0e0; font-family: 'Courier New', monospace; padding: 20px; text-align: center;}
        h1 {color: #ffdd00; text-shadow: 0 0 10px #ffdd00, 0 0 20px #ffdd00; font-size: 32px;}
        h1 i {font-size: 36px;}
      .container { max-width: 600px; margin: auto; }
      .bloco {background: #1a1a1a; border: 1px solid #ffdd00; border-radius: 10px; padding: 15px; margin: 10px 0; text-align: left; box-shadow: 0 0 15px rgba(255, 221, 0, 0.3);}
        button {background: #ffdd00; color: #0a0a0a; border: none; padding: 12px 25px; border-radius: 6px; font-weight: bold; cursor: pointer; margin: 8px; font-size: 17px; display: inline-flex; align-items: center; justify-content: center; gap: 10px;}
        button i {font-size: 22px;}
        button:hover {background: #ffcc00; box-shadow: 0 0 15px #ffdd00, 0 0 25px #ffdd00;}
        input {background: #222; color: #e0e0e0; border: 1px solid #444; padding: 10px; border-radius: 5px; margin: 5px; font-size: 16px; width: 80%;}
      .tx-form { background: #111; padding: 15px; border-radius: 10px; margin: 20px 0; }
      .voltar {color:#ffdd00; display:block; text-align:center; margin-top:20px; font-size:18px; text-decoration:none;}
    </style>
</head>
<body>
    <div class="container">
        <h1><i class="fa-solid fa-cube"></i> IGNI-15 V9.6.4 GOLD <i class="fa-solid fa-cube"></i></h1>
        <button onclick="window.location.href='/mine'"><i class="fa-solid fa-hammer"></i> MINERAR</button>
        <button onclick="window.location.href='/chain'"><i class="fa-solid fa-link"></i> VER CHAIN</button>
        <button onclick="window.location.href='/verify'"><i class="fa-solid fa-shield-halved"></i> VERIFICAR</button>
        <div class="tx-form">
            <h2><i class="fa-solid fa-paper-plane"></i> ENVIAR TRANSAÇÃO</h2>
            <form action="/transaction" method="post">
                <input type="text" name="sender" placeholder="De: Gênesis" required><br>
                <input type="text" name="receiver" placeholder="Para: Comandante" required><br>
                <input type="number" name="amount" placeholder="Quantidade: 1000" required><br>
                <button type="submit"><i class="fa-solid fa-rocket"></i> ENVIAR</button>
            </form>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/mine')
def mine():
    igni_chain.add_block(igni_chain.pending_transactions)
    igni_chain.pending_transactions = []
    return render_template_string('<!DOCTYPE html><html><head><title>Minerado</title><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"><style>body{background:#0a0a0a;color:#ffdd00;font-family:"Courier New";text-align:center;padding:50px;}h1{font-size:40px;text-shadow:0 0 20px #ffdd00;}.voltar{color:#ffdd00;font-size:18px;text-decoration:none;}</style></head><body><h1><i class="fa-solid fa-hammer"></i> BLOCO MINERADO! <i class="fa-solid fa-hammer"></i></h1><p style="color:#e0e0e0">Novo bloco adicionado à chain</p><br><a class="voltar" href="/"><i class="fa-solid fa-house"></i> VOLTAR</a></body></html>')

@app.route('/chain')
def chain():
    chain_data = []
    for block in igni_chain.chain:
        chain_data.append({"index": block.index, "hash": block.hash, "prev": block.previous_hash, "tx": block.transactions})
    return render_template_string('<!DOCTYPE html><html><head><title>Chain</title><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"><style>body{background:#0a0a0a;color:#e0e0e0;font-family:"Courier New";padding:20px;}h1{color:#ffdd00;text-align:center;text-shadow:0 0 10px #ffdd00;}.bloco{background:#1a1a1a;border:1px solid #ffdd00;border-radius:10px;padding:15px;margin:15px 0;box-shadow:0 0 15px rgba(255,221,0,0.2);}.voltar{color:#ffdd00;display:block;text-align:center;margin-top:20px;}</style></head><body><h1><i class="fa-solid fa-link"></i> IGNI CHAIN</h1>{% for b in data %}<div class="bloco"><b>Bloco #{{ b.index }}</b><br><small>Hash: {{ b.hash[:20] }}...</small><br><small>Prev: {{ b.prev[:20] }}...</small><br><small>TX: {{ b.tx }}</small></div>{% endfor %}<a class="voltar" href="/"><i class="fa-solid fa-house"></i> VOLTAR</a></body></html>', data=chain_data)

@app.route('/verify')
def verify():
    status = igni_chain.is_chain_valid()
    cor = "#00ff88" if status else "#ff0000"
    return render_template_string('<!DOCTYPE html><html><head><title>Verificar</title><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"><style>body{background:#0a0a0a;color:{{cor}};font-family:"Courier New";text-align:center;padding:50px;}h1{font-size:40px;text-shadow:0 0 20px {{cor}};}.voltar{color:#ffdd00;font-size:18px;text-decoration:none;}</style></head><body><h1><i class="fa-solid fa-shield-halved"></i> CHAIN VÁLIDA: {{status}} <i class="fa-solid fa-shield-halved"></i></h1><p style="color:#e0e0e0">Integridade da blockchain confirmada</p><br><a class="voltar" href="/"><i class="fa-solid fa-house"></i> VOLTAR</a></body></html>', status=status, cor=cor)

@app.route('/transaction', methods=['POST'])
def transaction():
    tx = f"{request.form['sender']} > {request.form['receiver']} > {request.form['amount']}"
    igni_chain.pending_transactions.append(tx)
    return render_template_string('<!DOCTYPE html><html><head><title>TX</title><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"><style>body{background:#0a0a0a;color:#ffdd00;font-family:"Courier New";text-align:center;padding:50px;}h1{font-size:40px;text-shadow:0 0 20px #ffdd00;}.voltar{color:#ffdd00;font-size:18px;text-decoration:none;}</style></head><body><h1><i class="fa-solid fa-rocket"></i> TRANSAÇÃO ADICIONADA! <i class="fa-solid fa-rocket"></i></h1><p style="color:#e0e0e0">Aguardando mineração</p><br><a class="voltar" href="/"><i class="fa-solid fa-house"></i> VOLTAR</a></body></html>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)