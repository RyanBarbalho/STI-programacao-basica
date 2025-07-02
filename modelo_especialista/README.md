# Modelo Especialista - Avaliador de Código C

Sistema de avaliação automática de código C que combina análise estática e dinâmica.

## 🚀 Uso Básico

```python
from modelo_especialista import AvaliadorCodigo

avaliador = AvaliadorCodigo()
resultado = avaliador.avaliar_completo(codigo, enunciado, casos_teste)
```

## 📋 Componentes

- **`AvaliadorCodigo`**: Avaliação completa (estática + dinâmica)
- **`ClassificadorCodigo`**: Identifica o tipo de problema pelo enunciado
- **`BASE_DE_REGRAS`**: Regras de classificação dos 7 tipos

## 🔧 Métodos Principais

### Avaliação Completa
```python
resultado = avaliador.avaliar_completo(codigo, enunciado, casos_teste)
# Retorna: {'status': 'SUCESSO', 'avaliacao_estatica': {...}, 'avaliacao_dinamica': {...}}
```

### Apenas Estática
```python
resultado = avaliador.avaliar_estatico(codigo, enunciado)
# Retorna: {'conceitos_verificados': [...], 'conceitos_faltantes': [...]}
```

### Apenas Dinâmica
```python
resultado = avaliador.avaliar_dinamico(codigo, casos_teste)
# Retorna: {'status': 'SUCESSO', 'detalhes': '...'}
```

## 📊 Tipos de Problemas

1. **Tipo 1**: Saída básica (`printf`, `stdio.h`, `main`)
2. **Tipo 2**: Entrada/Aritmética (`scanf`, operadores)
3. **Tipo 3**: Condicionais (`if/else`)
4. **Tipo 4**: Repetição (`while`, `for`)
5. **Tipo 5**: Vetores (`arrays`)
6. **Tipo 6**: Matrizes (arrays 2D)
7. **Tipo 7**: Funções (definição, parâmetros)

## 🧪 Testes

```bash
# Exemplo de uso
python exemplo_uso_avaliador.py

# Todos os casos de teste
python rodar_todos_os_casos.py
```

## ⚙️ Dependências

- Python 3.6+
- GCC (para avaliação dinâmica)
- Streamlit (para interface)