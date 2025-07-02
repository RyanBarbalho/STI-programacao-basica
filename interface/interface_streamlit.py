#!/usr/bin/env python3
"""
Interface Streamlit para o Sistema de Avaliação de Código C
Permite que alunos resolvam problemas e recebam feedback automático
"""

import streamlit as st
import json
import os
import sys
from pathlib import Path

import sys
from pathlib import Path

def setup_imports():
    """Configura os imports para sibling directories"""
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent  # Vai para o diretório pai

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

setup_imports()

# Agora pode importar normalmente
from modelo_especialista import AvaliadorCodigo, ClassificadorCodigo, BASE_DE_REGRAS

# Configuração da página
st.set_page_config(
    page_title="Sistema de Avaliação de Código C",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .problem-card {
        background-color: black;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ffeaa7;
    }
    .info-message {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #bee5eb;
    }
    .code-editor {
        font-family: 'Courier New', monospace;
        font-size: 14px;
    }
    .stButton > button {
        width: 100%;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_base_de_casos():
    """Carrega todos os casos de teste da base de dados"""
    base_dir = Path("../modelo_especialista/base_de_casos")
    casos = {}

    for arquivo in base_dir.glob("tipo_*.json"):
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            casos[arquivo.stem] = dados #casos[nomeDoArquivo] = dados

    return casos

@st.cache_resource
def inicializar_avaliador():
    """Inicializa o avaliador de código"""
    return AvaliadorCodigo()

def get_tipo_descricao(tipo):
    """Retorna a descrição do tipo de problema"""
    descricoes = {
        'tipo_1': 'Saída e Conceitos Iniciais',
        'tipo_2': 'Entrada e Aritmética',
        'tipo_3': 'Condicionais',
        'tipo_4': 'Repetição',
        'tipo_5': 'Vetores',
        'tipo_6': 'Matrizes',
        'tipo_7': 'Funções'
    }
    return descricoes.get(tipo, 'Desconhecido')

def exibir_problema(problema):
    """Exibe as informações do problema de forma organizada"""
    st.markdown(f"""
    <div class="problem-card">
        <h3>📋 {problema['id']}</h3>
        <p><strong>Conceito Principal:</strong> {problema['conceito_principal']}</p>
        <p><strong>Enunciado:</strong></p>
        <p>{problema['enunciado']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Dicas e restrições
    if 'dicas' in problema and problema['dicas']:
        with st.expander("💡 Dicas", expanded=False):
            for i, dica in enumerate(problema['dicas'], 1):
                st.write(f"{i}. {dica}")

    if 'restricoes' in problema and problema['restricoes']:
        with st.expander("⚠️ Restrições", expanded=False):
            for i, restricao in enumerate(problema['restricoes'], 1):
                st.write(f"{i}. {restricao}")

    # Conceitos secundários
    if 'conceitos_secundarios' in problema and problema['conceitos_secundarios']:
        with st.expander("📚 Conceitos Relacionados", expanded=False):
            for conceito in problema['conceitos_secundarios']:
                st.write(f"• {conceito}")

def exibir_resultado_avaliacao(resultado):
    """Exibe o resultado da avaliação de forma clara e organizada"""

    # Status principal
    status = resultado['status']

    if status == "SUCESSO":
        st.markdown('<div class="success-message">', unsafe_allow_html=True)
        st.success("🎉 **SUCESSO!** Seu código está correto!")
        st.markdown('</div>', unsafe_allow_html=True)

    elif status == "SUCESSO_ALTERNATIVO":
        st.markdown('<div class="warning-message">', unsafe_allow_html=True)
        st.warning("✅ **SUCESSO ALTERNATIVO!** Seu código funciona, mas usa uma abordagem diferente.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Mostrar feedback alternativo
        if 'feedback_alternativo' in resultado:
            st.markdown("**💡 Sugestões para melhorar:**")
            for feedback in resultado['feedback_alternativo']:
                st.info(feedback)

    elif status == "REPROVADO_ESTATICO":
        st.markdown('<div class="error-message">', unsafe_allow_html=True)
        st.error("❌ **REPROVADO** - Verifique os conceitos faltantes.")
        st.markdown('</div>', unsafe_allow_html=True)

    elif status == "ERRO_COMPILACAO":
        st.markdown('<div class="error-message">', unsafe_allow_html=True)
        st.error("🔨 **ERRO DE COMPILAÇÃO**")
        st.code(resultado.get('detalhes', 'Erro desconhecido'))
        st.markdown('</div>', unsafe_allow_html=True)

    elif status == "RESPOSTA_ERRADA":
        st.markdown('<div class="error-message">', unsafe_allow_html=True)
        st.error(f"❌ **RESPOSTA INCORRETA** - {resultado.get('detalhes', '')}")

        # Mostrar detalhes do erro
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Entrada:**")
            st.code(resultado.get('entrada', ''))
        with col2:
            st.write("**Saída esperada:**")
            st.code(resultado.get('saida_esperada', ''))
            st.write("**Sua saída:**")
            st.code(resultado.get('saida_obtida', ''))
        st.markdown('</div>', unsafe_allow_html=True)

    elif status == "TEMPO_LIMITE_EXCEDIDO":
        st.markdown('<div class="error-message">', unsafe_allow_html=True)
        st.error("⏰ **TEMPO LIMITE EXCEDIDO** - Verifique loops infinitos.")
        st.markdown('</div>', unsafe_allow_html=True)

    elif status == "ERRO_EXECUCAO":
        st.markdown('<div class="error-message">', unsafe_allow_html=True)
        st.error("💥 **ERRO DE EXECUÇÃO**")
        st.code(resultado.get('detalhes', 'Erro desconhecido'))
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="error-message">', unsafe_allow_html=True)
        st.error(f"❌ **ERRO** - {resultado.get('detalhes', 'Erro desconhecido')}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Detalhes da análise estática
    if 'avaliacao_estatica' in resultado:
        estatica = resultado['avaliacao_estatica']

        with st.expander("📊 Análise Estática", expanded=False):
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Conceitos Específicos:**")
                if estatica['conceitos_especificos_verificados']:
                    for conceito in estatica['conceitos_especificos_verificados']:
                        st.success(f"✅ {conceito}")
                if estatica['conceitos_especificos_faltantes']:
                    for conceito in estatica['conceitos_especificos_faltantes']:
                        st.error(f"❌ {conceito}")

            with col2:
                st.write("**Conceitos Gerais:**")
                if estatica['conceitos_gerais_verificados']:
                    for conceito in estatica['conceitos_gerais_verificados']:
                        st.success(f"✅ {conceito}")
                if estatica['conceitos_gerais_faltantes']:
                    for conceito in estatica['conceitos_gerais_faltantes']:
                        st.error(f"❌ {conceito}")

    # Detalhes da análise dinâmica
    if 'avaliacao_dinamica' in resultado:
        dinamica = resultado['avaliacao_dinamica']

        with st.expander("🚀 Análise Dinâmica", expanded=False):
            if dinamica['status'] == "SUCESSO":
                st.success("✅ Todos os casos de teste passaram!")
            else:
                st.error(f"❌ {dinamica.get('detalhes', 'Falha na execução')}")

def main():
    """Função principal da interface"""

    # Cabeçalho
    st.markdown('<h1 class="main-header">💻 Sistema de Avaliação de Código C</h1>', unsafe_allow_html=True)

    # Carregar dados
    try:
        casos = carregar_base_de_casos()
        avaliador = inicializar_avaliador()
    except Exception as e:
        st.error(f"Erro ao carregar o sistema: {e}")
        return

    # Sidebar para seleção de problemas
    st.sidebar.title("📚 Problemas Disponíveis")

    # Organizar problemas por tipo
    problemas_por_tipo = {}
    for tipo, dados in casos.items():
        problemas_por_tipo[tipo] = dados  # dados já é a lista de problemas

    # Verificar se há problemas carregados
    if not problemas_por_tipo:
        st.error("Nenhum problema foi encontrado. Verifique se os arquivos JSON estão no diretório correto.")
        return

    # Seleção de tipo
    tipo_selecionado = st.sidebar.selectbox(
        "Selecione o tipo de problema:",
        list(problemas_por_tipo.keys()),
        format_func=lambda x: f"Tipo {x.split('_')[1]} - {get_tipo_descricao(x)}"
    )

    # Seleção de problema específico
    if tipo_selecionado and tipo_selecionado in problemas_por_tipo:
        problemas_tipo = problemas_por_tipo[tipo_selecionado]
    else:
        st.error("Tipo de problema não encontrado.")
        return
    problema_selecionado = st.sidebar.selectbox(
        "Selecione o problema:",
        problemas_tipo,
        format_func=lambda x: f"{x['id']} - {x['conceito_principal']}"
    )

    # Área principal
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 Problema")
        exibir_problema(problema_selecionado)

    with col2:
        st.subheader("💻 Seu Código")

        # Editor de código
        codigo_aluno = st.text_area(
            "Digite seu código C aqui:",
            value="#include <stdio.h>\n\nint main() {\n    // Seu código aqui\n    \n    return 0;\n}",
            height=400,
            help="Digite seu código C completo, incluindo #include e int main()"
        )

        # Botão de avaliação
        if st.button("🚀 Avaliar Código", type="primary"):
            if codigo_aluno.strip():
                with st.spinner("Avaliando seu código..."):
                    try:
                        # Preparar dados para avaliação
                        enunciado = problema_selecionado['enunciado']
                        casos_de_teste = problema_selecionado['casos_de_teste']

                        # Realizar avaliação completa
                        resultado = avaliador.avaliar_completo(
                            codigo_aluno,
                            enunciado,
                            casos_de_teste
                        )

                        # Exibir resultado
                        st.subheader("📊 Resultado da Avaliação")
                        exibir_resultado_avaliacao(resultado)

                    except Exception as e:
                        st.error(f"Erro durante a avaliação: {e}")
            else:
                st.warning("Por favor, digite algum código antes de avaliar.")

    # Informações adicionais
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Sobre o Sistema")
    st.sidebar.markdown("""
    Este sistema avalia seu código C de duas formas:

    **📊 Análise Estática:** Verifica se você usou os conceitos corretos

    **🚀 Análise Dinâmica:** Executa seu código e compara com os resultados esperados

    **✅ Sucesso:** Código correto e conceitos adequados

    **⚠️ Sucesso Alternativo:** Código funciona, mas usa abordagem diferente

    **❌ Reprovado:** Verifique os conceitos faltantes ou erros
    """)

if __name__ == "__main__":
    main()