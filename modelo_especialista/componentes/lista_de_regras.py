BASE_DE_REGRAS = {
    1: { # Saída e Conceitos Iniciais
        "pesos": {
            5: [
                "ola mundo", "hello world", "primeiro programa", "programa basico",
                "escreva ola mundo", "imprima ola mundo", "mostre ola mundo"
            ],
            3: [
                "escreva na tela", "quebra de linha", "print", "printf", "cout",
                "escreva uma mensagem", "imprima uma frase", "mostre um texto",
                "exiba na tela", "saida de dados", "output", "mensagem na tela",
                "nova linha", "endl", "\n", "pular linha", "quebrar linha",
                "imprima exatamente", "frase exata", "mensagem exata"
            ],
            1: [
                "imprima", "mostre", "exiba", "frase", "texto", "nome", "mensagem",
                "palavra", "string", "caractere", "char", "saida", "tela", "console",
                "terminal", "escrever", "escreva", "apresente", "apresentar",
                "demonstre", "demonstrar", "visualize", "visualizar"
            ]
        },
        "exclusoes": [
            "leia", "calcule", "se", "enquanto", "vetor", "matriz", "funcao",
            "input", "scanf", "cin", "entrada", "ler", "receber", "capturar",
            "condicional", "repeticao", "laco", "array", "procedimento"
        ]
    },

    2: { # Entrada e Aritmética
        "pesos": {
            5: [
                "leia dois", "leia tres", "leia dois numeros", "leia tres numeros",
                "entrada de dois valores", "entrada de tres valores",
                "scanf dois numeros", "cin dois numeros", "input dois valores"
            ],
            3: [
                "ponto flutuante", "leia", "scanf", "cin", "media aritmetica",
                "resto da divisao", "modulo", "divisao inteira", "divisao real",
                "soma de dois numeros", "produto de dois numeros", "diferenca",
                "subtracao", "multiplicacao", "divisao", "potenciacao", "raiz",
                "quadrado", "cubo", "elevado", "potencia", "raiz quadrada",
                "raiz cubica", "media", "media simples", "aritmetica",
                "operacao matematica", "calculo basico", "operador aritmetico",
                "calcular area", "calcular perimetro", "calcular volume",
                "area do triangulo", "area do retangulo", "area do circulo",
                "area do quadrado", "perimetro do triangulo", "perimetro do retangulo",
                "perimetro do circulo", "perimetro do quadrado"
            ],
            1: [
                "soma", "produto", "calcule", "area", "salario", "transforme", "valor",
                "numero", "inteiro", "float", "double", "real", "decimal",
                "positivo", "negativo", "par", "impar", "primo", "perfeito",
                "quadrado perfeito", "cubo perfeito", "fatorial", "fibonacci",
                "sequencia", "serie", "progressao", "termo", "soma dos termos",
                "produto dos termos", "media dos termos", "maior", "menor",
                "maximo", "minimo", "ordenar", "ordenacao", "crescente",
                "decrescente", "ascendente", "descendente", "calcular", "calculo",
                "triangulo", "retangulo", "circulo", "quadrado", "perimetro",
                "volume", "superficie", "base", "altura", "raio", "diametro",
                "comprimento", "largura", "formula", "equacao", "expressao matematica"
            ]
        },
        "exclusoes": [
            "vetor", "matriz", "array", "lista", "conjunto", "colecao",
            "repeticao", "laco", "enquanto", "for", "do while", "condicional",
            "if", "else", "switch", "case"
        ]
    },

    3: { # Condicionais
        "pesos": {
            5: [
                "se senao", "if else", "par ou impar", "maior de idade",
                "verificar paridade", "verificar idade", "verificar aprovacao",
                "verificar conceito", "verificar nota", "verificar status",
                "verificar situacao", "verificar condicao", "verificar estado",
                "verificar categoria", "verificar tipo", "verificar classe"
            ],
            3: [
                "verifique se", "caso contrario", "maior que", "menor que",
                "igual a", "diferente de", "maior ou igual", "menor ou igual",
                "comparacao", "comparar", "testar", "teste", "verificacao",
                "verificar", "checar", "checagem", "validar", "validacao",
                "condicional", "condicao", "se verdadeiro", "se falso",
                "caso seja", "caso nao seja", "quando", "quando nao",
                "desde que", "a menos que", "exceto se", "a nao ser que"
            ],
            1: [
                "se", "senao", "if", "else", "aprovado", "reprovado", "conceito",
                "nota", "media", "situacao", "status", "resultado", "resposta",
                "decisao", "escolha", "opcao", "alternativa", "possibilidade",
                "chance", "probabilidade", "criterio", "padrao", "regra",
                "condicao", "requisito", "exigencia", "limite", "limiar",
                "valor de corte", "ponto de corte", "linha divisoria"
            ]
        },
        "exclusoes": [
            "repeticao", "laco", "enquanto", "for", "do while", "repita",
            "ate que", "sentinela", "iteracao", "ciclo", "loop"
        ]
    },

    4: { # Repetição
        "pesos": {
            5: [
                "enquanto", "while", "for", "do while", "fatorial", "tabuada",
                "soma dos n primeiros", "produto dos n primeiros",
                "sequencia de fibonacci", "serie de fibonacci",
                "progressao aritmetica", "progressao geometrica",
                "soma de uma serie", "produto de uma serie",
                "calculo de serie", "calculo de sequencia"
            ],
            3: [
                "ate que", "repita", "N vezes", "sentinela", "iteracao",
                "ciclo", "loop", "repetir", "repeticao", "contador",
                "contagem", "contar", "incremento", "decremento",
                "acumulador", "acumular", "soma acumulada", "produto acumulado",
                "media acumulada", "maximo ate agora", "minimo ate agora",
                "maior ate agora", "menor ate agora", "primeiro", "ultimo",
                "anterior", "proximo", "sucessor", "antecessor"
            ],
            1: [
                "laco", "soma dos n", "acumule", "soma", "produto", "media",
                "contador", "contagem", "numero de vezes", "quantidade",
                "frequencia", "ocorrencia", "aparicao", "presenca",
                "existencia", "disponibilidade", "disponivel", "encontrado",
                "localizado", "identificado", "detectado", "reconhecido"
            ]
        },
        "exclusoes": [
            "vetor", "matriz", "array", "lista", "conjunto", "colecao",
            "funcao", "procedimento", "modulo", "subprograma"
        ]
    },

    5: { # Vetores
        "pesos": {
            5: [
                "vetor", "array", "lista", "conjunto de numeros", "sequencia de numeros",
                "armazenar numeros", "guardar numeros", "salvar numeros",
                "colecao de numeros", "serie de numeros", "sequencia de valores"
            ],
            3: [
                "N numeros", "conjunto de numeros", "armazene em", "ordem inversa",
                "posicao", "indice", "elementos", "tamanho do vetor",
                "dimensao do vetor", "comprimento do vetor", "numero de elementos",
                "quantidade de elementos", "total de elementos", "soma dos elementos",
                "produto dos elementos", "media dos elementos", "maior elemento",
                "menor elemento", "maximo", "minimo", "ordenar vetor",
                "ordenacao do vetor", "buscar no vetor", "procurar no vetor",
                "encontrar no vetor", "localizar no vetor", "verificar no vetor"
            ],
            1: [
                "posicao", "indice", "elementos", "valor", "dado", "informacao",
                "item", "entrada", "registro", "campo", "atributo", "propriedade",
                "caracteristica", "qualidade", "aspecto", "fator", "elemento",
                "componente", "parte", "pedaco", "fragmento", "secao", "segmento"
            ]
        },
        "exclusoes": [
            "matriz", "bidimensional", "tabela", "linhas e colunas",
            "diagonal principal", "diagonal secundaria", "linhas", "colunas",
            "duas dimensoes", "2d", "2-d", "duas dimensoes"
        ]
    },

    6: { # Matrizes
        "pesos": {
            5: [
                "matriz", "bidimensional", "tabela", "grade", "quadro",
                "duas dimensoes", "2d", "2-d", "linhas e colunas",
                "tabela de numeros", "grade de numeros", "quadro de numeros"
            ],
            3: [
                "tabela", "linhas e colunas", "diagonal principal", "diagonal secundaria",
                "linhas", "colunas", "posicao da matriz",
                "elemento da matriz", "valor da matriz", "dimensao da matriz",
                "tamanho da matriz", "ordem da matriz", "matriz quadrada",
                "matriz retangular", "matriz triangular", "matriz identidade",
                "matriz nula", "matriz transposta", "soma de matrizes",
                "produto de matrizes", "multiplicacao de matrizes",
                "determinante", "inversa", "adjunta", "cofator"
            ],
            1: [
                "linhas", "colunas", "posicao", "indice",
                "elemento", "valor", "dado", "informacao", "item", "entrada",
                "registro", "campo", "atributo", "propriedade", "caracteristica",
                "qualidade", "aspecto", "fator", "componente", "parte",
                "pedaco", "fragmento", "secao", "segmento"
            ]
        },
        "exclusoes": [
            "vetor", "array", "lista", "unidimensional", "uma dimensao",
            "1d", "1-d", "sequencia", "serie", "colecao simples"
        ]
    },

    7: { # Funções
        "pesos": {
            5: [
                "funcao", "procedimento", "crie uma funcao", "crie um procedimento",
                "defina uma funcao", "defina um procedimento", "implemente uma funcao",
                "implemente um procedimento", "desenvolva uma funcao",
                "desenvolva um procedimento", "escreva uma funcao",
                "escreva um procedimento", "criar funcao", "criar procedimento",
                "exiba um menu", "exibicao do menu", "funcao separada", "funcao chamada"
            ],
            3: [
                "retorne", "retornar", "modularize", "passagem de parametro",
                "parametro", "argumento", "valor de retorno", "tipo de retorno",
                "assinatura da funcao", "cabecalho da funcao", "prototipo da funcao",
                "declaracao da funcao", "definicao da funcao", "implementacao da funcao",
                "corpo da funcao", "escopo da funcao", "visibilidade da funcao",
                "chamada da funcao", "invocacao da funcao", "execucao da funcao",
                "reutilizacao", "reutilizar", "modularizacao", "modularizar",
                "organizacao do codigo", "estruturacao do codigo",
                "menu de opcoes", "opcoes", "separada", "chamada", "exibir"
            ],
            1: [
                "parametro", "chamar", "reutilizar", "argumento", "valor",
                "dado", "informacao", "entrada", "saida", "resultado",
                "retorno", "tipo", "classe", "categoria", "especie",
                "variedade", "sortimento", "assortimento", "selecao",
                "escolha", "opcao", "alternativa", "possibilidade"
            ]
        },
        "exclusoes": [
            "sem usar funcao", "nao crie funcao", "sem funcao", "sem procedimento",
            "nao use funcao", "nao use procedimento", "sem modularizacao",
            "codigo direto", "programa principal", "main", "programa unico"
        ]
    }
}