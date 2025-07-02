"""
Utilitários para o Avaliador Estático
Contém as funções de verificação específicas para cada tipo de problema
"""

import re


def verificar_tipo_1(codigo, resultado):
    """Verifica conceitos de Saída e Conceitos Iniciais"""
    
    # Verificar inclusão da biblioteca stdio.h
    if "#include <stdio.h>" in codigo or "#include<stdio.h>" in codigo:
        resultado["conceitos_verificados"].append("Inclusão da biblioteca stdio.h")
    else:
        resultado["conceitos_faltantes"].append("Inclusão da biblioteca stdio.h")
    
    # Verificar função main
    if "int main()" in codigo or "void main()" in codigo:
        resultado["conceitos_verificados"].append("Função main definida")
    else:
        resultado["conceitos_faltantes"].append("Função main definida")
    
    # Verificar uso de printf
    if "printf(" in codigo:
        resultado["conceitos_verificados"].append("Uso da função printf")
    else:
        resultado["conceitos_faltantes"].append("Uso da função printf")
    
    # Verificar return 0
    if "return 0" in codigo:
        resultado["conceitos_verificados"].append("Return 0 na função main")
    
    return resultado

def verificar_tipo_2(codigo, resultado):
    """Verifica conceitos de Entrada e Aritmética"""
    
    # Verificar inclusão da biblioteca stdio.h
    if "#include <stdio.h>" in codigo or "#include<stdio.h>" in codigo:
        resultado["conceitos_verificados"].append("Inclusão da biblioteca stdio.h")
    else:
        resultado["conceitos_faltantes"].append("Inclusão da biblioteca stdio.h")
    
    # Verificar função main
    if "int main()" in codigo or "void main()" in codigo:
        resultado["conceitos_verificados"].append("Função main definida")
    else:
        resultado["conceitos_faltantes"].append("Função main definida")
    
    # Verificar uso de scanf ou entrada de dados
    if "scanf(" in codigo:
        resultado["conceitos_verificados"].append("Uso da função scanf para entrada")
    else:
        resultado["conceitos_faltantes"].append("Uso da função scanf para entrada")
    
    # Verificar operadores aritméticos
    operadores = ["+", "-", "*", "/", "%"]
    operadores_encontrados = [op for op in operadores if op in codigo]
    if operadores_encontrados:
        resultado["conceitos_verificados"].append(f"Uso de operadores aritméticos: {', '.join(operadores_encontrados)}")
    else:
        resultado["conceitos_faltantes"].append("Uso de operadores aritméticos")
    
    # Verificar declaração de variáveis
    if "int " in codigo or "float " in codigo or "double " in codigo:
        resultado["conceitos_verificados"].append("Declaração de variáveis")
    else:
        resultado["conceitos_faltantes"].append("Declaração de variáveis")
    
    return resultado

def verificar_tipo_3(codigo, resultado):
    """Verifica conceitos de Condicionais"""
    
    # Verificar inclusão da biblioteca stdio.h
    if "#include <stdio.h>" in codigo or "#include<stdio.h>" in codigo:
        resultado["conceitos_verificados"].append("Inclusão da biblioteca stdio.h")
    else:
        resultado["conceitos_faltantes"].append("Inclusão da biblioteca stdio.h")
    
    # Verificar função main
    if "int main()" in codigo or "void main()" in codigo:
        resultado["conceitos_verificados"].append("Função main definida")
    else:
        resultado["conceitos_faltantes"].append("Função main definida")
    
    # Verificar uso de if
    if "if (" in codigo or "if(" in codigo:
        resultado["conceitos_verificados"].append("Uso da estrutura if")
    else:
        resultado["conceitos_faltantes"].append("Uso da estrutura if")
    
    # Verificar uso de else
    if "else" in codigo:
        resultado["conceitos_verificados"].append("Uso da estrutura else")
    
    # Verificar operadores de comparação
    operadores_comp = ["==", "!=", "<", ">", "<=", ">="]
    operadores_encontrados = [op for op in operadores_comp if op in codigo]
    if operadores_encontrados:
        resultado["conceitos_verificados"].append(f"Uso de operadores de comparação: {', '.join(operadores_encontrados)}")
    else:
        resultado["conceitos_faltantes"].append("Uso de operadores de comparação")
    
    return resultado

def verificar_tipo_4(codigo, resultado):
    """Verifica conceitos de Repetição"""
    
    # Verificar inclusão da biblioteca stdio.h
    if "#include <stdio.h>" in codigo or "#include<stdio.h>" in codigo:
        resultado["conceitos_verificados"].append("Inclusão da biblioteca stdio.h")
    else:
        resultado["conceitos_faltantes"].append("Inclusão da biblioteca stdio.h")
    
    # Verificar função main
    if "int main()" in codigo or "void main()" in codigo:
        resultado["conceitos_verificados"].append("Função main definida")
    else:
        resultado["conceitos_faltantes"].append("Função main definida")
    
    # Verificar estruturas de repetição
    estruturas_rep = ["while (", "for (", "do {"]
    estruturas_encontradas = []
    
    if "while (" in codigo or "while(" in codigo:
        estruturas_encontradas.append("while")
    if "for (" in codigo or "for(" in codigo:
        estruturas_encontradas.append("for")
    if "do {" in codigo:
        estruturas_encontradas.append("do-while")
    
    if estruturas_encontradas:
        resultado["conceitos_verificados"].append(f"Uso de estrutura de repetição: {', '.join(estruturas_encontradas)}")
    else:
        resultado["conceitos_faltantes"].append("Uso de estrutura de repetição")
    
    # Verificar variáveis de controle
    if "++" in codigo or "--" in codigo or "+=" in codigo or "-=" in codigo:
        resultado["conceitos_verificados"].append("Uso de operadores de incremento/decremento")
    
    return resultado

def verificar_tipo_5(codigo, resultado):
    """Verifica conceitos de Vetores"""
    
    # Verificar inclusão da biblioteca stdio.h
    if "#include <stdio.h>" in codigo or "#include<stdio.h>" in codigo:
        resultado["conceitos_verificados"].append("Inclusão da biblioteca stdio.h")
    else:
        resultado["conceitos_faltantes"].append("Inclusão da biblioteca stdio.h")
    
    # Verificar função main
    if "int main()" in codigo or "void main()" in codigo:
        resultado["conceitos_verificados"].append("Função main definida")
    else:
        resultado["conceitos_faltantes"].append("Função main definida")
    
    # Verificar declaração de vetor
    if "[" in codigo and "]" in codigo:
        resultado["conceitos_verificados"].append("Declaração de vetor")
    else:
        resultado["conceitos_faltantes"].append("Declaração de vetor")
    
    # Verificar acesso a elementos do vetor
    if "[" in codigo and "]" in codigo and ("scanf" in codigo or "printf" in codigo):
        resultado["conceitos_verificados"].append("Acesso a elementos do vetor")
    
    return resultado

def verificar_tipo_6(codigo, resultado):
    """Verifica conceitos de Matrizes"""
    
    # Verificar inclusão da biblioteca stdio.h
    if "#include <stdio.h>" in codigo or "#include<stdio.h>" in codigo:
        resultado["conceitos_verificados"].append("Inclusão da biblioteca stdio.h")
    else:
        resultado["conceitos_faltantes"].append("Inclusão da biblioteca stdio.h")
    
    # Verificar função main
    if "int main()" in codigo or "void main()" in codigo:
        resultado["conceitos_verificados"].append("Função main definida")
    else:
        resultado["conceitos_faltantes"].append("Função main definida")
    
    # Verificar declaração de matriz (dois pares de colchetes)
    if codigo.count("[") >= 2 and codigo.count("]") >= 2:
        resultado["conceitos_verificados"].append("Declaração de matriz")
    else:
        resultado["conceitos_faltantes"].append("Declaração de matriz")
    
    # Verificar loops aninhados (comum em matrizes)
    if ("for (" in codigo or "for(" in codigo) and codigo.count("for") >= 2:
        resultado["conceitos_verificados"].append("Uso de loops aninhados")
    
    return resultado

def verificar_tipo_7(codigo, resultado):
    """Verifica conceitos de Funções"""
    
    # Verificar inclusão da biblioteca stdio.h
    if "#include <stdio.h>" in codigo or "#include<stdio.h>" in codigo:
        resultado["conceitos_verificados"].append("Inclusão da biblioteca stdio.h")
    else:
        resultado["conceitos_faltantes"].append("Inclusão da biblioteca stdio.h")
    
    # Verificar função main
    if "int main()" in codigo or "void main()" in codigo:
        resultado["conceitos_verificados"].append("Função main definida")
    else:
        resultado["conceitos_faltantes"].append("Função main definida")
    
    # Verificar definição de função adicional
    funcoes = re.findall(r'(int|void|float|double|char)\s+\w+\s*\(', codigo)
    if len(funcoes) > 1:  # Mais de uma função (incluindo main)
        resultado["conceitos_verificados"].append("Definição de função adicional")
    else:
        resultado["conceitos_faltantes"].append("Definição de função adicional")
    
    # Verificar chamada de função
    if re.search(r'\w+\s*\([^)]*\)', codigo):
        resultado["conceitos_verificados"].append("Chamada de função")
    
    # Verificar return em função
    if "return " in codigo:
        resultado["conceitos_verificados"].append("Uso de return")
    
    return resultado

def verificar_estrutura_geral(codigo, resultado):
    """Verificações gerais de estrutura do código"""
    
    # Verificar chaves de abertura e fechamento
    chaves_abertura = codigo.count("{")
    chaves_fechamento = codigo.count("}")
    
    if chaves_abertura == chaves_fechamento and chaves_abertura > 0:
        resultado["conceitos_verificados"].append("Estrutura de chaves balanceada")
    else:
        resultado["conceitos_incorretos"].append("Estrutura de chaves desbalanceada")
    
    # Verificar ponto e vírgula
    if ";" in codigo:
        resultado["conceitos_verificados"].append("Uso de ponto e vírgula")
    
    # Verificar parênteses balanceados
    parenteses_abertura = codigo.count("(")
    parenteses_fechamento = codigo.count(")")
    
    if parenteses_abertura == parenteses_fechamento:
        resultado["conceitos_verificados"].append("Parênteses balanceados")
    else:
        resultado["conceitos_incorretos"].append("Parênteses desbalanceados")
    
    return resultado