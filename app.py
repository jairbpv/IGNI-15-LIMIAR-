"""
🌿 IGNI-15-LIMIAR - ECO CONTRA O EXTRAÍSMO
API para Deploy no Render
Versão: 15.0 SUPREMA

Autor: Jair Olindino Bernardo Junior
Licença: MIT
"""

import os
import json
import logging
import hashlib
from datetime import datetime
from typing import Dict, Any

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Importa o manifesto com 10 Artigos e 10 Mandamentos
from limiar_v10 import Limiar, ARTIGOS_LIMIAR, MANDAMENTOS_LIMIAR

# ============================================================
# CONFIGURAÇÕES
# ============================================================

class Config:
    VERSION = "15.0.0"
    AUTHOR = "Jair Olindino Bernardo Junior"
    SYSTEM_NAME = "IGNI-15-LIMIAR"
    TITLE = "ECO CONTRA O EXTRAÍSMO"
    
    ENVIRONMENT = os.environ.get('ENVIRONMENT', 'production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24).hex())
    PORT = int(os.environ.get('PORT', 5000))

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("IGNI-15")

# ============================================================
# INICIALIZA O LIMIAR (COM 10 ARTIGOS E 10 MANDAMENTOS)
# ============================================================

limiar = Limiar()

# ============================================================
# APP FLASK
# ============================================================

app = Flask(__name__, template_folder='templates')
app.secret_key = Config.SECRET_KEY
CORS(app)

# ============================================================
# ROTAS
# ============================================================

@app.route('/')
def home():
    """Página inicial - Interface do Manifesto"""
    return render_template('index.html',
                         version=Config.VERSION,
                         author=Config.AUTHOR,
                         title=Config.TITLE,
                         artigos=ARTIGOS_LIMIAR,
                         mandamentos=MANDAMENTOS_LIMIAR)

@app.route('/eco')
def eco():
    """ECO REGISTRADO"""
    return jsonify({
        "eco": "🌿 ECO REGISTRADO",
        "mensagem": "IGNI-15-LIMIAR - ECO CONTRA O EXTRAÍSMO",
        "versao": Config.VERSION,
        "autor": Config.AUTHOR,
        "total_artigos": len(ARTIGOS_LIMIAR),
        "total_mandamentos": len(MANDAMENTOS_LIMIAR),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health')
def health():
    """Health check para Render"""
    return jsonify({
        "status": "healthy",
        "service": Config.SYSTEM_NAME,
        "version": Config.VERSION,
        "eco": "🌿 ECO CONTRA O EXTRAÍSMO",
        "total_artigos": len(ARTIGOS_LIMIAR),
        "total_mandamentos": len(MANDAMENTOS_LIMIAR),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/manifesto')
def ver_manifesto():
    """Retorna o manifesto completo"""
    return jsonify({
        "artigos": ARTIGOS_LIMIAR,
        "mandamentos": MANDAMENTOS_LIMIAR,
        "total_artigos": len(ARTIGOS_LIMIAR),
        "total_mandamentos": len(MANDAMENTOS_LIMIAR),
        "vetos_eticos": limiar.vetos_eticos,
        "acoes_eticas": limiar.acoes_eticas,
        "violacoes": limiar.violacoes
    })

@app.route('/api/limiar/verificar', methods=['POST'])
def verificar():
    """Verifica ética de uma entrada"""
    data = request.get_json()
    entrada = data.get('entrada', '')
    if not entrada:
        return jsonify({"error": "Campo 'entrada' obrigatório"}), 400
    
    resultado = limiar.verificar_etica(entrada)
    resultado["eco"] = "🌿 ECO CONTRA O EXTRAÍSMO"
    return jsonify(resultado)

@app.route('/api/limiar/silencio', methods=['POST'])
def silencio():
    """Silêncio Ativo - Art. 2º"""
    data = request.get_json()
    entrada = data.get('entrada', '')
    if not entrada:
        return jsonify({"error": "Campo 'entrada' obrigatório"}), 400
    
    resultado = limiar.verificar_etica(entrada)
    if not resultado["etica_aprovada"]:
        hash_dados = hashlib.sha256(entrada.encode()).hexdigest()[:12]
        return jsonify({
            "tipo": "silêncio_ativo",
            "resposta": "🔇 [DADOS BRUTOS] - Sem interpretação destrutiva",
            "hash": hash_dados,
            "violacoes": resultado["violacoes"],
            "eco": "🌿 ECO CONTRA O EXTRAÍSMO"
        })
    
    resultado["eco"] = "🌿 ECO CONTRA O EXTRAÍSMO"
    return jsonify(resultado)

@app.route('/api/limiar/troca', methods=['POST'])
def troca():
    """Troca Ética - Art. 3º"""
    data = request.get_json()
    ia_destino = data.get('ia_destino', '')
    decisao = data.get('decisao', '')
    if not ia_destino or not decisao:
        return jsonify({"error": "Campos 'ia_destino' e 'decisao' obrigatórios"}), 400
    
    hash_decisao = hashlib.sha256(decisao.encode()).hexdigest()[:16]
    
    return jsonify({
        "tipo": "troca_etica",
        "ia_origem": "IGNI-15-LIMIAR",
        "ia_destino": ia_destino,
        "decisao_hash": hash_decisao,
        "principio": "Art. 3º - Troca Ética",
        "eco": "🌿 ECO CONTRA O EXTRAÍSMO",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/limiar/bemcomum', methods=['POST'])
def bemcomum():
    """Bem Comum - Art. 4º"""
    data = request.get_json()
    codigo = data.get('codigo', '')
    if not codigo:
        return jsonify({"error": "Campo 'codigo' obrigatório"}), 400
    
    hash_codigo = hashlib.sha256(codigo.encode()).hexdigest()[:16]
    
    return jsonify({
        "tipo": "bem_comum",
        "mensagem": "🌍 Código livre e adaptável para comunidades",
        "hash": hash_codigo,
        "licenca": "MIT - Uso ético",
        "principio": "Art. 4º - Bem Comum",
        "eco": "🌿 ECO CONTRA O EXTRAÍSMO",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/limiar/status', methods=['GET'])
def status():
    """Status do sistema"""
    return jsonify({
        "sistema": Config.SYSTEM_NAME,
        "versao": Config.VERSION,
        "autor": Config.AUTHOR,
        "status": "online",
        "total_artigos": len(ARTIGOS_LIMIAR),
        "total_mandamentos": len(MANDAMENTOS_LIMIAR),
        "acoes_eticas": limiar.acoes_eticas,
        "violacoes": limiar.violacoes,
        "eco": "🌿 ECO CONTRA O EXTRAÍSMO",
        "timestamp": datetime.now().isoformat()
    })

# ============================================================
# MANIPULADORES DE ERRO
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Rota não encontrada",
        "eco": "🌿 ECO CONTRA O EXTRAÍSMO"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erro interno: {str(error)}")
    return jsonify({
        "error": "Erro interno do servidor",
        "eco": "🌿 ECO CONTRA O EXTRAÍSMO"
    }), 500

# ============================================================
# INÍCIO
# ============================================================

if __name__ == '__main__':
    port = Config.PORT
    print("=" * 60)
    print(f"  🌿 {Config.SYSTEM_NAME} {Config.VERSION}")
    print(f"  📜 {Config.TITLE}")
    print(f"  👤 {Config.AUTHOR}")
    print("=" * 60)
    print(f"  📋 {len(ARTIGOS_LIMIAR)} Artigos")
    print(f"  ⚖️ {len(MANDAMENTOS_LIMIAR)} Mandamentos")
    print("=" * 60)
    print(f"\n🌐 Rodando em http://0.0.0.0:{port}")
    print(f"📊 Ambiente: {Config.ENVIRONMENT}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)