import os
import json
import hashlib
import time
from flask import Flask, render_template_string, request, redirect, url_for

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
        dados = str(self.indice) + str(self.transacoes) + str(self.hash_anterior) + str(self.timestamp)
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
        json.dump([bloco.to_dict() for bloco in cadeia], f, indent=4)

def carregar_cadeia():
    if os.path.exists(ARQUIVO_CADEIA):
        with open(ARQUIVO_CADEIA, 'r') as f:
            dados = json.load(f)
            return [Bloco.from_dict(bloco) for bloco in dados]
    return []

blockchain = carregar_cadeia()
transacoes_pendentes = []

if not blockchain:
    bloco_genesis = Bloco(0, ["Genesis Block"], "0")
    blockchain.append(bloco_genesis)
    salvar_cadeia(blockchain)

def calcular_saldos():
    saldos = {'Alice': 0, 'Bob': 0, 'Comandante': 0}
    for bloco in blockchain:
        for tx in bloco.transacoes:
            if tx!= "Genesis Block":
                try:
                    partes = tx.split(' > ')
                    de = partes[0]
                    para = partes[1]
                    valor = int(partes[2])
                    if de in saldos: saldos[de] -= valor
                    if para in saldos: saldos[para] += valor
                except: pass
    return saldos

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>IGNI-15 V9.8.4 OURO 3D</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #000; color: #FFD700; font-family: Arial; text-align: center; margin: 0; overflow-x: hidden; font-size: 18px; }
      .moedas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
      .moeda { position: absolute; width: 35px; height: 35px; background: radial-gradient(circle at 30% 30%, #FFF, #FFD700, #B8860B); border-radius: 50%; box-shadow: 0 0 20px #FFD700; animation: cair 5s linear infinite; }
        @keyframes cair { 0% { transform: translateY(-100px) rotateX(0deg); opacity: 1; } 100% { transform: translateY(100vh) rotateX(720deg); opacity: 0; }
      .conteudo { position: relative; z-index: 1; padding: 10px; }
      .titulo { font-size: 38px; text-shadow: 0 0 20px #FFD700; margin: 20px; font-weight: bold; }
      .card { border: 3px solid #FFD700; border-radius: 20px; padding: 25px; margin: 20px 10px; background: rgba(0,0,0,0.85); box-shadow: 0 0 25px rgba(255,215,0,0.4); }
      .card h2 { font-size: 28px; margin: 10px 0; }
      .saldo { font-size: 42px; font-weight: bold; text-shadow: 0 0 20px #FFD700; margin: 10px 0; }
      .subtitulo { font-size: 24px; font-weight: bold; margin-bottom: 15px; }
        input, select { padding: 15px; margin: 8px; border-radius: 12px; border: 2px solid #FFD700; background: #111; color: #FFD700; font-size: 20px; width: 80%; max-width: 300px; }
        button { background: linear-gradient(45deg, #FFD700, #B8860B); color: #000; padding: 18px 30px; border: none; border-radius: 15px; font-weight: bold; cursor: pointer; box-shadow: 0 0 20px #FFD700; margin: 10px; font-size: 20px; width: 85%; max-width: 320px; }
        label { font-size: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="moedas" id="moedas"></div>
    <div class="conteudo">
        <h1 class="titulo">MEMORIA ETERNA</h1>
        <div class="card"><h2>ALICE</h2><div class="saldo">{{ saldos['Alice'] }} IGNI</div></div>
        <div class="card"><h2>BOB</h2><div class="saldo">{{ saldos['Bob'] }} IGNI</div></div>
        <div class="card"><h2>COMANDANTE</h2><div class="saldo">{{ saldos['Comandante'] }} IGNI</div></div>
        <div class="card">
            <div class="subtitulo">ENVIAR TRANSAÇÃO</div>
            <form action="/enviar" method="post">
                <label>DE:</label><br><select name="de"><option>Comandante</option><option>Alice</option><option>Bob</option></select><br>
                <label>PARA:</label><br><select name="para"><option>Alice</option><option>Bob</option><option>Comandante</option></select><br>
                <label>QUANTIDADE:</label><br><input type="number" name="quantidade" value="1000"><br>
                <button type="submit">ENVIAR TX</button>
            </form>
            <form action="/minerar" method="post"><button type="submit">MINERAR BLOCO</button></form>
        </div>
    </div>
<script>
    function criarMoeda() {
        const moeda = document.createElement('div');
        moeda.className = 'moeda';
        moeda.style.left = Math.random() * 100 + '%';
        moeda.style.animationDuration = (Math.random() * 3 + 3) + 's';
        document.getElementById('moedas').appendChild(moeda);
        setTimeout(() => moeda.remove(), 6000);
    }
    setInterval(criarMoeda, 300);
</script>
</body>
</html>
'''

@app.route('/')
def home():
    saldos = calcular_saldos()
    return render_template_string(HTML, saldos=saldos)

@app.route('/enviar', methods=['POST'])
def enviar():
    de = request.form['de']
    para = request.form['para']
    quantidade = request.form['quantidade']
    tx = f"{de} > {para} > {quantidade}"
    transacoes_pendentes.append(tx)
    return "TX ENVIADA E SALVA! <a href='/' style='color:gold'>VOLTAR</a>"

@app.route('/minerar', methods=['POST'])
def minerar():
    global transacoes_pendentes
    if transacoes_pendentes:
        ultimo = blockchain[-1]
        novo = Bloco(len(blockchain), transacoes_pendentes, ultimo.hash)
        blockchain.append(novo)
        salvar_cadeia(blockchain)
        transacoes_pendentes = []
    return "BLOCO MINERADO E SALVO! <a href='/' style='color:gold'>VOLTAR</a>"

@app.route('/chain')
def ver_chain():
    return {'cadeia': [b.to_dict() for b in blockchain]}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 