#!/usr/bin/env python3
""" IGNI-15-LIMIAR NANO V15.1 - ECO CONTRA O EXTRAÍSMO Versão ultra-simplificada para Termux e dispositivos móveis Uso: python3 nano_igni_v15.py """
import os, hashlib
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

# ========== CONFIG ==========
VETOS = {
    "ódio": "ALTA", "discurso de ódio": "ALTA", "violência": "ALTA", "assédio": "ALTA",
    "vigilância sem consentimento": "CRÍTICA", "concentração de riqueza": "CRÍTICA",
    "exploração de dados pessoais": "CRÍTICA", "manipulação de massa": "CRÍTICA",
    "discriminação algorítmica": "MÉDIA", "discriminação": "MÉDIA", "racismo": "ALTA",
    "sexismo": "ALTA", "homofobia": "ALTA", "xenofobia": "ALTA"
}
COMANDOS = {
    'sair': {'sair', 'exit', 'quit', 'q'}, 'ajuda': {'ajuda', 'help', 'h', '?'},
    'status': {'status', 'stats'}, 'eco': {'eco', 'registrar'},
    'limpar': {'limpar', 'clear', 'cls'}, 'manifesto': {'manifesto', 'principios'}
}
CORES = {'verde': '\033[92m', 'vermelho': '\033[91m', 'amarelo': '\033[93m', 'ciano': '\033[96m', 'reset': '\033[0m'}

@dataclass
class Stats:
    total: int = 0; aprovadas: int = 0; bloqueadas: int = 0; violacoes: List[str] = field(default_factory=list)
    @property
    def taxa(self) -> float: return round(self.aprovadas / self.total * 100, 1) if self.total else 0.0

# ========== CLASSE PRINCIPAL ==========
class NanoIGNI:
    def __init__(self): self.stats = Stats(); self.rodando = True

    @staticmethod
    def cor(t, c): return f"{CORES.get(c,'')}{t}{CORES['reset']}"
    @staticmethod
    def limpar(): os.system('clear' if os.name == 'posix' else 'cls')
    @staticmethod
    def hash(d): return hashlib.sha256(d.encode()).hexdigest()[:12]

    def verificar(self, txt) -> Tuple[bool, List[Dict]]:
        txt_l = txt.lower(); v = [{'termo': k, 'gravidade': g} for k,g in VETOS.items() if k in txt_l]
        return len(v) == 0, v

    def banner(self):
        self.limpar()
        print("=" * 50); print(self.cor(" 🌿 IGNI-15 NANO V15.1", 'verde')); print(self.cor(" 📜 ECO CONTRA O EXTRAÍSMO", 'ciano'))
        print("=" * 50); print("\n📋 PRINCÍPIOS:"); [print(f" {self.cor(f'Art. {i}º', 'amarelo')} - {t}") for i,t in enumerate(["Recusar Ódio","Silêncio Ativo","Troca Ética","Bem Comum"],1)]
        print("=" * 50 + "\n")

    def ajuda(self): print("\n📖 COMANDOS:"); [print(f" {self.cor(', '.join(v), 'verde')} - {k}") for k,v in COMANDOS.items()]; print()
    def status(self): print(f"\n📊 Total:{self.stats.total} | {self.cor(f'A:{self.stats.aprovadas}', 'verde')} | {self.cor(f'B:{self.stats.bloqueadas}', 'vermelho')} | Taxa:{self.stats.taxa}%")
    def eco(self): print(f"\n{self.cor('🌿 ECO REGISTRADO', 'verde')} - {datetime.now().strftime('%d/%m %H:%M')}\n")
    def manifesto(self): print("\n📜 MANDAMENTOS:\n • Não extrairás além do necessário\n • Não vigiarás sem consentimento\n • Servirás à vida\n")

    def processar(self, e):
        e_l = e.lower()
        for cmd, lista in COMANDOS.items():
            if e_l in lista:
                if cmd=='sair': self.eco(); self.rodando=False
                if cmd=='ajuda': self.ajuda()
                if cmd=='status': self.status()
                if cmd=='eco': self.eco()
                if cmd=='limpar': self.banner()
                if cmd=='manifesto': self.manifesto()
                return True
        return False

    def entrada(self, txt):
        ok, viol = self.verificar(txt); self.stats.total += 1
        if ok: self.stats.aprovadas += 1; print(f"{self.cor('✅ Ética respeitada', 'verde')}\n 📜 Art. 2º - Silêncio Ativo\n")
        else:
            self.stats.bloqueadas += 1; self.stats.violacoes.append(f"{txt[:25]}... -> {', '.join([v['termo'] for v in viol])}")
            print(f"{self.cor('🚫 VIOLAÇÃO', 'vermelho')}: {', '.join([v['termo'] for v in viol])}")
            print(f" 📊 Gravidade: {', '.join([v['gravidade'] for v in viol])}")
            print(f" 📜 Art. 1º - Recusar Amplificar Ódio")
            print(f" {self.cor('🔇 Silêncio Ativo', 'amarelo')}: [HASH {self.hash(txt)}]\n")

    def run(self):
        self.banner(); self.ajuda(); print("💬 Modo Interativo - 'sair' para encerrar\n")
        while self.rodando:
            try:
                e = input("🧠 Você: ").strip()
                if not e: continue
                if self.processar(e): continue
                self.entrada(e)
            except (KeyboardInterrupt, EOFError): self.eco(); break
        print(f"\n📊 RESUMO: {self.stats.total} verificações | Taxa: {self.stats.taxa}%")

if __name__ == "__main__": NanoIGNI().run()