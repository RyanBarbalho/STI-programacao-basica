# 🤖 Sistema de Dicas Inteligentes

## 📋 Visão Geral

O sistema agora inclui **dicas inteligentes personalizadas** geradas por IA (LLM) que analisam o código do aluno e fornecem orientações específicas para cada tipo de erro.

## 🚀 Como Funciona

### 1. **Dicas para Erro de Compilação**
- Analisa o código e o erro específico
- Gera dicas direcionadas para corrigir o problema
- Exemplo: "Verifique se você está usando aspas duplas `\"` em vez de aspas simples `'` para strings"

### 2. **Dicas para Resposta Incorreta**
- Compara a saída esperada com a obtida
- Identifica diferenças específicas
- Exemplo: "Sua saída está faltando a vírgula após 'Ola'. Verifique a pontuação exata."

### 3. **Dicas para Conceitos Faltantes**
- Analisa quais conceitos não foram usados
- Orienta sobre conceitos específicos do tipo de problema
- Exemplo: "Para este problema, você precisa usar uma estrutura condicional `if` para verificar as condições."

## ⚙️ Configuração

### Opção 1: Com API OpenAI (Recomendado)
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar API key
python config_api.py
```

**Para obter uma chave da API OpenAI:**
1. Acesse: https://platform.openai.com/api-keys
2. Faça login ou crie uma conta
3. Clique em "Create new secret key"
4. Copie a chave gerada

### Opção 2: Sem API (Modo Padrão)
Se você não configurar a API, o sistema usará dicas padrão pré-definidas que ainda são úteis.

## 💡 Tipos de Dicas

### 🔨 Erro de Compilação
- **Com IA**: Dicas específicas baseadas no erro exato
- **Sem IA**: Dicas gerais sobre sintaxe C

### ❌ Resposta Incorreta
- **Com IA**: Análise da diferença entre saída esperada e obtida
- **Sem IA**: Sugestão para revisar o código

### 📚 Conceitos Faltantes
- **Com IA**: Orientação específica sobre conceitos não utilizados
- **Sem IA**: Lista dos conceitos que deveriam ser usados

## 🎯 Exemplos de Dicas Inteligentes

### Erro de Compilação
```
Código: printf('Ola mundo!\n');
Erro: error: character constant too long for its type

🤖 Dica Inteligente:
"Você está usando aspas simples para uma string. Em C, use aspas duplas para strings: printf(\"Ola mundo!\\n\");"
```

### Resposta Incorreta
```
Esperado: 'Ola, Mundo!'
Obtido: 'Ola mundo!'

🤖 Dica Inteligente:
"Sua saída está faltando a vírgula após 'Ola' e 'Mundo' deve começar com maiúscula. Verifique a pontuação e capitalização."
```

### Conceitos Faltantes
```
Conceitos faltantes: ['Uso da função printf']

🤖 Dica Inteligente:
"Para este problema de saída, você precisa usar printf() para exibir texto na tela. Tente: printf(\"sua mensagem aqui\");"
```

## 🔧 Arquivos do Sistema

- `modelo_especialista/componentes/dicas_inteligentes.py` - Sistema principal de dicas
- `config_api.py` - Configuração da API
- `.env` - Arquivo com a chave da API (criado automaticamente)

## 💰 Custos

- **OpenAI API**: ~$0.002 por 1K tokens (muito barato)
- **Uso típico**: ~$0.01-0.05 por mês para uso moderado
- **Alternativa gratuita**: Dicas padrão sempre disponíveis

## 🛡️ Privacidade

- O código do aluno é enviado apenas para gerar dicas
- Não é armazenado permanentemente
- Apenas a dica gerada é retornada

## 🎉 Benefícios

1. **Feedback Personalizado**: Cada erro recebe uma dica específica
2. **Aprendizado Acelerado**: Dicas direcionadas ajudam a entender o problema
3. **Motivação**: Feedback construtivo e encorajador
4. **Flexibilidade**: Funciona com ou sem API

## 🚀 Como Usar

1. **Configure a API** (opcional): `python config_api.py`
2. **Execute a interface**: `streamlit run interface_streamlit.py`
3. **Teste um código com erro**
4. **Veja a dica inteligente** na seção "🤖 Dica Inteligente"

O sistema automaticamente detecta se a API está disponível e usa o modo apropriado!