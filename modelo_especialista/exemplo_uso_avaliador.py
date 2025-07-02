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

    # 6. Avaliação estática
    print("\n🔎 Avaliação estática...")
    resultado_estatico = avaliador.avaliar_estatico(codigo_aluno, enunciado)
    print(f"   Status: {resultado_estatico['status']}")

    # Conceitos específicos
    print(f"   Conceitos específicos verificados: {len(resultado_estatico['conceitos_especificos_verificados'])}")
    print(f"   Conceitos específicos faltantes: {len(resultado_estatico['conceitos_especificos_faltantes'])}")

    # Conceitos gerais
    print(f"   Conceitos gerais verificados: {len(resultado_estatico['conceitos_gerais_verificados'])}")
    print(f"   Conceitos gerais faltantes: {len(resultado_estatico['conceitos_gerais_faltantes'])}")

    if resultado_estatico['conceitos_especificos_verificados']:
        print("   ✓ Conceitos específicos encontrados:", ", ".join(resultado_estatico['conceitos_especificos_verificados']))

    if resultado_estatico['conceitos_especificos_faltantes']:
        print("   ❌ Conceitos específicos faltantes:", ", ".join(resultado_estatico['conceitos_especificos_faltantes']))

    if resultado_estatico['conceitos_gerais_verificados']:
        print("   ✓ Conceitos gerais encontrados:", ", ".join(resultado_estatico['conceitos_gerais_verificados']))

    if resultado_estatico['conceitos_gerais_faltantes']:
        print("   ❌ Conceitos gerais faltantes:", ", ".join(resultado_estatico['conceitos_gerais_faltantes']))

    # 7. Avaliação dinâmica (se a estática passar)
    if resultado_estatico['status'] == "APROVADO":
        print("\n🔎 Avaliação dinâmica...")
        resultado_dinamico = avaliador.avaliar_dinamico(codigo_aluno, casos_de_teste)
        print(f"   Status: {resultado_dinamico['status']}")
        if resultado_dinamico['status'] == "SUCESSO":
            print("   ✓ Todos os casos de teste passaram!")
        else:
            print(f"   ❌ {resultado_dinamico['detalhes']}")

    # 8. Avaliação completa
    print("\n🎯 Avaliação completa...")
    resultado_completo = avaliador.avaliar_completo(codigo_aluno, enunciado, casos_de_teste)
    print(f"   Status final: {resultado_completo['status']}")

    print("\n=== FIM DO EXEMPLO ===")

if __name__ == "__main__":
    exemplo_avaliacao_completa()