# Sistema de Avaliação de Código - Modelo Especialista

Este sistema implementa um avaliador inteligente de códigos em C que combina análise estática e dinâmica para avaliar soluções de problemas de programação.

## Instalação e Configuração

### 1. Configurar Ambiente Python

```bash
# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar GCC (para Avaliação Dinâmica)

**Verificar se o GCC está instalado:**
```bash
python verificar_gcc.py
```

**Se o GCC não estiver instalado:**

**Windows:**
1. Instalar MSYS2: `winget install MSYS2.MSYS2`
2. Abrir MSYS2 e executar: `pacman -S mingw-w64-x86_64-gcc`
3. Adicionar `C:\msys64\mingw64\bin` ao PATH do usuário
4. Reiniciar terminal e testar: `gcc --version`

**Linux:**
```bash
sudo apt update && sudo apt install gcc  # Ubuntu/Debian
sudo yum install gcc                     # CentOS/RHEL
```

**macOS:**
```bash
xcode-select --install
```

### 3. Testar Instalação

```bash
# Testar GCC
python verificar_gcc.py

# Testar sistema completo
python modelo_especialista/exemplo_uso_avaliador.py
```

## Componentes do Sistema

### 1. Componentes (`componentes/`)
- **Classificador de Enunciados** (`classificador_de_enunciados.py`): Identifica automaticamente o tipo de problema baseado no enunciado
- **Avaliador de Código** (`avaliador_codigo.py`): Combina análise estática e dinâmica
- **Avaliador Utilitário** (`avaliador_util.py`): Funções auxiliares para verificação estática
- **Lista de Regras** (`lista_de_regras.py`): Define as regras para classificação de enunciados

### 2. Base de Casos (`base_de_casos/`)
- Contém exemplos de problemas organizados por tipo
- Cada problema inclui enunciado, casos de teste e solução

### 3. Exemplos (`exemplo_uso_avaliador.py`)
- Demonstra como usar o sistema de avaliação
- Inclui exemplos para todos os tipos de problemas

## Tipos de Problemas Suportados

1. **Tipo 1**: Saída e Conceitos Iniciais
   - Conceitos: printf, stdio.h, função main
   - Exemplo: "Escreva um programa que imprima 'Olá, Mundo!'"

2. **Tipo 2**: Entrada e Aritmética
   - Conceitos: scanf, operadores aritméticos, variáveis
   - Exemplo: "Leia dois números e calcule a soma"

3. **Tipo 3**: Condicionais
   - Conceitos: if/else, operadores de comparação
   - Exemplo: "Verifique se um número é par ou ímpar"

4. **Tipo 4**: Repetição
   - Conceitos: while, for, do-while, contadores
   - Exemplo: "Calcule o fatorial usando um laço"

5. **Tipo 5**: Vetores
   - Conceitos: arrays, índices, acesso a elementos
   - Exemplo: "Armazene N números em um vetor"

6. **Tipo 6**: Matrizes
   - Conceitos: matrizes bidimensionais, loops aninhados
   - Exemplo: "Crie uma matriz 3x3 e calcule a diagonal"

7. **Tipo 7**: Funções
   - Conceitos: definição de funções, parâmetros, return
   - Exemplo: "Crie uma função para calcular a área"

## Como Usar

### Uso Básico

```python
from modelo_especialista import avaliador_completo

# Exemplo de uso
enunciado = "Escreva um programa que imprima 'Olá, Mundo!'"
codigo_aluno = """
#include <stdio.h>
int main() {
    printf("Olá, Mundo!\\n");
    return 0;
}
"""
casos_de_teste = [{"entrada": None, "saida_esperada": "Olá, Mundo!\n"}]

resultado = avaliador_completo(codigo_aluno, enunciado, casos_de_teste)
print(f"Status: {resultado['status']}")
```

### Análise Apenas Estática

```python
from modelo_especialista import avaliador_estatico

resultado = avaliador_estatico(codigo_aluno, enunciado)
print(f"Conceitos verificados: {resultado['conceitos_verificados']}")
print(f"Conceitos faltantes: {resultado['conceitos_faltantes']}")
```

### Análise Apenas Dinâmica

```python
from modelo_especialista import avaliador_dinamico

resultado = avaliador_dinamico(codigo_aluno, casos_de_teste)
print(f"Status: {resultado['status']}")
```

### Uso Direto dos Componentes

```python
from modelo_especialista.componentes import avaliador_completo, classificar_enunciado

# Classificar um enunciado
classificacao = classificar_enunciado("Leia dois números e calcule a soma", MODELO_ESPECIALISTA)
print(f"Tipo identificado: {classificacao['tipo_principal']}")
```

## Executando os Exemplos

Para ver o sistema em ação, execute:

```bash
cd modelo_especialista
python exemplo_uso_avaliador.py
```

## Estrutura de Retorno

### Avaliador Estático
```python
{
    "tipo_problema": "1",
    "confianca_classificacao": 95.5,
    "status": "APROVADO",
    "conceitos_verificados": ["Inclusão da biblioteca stdio.h", "Função main definida"],
    "conceitos_faltantes": [],
    "conceitos_incorretos": []
}
```

### Avaliador Dinâmico
```python
{
    "status": "SUCESSO",
    "detalhes": "Todos os casos de teste passaram!"
}
```

### Avaliador Completo
```python
{
    "status": "SUCESSO",
    "avaliacao_estatica": {...},
    "avaliacao_dinamica": {...},
    "detalhes": "Todos os casos de teste passaram!"
}
```

## Requisitos

- Python 3.6+
- Compilador GCC (para avaliação dinâmica)
- Bibliotecas padrão: `subprocess`, `os`, `re`, `json`

## Fluxo de Avaliação

1. **Classificação**: O sistema classifica o enunciado para identificar o tipo de problema
2. **Análise Estática**: Verifica se os conceitos específicos do tipo estão presentes no código
3. **Análise Dinâmica**: Se a estática passar, executa o código e verifica os casos de teste
4. **Resultado Final**: Retorna o status e detalhes da avaliação

## Vantagens do Sistema

- **Eficiência**: Análise estática rápida antes da execução
- **Precisão**: Verifica conceitos específicos de cada tipo de problema
- **Flexibilidade**: Suporta diferentes tipos de problemas
- **Robustez**: Trata erros de compilação e loops infinitos
- **Feedback Detalhado**: Identifica conceitos faltantes e incorretos

## Extensibilidade

O sistema pode ser facilmente estendido:
- Adicionando novos tipos de problemas
- Incluindo mais conceitos para verificação
- Criando novos casos de teste
- Implementando verificações mais sofisticadas 