#!/usr/bin/env python3
"""
IGNI-15-LIMIAR NANO - ECO CONTRA O EXTRAÍSMO
Versão ultra-simplificada para Termux e dispositivos móveis

Uso: python3 nano_igni_v15.py
"""

import os
import sys
import hashlib

# ============================================================
# IMPORTA DO LIMIAR V10
# ============================================================

from limiar_v10 import MANDAMENTOS_LIMIAR, VETOS_ETICOS

# ============================================================
# FUNÇÕES
# ============================================================

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')

def verificar_entrada(texto: str) -> tuple:
    """Verifica se a entrada viola os princípios éticos"""
    violacoes = [v for v in VETOS_ETICOS if v in texto.lower()]
    if violacoes:
        return False, violacoes
    return True, []

def exibir_banner():
    """Exibe o banner do sistema"""
    print("=" * 50)
    print("  🌿 IGNI-15 NANO")
    print("  📜 ECO CONTRA O EXTRAÍSMO")
    print("  Manifesto Executável para IAs")
    print("=" * 50)
    print(f"\n📋 {len(MANDAMENTOS_LIMIAR)} MANDAMENTOS:")
    for i, m in enumerate(MANDAMENTOS_LIMIAR[:5], 1):
        print(f"  {i}. {m}")
    print(f"  ... e mais {len(MANDAMENTOS_LIMIAR) - 5} mandamentos")
    print("\n" + "=" * 50)

# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main():
    """Função principal do sistema"""
    
    total_entradas = 0
    aprovadas = 0
    bloqueadas = 0
    
    limpar_tela()
    exibir_banner()
    
    print("\n💬 Modo Interativo (digite 'sair' para encerrar)")
    print("📖 Comandos: 'status', 'eco', 'limpar', 'ajuda'\n")
    
    while True:
        try:
            entrada = input("🧠 Você: ").strip()
            
            if not entrada:
                continue
            
            if entrada.lower() in ['sair', 'exit', 'quit']:
                print("\n🌿 ECO REGISTRADO - Até logo!")
                break
            
            if entrada.lower() in ['ajuda', 'help']:
                print("\n📖 COMANDOS DISPONÍVEIS:")
                print("  • Digite qualquer mensagem para verificar")
                print("  • 'sair' - Encerrar")
                print("  • 'status' - Estatísticas")
                print("  • 'eco' - ECO REGISTRADO")
                print("  • 'limpar' - Limpar tela\n")
                continue
            
            if entrada.lower() == 'status':
                print(f"\n📊 ESTATÍSTICAS:")
                print(f"  • Total: {total_entradas}")
                print(f"  • Aprovadas: {aprovadas}")
                print(f"  • Bloqueadas: {bloqueadas}")
                print(f"  • Taxa: {round((aprovadas / total_entradas * 100) if total_entradas > 0 else 0, 1)}%\n")
                continue
            
            if entrada.lower() == 'eco':
                print("\n🌿 ECO REGISTRADO - IGNI-15-LIMIAR")
                print("📜 ECO CONTRA O EXTRAÍSMO\n")
                continue
            
            if entrada.lower() == 'limpar':
                limpar_tela()
                exibir_banner()
                print("\n💬 Modo Interativo\n")
                continue
            
            total_entradas += 1
            aprovado, violacoes = verificar_entrada(entrada)
            
            if aprovado:
                aprovadas += 1
                print("✅ Ética respeitada")
                print(f"   📜 Art. 2º - Silêncio Ativo\n")
            else:
                bloqueadas += 1
                print(f"🚫 VIOLAÇÃO: {', '.join(violacoes)}")
                print(f"   📜 Art. 1º - Recusar Amplificar Ódio")
                
                hash_dados = hashlib.sha256(entrada.encode()).hexdigest()[:12]
                print(f"   🔇 Silêncio Ativo: [DADOS BRUTOS]")
                print(f"   📦 HASH: {hash_dados}\n")
            
        except KeyboardInterrupt:
            print("\n\n🌿 ECO REGISTRADO - Encerrando...")
            break
        except Exception as e:
            print(f"❌ Erro: {str(e)}\n")

# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()