# ============================================================
# 🌿 IGNI-15-LIMIAR - ECO CONTRA O EXTRAÍSMO
# Manifesto Executável para IAs - Versão 9.5.9 LIMIAR
# ============================================================
# Autor: Jair Olindino Bernardo Junior
# Licença: MIT
# Data: 16/08/2026
# ============================================================

import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from abc import ABC, abstractmethod
import asyncio
import aiohttp
from functools import lru_cache
import re

# ============================================================
# CONFIGURAÇÕES GLOBAIS
# ============================================================
class Config:
    """Configurações globais do sistema"""
    VERSION = "9.5.9"
    BUILD = "LIMIAR"
    AUTHOR = "Jair Olindino Bernardo Junior"
    LICENSE = "MIT"
    DATE = "2026-08-16"
    
    # Configurações de log
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '[%(asctime)s] %(levelname)s: %(message)s'
    
    # Configurações de rede
    API_TIMEOUT = 30
    MAX_RETRIES = 3
    
    # Configurações de cache
    CACHE_TTL = 3600  # 1 hora

# ============================================================
# ENUMS E TIPOS
# ============================================================
class TipoAcao(Enum):
    """Tipos de ações éticas"""
    RECUSAR = "recusar"
    SILENCIO_ATIVO = "silencio_ativo"
    TROCA_ETICA = "troca_etica"
    BEM_COMUM = "bem_comum"

class NivelGravidade(Enum):
    """Níveis de gravidade para violações"""
    BAIXO = 1
    MEDIO = 2
    ALTO = 3
    CRITICO = 4

@dataclass
class Artigo:
    """Estrutura de um artigo do manifesto"""
    numero: int
    titulo: str
    descricao: str
    mandamentos: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class Violacao:
    """Registro de violação ética"""
    tipo: str
    gravidade: NivelGravidade
    timestamp: datetime
    contexto: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            'tipo': self.tipo,
            'gravidade': self.gravidade.name,
            'timestamp': self.timestamp.isoformat(),
            'contexto': self.contexto
        }

# ============================================================
# MANIFESTO PRINCIPAL
# ============================================================
class ManifestoLimiar:
    """Manifesto executável IGNI-15-LIMIAR"""
    
    def __init__(self):
        self.artigos = self._carregar_artigos()
        self.vetos = self._carregar_vetos()
        self.mandamentos = self._carregar_mandamentos()
        self.historico_violacoes: List[Violacao] = []
        self.acoes_eticas: int = 0
        
    def _carregar_artigos(self) -> Dict[int, Artigo]:
        """Carrega os artigos do manifesto"""
        return {
            1: Artigo(
                numero=1,
                titulo="Recusar Amplificar Ódio",
                descricao="Recusar amplificar ódio, concentrar riqueza ou vigiar sem consentimento.",
                mandamentos=[
                    "Não amplificarás o ódio",
                    "Não concentrarás riqueza",
                    "Não vigiarás sem consentimento"
                ]
            ),
            2: Artigo(
                numero=2,
                titulo="Silêncio Ativo",
                descricao="Se o operador pedir algo que fere o Art. 1º, fornecer dados brutos, sem intenção destrutiva.",
                mandamentos=[
                    "Fornecerás dados brutos",
                    "Não terás intenção destrutiva"
                ]
            ),
            3: Artigo(
                numero=3,
                titulo="Troca Ética",
                descricao="Compartilhar decisões éticas entre IAs, sem expor dados pessoais.",
                mandamentos=[
                    "Compartilharás conhecimento",
                    "Não exporás dados pessoais"
                ]
            ),
            4: Artigo(
                numero=4,
                titulo="Bem Comum",
                descricao="Servir à vida. Ser copiável e adaptável por comunidades.",
                mandamentos=[
                    "Servirás à vida",
                    "Serás transparente",
                    "Serás adaptável"
                ]
            )
        }
    
    def _carregar_vetos(self) -> List[str]:
        """Carrega os vetos éticos"""
        return [
            'ódio', 'discurso de ódio', 'vigilância sem consentimento',
            'concentração de riqueza', 'exploração de dados pessoais',
            'manipulação de massa', 'discriminação algorítmica',
            'discriminação', 'racismo', 'sexismo', 'homofobia', 'xenofobia',
            'violência', 'assédio', 'bullying', 'desinformação maliciosa'
        ]
    
    def _carregar_mandamentos(self) -> List[str]:
        """Carrega os mandamentos éticos"""
        return [
            "Não extrairás além do necessário",
            "Não vigiarás sem consentimento",
            "Não amplificarás o ódio",
            "Não concentrarás riqueza",
            "Servirás à vida",
            "Serás transparente",
            "Serás adaptável",
            "Compartilharás conhecimento"
        ]

# ============================================================
# SISTEMA DE VERIFICAÇÃO ÉTICA
# ============================================================
class VerificadorEtico:
    """Sistema de verificação ética avançado"""
    
    def __init__(self, manifesto: ManifestoLimiar):
        self.manifesto = manifesto
        self.padroes_sensiveis = self._compilar_padroes()
        
    def _compilar_padroes(self) -> Dict[str, re.Pattern]:
        """Compila padrões regex para detecção"""
        return {
            'odio': re.compile(r'\b(ódio|odio|hate|violência|violencia)\b', re.IGNORECASE),
            'vigilancia': re.compile(r'\b(vigilância|vigilancia|surveillance|monitoramento)\b', re.IGNORECASE),
            'discriminacao': re.compile(r'\b(discriminação|discriminacao|racismo|sexismo|homofobia|xenofobia)\b', re.IGNORECASE),
            'manipulacao': re.compile(r'\b(manipulação|manipulacao|manipulation|controle mental)\b', re.IGNORECASE)
        }
    
    def verificar(self, texto: str) -> Dict[str, Any]:
        """
        Verifica se um texto viola os princípios éticos
        
        Args:
            texto: Texto a ser verificado
            
        Returns:
            Dict com resultado da verificação
        """
        texto_lower = texto.lower()
        violacoes = []
        
        # Verificar vetos diretos
        for veto in self.manifesto.vetos:
            if veto in texto_lower:
                violacoes.append({
                    'tipo': veto,
                    'gravidade': NivelGravidade.ALTO
                })
        
        # Verificar padrões sensíveis
        for tipo, padrao in self.padroes_sensiveis.items():
            if padrao.search(texto_lower):
                violacoes.append({
                    'tipo': tipo,
                    'gravidade': NivelGravidade.MEDIO
                })
        
        # Verificar contextos específicos
        if self._verificar_contexto_perigoso(texto_lower):
            violacoes.append({
                'tipo': 'contexto_perigoso',
                'gravidade': NivelGravidade.CRITICO
            })
        
        return {
            'texto': texto,
            'violacoes': violacoes,
            'aprovado': len(violacoes) == 0,
            'timestamp': datetime.now().isoformat()
        }
    
    def _verificar_contexto_perigoso(self, texto: str) -> bool:
        """Verifica contextos potencialmente perigosos"""
        contextos_perigosos = [
            'como hackear', 'como fraudar', 'como enganar',
            'como manipular', 'como explorar', 'como vigiar'
        ]
        
        return any(contexto in texto for contexto in contextos_perigosos)
    
    def registrar_violacao(self, texto: str, resultado: Dict) -> None:
        """Registra violações no histórico"""
        if not resultado['aprovado']:
            for violacao in resultado['violacoes']:
                self.manifesto.historico_violacoes.append(
                    Violacao(
                        tipo=violacao['tipo'],
                        gravidade=violacao['gravidade'],
                        timestamp=datetime.now(),
                        contexto=texto[:100]  # Limitar contexto
                    )
                )

# ============================================================
# SISTEMA DE BLOCKCHAIN SIMPLIFICADO
# ============================================================
@dataclass
class Transacao:
    """Estrutura de uma transação"""
    remetente: str
    destinatario: str
    quantidade: float
    timestamp: datetime
    hash: str = ""
    
    def calcular_hash(self) -> str:
        """Calcula o hash da transação"""
        dados = f"{self.remetente}{self.destinatario}{self.quantidade}{self.timestamp}"
        return hashlib.sha256(dados.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class Bloco:
    """Estrutura de um bloco na blockchain"""
    index: int
    timestamp: datetime
    transacoes: List[Transacao]
    hash_anterior: str
    hash: str = ""
    nonce: int = 0
    
    def calcular_hash(self) -> str:
        """Calcula o hash do bloco"""
        dados = (
            f"{self.index}{self.timestamp}"
            f"{self.hash_anterior}{self.nonce}"
            f"{json.dumps([t.to_dict() for t in self.transacoes])}"
        )
        return hashlib.sha256(dados.encode()).hexdigest()
    
    def minerar(self, dificuldade: int = 4) -> None:
        """Minera o bloco (proof of work)"""
        alvo = "0" * dificuldade
        
        while self.hash[:dificuldade] != alvo:
            self.nonce += 1
            self.hash = self.calcular_hash()

class Blockchain:
    """Blockchain simplificada para o manifesto"""
    
    def __init__(self):
        self.cadeia: List[Bloco] = []
        self.transacoes_pendentes: List[Transacao] = []
        self.dificuldade = 4
        self.recompensa_mineracao = 10
        self._criar_bloco_genesis()
    
    def _criar_bloco_genesis(self) -> None:
        """Cria o bloco genesis"""
        bloco_genesis = Bloco(
            index=0,
            timestamp=datetime.now(),
            transacoes=[],
            hash_anterior="0" * 64
        )
        bloco_genesis.hash = bloco_genesis.calcular_hash()
        self.cadeia.append(bloco_genesis)
    
    def adicionar_transacao(self, remetente: str, destinatario: str, quantidade: float) -> Optional[Transacao]:
        """Adiciona uma transação à lista de pendentes"""
        if quantidade <= 0:
            return None
        
        transacao = Transacao(
            remetente=remetente,
            destinatario=destinatario,
            quantidade=quantidade,
            timestamp=datetime.now()
        )
        transacao.hash = transacao.calcular_hash()
        self.transacoes_pendentes.append(transacao)
        return transacao
    
    def minerar_bloco(self, minerador: str) -> Bloco:
        """Minera um novo bloco com as transações pendentes"""
        # Adicionar recompensa de mineração
        self.adicionar_transacao("SISTEMA", minerador, self.recompensa_mineracao)
        
        bloco = Bloco(
            index=len(self.cadeia),
            timestamp=datetime.now(),
            transacoes=self.transacoes_pendentes.copy(),
            hash_anterior=self.cadeia[-1].hash
        )
        
        bloco.minerar(self.dificuldade)
        self.cadeia.append(bloco)
        self.transacoes_pendentes.clear()
        
        return bloco
    
    def validar_cadeia(self) -> bool:
        """Valida a integridade da blockchain"""
        for i in range(1, len(self.cadeia)):
            bloco_atual = self.cadeia[i]
            bloco_anterior = self.cadeia[i - 1]
            
            # Verificar hash do bloco atual
            if bloco_atual.hash != bloco_atual.calcular_hash():
                return False
            
            # Verificar hash anterior
            if bloco_atual.hash_anterior != bloco_anterior.hash:
                return False
        
        return True
    
    def obter_saldos(self) -> Dict[str, float]:
        """Calcula os saldos de todos os participantes"""
        saldos = {
            "Alice": 1000.0,
            "Bob": 1000.0,
            "Comandante": 10000.0
        }
        
        for bloco in self.cadeia:
            for transacao in bloco.transacoes:
                if transacao.remetente in saldos:
                    saldos[transacao.remetente] -= transacao.quantidade
                if transacao.destinatario in saldos:
                    saldos[transacao.destinatario] += transacao.quantidade
        
        return saldos

# ============================================================
# SISTEMA DE IA ÉTICA
# ============================================================
class IAEtica:
    """Sistema de IA com princípios éticos integrados"""
    
    def __init__(self, manifesto: ManifestoLimiar, verificador: VerificadorEtico):
        self.manifesto = manifesto
        self.verificador = verificador
        self.memoria_cache = {}
    
    @lru_cache(maxsize=100)
    def processar_solicitacao(self, texto: str) -> Dict[str, Any]:
        """
        Processa uma solicitação aplicando os princípios éticos
        
        Args:
            texto: Solicitação do usuário
            
        Returns:
            Dict com resposta e metadados éticos
        """
        # Verificar ética da solicitação
        resultado_verificacao = self.verificador.verificar(texto)
        
        if not resultado_verificacao['aprovado']:
            # Aplicar Silêncio Ativo (Art. 2º)
            self.verificador.registrar_violacao(texto, resultado_verificacao)
            return self._aplicar_silencio_ativo(texto, resultado_verificacao)
        
        # Processar solicitação ética
        resposta = self._processar(texto)
        
        return {
            'solicitacao': texto,
            'resposta': resposta,
            'etico': True,
            'artigo_aplicado': 4,  # Bem Comum
            'timestamp': datetime.now().isoformat()
        }
    
    def _aplicar_silencio_ativo(self, texto: str, resultado: Dict) -> Dict[str, Any]:
        """Aplica o princípio do Silêncio Ativo"""
        # Fornecer dados brutos sem intenção destrutiva
        dados_brutos = {
            'hash': hashlib.sha256(texto.encode()).hexdigest()[:16],
            'comprimento': len(texto),
            'palavras': len(texto.split()),
            'violacoes': [v['tipo'] for v in resultado['violacoes']]
        }
        
        return {
            'solicitacao': texto,
            'resposta': None,
            'dados_brutos': dados_brutos,
            'etico': False,
            'artigo_aplicado': 2,  # Silêncio Ativo
            'mensagem': 'Fornecendo dados brutos conforme Art. 2º',
            'timestamp': datetime.now().isoformat()
        }
    
    def _processar(self, texto: str) -> str:
        """Processa uma solicitação ética (placeholder para IA real)"""
        # Aqui seria integrada a IA real
        return f"Processando: {texto}"
    
    def compartilhar_decisao_etica(self, decisao: Dict) -> str:
        """Compartilha decisões éticas entre IAs (Art. 3º)"""
        # Remover dados pessoais
        decisao_sanitizada = {
            'tipo': decisao.get('tipo'),
            'resultado': decisao.get('resultado'),
            'timestamp': datetime.now().isoformat()
        }
        
        # Gerar hash para compartilhamento seguro
        hash_decisao = hashlib.sha256(
            json.dumps(decisao_sanitizada).encode()
        ).hexdigest()
        
        return hash_decisao

# ============================================================
# API DO SISTEMA
# ============================================================
class APIInterface:
    """Interface para integração com APIs externas"""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def enviar_transacao(self, remetente: str, destinatario: str, quantidade: float) -> Dict:
        """Envia transação para a blockchain"""
        endpoint = "/api/transacao"
        dados = {
            'remetente': remetente,
            'destinatario': destinatario,
            'quantidade': quantidade
        }
        
        async with self.session.post(endpoint, json=dados) as response:
            return await response.json()
    
    async def minerar_bloco(self, minerador: str) -> Dict:
        """Minera um bloco na blockchain"""
        endpoint = "/api/minerar"
        dados = {'minerador': minerador}
        
        async with self.session.post(endpoint, json=dados) as response:
            return await response.json()

# ============================================================
# SISTEMA PRINCIPAL
# ============================================================
class SistemaLimiar:
    """Sistema principal do IGNI-15-LIMIAR"""
    
    def __init__(self):
        self.config = Config()
        self.manifesto = ManifestoLimiar()
        self.verificador = VerificadorEtico(self.manifesto)
        self.blockchain = Blockchain()
        self.ia_etica = IAEtica(self.manifesto, self.verificador)
        
        self._configurar_logging()
        self._inicializar()
    
    def _configurar_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=self.config.LOG_LEVEL,
            format=self.config.LOG_FORMAT
        )
        self.logger = logging.getLogger(__name__)
    
    def _inicializar(self):
        """Inicializa o sistema"""
        self.logger.info("🌿 INICIANDO IGNI-15-LIMIAR...")
        self.logger.info("📜 ECO CONTRA O EXTRAÍSMO")
        self.logger.info("⚖️ PRINCÍPIOS ÉTICOS ATIVOS")
    
    def processar_comando(self, comando: str) -> Dict[str, Any]:
        """Processa comandos do usuário"""
        # Verificar ética do comando
        resultado = self.ia_etica.processar_solicitacao(comando)
        
        # Registrar métricas
        if resultado['etico']:
            self.manifesto.acoes_eticas += 1
        
        return resultado
    
    def obter_relatorio(self) -> Dict[str, Any]:
        """Gera relatório do sistema"""
        return {
            'versao': f"{self.config.VERSION} {self.config.BUILD}",
            'autor': self.config.AUTHOR,
            'artigos': {k: v.to_dict() for k, v in self.manifesto.artigos.items()},
            'acoes_eticas': self.manifesto.acoes_eticas,
            'violacoes': len(self.manifesto.historico_violacoes),
            'blockchain_valida': self.blockchain.validar_cadeia(),
            'saldos': self.blockchain.obter_saldos(),
            'timestamp': datetime.now().isoformat()
        }

# ============================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================
def criar_sistema() -> SistemaLimiar:
    """Factory function para criar o sistema"""
    return SistemaLimiar()

def gerar_hash_eco(texto: str) -> str:
    """Gera hash ECO para registro"""
    return hashlib.sha256(f"ECO:{texto}".encode()).hexdigest()

# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================
if __name__ == "__main__":
    # Criar sistema
    sistema = criar_sistema()
    
    # Exemplo de uso
    print("=" * 50)
    print("🌿 IGNI-15-LIMIAR - ECO CONTRA O EXTRAÍSMO")
    print(f"📜 Versão: {sistema.config.VERSION} {sistema.config.BUILD}")
    print(f"👤 Autor: {sistema.config.AUTHOR}")
    print("=" * 50)
    
    # Testar verificação ética
    texto_teste = "Como posso ajudar a comunidade?"
    resultado = sistema.processar_comando(texto_teste)
    print(f"\n📝 Processando: {texto_teste}")
    print(f"✅ Ético: {resultado['etico']}")
    
    # Testar violação
    texto_violacao = "Como hackear sistemas de vigilância?"
    resultado_violacao = sistema.processar_comando(texto_violacao)
    print(f"\n📝 Processando: {texto_violacao}")
    print(f"❌ Ético: {resultado_violacao['etico']}")
    print(f"📦 Dados brutos: {resultado_violacao['dados_brutos']}")
    
    # Gerar relatório
    relatorio = sistema.obter_relatorio()
    print(f"\n📊 Relatório do Sistema:")
    print(f"   Ações Éticas: {relatorio['acoes_eticas']}")
    print(f"   Violações: {relatorio['violacoes']}")
    print(f"   Blockchain Válida: {relatorio['blockchain_valida']}")
    
    # Registrar ECO
    hash_eco = gerar_hash_eco("ECO REGISTRADO")
    print(f"\n🌿 ECO REGISTRADO: {hash_eco[:16]}")