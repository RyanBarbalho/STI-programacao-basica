# Estrutura de dados robusta para o especialista
MODELO_ESPECIALISTA = {
    1: { # Saída e Conceitos Iniciais
        "pesos": {
            5: ["ola mundo"],
            3: ["escreva na tela", "quebra de linha"],
            1: ["imprima", "mostre", "exiba", "frase", "texto"]
        },
        "exclusoes": ["leia", "calcule", "se", "enquanto", "vetor", "matriz", "funcao"]
    },
    2: { # Entrada e Aritmética
        "pesos": {
            5: ["leia dois", "leia tres"],
            3: ["ponto flutuante", "leia", "scanf", "media aritmetica", "resto da divisao"],
            1: ["soma", "produto", "calcule", "area", "salario", "transforme", "valor"]
        },
        "exclusoes": []
    },
    3: { # Condicionais
        "pesos": {
            5: ["se senao", "par ou impar", "maior de idade"],
            3: ["verifique se", "caso contrario", "maior que", "menor que"],
            1: ["se", "senao", "aprovado", "reprovado", "conceito"]
        },
        "exclusoes": []
    },
    4: { # Repetição
        "pesos": {
            5: ["enquanto", "for", "do while", "fatorial", "tabuada"],
            3: ["ate que", "repita", "N vezes", "sentinela"],
            1: ["laco", "soma dos n", "acumule"]
        },
        "exclusoes": []
    },
    5: { # Vetores
        "pesos": {
            5: ["vetor", "array"],
            3: ["N numeros", "conjunto de numeros", "armazene em", "ordem inversa"],
            1: ["posicao", "indice", "elementos"]
        },
        "exclusoes": ["matriz", "bidimensional"]
    },
    6: { # Matrizes
        "pesos": {
            5: ["matriz", "bidimensional"],
            3: ["tabela", "linhas e colunas", "diagonal principal", "diagonal secundaria"],
            1: ["linhas", "colunas"]
        },
        "exclusoes": []
    },
    7: { # Funções
        "pesos": {
            5: ["funcao", "procedimento", "crie uma funcao"],
            3: ["retorne", "retornar", "modularize", "passagem de parametro"],
            1: ["parametro", "chamar", "reutilizar"]
        },
        "exclusoes": ["sem usar funcao", "nao crie funcao"]
    }
}