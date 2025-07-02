#!/usr/bin/env python3
"""
Exemplo de uso do Avaliador de Código
Demonstra como usar o avaliador estático e dinâmico
"""

import json
import os
import sys
import time

import requests

# Adiciona o diretório componentes ao sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
componentes_dir = os.path.join(current_dir, 'componentes')
sys.path.insert(0, componentes_dir)

# Imports do sistema
from componentes import (BASE_DE_REGRAS, AvaliadorCodigo, ClassificadorCodigo)


def exemplo_avaliacao_completa():
    """
    Exemplo completo de uso do sistema de avaliação
    """
    print("=== EXEMPLO DE USO DO SISTEMA DE AVALIAÇÃO ===\n")

    # 1. Criar instância do avaliador
    avaliador = AvaliadorCodigo()
    classificador = ClassificadorCodigo(BASE_DE_REGRAS)
    print("✓ Avaliador criado com sucesso")

    # 2. Exemplo de código do aluno
    codigo_aluno = """
#include <stdio.h>

int main() {
    printf("Hello World\\n");
    return 0;
}
"""

    # 3. Exemplo de enunciado
    enunciado = "escreva um programa que imprima 'Hello World' na tela"

    # 4. Exemplo de casos de teste
    casos_de_teste = [
        {
            "entrada": "",
            "saida_esperada": "Hello World"
        }
    ]

    print(f"📝 Enunciado: {enunciado}")
    print(f"💻 Código do aluno:\n{codigo_aluno}")

    # 5. Classificar o enunciado
    print("\n🔍 Classificando enunciado...")
    classificacao = classificador.classificar_enunciado(enunciado)
    print(f"   Tipo identificado: {classificacao['tipo_principal']}")
    print(f"   Confiança: {classificacao['confianca']:.1f}%")
    print(f"   Status: {classificacao['status']}")

        # 6. Avaliação completa
    print("\n🎯 AVALIAÇÃO COMPLETA")
    resultado_completo = avaliador.avaliar_completo(codigo_aluno, enunciado, casos_de_teste)

    # Status principal
    print(f"   Status: {resultado_completo['status']}")

    # Detalhes da análise estática
    estatica = resultado_completo['avaliacao_estatica']
    print(f"   📊 Conceitos específicos: {len(estatica['conceitos_especificos_verificados'])}/{len(estatica['conceitos_especificos_verificados']) + len(estatica['conceitos_especificos_faltantes'])}")
    print(f"   📊 Conceitos gerais: {len(estatica['conceitos_gerais_verificados'])}/{len(estatica['conceitos_gerais_verificados']) + len(estatica['conceitos_gerais_faltantes'])}")

    # Detalhes da análise dinâmica
    dinamica = resultado_completo['avaliacao_dinamica']
    if dinamica:
        print(f"   🚀 Execução: {dinamica['status']}")

    # Mostrar conceitos específicos encontrados
    if estatica['conceitos_especificos_verificados']:
        print(f"   ✅ Conceitos específicos: {', '.join(estatica['conceitos_especificos_verificados'])}")

    # Mostrar conceitos específicos faltantes
    if estatica['conceitos_especificos_faltantes']:
        print(f"   ❌ Conceitos específicos faltantes: {', '.join(estatica['conceitos_especificos_faltantes'])}")

    # Mostrar feedback alternativo se aplicável
    if resultado_completo['status'] == "SUCESSO_ALTERNATIVO":
        print(f"   💡 Observação: {resultado_completo['observacao']}")
        if 'feedback_alternativo' in resultado_completo:
            for feedback in resultado_completo['feedback_alternativo']:
                print(f"   💡 {feedback}")

    print("\n=== FIM DO EXEMPLO ===")

if __name__ == "__main__":
    exemplo_avaliacao_completa()