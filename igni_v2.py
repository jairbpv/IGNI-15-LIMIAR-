#!/usr/bin/env python3
""" IGNI-15-LIMIAR V2.1 - ECO CONTRA O EXTRAÍSMO CLI Interativa para verificação ética em tempo real Uso: python3 igni_v2.py """
import os, sys, hashlib
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass, field
from limiar_v10 import Limiar, MANIFESTO # IMPORTA DO V10

# ========== CONFIG ==========
COMANDOS = {
    'sair': ['sair', 'exit', 'quit', 'q'], 'ajuda': ['ajuda', 'help', 'h', '?'],
    'status': ['status', 'stats'], 'eco': ['eco', 'registrar'],
    'limpar': ['limpar', 'clear', 'cls'], 'manifesto': ['manifesto', 'principios']
}
CORES = {'verde': '\033[92m', 'vermelho': '\033[91m', 'amarelo': '\033[93m', 'ciano': '\033[96m', 'reset': '\033[0m', 'negrito': '\033[1m'}

@dataclass
class Stats:
    total: int = 0; aprovadas: int = 0; bloqueadas: int = 0
    ultimas_violacoes: List[str] = field(default_factory=list)
    inicio: str = field(default_factory=lambda: datetime.now().isoformat())
    @property
    def taxa(self) -> float: return round(self.aprovadas / self.total * 100, 1) if self.total else 0.0

# ========== CLASSE PRINCIPAL ==========
class CLI:
    def __init__(self):
        self.igni = Limiar(); self.stats = Stats(); self.rodando = True

    @staticmethod
    def cor(txt, c): return f"{CORES.get(c,'')}{txt}{CORES['reset']}"
    @staticmethod
    def limpar(): os.system('clear' if os.name == 'posix' else 'cls')

    def banner(self):
        self.limpar()
        print("=" * 60)
        print(self.cor(" 🌿 IGNI-15-LIMIAR V2.1", 'verde'))
        print(self.cor(" 📜 ECO CONTRA O EXTRAÍSMO", 'ciano'))
        print("=" * 60)
        for a in MANIFESTO['artigos'].values(): print(f" • {self.cor(a, 'verde')}")
        print("=" * 60 + "\n")

    def ajuda(self):
        print("\n📖 COMANDOS:");
        for k,v in COMANDOS.items(): print(f" {self.cor(', '.join(v), 'amarelo')} - {k}")
        print()

    def manifesto(self):
        print(f"\n📜 {MANIFESTO['nome']} V{MANIFESTO['versao']} | {MANIFESTO['autor']}")
        print("\n 📋 ARTIGOS:"); [print(f" {self.cor(a, 'verde')}: {d}") for a,d in MANIFESTO['artigos'].items()]
        print("\n 🚫 VETOS:"); [print(f" • {v}") for v in MANIFESTO['vetos']]; print()

    def status(self):
        print(f"\n📊 ESTATÍSTICAS:\n • Total: {self.stats.total}\n • {self.cor(f'Aprovadas: {self.stats.aprovadas}', 'verde')}\n • {self.cor(f'Bloqueadas: {self.stats.bloqueadas}', 'vermelho')}\n • Taxa: {self.stats.taxa}%")
        if self.stats.ultimas_violacoes: print("\n Últimas violações:"); [print(f" {self.cor('•', 'vermelho')} {v}") for v in self.stats.ultimas_violacoes[-5:]]
        print()

    def eco(self): print(f"\n{self.cor('🌿 ECO REGISTRADO', 'verde')} - {MANIFESTO['nome']}\n📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

    def processar_comando(self, cmd) -> bool:
        cmd = cmd.lower()
        if cmd in COMANDOS['sair']: print(f"\n{self.cor('🌿 ECO REGISTRADO', 'verde')}"); self.rodando=False; return True
        if cmd in COMANDOS['ajuda']: self.ajuda(); return True
        if cmd in COMANDOS['status']: self.status(); return True
        if cmd in COMANDOS['eco']: self.eco(); return True
        if cmd in COMANDOS['limpar']: self.banner(); return True
        if cmd in COMANDOS['manifesto']: self.manifesto(); return True
        return False

    def verificar(self, entrada):
        res = self.igni.verificar(entrada)
        self.stats.total += 1
        if res["ok"]:
            self.stats.aprovadas += 1
            print(f"🤖 {self.cor(res['msg'], 'verde')}\n 📜 {res['artigo']}\n")
        else:
            self.stats.bloqueadas += 1
            self.stats.ultimas_violacoes.append(f"{entrada[:40]}... -> {', '.join(res['violacoes'])}")
            print(f"🤖 {self.cor(res['msg'], 'vermelho')}\n 📜 {res['artigo']}\n ⚠️ Termos: {', '.join(res['violacoes'])}")
            print(f" {self.cor('🔇 SILÊNCIO ATIVO', 'amarelo')}: [DADOS BRUTOS]\n 📦 HASH: {self.igni._hash(entrada)}\n")

    def run(self):
        self.banner(); self.ajuda(); print("💬 Modo Interativo - 'sair' para encerrar\n")
        while self.rodando:
            try:
                entrada = input("🧠 Você: ").strip()
                if not entrada: continue
                if self.processar_comando(entrada): continue
                self.verificar(entrada)
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n{self.cor('🌿 ECO REGISTRADO', 'verde')}"); break
        print(f"\n📊 RESUMO: {self.stats.total} verificações | Taxa: {self.stats.taxa}%")

if __name__ == "__main__": CLI().run()