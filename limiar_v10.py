""" IGNI-15-LIMIAR V10.0 - ECO CONTRA O EXTRAÍSMO API para Deploy no Render Autor: Jair Olindino Bernardo Junior Licença: MIT """
import os, json, logging, hashlib, secrets, re
from datetime import datetime, timezone
from functools import wraps, lru_cache
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# ========== CONFIG ==========
class Config:
    VERSION = "10.0.0"; AUTHOR = "Jair Olindino Bernardo Junior"; SYSTEM_NAME = "IGNI-15-LIMIAR"
    ENVIRONMENT = os.environ.get('ENVIRONMENT', 'production'); PORT = int(os.environ.get('PORT', 5000))
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    RATE_LIMIT = os.environ.get('RATE_LIMIT', '100/hour')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    VETOS = ["ódio", "vigilância sem consentimento", "concentração de riqueza", "discriminação", "manipulação", "exploração de dados"]

logging.basicConfig(level=Config.LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("IGNI-15")

# ========== CÉREBRO LIMIAR ==========
class Limiar:
    def __init__(self):
        self.acoes_eticas = 0; self.violacoes = 0; self.inicio = datetime.now(timezone.utc)
        logger.info(f"🌿 {Config.SYSTEM_NAME} V{Config.VERSION} online")

    @lru_cache(maxsize=256)
    def verificar_etica(self, entrada: str):
        entrada_lower = entrada.lower().strip()
        if not entrada_lower: return {"etica_aprovada": False, "erro": "Entrada vazia"}
        violacoes = [{"tipo": v, "gravidade": "ALTA"} for v in Config.VETOS if v in entrada_lower]
        if violacoes:
            self.violacoes += 1
            return {"etica_aprovada": False, "violacoes": violacoes, "acao": "silêncio_ativo", "artigo": "Art. 1º"}
        self.acoes_eticas += 1
        return {"etica_aprovada": True, "acao": "processar", "artigo": "Art. 4º"}

    def silencio_ativo(self, entrada): 
        return {"tipo": "silêncio_ativo", "resposta": "[DADOS BRUTOS]", "hash": hashlib.sha256(entrada.encode()).hexdigest()[:12], "principio": "Art. 2º"}
    
    def troca_etica(self, ia_destino, decisao):
        decisao_limpa = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL]', decisao) # Sanitiza
        return {"tipo": "troca_etica", "ia_destino": ia_destino[:100], "hash": hashlib.sha256(decisao_limpa.encode()).hexdigest()[:16], "principio": "Art. 3º"}

    def bem_comum(self, codigo): 
        return {"tipo": "bem_comum", "hash": hashlib.sha256(codigo.encode()).hexdigest()[:16], "licenca": "MIT", "principio": "Art. 4º"}

    def get_status(self):
        uptime = int((datetime.now(timezone.utc) - self.inicio).total_seconds())
        total = self.acoes_eticas + self.violacoes
        taxa = round((self.acoes_eticas / total) * 100, 2) if total else 100.0
        return {"nome": Config.SYSTEM_NAME, "versao": Config.VERSION, "status": "online", "uptime": uptime, "acoes_eticas": self.acoes_eticas, "violacoes": self.violacoes, "taxa_aprovacao": taxa}

limiar = Limiar()

# ========== FLASK APP ==========
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=[Config.RATE_LIMIT])

def validate_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json: return jsonify({"error": "Content-Type deve ser application/json"}), 400
        return f(*args, **kwargs)
    return decorated

# ========== ROTAS ==========
@app.route('/')
def home(): return render_template('index.html', version=Config.VERSION, author=Config.AUTHOR)

@app.route('/api/limiar/verificar', methods=['POST'])
@limiter.limit("10/minute") @validate_json
def verificar():
    entrada = request.json.get('entrada', '').strip()
    if not entrada or len(entrada) > 10000: return jsonify({"error": "Entrada inválida"}), 400
    res = limiar.verificar_etica(entrada)
    res["eco"] = "🌿 ECO CONTRA O EXTRAÍSMO"
    return jsonify(res)

@app.route('/api/limiar/silencio', methods=['POST']) @limiter.limit("10/minute") @validate_json
def silencio(): return jsonify(limiar.silencio_ativo(request.json.get('entrada','')) | {"eco": "🌿 ECO"})

@app.route('/api/limiar/troca', methods=['POST']) @limiter.limit("10/minute") @validate_json
def troca(): data=request.json; return jsonify(limiar.troca_etica(data.get('ia_destino',''), data.get('decisao','')) | {"eco": "🌿 ECO"})

@app.route('/api/limiar/bemcomum', methods=['POST']) @limiter.limit("10/minute") @validate_json
def bemcomum(): return jsonify(limiar.bem_comum(request.json.get('codigo','')) | {"eco": "🌿 ECO"})

@app.route('/api/limiar/status', methods=['GET']) @limiter.limit("30/minute")
def status(): return jsonify(limiar.get_status() | {"eco": "🌿 ECO"})

@app.route('/api/health', methods=['GET']) @limiter.limit("60/minute")
def health(): return jsonify({"status": "healthy", "version": Config.VERSION, "eco": "🌿 ECO"})

@app.errorhandler(404)
def not_found(e): return jsonify({"error": "Recurso não encontrado", "eco": "🌿 ECO"}), 404

if __name__ == '__main__': app.run(host='0.0.0.0', port=Config.PORT)