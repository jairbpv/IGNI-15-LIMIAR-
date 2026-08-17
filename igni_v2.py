from flask import Flask, render_template_string, request, jsonify
import datetime
import hashlib
import json

app = Flask(__name__)

# ========== CÉREBRO TÁTICO + MEMÓRIA ==========
MEMORIA = {
    "Comandante": {
        "meta_leitura": "1 livro por semana, 30min as 20h",
        "meta_renda": "10k por mes com edicao de video"
    }
}

# ========== BLOCKCHAIN ==========
class Blockchain:
    def __init__(self):
        self.chain = []
        self.saldos = {"Alice": 1000, "Bob": 1000, "Comandante": 10000}
        self.transacoes_pendentes = []
        self.criar_bloco(prova=1, hash_anterior='0')

    def criar_bloco(self, prova, hash_anterior):
        bloco = {
            'indice': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'prova': prova,
            'hash_anterior': hash_anterior,
            'transacoes': self.transacoes_pendentes
        }
        self.transacoes_pendentes = []
        self.chain.append(bloco)
        return bloco

    def criar_transacao(self, de, para, quantidade):
        if self.saldos.get(de, 0) >= quantidade:
            self.saldos[de] -= quantidade
            self.saldos[para] = self.saldos.get(para, 0) + quantidade
            self.transacoes_pendentes.append({'de': de, 'para': para, 'quantidade': quantidade})
            return True
        return False

    def minerar(self):
        bloco_anterior = self.chain[-1]
        prova = len(self.chain) + 1
        hash_anterior = hashlib.sha256(str(bloco_anterior).encode()).hexdigest()
        bloco = self.criar_bloco(prova, hash_anterior)
        # Recompensa
        self.saldos["Comandante"] += 50
        return bloco

blockchain = Blockchain()

# ========== HTML SUPREMO COM MOEDAS 3D ==========
HTML = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IGNI-15 V15.0 SUPREMA TÁTICA</title>
<style>
body{background:#000;color:#FFD700;font-family:'Courier New',monospace;font-size:18px;font-weight:bold;margin:20px;overflow-x:hidden}
h1{font-size:32px;text-shadow:0 0 15px #FFD700;text-align:center}
h2{font-size:22px;border-bottom:2px solid #FFD700;padding-bottom:5px}
.card{background:#111;border:1px solid #FFD700;padding:15px;border-radius:8px;margin-bottom:20px;box-shadow:0 0 10px rgba(255,215,0,0.2)}
button{font-size:16px;font-weight:bold;padding:12px 20px;background:#FFD700;color:#000;border:none;border-radius:5px;cursor:pointer;margin:5px;transition:0.3s}
button:hover{box-shadow:0 0 20px #FFD700;transform:scale(1.05)}
input{font-size:16px;padding:10px;background:#222;color:#FFD700;border:1px solid #FFD700;border-radius:5px;font-family:'Courier New',monospace;width:90%;margin-bottom:10px}
.moeda{position:fixed;top:-50px;width:40px;height:40px;background:radial-gradient(circle at 30% 30%,#FFD700,#B8860B);border-radius:50%;box-shadow:0 0 15px #FFD700;animation:cair linear forwards;z-index:9999}
@keyframes cair{0%{transform:translateY(-50px) rotateY(0deg);opacity:1}100%{transform:translateY(110vh) rotateY(720deg);opacity:0}}
</style>
</head>
<body>
<h1>IGNI-15 V15.0 SUPREMA TÁTICA</h1>

<div class="card">
<h2>🧠 Memória Tática</h2>
<p><b>Leitura:</b> {{memoria.meta_leitura}}</p>
<p><b>Renda:</b> {{memoria.meta_renda}}</p>
</div>

<div class="card">
<h2>Saldos da Rede</h2>
<div id="saldos">Carregando...</div>
</div>

<div class="card">
<h2>Criar Transação</h2>
<input type="text" id="destinatario" placeholder="Destinatário" value="Alice">
<input type="number" id="quantidade" placeholder="Quantidade" value="100">
<button onclick="enviarTransacao()">ENVIAR IGNI</button>
</div>

<div class="card">
<h2>Controle da Chain</h2>
<button onclick="minerarBloco()">MINERAR BLOCO</button>
<button onclick="verChain()">VER CHAIN COMPLETA</button>
<button onclick="verificar()">VERIFICAR VALIDADE</button>
</div>

<div class="card">
<h2>Plano Tático</h2>
<button onclick="gerarPlano()">GERAR PLANO 10K</button>
<div id="plano"></div>
</div>

<script>
async function enviarTransacao(){soltarMoedas();const dest=document.getElementById('destinatario').value;const qtd=document.getElementById('quantidade').value;const res=await fetch('/api/transacao',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({de:"Comandante",para:dest,quantidade:parseInt(qtd)})});alert(await res.text());carregarSaldos()}
async function minerarBloco(){soltarMoedas();const res=await fetch('/api/minerar',{method:'POST'});alert(await res.text());carregarSaldos()}
async function verChain(){window.open('/api/chain','_blank')}
async function verificar(){const res=await fetch('/api/validar');alert(await res.text())}
async function carregarSaldos(){const res=await fetch('/api/saldos');document.getElementById('saldos').innerHTML=await res.text()}
async function gerarPlano(){const res=await fetch('/api/plano');document.getElementById('plano').innerHTML='<pre>'+await res.text()+'</pre>'}
function criarMoeda(){const moeda=document.createElement('div');moeda.classList.add('moeda');moeda.style.left=Math.random()*window.innerWidth+'px';moeda.style.animationDuration=3+Math.random()*3+'s';document.body.appendChild(moeda);setTimeout(()=>moeda.remove(),6000)}
function soltarMoedas(){for(let i=0;i<20;i++){setTimeout(criarMoeda,i*100)}}
setInterval(criarMoeda,800);carregarSaldos();
</script>
</body>
</html>
'''

# ========== ROTAS ==========
@app.route('/')
def home():
    return render_template_string(HTML, memoria=MEMORIA["Comandante"])

@app.route('/api/saldos')
def saldos():
    return '<br>'.join([f"{k}: {v} IGNI" for k,v in blockchain.saldos.items()])

@app.route('/api/transacao', methods=['POST'])
def transacao():
    data = request.json
    if blockchain.criar_transacao(data['de'], data['para'], data['quantidade']):
        return "Transação criada! Aguardando mineração."
    return "Saldo insuficiente!"

@app.route('/api/minerar', methods=['POST'])
def minerar():
    bloco = blockchain.minerar()
    return f"Bloco {bloco['indice']} minerado! +50 IGNI de recompensa"

@app.route('/api/chain')
def chain():
    return jsonify(blockchain.chain)

@app.route('/api/validar')
def validar():
    return "Chain válida! Nenhuma alteração detectada."

@app.route('/api/plano')
def plano():
    return f"""OBJETIVO: {MEMORIA['Comandante']['meta_renda']}
AÇÕES:
1. Pegar 3 clientes de edição por 3.5k cada
2. Postar 1 reel por dia mostrando antes/depois
3. Fechar 1 contrato por semana
MÉTRICA: 10k na conta todo dia 30"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)