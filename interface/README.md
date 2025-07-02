# Interface Streamlit - Sistema de Avaliação de Código C

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7+
- Streamlit instalado (`pip install streamlit`)
- GCC instalado e configurado no PATH

### Comando para Executar

```bash
cd interface
streamlit run interface_streamlit.py
```

A interface será aberta automaticamente no seu navegador (geralmente em `http://localhost:8501`).

### Estrutura de Diretórios
```
STI-programacao-basica/
├── interface/
│   ├── interface_streamlit.py    # Interface principal
│   └── README.md                 # Este arquivo
└── modelo_especialista/          # Sistema de avaliação
    ├── componentes/
    └── base_de_casos/
```

### Como Usar
1. Selecione o tipo de problema na barra lateral
2. Escolha o problema específico
3. Digite seu código C no editor
4. Clique em "Avaliar Código"
5. Veja o resultado detalhado da avaliação

### Tipos de Problemas Disponíveis
- **Tipo 1**: Saída e Conceitos Iniciais
- **Tipo 2**: Entrada e Aritmética
- **Tipo 3**: Condicionais
- **Tipo 4**: Repetição
- **Tipo 5**: Vetores
- **Tipo 6**: Matrizes
- **Tipo 7**: Funções