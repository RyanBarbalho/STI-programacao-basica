#!/usr/bin/env python3
"""
Script para rodar todos os casos de teste da base de casos
"""

import json
import os
import sys
from pathlib import Path

# Adiciona o diretório modelo_especialista ao sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
modelo_dir = os.path.join(current_dir, 'modelo_especialista')
sys.path.insert(0, modelo_dir)

from modelo_especialista.componentes.avaliador_codigo import AvaliadorCodigo


def rodar_casos_tipo(tipo_problema):
    """Roda todos os casos de teste de um tipo específico"""
    arquivo_json = f"modelo_especialista/base_de_casos/tipo_{tipo_problema}.json"

    if not os.path.exists(arquivo_json):
        print(f"❌ Arquivo {arquivo_json} não encontrado!")
        return

    print(f"\n{'='*60}")
    print(f"📋 TESTANDO CASOS DO TIPO {tipo_problema}")
    print(f"{'='*60}")

    # Carregar casos de teste
    with open(arquivo_json, 'r', encoding='utf-8') as f:
        casos = json.load(f)

    # Criar avaliador
    avaliador = AvaliadorCodigo()

    # Contadores
    total_casos = len(casos)
    casos_sucesso = 0
    casos_falha = 0

    # Testar cada caso
    for i, caso in enumerate(casos, 1):
        print(f"\n🔍 Caso {i}/{total_casos}: {caso['id']}")
        print(f"   📝 Enunciado: {caso['enunciado'][:80]}...")

        # Extrair dados do caso
        codigo_aluno = caso['solucao']
        enunciado = caso['enunciado']
        casos_de_teste = caso['casos_de_teste']

        # Avaliar o código
        try:
            resultado = avaliador.avaliar_completo(codigo_aluno, enunciado, casos_de_teste)

            # Exibir resultado
            print(f"   📊 Status: {resultado['status']}")

            # Detalhes da análise estática
            estatica = resultado['avaliacao_estatica']
            print(f"   📈 Conceitos específicos: {len(estatica['conceitos_especificos_verificados'])}/{len(estatica['conceitos_especificos_verificados']) + len(estatica['conceitos_especificos_faltantes'])}")
            print(f"   📈 Conceitos gerais: {len(estatica['conceitos_gerais_verificados'])}/{len(estatica['conceitos_gerais_verificados']) + len(estatica['conceitos_gerais_faltantes'])}")

            # Detalhes da análise dinâmica
            dinamica = resultado['avaliacao_dinamica']
            if dinamica:
                print(f"   🚀 Execução: {dinamica['status']}")

            # Mostrar conceitos específicos encontrados
            if estatica['conceitos_especificos_verificados']:
                print(f"   ✅ Conceitos específicos: {', '.join(estatica['conceitos_especificos_verificados'])}")

            # Mostrar conceitos específicos faltantes
            if estatica['conceitos_especificos_faltantes']:
                print(f"   ❌ Conceitos específicos faltantes: {', '.join(estatica['conceitos_especificos_faltantes'])}")

            # Mostrar feedback alternativo se aplicável
            if resultado['status'] == "SUCESSO_ALTERNATIVO":
                print(f"   💡 Observação: {resultado['observacao']}")
                if 'feedback_alternativo' in resultado:
                    for feedback in resultado['feedback_alternativo']:
                        print(f"   💡 {feedback}")

            # Contar sucessos/falhas
            if resultado['status'] in ['SUCESSO', 'SUCESSO_ALTERNATIVO']:
                casos_sucesso += 1
                print(f"   ✅ SUCESSO")
            else:
                casos_falha += 1
                print(f"   ❌ FALHA")
                if 'detalhes' in resultado:
                    print(f"   📋 Detalhes: {resultado['detalhes']}")

        except Exception as e:
            casos_falha += 1
            print(f"   ❌ ERRO: {str(e)}")

    # Resumo do tipo
    print(f"\n📊 RESUMO TIPO {tipo_problema}:")
    print(f"   Total de casos: {total_casos}")
    print(f"   Sucessos: {casos_sucesso}")
    print(f"   Falhas: {casos_falha}")
    print(f"   Taxa de sucesso: {(casos_sucesso/total_casos)*100:.1f}%")

    return casos_sucesso, casos_falha


def main():
    """Função principal"""
    print("🚀 INICIANDO TESTES DE TODOS OS CASOS")
    print("="*60)

    # Verificar se o GCC está disponível
    try:
        import subprocess
        subprocess.run(['gcc', '--version'], capture_output=True, check=True)
        print("✅ GCC encontrado - compilação disponível")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  GCC não encontrado - apenas análise estática será executada")

    # Contadores globais
    total_sucessos = 0
    total_falhas = 0
    total_casos = 0

    # Testar todos os tipos (1 a 7)
    for tipo in range(1, 8):
        sucessos, falhas = rodar_casos_tipo(tipo)
        total_sucessos += sucessos
        total_falhas += falhas
        total_casos += sucessos + falhas

    # Resumo final
    print(f"\n{'='*60}")
    print("📊 RESUMO FINAL")
    print(f"{'='*60}")
    print(f"   Total de casos testados: {total_casos}")
    print(f"   Total de sucessos: {total_sucessos}")
    print(f"   Total de falhas: {total_falhas}")
    if total_casos > 0:
        print(f"   Taxa de sucesso geral: {(total_sucessos/total_casos)*100:.1f}%")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()