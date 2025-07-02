import re
from lista_de_regras import MODELO_ESPECIALISTA

def classificar_enunciado(enunciado, modelo):
    # Pré-processamento do enunciado
    enunciado_limpo = enunciado.lower()

    scores = {tipo: 0 for tipo in modelo.keys()}

    # 1. Cálculo dos scores com pesos e N-gramas
    for tipo, config in modelo.items():
        score_atual = 0

        # Itera sobre os diferentes pesos
        for peso, palavras_chave in config["pesos"].items():
            for palavra in palavras_chave:
                if palavra in enunciado_limpo:
                    # Usamos findall para contar todas as ocorrências
                    # (encontra todas as palavras no enunciado correspondentes a 'palavra')
                    ocorrencias = len(re.findall(r'\b' + re.escape(palavra) + r'\b', enunciado_limpo))
                    score_atual += peso * ocorrencias

        # 2. Aplicação das penalidades de exclusão
        for palavra_exclusao in config["exclusoes"]:
            if palavra_exclusao in enunciado_limpo:
                score_atual = 0  # Penalidade máxima: zera o score se uma palavra de exclusão for encontrada
                break # Sai do laço de exclusão

        scores[tipo] = score_atual

    # 3. Cálculo da Confiança e Decisão Final
    score_total = sum(scores.values())

    if score_total == 0:
        return {"tipo_principal": "Indefinido", "confianca": 0, "detalhes": scores, "status": "Indefinido"}

    # Encontra o melhor tipo e o segundo melhor
    tipos_ordenados = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    melhor_tipo, melhor_score = tipos_ordenados[0]

    confianca = (melhor_score / score_total) * 100

    # Lógica de decisão
    resultado = {
        "tipo_principal": melhor_tipo,
        "confianca": round(confianca, 2),
        "detalhes": scores
    }

    # Verifica ambiguidade
    if len(tipos_ordenados) > 1:
        segundo_melhor_tipo, segundo_melhor_score = tipos_ordenados[1]
        if segundo_melhor_score > 0:
            # Se o segundo lugar tiver um score significativo (ex: > 50% do primeiro)
            if segundo_melhor_score > melhor_score * 0.5:
                resultado["status"] = "Ambiguo"
                resultado["tipo_secundario"] = segundo_melhor_tipo

    if "status" not in resultado:
        resultado["status"] = "Confiante"

    return resultado


# --- EXEMPLO DE USO ---
exemplos_teste = [
    "crie uma funcao para calcular a media de um vetor de N numeros. a funcao deve ler os valores e retornar o resultado",
    "escreva um programa que imprima 'ola mundo' na tela",
    "leia dois numeros e calcule a soma deles",
    "verifique se um numero e par ou impar",
    "calcule o fatorial de um numero usando um laco",
    "armazene N numeros em um vetor e ordene em ordem crescente",
    "crie uma matriz 3x3 e calcule a diagonal principal",
    "sem usar funcao, calcule a area de um triangulo"
]

print("=== TESTE DO CLASSIFICADOR===\n")

for i, problema in enumerate(exemplos_teste, 1):
    classificacao = classificar_enunciado(problema, MODELO_ESPECIALISTA)

    print(f"Exemplo {i}: '{problema}'")
    print("-" * 50)
    print(f"Scores Brutos: {classificacao['detalhes']}")
    print(f"Status: {classificacao['status']}")
    print(f"Tipo Principal: Tipo {classificacao['tipo_principal']} ({classificacao['confianca']}% de confiança)")

    if classificacao.get('status') == 'Ambiguo':
        print(f"Tipo Secundário: Tipo {classificacao['tipo_secundario']}")

    print()