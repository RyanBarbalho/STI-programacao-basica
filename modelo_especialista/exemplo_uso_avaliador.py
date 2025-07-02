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
from componentes import (MODELO_ESPECIALISTA, AvaliadorCodigo,
                         classificar_enunciado)


def exemplo_avaliacao_completa():
    """
    Exemplo completo de uso do sistema de avaliação
    """
    print("=== EXEMPLO DE USO DO SISTEMA DE AVALIAÇÃO ===\n")
    
    # 1. Criar instância do avaliador
    avaliador = AvaliadorCodigo()
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
    classificacao = classificar_enunciado(enunciado, MODELO_ESPECIALISTA)
    print(f"   Tipo identificado: {classificacao['tipo_principal']}")
    print(f"   Confiança: {classificacao['confianca']:.1f}%")
    print(f"   Status: {classificacao['status']}")
    
    # 6. Avaliação estática
    print("\n📊 Avaliação estática...")
    resultado_estatico = avaliador.avaliar_estatico(codigo_aluno, enunciado)
    print(f"   Status: {resultado_estatico['status']}")
    print(f"   Conceitos verificados: {len(resultado_estatico['conceitos_verificados'])}")
    print(f"   Conceitos faltantes: {len(resultado_estatico['conceitos_faltantes'])}")
    
    if resultado_estatico['conceitos_verificados']:
        print("   ✓ Conceitos encontrados:", ", ".join(resultado_estatico['conceitos_verificados']))
    
    if resultado_estatico['conceitos_faltantes']:
        print("   ❌ Conceitos faltantes:", ", ".join(resultado_estatico['conceitos_faltantes']))
    
    # 7. Avaliação dinâmica (se a estática passar)
    if resultado_estatico['status'] == "APROVADO":
        print("\n⚡ Avaliação dinâmica...")
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

def exemplo_classificacao():
    """
    Exemplo de uso apenas da classificação
    """
    print("\n=== EXEMPLO DE CLASSIFICAÇÃO ===\n")
    
    exemplos = [
        "escreva um programa que imprima 'ola mundo' na tela",
        "leia dois numeros e calcule a soma deles",
        "verifique se um numero e par ou impar",
        "calcule o fatorial de um numero usando um laco",
        "armazene N numeros em um vetor e ordene em ordem crescente",
        "crie uma matriz 3x3 e calcule a diagonal principal",
        "crie uma funcao para calcular a media de um vetor"
    ]
    
    for i, exemplo in enumerate(exemplos, 1):
        classificacao = classificar_enunciado(exemplo, MODELO_ESPECIALISTA)
        print(f"Exemplo {i}: '{exemplo}'")
        print(f"   Tipo: {classificacao['tipo_principal']} | Confiança: {classificacao['confianca']:.1f}% | Status: {classificacao['status']}")
        print()


if __name__ == "__main__":
    exemplo_avaliacao_completa()
    exemplo_classificacao() 