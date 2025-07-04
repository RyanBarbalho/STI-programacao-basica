"""
Utilitários para o Avaliador Estático
Contém as funções de verificação específicas para cada tipo de problema
"""

import re



def verificar_tipo_1(codigo, resultado):
    """Verifica conceitos de Saída e Conceitos Iniciais"""

    # Verificar uso de printf com regex
    if re.search(r'\bprintf\s*\([^)]*\)', codigo):
        resultado["conceitos_especificos_verificados"].append("Uso da função printf")
    else:
        resultado["conceitos_especificos_faltantes"].append("Uso da função printf")

    return resultado

def verificar_tipo_2(codigo, resultado):
    """Verifica conceitos de Entrada e Aritmética"""

    # Verificar uso de scanf com regex
    if re.search(r'\bscanf\s*\([^)]*\)', codigo):
        resultado["conceitos_especificos_verificados"].append("Uso da função scanf para entrada")
    else:
        resultado["conceitos_especificos_faltantes"].append("Uso da função scanf para entrada")

    # Verificar operadores aritméticos com regex
    operadores = ["+", "-", "*", "/", "%"]
    operadores_encontrados = []
    for op in operadores:
        # Evitar capturar operadores em strings ou comentários
        if re.search(rf'(?<!["\']){re.escape(op)}(?!["\'])', codigo):
            operadores_encontrados.append(op)

    if operadores_encontrados:
        resultado["conceitos_especificos_verificados"].append(f"Uso de operadores aritméticos: {', '.join(operadores_encontrados)}")
    else:
        resultado["conceitos_especificos_faltantes"].append("Uso de operadores aritméticos")

    # Verificar declaração de variáveis com regex
    if re.search(r'\b(int|float|double|char)\s+\w+', codigo):
        resultado["conceitos_especificos_verificados"].append("Declaração de variáveis")
    else:
        resultado["conceitos_especificos_faltantes"].append("Declaração de variáveis")

    return resultado

def verificar_tipo_3(codigo, resultado):
    """Verifica conceitos de Condicionais"""

    # Verificar uso de if com regex mais inteligente
    if re.search(r'\bif\s*\([^)]*\)', codigo):
        resultado["conceitos_especificos_verificados"].append("Uso da estrutura if")
    else:
        resultado["conceitos_especificos_faltantes"].append("Uso da estrutura if")

    # Verificar uso de else com regex
    if re.search(r'\belse\b', codigo):
        resultado["conceitos_especificos_verificados"].append("Uso da estrutura else")

    # Verificar operadores de comparação com regex
    operadores_comp = ["==", "!=", "<", ">", "<=", ">="]
    operadores_encontrados = []
    for op in operadores_comp:
        if re.search(rf'(?<!["\']){re.escape(op)}(?!["\'])', codigo):
            operadores_encontrados.append(op)

    if operadores_encontrados:
        resultado["conceitos_especificos_verificados"].append(f"Uso de operadores de comparação: {', '.join(operadores_encontrados)}")
    else:
        resultado["conceitos_especificos_faltantes"].append("Uso de operadores de comparação")

    return resultado

def verificar_tipo_4(codigo, resultado):
    """Verifica conceitos de Repetição"""

    # Verificar estruturas de repetição com regex
    estruturas_encontradas = []

    if re.search(r'\bwhile\s*\([^)]*\)', codigo):
        estruturas_encontradas.append("while")
    if re.search(r'\bfor\s*\([^)]*\)', codigo):
        estruturas_encontradas.append("for")
    if re.search(r'\bdo\s*\{', codigo):
        estruturas_encontradas.append("do-while")

    if estruturas_encontradas:
        resultado["conceitos_especificos_verificados"].append(f"Uso de estrutura de repetição: {', '.join(estruturas_encontradas)}")
    else:
        resultado["conceitos_especificos_faltantes"].append("Uso de estrutura de repetição")

    # Verificar variáveis de controle com regex
    if re.search(r'\b(\+\+|--|\+=|-=)\b', codigo):
        resultado["conceitos_especificos_verificados"].append("Uso de operadores de incremento/decremento")

    return resultado

def verificar_tipo_5(codigo, resultado):
    """Verifica conceitos de Vetores"""

    # Verificar declaração de vetor
    if "[" in codigo and "]" in codigo:
        resultado["conceitos_especificos_verificados"].append("Declaração de vetor")
    else:
        resultado["conceitos_especificos_faltantes"].append("Declaração de vetor")

    # Verificar acesso a elementos do vetor
    if "[" in codigo and "]" in codigo and ("scanf" in codigo or "printf" in codigo):
        resultado["conceitos_especificos_verificados"].append("Acesso a elementos do vetor")

    return resultado

def verificar_tipo_6(codigo, resultado):
    """Verifica conceitos de Matrizes"""

    # Verificar declaração de matriz (dois pares de colchetes)
    if codigo.count("[") >= 2 and codigo.count("]") >= 2:
        resultado["conceitos_especificos_verificados"].append("Declaração de matriz")
    else:
        resultado["conceitos_especificos_faltantes"].append("Declaração de matriz")

    # Verificar loops aninhados (comum em matrizes)
    if ("for (" in codigo or "for(" in codigo) and codigo.count("for") >= 2:
        resultado["conceitos_especificos_verificados"].append("Uso de loops aninhados")

    return resultado

def verificar_tipo_7(codigo, resultado):
    """Verifica conceitos de Funções"""

    # Verificar definição de função adicional (excluindo main)
    funcoes = re.findall(r'(int|void|float|double|char)\s+(\w+)\s*\(', codigo)
    funcoes_adicionais = [f[1] for f in funcoes if f[1].lower() != 'main']

    if funcoes_adicionais:
        resultado["conceitos_especificos_verificados"].append("Definição de função adicional")
    else:
        resultado["conceitos_especificos_faltantes"].append("Definição de função adicional")

    # Verificar chamada de função (excluindo printf, scanf, main)
    chamadas = re.findall(r'\b(\w+)\s*\([^)]*\)', codigo)
    chamadas_validas = [c for c in chamadas if c.lower() not in ['printf', 'scanf', 'main']]

    if chamadas_validas:
        resultado["conceitos_especificos_verificados"].append("Chamada de função")

    # Verificar return em função (excluindo return 0)
    if re.search(r'\breturn\s+(?!0\b)', codigo):
        resultado["conceitos_especificos_verificados"].append("Uso de return")

    return resultado

def verificar_estrutura_geral(codigo, resultado):
    """Verificações gerais de estrutura do código"""
    # Verificar chaves de abertura e fechamento
    chaves_abertura = codigo.count("{")
    chaves_fechamento = codigo.count("}")

    if chaves_abertura == chaves_fechamento and chaves_abertura > 0:
        resultado["conceitos_gerais_verificados"].append("Estrutura de chaves balanceada")
    else:
        resultado["conceitos_incorretos"].append("Estrutura de chaves desbalanceada")

    # Verificar ponto e vírgula (mais inteligente)
    if re.search(r'[^;]\s*;', codigo):
        resultado["conceitos_gerais_verificados"].append("Uso de ponto e vírgula")
    else:
        resultado["conceitos_gerais_faltantes"].append("Uso de ponto e vírgula")

    # Verificar parênteses balanceados
    parenteses_abertura = codigo.count("(")
    parenteses_fechamento = codigo.count(")")

    if parenteses_abertura == parenteses_fechamento:
        resultado["conceitos_gerais_verificados"].append("Parênteses balanceados")
    else:
        resultado["conceitos_incorretos"].append("Parênteses desbalanceados")

    return resultado