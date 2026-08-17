import os
import json
import hashlib
import time
from flask import Flask, render_template_string, request

app = Flask(__name__)
ARQUIVO_CADEIA = 'igni_chain.json'

class Bloco:
    def __init__(self, indice, transacoes, hash_anterior):
        self.indice = indice
        self.transacoes = transacoes
        self.hash_anterior = hash_anterior
        self.timestamp = time.time()
        self.hash = self.calcular_hash()

    def calcular_hash(self):
        dados = f"{self.indice}{self.transacoes}{self.hash_anterior}{self.timestamp}"
        return hashlib.sha256(dados.encode()).hexdigest()

    def to_dict(self):
        return {'indice': self.indice, 'transacoes': self.transacoes, 'hash_anterior': self.hash_anterior, 'timestamp': self.timestamp, 'hash': self.hash}

    @staticmethod
    def from_dict(dados):
        bloco = Bloco(dados['indice'], dados['transacoes'], dados['hash_anterior'])
        bloco.timestamp = dados['timestamp']
        bloco.hash = dados['hash']
        return bloco

def salvar_cadeia(cadeia):
    with open(ARQUIVO_CADEIA, 'w') as f:
        json.dump([b.to_dict() for b in cadeia], f, indent=4)

def carregar_cadeia():
    if os.path.exists(ARQUIVO_CADEIA):
        with open(ARQUIVO_CADEIA, 'r') as f:
            return [Bloco.from_dict(b) for b in json.load(f)]
    return []

blockchain = carregar_cadeia()
transacoes_pendentes = []

if not blockchain:
    blockchain.append(Bloco(0, ["Genesis Block"], "0"))
    salvar_cadeia(blockchain)

def calcular_saldos():
    saldos = {'Alice': 0, 'Bob': 0, 'Comandante': 0}
    for bloco in blockchain:
        for tx in bloco.transacoes:
            if tx!= "Genesis Block":
                try:
                    de, para, valor = tx.split(' > ')
                    saldos[de] -= int(valor)
                    saldos[para] += int(valor)
                except: pass
    return saldos

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>IGNI-15 V9.9.0 MEMORIA ETERNA</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: #000; 
            color: #FFD700; 
            font-family: 'Orbitron', Arial; 
            text-align: center; 
            overflow-x: hidden;
        }
      .moedas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
      .moeda { 
            position: absolute; width: 40px; height: 40px; 
            background: radial-gradient(circle at 30% 30%, #FFF 0%, #FFD700 40%, #B8860B 100%);
            border-radius: 50%; box-shadow: 0 0 25px #FFD700; 
            animation: cair 4s linear infinite; 
        }
        @keyframes cair { 
            0% { transform: translateY(-100px) rotateX(0deg); opacity: 1; } 
            100% { transform: translateY(100vh) rotateX(720deg); opacity: 0; } 
        }
      .conteudo { position: relative; z-index: 1; padding: 20px; }
      .titulo { font-size: 48px; font-weight: 900; text-shadow: 0 0 30px #FFD700; margin: 30px 0; letter-spacing: 3px; }
      .card { 
            border: 3px solid #FFD700; border-radius: 25px; padding: 30px; 
            margin: 25px auto; background: rgba(255,215,0,0.05);
            box-shadow: 0 0 30px rgba(255,215,0,0.3); max-width: 400px;
        }
      .nome { font-size: 32px; font-weight: 700; margin-bottom: 10px; }
      .saldo { font-size: 50px; font-weight: 900; text-shadow: 0 0 25px #FFD700; }
      .subtitulo { font-size: 28px; font-weight: 700; margin-bottom: 20px; }
        input, select { 
            padding: 18px; margin: 10px; border-radius: 15px; 
            border: 2px solid #FFD700; background: #111; color: #FFD700; 
            font-size: 22px; font-family: 'Orbitron'; width: 90%; max-width: 350px;
        }
        button { 
            background: linear-gradient(45deg, #FFD700, #FFA500); 
            color: #000; padding: 20px 35px; border: none; 
            border-radius: 18px; font-weight: 900; cursor: pointer; 
            box-shadow: 0 0 25px #FFD700; margin: 12px;
            font-size: 22px; font-family: 'Orbitron'; width: 90%; max-width: 350px;
        }
        label { font-size: 22px; font-weight: 700; }
    </style>
</head>
<body>
    <div class="moedas" id="moedas"></div>
    <div class="conteudo">
        <h1 class="titulo">MEMORIA ETERNA</h1>
        
        <div class="card">
            <div class="nome">ALICE</div>
            <div class="saldo">{{ saldos['Alice'] }} IGNI</div>
        </div>
        
        <div class="card">
            <div class="nome">BOB</div>
            <div class="saldo">{{ saldos['Bob'] }} IGNI</div>
        </div>
        
        <div class="card">
            <div class="nome">COMANDANTE</div>
            <div class="saldo">{{ saldos['Comandante'] }} IGNI</div>
        </div>

        <div class="card">
            <div class="subtitulo">ENVIAR TRANSAÇÃO</div>
            <form action="/enviar" method="post">
                <label>DE:</label><br>
                <select name="de"><option>Comandante</option><option>Alice</option><option>Bob</option></select><br>
                <label>PARA:</label><br>
                <select name="para"><option>Alice</option><option>Bob</option><option>Comandante</option></select><br>
                <label>QUANTIDADE:</label><br>
                <input type="number" name="quantidade" value="1000"><br>
                <button type="submit">ENVIAR TX</button>
            </form>
            <form action="/minerar" method="post">
                <button type="submit">MINERAR BLOCO</button>
            </form>
        </div>
    </div>

<script>
    function criarMoeda() {
        const moeda = document.createElement('div');
        moeda.className = 'moeda';
        moeda.style.left = Math.random() * 100 + '%';
        moeda.style.animationDuration = (Math.random() * 2 + 3) + 's';
        document.getElementById('moedas').appendChild(moeda);
        setTimeout(() => moeda.remove(), 5000);
    }
    setInterval(criarMoeda, 250);
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML, saldos=calcular_saldos())

@app.route('/enviar', methods=['POST'])
def enviar():
    transacoes_pendentes.append(f"{request.form['de']} > {request.form['para']} > {request.form['quantidade']}")
    return "TX ENVIADA! <a href='/' style='color:gold'>VOLTAR</a>"

@app.route('/minerar', methods=['POST'])
def minerar():
    global transacoes_pendentes
    if transacoes_pendentes:
        blockchain.append(Bloco(len(blockchain), transacoes_pendentes, blockchain[-1].hash))
        salvar_cadeia(blockchain)
        transacoes_pendentes = []
    return "BLOCO MINERADO! <a href='/' style='color:gold'>VOLTAR</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)