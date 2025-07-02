# STI-programacao-basica

Sistema Tutor Inteligente aplicado ao ensino de programação básica em C. O sistema oferece avaliação automática de código combinando análise estática e dinâmica, com interface web interativa.

## ✨ Funcionalidades

- **Avaliação Automática**: Análise estática e dinâmica de código C
- **Interface Web**: Interface Streamlit intuitiva para alunos
- **7 Tipos de Problemas**: Desde conceitos básicos até funções
- **Feedback Inteligente**: Identifica conceitos faltantes e erros
- **Base de Casos**: Problemas organizados por dificuldade

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone <url-do-repositorio>
cd STI-programacao-basica
```

### 2. Criar Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar GCC (Obrigatório)
O sistema precisa do GCC para avaliação dinâmica dos códigos.

**Verificar instalação:**
```bash
python verificar_gcc.py
```

**Se não estiver instalado:**

**Windows:**
```bash
# Instalar MSYS2
winget install MSYS2.MSYS2

# Abrir MSYS2 e executar:
pacman -S mingw-w64-x86_64-gcc

# Adicionar ao PATH: C:\msys64\mingw64\bin
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install gcc

# CentOS/RHEL
sudo yum install gcc
```

**macOS:**
```bash
xcode-select --install
```

## 🎯 Como Usar

### Interface Web (Recomendado)
```bash
cd interface
streamlit run interface_streamlit.py
```

A interface será aberta em `http://localhost:8501` com:
- Seleção de tipos de problema
- Editor de código integrado
- Feedback em tempo real
- Dicas e orientações

### Exemplo Programático
```bash
cd modelo_especialista
python exemplo_uso_avaliador.py
```

### Teste Completo do Sistema
```bash
cd modelo_especialista
python rodar_todos_os_casos.py
```

## 📚 Tipos de Problemas Suportados

**(É recomendado escrever o código em algum editor de texto de ide ou semelhante e colar no editor da interface)**

1. **Tipo 1 - Saída e Conceitos Iniciais**
   - printf, stdio.h, função main
   - Exemplo: "Escreva um programa que imprima 'Olá, Mundo!'"

2. **Tipo 2 - Entrada e Aritmética**
   - scanf, operadores aritméticos, variáveis
   - Exemplo: "Leia dois números e calcule a soma"

3. **Tipo 3 - Condicionais**
   - if/else, operadores de comparação
   - Exemplo: "Verifique se um número é par ou ímpar"

4. **Tipo 4 - Repetição**
   - while, for, do-while, contadores
   - Exemplo: "Calcule o fatorial usando um laço"

5. **Tipo 5 - Vetores**
   - arrays, índices, acesso a elementos
   - Exemplo: "Armazene N números em um vetor"

6. **Tipo 6 - Matrizes**
   - matrizes bidimensionais, loops aninhados
   - Exemplo: "Crie uma matriz 3x3 e calcule a diagonal"

7. **Tipo 7 - Funções**
   - definição de funções, parâmetros, return
   - Exemplo: "Crie uma função para calcular a área"

## 🧪 Testes

### Executar Todos os Casos de Teste
```bash
cd modelo_especialista
python rodar_todos_os_casos.py
```

## 📁 Estrutura do Projeto

```
STI-programacao-basica/
├── interface/                    # Interface web Streamlit
│   ├── interface_streamlit.py   # Aplicação principal
│   └── README.md               # Documentação da interface
├── modelo_especialista/         # Sistema de avaliação
│   ├── componentes/            # Componentes do avaliador
│   ├── base_de_casos/          # Problemas e casos de teste
│   ├── exemplo_uso_avaliador.py # Exemplo de uso
│   └── rodar_todos_os_casos.py # Testes completos
├── requirements.txt            # Dependências Python
├── verificar_gcc.py           # Verificador do GCC
└── README.md                  # Este arquivo
```

## 💡 Exemplo de Uso Rápido

```python
from modelo_especialista import AvaliadorCodigo

# Criar avaliador
avaliador = AvaliadorCodigo()

# Código do aluno
codigo = """
#include <stdio.h>
int main() {
    printf("Hello World\\n");
    return 0;
}
"""

# Avaliar
resultado = avaliador.avaliar_completo(
    codigo,
    "Escreva um programa que imprima 'Hello World'",
    [{"entrada": "", "saida_esperada": "Hello World"}]
)

print(f"Status: {resultado['status']}")
```

## 🔧 Solução de Problemas

### Erro de importação
- Verifique se o ambiente virtual está ativado
- Reinstale as dependências: `pip install -r requirements.txt`

### Interface não carrega
- Confirme que o Streamlit está instalado
- Verifique se está no diretório correto: `cd interface`

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais no contexto do ensino de programação básica.
