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
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>IGNI-15 V9.7.0 COIN 3D REAL</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
            @keyframes spin3d { 0% {transform: rotateY(0deg) rotateX(10deg);} 100% {transform: rotateY(360deg) rotateX(10deg);} }
            @keyframes floatUp { 0%,100% {transform: translateY(0px);} 50% {transform: translateY(-25px);} }
            @keyframes shimmer { 0%{filter:brightness(1)} 50%{filter:brightness(1.8)} 100%{filter:brightness(1)} }

            body {background: radial-gradient(ellipse at center, #1a1200 0%, #000000 100%); color:#e0e0e0; font-family:'Orbitron', sans-serif; padding:20px; text-align:center; overflow-x:hidden;}
            canvas {position:fixed; top:0; left:0; z-index:0;}
           .container { max-width:700px; margin:auto; position:relative; z-index:2; }
            h1 {color:#ffd700; font-size:40px; font-weight:900; text-shadow:0 0 20px #ffd700; animation:shimmer 3s infinite;}

           .coin-wrapper { width:180px; height:180px; margin:40px auto; animation: floatUp 3s ease-in-out infinite; perspective: 800px; }
           .coin-main { width:100%; height:100%; position:relative; animation: spin3d 2.5s linear infinite; transform-style: preserve-3d; }
           .coin-face { position:absolute; width:100%; height:100%; border-radius:50%; background: radial-gradient(circle at 30% 30%, #fff8c0 0%, #ffd700 40%, #ffaa00 80%, #b8860b 100%); border:4px solid #ffed4e; box-shadow: 0 0 60px #ffd700, inset 0 0 30px rgba(255,255,255,0.6); display:flex; align-items:center; justify-content:center; font-size:70px; color:#8B4513; font-weight:900; backface-visibility: hidden; }
           .coin-front {transform: translateZ(15px);}
           .coin-back {transform: rotateY(180deg) translateZ(15px); background: radial-gradient(circle at 30% 30%, #ffd700 0%,