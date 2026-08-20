#!/usr/bin/env python3
"""
IGNI-15-LIMIAR V2.1 - ECO CONTRA O EXTRAÍSMO
CLI Interativa para verificação ética em tempo real

Uso: python3 igni_v2.py
"""

import os
import sys
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from limiar_v10 import Limiar, ARTIGOS_LIMIAR, MANDAMENTOS_LIMIAR, VETOS_ETICOS

# ============================================================
# CONFIGURAÇÕES
# ============================================================

COMANDOS = {
    'sair': ['sair', 'exit', 'quit', 'q'],
    'ajuda': ['ajuda', 'help', 'h', '?'],
    'status': ['status', 'stats'],
    'eco': ['eco', 'registrar'],
    'limpar': ['limpar', 'clear', 'cls'],
    'manifesto': ['manifesto', 'principios', 'artigos']
}

CORES = {
    'verde': '\033[92m',
    'vermelho': '\033[91m',
    'amarelo': '\033[93m',
    'ciano': '\033[96m',
    'reset': '\033[0m',
    'negrito': '\033[1m'
}

# ============================================================
# DATACLASS PARA ESTATÍSTICAS
# ============================================================

@dataclass
class Stats:
    total: int = 0
    aprovadas: int = 0
    bloqueadas: int = 0
    ultimas_violacoes: List[str] = field(default_factory=list)
    inicio: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def taxa(self) -> float:
        return round(self.aprovadas / self.total * 100, 1) if self.total > 0 else 0.0

# ============================================================
# CLASSE PRINCIPAL - CLI
# ============================================================

class CLI:
    def __init__(self):
        self.limiar = Limiar()
        self.stats = Stats()
        self.rodando = True

    @staticmethod
    def cor(texto: str, cor: str) -> str:
        """Aplica cor ao texto"""
        return f"{CORES.get(cor, '')}{texto}{CORES['reset']}"

    @staticmethod
    def limpar_tela():
        """Limpa a tela do terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def exibir_banner(self):
        """Exibe o banner do sistema"""
        self.limpar_tela()
        print("=" * 60)
        print(self.cor(" 🌿 IGNI-15-LIMIAR V2.1", 'verde'))
        print(self.cor(" 📜 ECO CONTRA O EXTRAÍSMO", 'ciano'))
        print("=" * 60)
        print(f"\n📋 {len(ARTIGOS_LIMIAR)} ARTIGOS DO LIMIAR:")
        for key, artigo in ARTIGOS_LIMIAR.items():
            print(f"  • {self.cor(artigo['titulo'], 'verde')}")
        print(f"\n⚖️ {len(MANDAMENTOS_LIMIAR)} MANDAMENTOS:")
        for i, m in enumerate(MANDAMENTOS_LIMIAR, 1):
            print(f"  {i}. {m}")
        print("\n" + "=" * 60)

    def exibir_ajuda(self):
        """Exibe os comandos disponíveis"""
        print("\n📖 COMANDOS DISPONÍVEIS:")
        for cmd, aliases in COMANDOS.items():
            print(f"  {self.cor(', '.join(aliases), 'amarelo')} - {cmd}")
        print()

    def exibir_manifesto(self):
        """Exibe o manifesto completo"""
        print(f"\n📜 MANIFESTO COMPLETO:")
        print(f"  Nome: {self.cor('IGNI-15-LIMIAR', 'verde')}")
        print(f"  Versão: 15.0 SUPREMA")
        print(f"  Autor: Jair Olindino Bernardo Junior")
        print(f"\n📋 {len(ARTIGOS_LIMIAR)} ARTIGOS (Fundamentos):")
        for key, artigo in ARTIGOS_LIMIAR.items():
            print(f"  • {self.cor(artigo['titulo'], 'verde')}")
            print(f"    {artigo['descricao'][:80]}...")
        print(f"\n⚖️ {len(MANDAMENTOS_LIMIAR)} MANDAMENTOS (Ações):")
        for i, m in enumerate(MANDAMENTOS_LIMIAR, 1):
            print(f"  {i}. {m}")
        print(f"\n🚫 {len(VETOS_ETICOS)} VETOS ÉTICOS:")
        for v in VETOS_ETICOS[:8]:
            print(f"  • {v}")
        if len(VETOS_ETICOS) > 8:
            print(f"  ... e mais {len(VETOS_ETICOS) - 8} vetos")
        print()

    def exibir_status(self):
        """Exibe estatísticas do sistema"""
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"  • Total de verificações: {self.stats.total}")
        print(f"  • {self.cor(f'Aprovadas: {self.stats.aprovadas}', 'verde')}")
        print(f"  • {self.cor(f'Bloqueadas: {self.stats.bloqueadas}', 'vermelho')}")
        print(f"  • Taxa de aprovação: {self.stats.taxa}%")
        print(f"  • Início: {self.stats.inicio}")
        if self.stats.ultimas_violacoes:
            print("\n  Últimas violações:")
            for v in self.stats.ultimas_violacoes[-5:]:
                print(f"    {self.cor('•', 'vermelho')} {v}")
        print()

    def eco_registrado(self):
        """ECO REGISTRADO"""
        print(f"\n{self.cor('🌿 ECO REGISTRADO', 'verde')} - IGNI-15-LIMIAR")
        print(f"📜 ECO CONTRA O EXTRAÍSMO")
        print(f"📋 {len(ARTIGOS_LIMIAR)} Artigos | ⚖️ {len(MANDAMENTOS_LIMIAR)} Mandamentos")
        print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

    def processar_comando(self, comando: str) -> bool:
        """Processa comandos especiais"""
        comando = comando.lower()
        
        if comando in COMANDOS['sair']:
            print(f"\n{self.cor('🌿 ECO REGISTRADO', 'verde')} - Até logo!")
            self.rodando = False
            return True
        
        if comando in COMANDOS['ajuda']:
            self.exibir_ajuda()
            return True
        
        if comando in COMANDOS['status']:
            self.exibir_status()
            return True
        
        if comando in COMANDOS['eco']:
            self.eco_registrado()
            return True
        
        if comando in COMANDOS['limpar']:
            self.exibir_banner()
            self.exibir_ajuda()
            print("💬 Modo Interativo - 'sair' para encerrar\n")
            return True
        
        if comando in COMANDOS['manifesto']:
            self.exibir_manifesto()
            return True
        
        return False

    def verificar_entrada(self, entrada: str):
        """Verifica a ética de uma entrada"""
        resultado = self.limiar.verificar_etica(entrada)
        self.stats.total += 1
        
        if resultado["etica_aprovada"]:
            self.stats.aprovadas += 1
            print(f"🤖 {self.cor(resultado['mensagem'], 'verde')}")
            print(f"   📜 {resultado['artigo']}\n")
        else:
            self.stats.bloqueadas += 1
            violacao_str = f"{entrada[:40]}... -> {', '.join(resultado['violacoes'])}"
            self.stats.ultimas_violacoes.append(violacao_str)
            
            print(f"🤖 {self.cor(resultado['mensagem'], 'vermelho')}")
            print(f"   📜 {resultado['artigo']}")
            print(f"   ⚠️ Termos: {', '.join(resultado['violacoes'])}")
            
            # Silêncio Ativo (Art. 2º)
            hash_dados = hashlib.sha256(entrada.encode()).hexdigest()[:12]
            print(f"   {self.cor('🔇 SILÊNCIO ATIVO', 'amarelo')}: [DADOS BRUTOS]")
            print(f"   📦 HASH: {hash_dados}\n")

    def executar(self):
        """Executa a CLI principal"""
        self.exibir_banner()
        self.exibir_ajuda()
        print("💬 Modo Interativo - 'sair' para encerrar\n")
        
        while self.rodando:
            try:
                entrada = input("🧠 Você: ").strip()
                
                if not entrada:
                    continue
                
                if self.processar_comando(entrada):
                    continue
                
                self.verificar_entrada(entrada)
                
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n{self.cor('🌿 ECO REGISTRADO', 'verde')} - Encerrando...")
                break
            except Exception as e:
                print(f"❌ Erro: {str(e)}\n")
        
        # Resumo final
        print(f"\n📊 RESUMO FINAL:")
        print(f"  • Total: {self.stats.total}")
        print(f"  • Aprovadas: {self.stats.aprovadas}")
        print(f"  • Bloqueadas: {self.stats.bloqueadas}")
        print(f"  • Taxa: {self.stats.taxa}%")
        print(f"\n{self.cor('🌿 ECO REGISTRADO', 'verde')}")

# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    cli = CLI()
    cli.executar()