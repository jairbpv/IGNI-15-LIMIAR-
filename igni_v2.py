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
    saldo_alice = get_balance("Alice")
    saldo_bob = get_balance("Bob")
    saldo_comandante = get_balance("Comandante")
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>IGNI-15 V9.7.1 MULTI-CARTEIRA</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
            @keyframes spin3d { 0% {transform: rotateY(0deg) rotateX(10deg);} 100% {transform: rotateY(360deg) rotateX(10deg);} }
            @keyframes floatUp { 0%,100% {transform: translateY(0px);} 50% {transform: translateY(-20px);} }
            @keyframes shimmer { 0%{filter:brightness(1)} 50%{filter:brightness(1.8)} 100%{filter:brightness(1)} }

            body {background: radial-gradient(ellipse at center, #1a1200 0%, #000000 100%); color:#e0e0e0; font-family:'Orbitron', sans-serif; padding:20px; text-align:center; overflow-x:hidden;}
            canvas {position:fixed; top:0; left:0; z-index:0;}
          .container { max-width:900px; margin:auto; position:relative; z-index:2; }
            h1 {color:#ffd700; font-size:32px; font-weight:900; text-shadow:0 0 20px #ffd700; animation:shimmer 3s infinite;}

          .wallets { display:flex; justify-content:center; gap:30px; flex-wrap:wrap; margin:30px 0; }
          .wallet-card { background:rgba(20,15,0,0.7); padding:20px; border-radius:20px; border:2px solid #ffd700; backdrop-filter:blur(15px); width:250px; }

          .coin-wrapper { width:120px; height:120px; margin:15px auto; animation: floatUp 3s ease-in-out infinite; perspective: 800px; }
          .coin-main { width:100%; height:100%; position:relative; animation: spin3d 2.5s linear infinite; transform-style: preserve-3d; }
          .coin-face { position:absolute; width:100%; height:100%; border-radius:50%; background: radial-gradient(circle at 30% 30%, #fff8c0 0%, #ffd700 40%, #ffaa00 80%, #b8860b 100%); border:3px solid #ffed4e; box-shadow: 0 0 40px #ffd700, inset 0 0 20px rgba(255,255,255,0.6); display:flex; align-items:center; justify-content:center; font-size:40px; color:#8B4513; font-weight:900; backface-visibility: hidden; }
          .coin-front {transform: translateZ(12px);}
          .coin-back {transform: rotateY(180deg) translateZ(12px);}
          .coin-rim { position:absolute; width:100%; height:100%; border-radius:50%; background: repeating-conic-gradient(#ffd700 0deg 10deg, #ffaa00 10deg 20deg); transform: rotateY(90deg) translateZ(12px); }

          .saldo-valor {font-size:36px; color:#ffd700; font-weight:900; text-shadow:0 0 20px #ffd700; animation:shimmer 2s infinite;}
          .saldo-label {color:#ffed4e; font-size:14px; margin-bottom:10px;}
            button {background: linear-gradient(145deg, #ffd700, #ffaa00); color:#1a1200; border:none; padding:14px 28px; border-radius:12px; font-weight:900; cursor:pointer; margin:10px; font-size:16px; display:inline-flex; align-items:center; gap:10px; transition:all 0.3s; box-shadow:0 0 25px rgba(255,215,0,0.5); font-family:'Orbitron';}
            button:hover {transform:scale(1.1); box-shadow:0 0 50px #ffd700;}
          .tx-form { background:rgba(20,15,0,0.7); padding:25px; border-radius:20px; margin:30px 0; border:2px solid #ffd700; backdrop-filter:blur(15px);}
            input {background:#1a1200; color:#ffd700; border:2px solid #ffaa00; padding:12px; border-radius:10px; margin:8px; font-size:15px; width:80%; font-family:'Orbitron';}
        </style>
    </head>
    <body>
    <canvas id="goldrain"></canvas>
        <div class="container">
            <h1><i class="fa-solid fa-crown"></i> IGNI-15 V9.7.1 MULTI-CARTEIRA <i class="fa-solid fa-crown"></i></h1>

            <div class="wallets">
                <div class="wallet-card">
                    <h3>ALICE</h3>
                    <div class="coin-wrapper"><div class="coin-main"><div class="coin-face coin-front">A</div><div class="coin-face coin-back">IGNI</div><div class="coin-rim"></div></div></div>
                    <div class="saldo-valor">{{ saldo_alice }}</div>
                    <div class="saldo-label">IGNI</div>
                </div>

                <div class="wallet-card">
                    <h3>BOB</h3>
                    <div class="coin-wrapper"><div class="coin-main"><div class="coin-face coin-front">B</div><div class="coin-face coin-back">IGNI</div><div class="coin-rim"></div></div></div>
                    <div class="saldo-valor">{{ saldo_bob }}</div>
                    <div class="saldo-label">IGNI</div>
                </div>

                <div class="wallet-card">
                    <h3>COMANDANTE</h3>
                    <div class="coin-wrapper"><div class="coin-main"><div class="coin-face coin-front"><i class="fa-solid fa-crown"></i></div><div class="coin-face coin-back">IGNI</div><div class="coin-rim"></div></div></div>
                    <div class="saldo-valor">{{ saldo_comandante }}</div>
                    <div class="saldo-label">IGNI</div>
                </div>
            </div>

            <button onclick="window.location.href='/mine'"><i class="fa-solid fa-hammer"></i> MINERAR</button>
            <button onclick="window.location.href='/chain'"><i class="fa-solid fa-link"></i> CORRENTE</button>
            <button onclick="window.location.href='/verify'"><i class="fa-solid fa-shield-halved"></i> AUDITAR</button>

            <div class="tx-form">
                <h2><i class="fa-solid fa-paper-plane"></i> TRANSFERIR IGNI</h2>
                <form action="/transaction" method="post">
                    <input type="text" name="sender" placeholder="DE: Alice" required><br>
                    <input type="text" name="receiver" placeholder="PARA: Bob" required><br>
                    <input type="number" name="amount" placeholder="QUANTIDADE: 100" required><br>
                    <button type="submit"><i class="fa-solid fa-bolt"></i> ENVIAR AGORA</button>
                </form>
            </div>
        </div>
    <script>
    const canvas=document.getElementById('goldrain'); const ctx=canvas.getContext('2d');
    canvas.width=window.innerWidth; canvas.height=window.innerHeight;
    let coins=[];
    for(let i=0;i<40;i++){
        coins.push({x:Math.random()*canvas.width, y:Math.random()*canvas.height-200, r:Math.random()*6+5, s:Math.random()*2+1, rot:Math.random()*360, rs:Math.random()*2+1})
    }
    function draw(){
        ctx.clearRect(0,0,canvas.width,canvas.height);
        coins.forEach(c=>{
            ctx.save(); ctx.translate(c.x,c.y); ctx.rotate(c.rot*Math.PI/180);
            let grad=ctx.createRadialGradient(-c.r/3,-c.r/3,0,c.r/3,c.r/3,c.r);
            grad.addColorStop(0,'#fff8c0'); grad.addColorStop(0.3,'#ffd700'); grad.addColorStop(0.7,'#ffaa00'); grad.addColorStop(1,'#b8860b');
            ctx.fillStyle=grad; ctx.beginPath(); ctx.arc(0,0,c.r,0,Math.PI*2); ctx.fill();
            ctx.strokeStyle='#ffed4e'; ctx.lineWidth=1.5; ctx.stroke();
            ctx.fillStyle='rgba(255,255,255,0.6)'; ctx.beginPath(); ctx.arc(-c.r/3,-c.r/3,c.r/4,0,Math.PI*2); ctx.fill();
            ctx.restore();
            c.y+=c.s; c.rot+=c.rs;
            if(c.y>canvas.height+50){c.y=-50; c.x=Math.random()*canvas.width;}
        });
        requestAnimationFrame(draw);
    } draw();
    </script>
    </body>
    </html>
    ''', saldo_alice=saldo_alice, saldo_bob=saldo_bob, saldo_comandante=saldo_comandante)

@app.route('/mine')
def mine():
    igni_chain.add_block(igni_chain.pending_transactions)
    igni_chain.pending_transactions = []
    return '<style>body{background:#000;color:#ffd700;text-align:center;padding:50px;font-family:Orbitron;}h1{font-size:50px;text-shadow:0 0 40px #ffd700;}</style><h1><i class="fa-solid fa-hammer"></i> BLOCO MINERADO! </h1><a href="/" style="color:#ffd700;font-size:20px;">VOLTAR</a>'

@app.route('/chain')
def chain():
    blocks = "<br>".join([f"Bloco {b.index}: {b.transactions}" for b in igni_chain.chain])
    return f"<body style='background:#000;color:#ffd700;text-align:center;padding:50px;font-family:Orbitron;'><h1>CORRENTE IGNI</h1><div style='text-align:left;max-width:600px;margin:auto;'>{blocks}</div><br><a href='/' style='color:#ffd700'>VOLTAR</a></body>"

@app.route('/verify')
def verify():
    valid = "100% VÁLIDA" if igni_chain.is_chain_valid() else "INVÁLIDA"
    color = "#00ff88" if igni_chain.is_chain_valid() else "#ff0000"
    return f"<body style='background:#000;color:{color};text-align:center;padding:50px;font-family:Orbitron;'><h1>CHAIN {valid}</h1><a href='/' style='color:#ffd700'>VOLTAR</a></body>"

@app.route('/transaction', methods=['POST'])
def transaction():
    tx = f"{request.form['sender']} > {request.form['receiver']} > {request.form['amount']}"
    igni_chain.pending_transactions.append(tx)
    return '<style>body{background:#000;color:#ffd700;text-align:center;padding:50px;font-family:Orbitron;}h1{font-size:50px;text-shadow:0 0 40px #ffd700;}</style><h1><i class="fa-solid fa-bolt"></i> TX ENVIADA! </h1><a href="/" style="color:#ffd700;font-size:20px;">VOLTAR</a>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
