import json
import os
import subprocess
import uuid

from .avaliador_util import (verificar_estrutura_geral, verificar_tipo_1,
                             verificar_tipo_2, verificar_tipo_3,
                             verificar_tipo_4, verificar_tipo_5,
                             verificar_tipo_6, verificar_tipo_7)
from .classificador_de_enunciados import classificar_enunciado
from .lista_de_regras import BASE_DE_REGRAS
from .dicas_inteligentes import DicasInteligentes


class AvaliadorCodigo:
    """
    Classe principal para avaliação de código C.
    Combina análise estática e dinâmica.
    """

    def __init__(self):
        self.BASE_DE_REGRAS = BASE_DE_REGRAS
        self.dicas_inteligentes = DicasInteligentes()

    def avaliar_estatico(self, codigo_aluno, enunciado):
        """
        Avalia estaticamente o código do aluno verificando se os conceitos
        do tipo de problema identificado estão corretos.
        """
        # 1. Classificar o enunciado para identificar o tipo de problema
        classificacao = classificar_enunciado(enunciado, self.BASE_DE_REGRAS)
        tipo_problema = classificacao['tipo_principal']

        # 2. Análise estática baseada no tipo de problema
        resultado_estatico = {
            "tipo_problema": tipo_problema,
            "confianca_classificacao": classificacao['confianca'],
            "status": "APROVADO",
            "detalhes": [],
            "conceitos_especificos_verificados": [],
            "conceitos_especificos_faltantes": [],
            "conceitos_gerais_verificados": [],
            "conceitos_gerais_faltantes": [],
            "conceitos_incorretos": []
        }

        # Normalizar o código para análise
        codigo_normalizado = codigo_aluno.lower()

        # 3. Verificações específicas por tipo de problema
        if tipo_problema == "1" or tipo_problema == 1:  # Saída e Conceitos Iniciais
            resultado_estatico = verificar_tipo_1(codigo_normalizado, resultado_estatico)

        elif tipo_problema == "2" or tipo_problema == 2:  # Entrada e Aritmética
            resultado_estatico = verificar_tipo_2(codigo_normalizado, resultado_estatico)

        elif tipo_problema == "3" or tipo_problema == 3:  # Condicionais
            resultado_estatico = verificar_tipo_3(codigo_normalizado, resultado_estatico)

        elif tipo_problema == "4" or tipo_problema == 4:  # Repetição
            resultado_estatico = verificar_tipo_4(codigo_normalizado, resultado_estatico)

        elif tipo_problema == "5" or tipo_problema == 5:  # Vetores
            resultado_estatico = verificar_tipo_5(codigo_normalizado, resultado_estatico)

        elif tipo_problema == "6" or tipo_problema == 6:  # Matrizes
            resultado_estatico = verificar_tipo_6(codigo_normalizado, resultado_estatico)

        elif tipo_problema == "7" or tipo_problema == 7:  # Funções
            resultado_estatico = verificar_tipo_7(codigo_normalizado, resultado_estatico)

        # 4. Verificações gerais de estrutura
        resultado_estatico = verificar_estrutura_geral(codigo_normalizado, resultado_estatico)

        # 5. Determinar status final
        if (resultado_estatico["conceitos_especificos_faltantes"] or
            resultado_estatico["conceitos_gerais_faltantes"] or
            resultado_estatico["conceitos_incorretos"]):
            resultado_estatico["status"] = "REPROVADO"

        return resultado_estatico

    def avaliar_dinamico(self, codigo_aluno, casos_de_teste):
        """
        Avalia dinamicamente o código C seguindo o fluxo:
        1. String → Arquivo .c temporário
        2. Compilar com gcc
        3. Executar e capturar saída
        4. Comparar com resultado esperado
        5. Limpar arquivos temporários
        """
        # Gerar nomes únicos para evitar conflitos
        arquivo_id = str(uuid.uuid4())[:8]
        caminho_arquivo_c = f"temp_aluno_{arquivo_id}.c"
        caminho_executavel = f"temp_exec_{arquivo_id}"

        try:
            # 1. Salvar a string do código em arquivo temporário .c
            with open(caminho_arquivo_c, "w", encoding='utf-8') as f:
                f.write(codigo_aluno)

            print(f"   📝 Código salvo em: {caminho_arquivo_c}")

            # 2. Verificar se o GCC está disponível
            try:
                subprocess.run(['gcc', '--version'], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Limpar arquivo temporário antes de retornar
                if os.path.exists(caminho_arquivo_c):
                    os.remove(caminho_arquivo_c)
                return {
                    "status": "ERRO_COMPILADOR",
                    "detalhes": "GCC não encontrado. Instale o MinGW ou configure o PATH."
                }

            # 3. Compilar o código com gcc
            print("   🔨 Compilando código...")
            compilacao = subprocess.run(
                ['gcc', caminho_arquivo_c, '-o', caminho_executavel],
                capture_output=True, text=True, timeout=10
            )

            # 4. Verificar erros de compilação
            if compilacao.returncode != 0:
                # Limpar arquivos temporários antes de retornar
                if os.path.exists(caminho_arquivo_c):
                    os.remove(caminho_arquivo_c)
                    print(f"   🗑️ Arquivo removido: {caminho_arquivo_c}")
                if os.path.exists(caminho_executavel):
                    os.remove(caminho_executavel)
                    print(f"   🗑️ Executável removido: {caminho_executavel}")
                # Gerar dica inteligente para erro de compilação
                dica = self.dicas_inteligentes.gerar_dica_erro_compilacao(
                    codigo_aluno, compilacao.stderr, "Compilação"
                )

                return {
                    "status": "ERRO_COMPILACAO",
                    "detalhes": compilacao.stderr,
                    "arquivo_compilado": caminho_arquivo_c,
                    "dica_inteligente": dica
                }

            print("   ✅ Compilação bem-sucedida!")

            # 5. Executar os casos de teste
            print(f"   🧪 Iniciando execução de {len(casos_de_teste)} caso(s) de teste...")
            for i, caso in enumerate(casos_de_teste):
                print(f"   🚀 Executando caso de teste {i+1}...")

                try:
                    # Executar o programa
                    execucao = subprocess.run(
                        [f'./{caminho_executavel}'] if os.name != 'nt' else [caminho_executavel],
                        input=caso['entrada'],
                        capture_output=True,
                        text=True,
                        timeout=5  # Timeout para evitar loops infinitos
                    )

                    # 6. Capturar e normalizar saídas
                    saida_obtida = execucao.stdout.strip() if execucao.stdout else ""
                    saida_esperada = caso.get('saida_esperada', '').strip() if caso.get('saida_esperada') else ""

                    # Remover prompts comuns de entrada da saída obtida
                    import re
                    # Padrões comuns de prompts que devem ser removidos
                    prompts_para_remover = [
                        # Padrões básicos
                        r'Digite.*?:',
                        r'Entre.*?:',
                        r'Informe.*?:',
                        r'Digite o.*?:',
                        r'Digite a.*?:',
                        r'Digite um.*?:',
                        r'Digite uma.*?:',
                        r'Digite dois.*?:',
                        r'Digite tres.*?:',
                        r'Digite as.*?:',
                        r'Digite os.*?:',
                        r'Quantos.*?:',
                        r'Entre com.*?:',
                        r'Informe o.*?:',
                        r'Informe a.*?:',
                        r'Informe um.*?:',
                        r'Informe uma.*?:',
                        r'Informe dois.*?:',
                        r'Informe tres.*?:',
                        r'Informe as.*?:',
                        r'Informe os.*?:',
                        r'Entre o.*?:',
                        r'Entre a.*?:',
                        r'Entre um.*?:',
                        r'Entre uma.*?:',
                        r'Entre dois.*?:',
                        r'Entre tres.*?:',
                        r'Entre as.*?:',
                        r'Entre os.*?:',

                        # Padrões específicos para casos problemáticos
                        r'Digite uma nota entre.*?:',
                        r'Digite novamente.*?:',
                        r'Valor invalido.*?:',
                        r'Digite o primeiro.*?:',
                        r'Digite o segundo.*?:',
                        r'Digite a primeira.*?:',
                        r'Digite a segunda.*?:',
                        r'Digite os.*?elementos.*?:',
                        r'Digite os.*?numeros.*?:',
                        r'Digite.*?numeros.*?:',
                        r'Digite.*?elementos.*?:',
                        r'Quantos alunos.*?:',
                        r'Quantos numeros.*?:',
                        r'Quantos elementos.*?:',

                        # Padrões com variações de pontuação
                        r'Digite.*?\?',
                        r'Entre.*?\?',
                        r'Informe.*?\?',
                        r'Quantos.*?\?',

                        # Padrões com espaços extras
                        r'\s*Digite.*?:',
                        r'\s*Entre.*?:',
                        r'\s*Informe.*?:',
                        r'\s*Quantos.*?:',
                    ]

                                        # Remover prompts da saída obtida
                    for padrao in prompts_para_remover:
                        saida_obtida = re.sub(padrao, '', saida_obtida, flags=re.IGNORECASE)

                    # Normalização robusta de formatação
                    def normalizar_saida(texto):
                        if not texto:
                            return ""

                        # Normalizar quebras de linha (Windows, Unix, Mac)
                        texto = re.sub(r'\r\n', '\n', texto)
                        texto = re.sub(r'\r', '\n', texto)

                        # Normalizar múltiplas quebras de linha para uma única
                        texto = re.sub(r'\n\s*\n', '\n', texto)

                        # Normalizar espaços múltiplos para um único espaço
                        texto = re.sub(r'[ \t]+', ' ', texto)

                        # Remover espaços no início e fim de cada linha
                        linhas = texto.split('\n')
                        linhas = [linha.strip() for linha in linhas]

                        # Remover linhas vazias no início e fim
                        while linhas and not linhas[0].strip():
                            linhas.pop(0)
                        while linhas and not linhas[-1].strip():
                            linhas.pop()

                        # Juntar linhas e remover espaços extras no início e fim
                        return '\n'.join(linhas).strip()

                    # Aplicar normalização
                    saida_obtida = normalizar_saida(saida_obtida)
                    saida_esperada = normalizar_saida(saida_esperada)

                    # Display melhorado da entrada, saída esperada e saída obtida
                    print("   " + "="*60)
                    print(f"   📋 CASO DE TESTE {i+1}")
                    print("   " + "="*60)
                    entrada_caso = caso.get('entrada', '') or ""
                    if entrada_caso.strip():
                        print(f"   📝 Entrada: '{entrada_caso.strip()}'")
                    else:
                        print(f"   📝 Entrada: (sem entrada)")
                    print(f"   ✅ Saída esperada: '{saida_esperada}'")
                    print(f"   📤 Saída obtida: '{saida_obtida}'")
                    print("   " + "-"*60)

                    # 7. Comparar saídas com flexibilidade
                    def comparar_saidas(obtida, esperada):
                        # Se são idênticas, sucesso
                        if obtida == esperada:
                            return True, "Exata"

                        # Normalizar ainda mais para comparação flexível
                        def normalizar_para_comparacao(texto):
                            # Remover todos os espaços extras
                            texto = re.sub(r'\s+', ' ', texto)
                            # Converter para minúsculas para comparação case-insensitive
                            return texto.lower().strip()

                        obtida_norm = normalizar_para_comparacao(obtida)
                        esperada_norm = normalizar_para_comparacao(esperada)

                        # Comparação case-insensitive e sem espaços extras
                        if obtida_norm == esperada_norm:
                            return True, "Normalizada"

                        # Verificar se a saída obtida contém a esperada (para casos com prompts extras)
                        if obtida_norm and esperada_norm and esperada_norm in obtida_norm:
                            return True, "Contém"

                        # Verificar se a esperada contém a obtida (para casos com formatação mais simples)
                        if obtida_norm and esperada_norm and obtida_norm in esperada_norm:
                            return True, "Contida"

                        return False, "Diferente"

                    sucesso, tipo_comparacao = comparar_saidas(saida_obtida, saida_esperada)

                    if sucesso:
                        print(f"   ✅ RESULTADO: PASSOU (Comparação {tipo_comparacao})")
                    else:
                        print(f"   ❌ RESULTADO: FALHOU (Comparação {tipo_comparacao})")
                    print("   " + "="*60)

                    if not sucesso:
                        # Limpar arquivos temporários antes de retornar
                        if os.path.exists(caminho_arquivo_c):
                            os.remove(caminho_arquivo_c)
                            print(f"   🗑️ Arquivo removido: {caminho_arquivo_c}")
                        if os.path.exists(caminho_executavel):
                            os.remove(caminho_executavel)
                            print(f"   🗑️ Executável removido: {caminho_executavel}")
                        # Gerar dica inteligente para resposta incorreta
                        dica = self.dicas_inteligentes.gerar_dica_resposta_errada(
                            codigo_aluno, caso.get('entrada', '') or '',
                            saida_esperada or '', saida_obtida or '',
                            "Execução"
                        )

                        return {
                            "status": "RESPOSTA_ERRADA",
                            "detalhes": f"Falhou no caso de teste {i+1}",
                            "entrada": caso.get('entrada', '') or '',
                            "saida_esperada": saida_esperada or '',
                            "saida_obtida": saida_obtida or '',
                            "arquivo_compilado": caminho_arquivo_c,
                            "dica_inteligente": dica
                        }

                except subprocess.TimeoutExpired:
                    # Limpar arquivos temporários antes de retornar
                    if os.path.exists(caminho_arquivo_c):
                        os.remove(caminho_arquivo_c)
                        print(f"   🗑️ Arquivo removido: {caminho_arquivo_c}")
                    if os.path.exists(caminho_executavel):
                        os.remove(caminho_executavel)
                        print(f"   🗑️ Executável removido: {caminho_executavel}")
                    return {
                        "status": "TEMPO_LIMITE_EXCEDIDO",
                        "detalhes": "Programa demorou demais para responder. Verifique loops infinitos.",
                        "arquivo_compilado": caminho_arquivo_c
                    }
                except Exception as e:
                    # Limpar arquivos temporários antes de retornar
                    if os.path.exists(caminho_arquivo_c):
                        os.remove(caminho_arquivo_c)
                        print(f"   🗑️ Arquivo removido: {caminho_arquivo_c}")
                    if os.path.exists(caminho_executavel):
                        os.remove(caminho_executavel)
                        print(f"   🗑️ Executável removido: {caminho_executavel}")
                    return {
                        "status": "ERRO_EXECUCAO",
                        "detalhes": f"Erro ao executar programa: {str(e)}",
                        "arquivo_compilado": caminho_arquivo_c
                    }

            # 8. Sucesso - todos os casos passaram
            print("   " + "="*60)
            print(f"   🎉 TODOS OS {len(casos_de_teste)} CASOS DE TESTE PASSARAM!")
            print("   " + "="*60)
            return {"status": "SUCESSO", "detalhes": "Todos os casos de teste passaram!"}

        except Exception as e:
            return {
                "status": "ERRO_GERAL",
                "detalhes": f"Erro inesperado: {str(e)}"
            }

        finally:
            # 9. Limpeza dos arquivos temporários
            try:
                if os.path.exists(caminho_arquivo_c):
                    os.remove(caminho_arquivo_c)
                    print(f"   🗑️ Arquivo removido: {caminho_arquivo_c}")

                if os.path.exists(caminho_executavel):
                    os.remove(caminho_executavel)
                    print(f"   🗑️ Executável removido: {caminho_executavel}")

                # Remover extensão .exe no Windows
                if os.name == 'nt' and os.path.exists(f"{caminho_executavel}.exe"):
                    os.remove(f"{caminho_executavel}.exe")
                    print(f"   🗑️ Executável .exe removido: {caminho_executavel}.exe")

            except Exception as e:
                print(f"   ⚠️ Erro ao limpar arquivos: {e}")

    def avaliar_completo(self, codigo_aluno, enunciado, casos_de_teste):
        """
        Avalia o código de forma completa (estática + dinâmica).
        """
        # 1. Avaliação estática
        resultado_estatico = self.avaliar_estatico(codigo_aluno, enunciado)

        # 2. Avaliação dinâmica
        resultado_dinamico = self.avaliar_dinamico(codigo_aluno, casos_de_teste)

        # 3. Integração inteligente das análises
        resultado_final = self._integrar_analises(resultado_estatico, resultado_dinamico, enunciado, codigo_aluno)

        return resultado_final

    def _integrar_analises(self, resultado_estatico, resultado_dinamico, enunciado, codigo_aluno):
        """
        Integra os resultados das análises estática e dinâmica de forma inteligente.
        """
        # Se a análise dinâmica passou, mas a estática falhou em conceitos específicos
        if (resultado_dinamico["status"] == "SUCESSO" and
            resultado_estatico["conceitos_especificos_faltantes"]):

            # Gerar feedback inteligente
            feedback_alternativo = self._gerar_feedback_alternativo(
                resultado_estatico["conceitos_especificos_faltantes"],
                resultado_estatico["tipo_problema"]
            )

            return {
                "status": "SUCESSO_ALTERNATIVO",
                "avaliacao_estatica": resultado_estatico,
                "avaliacao_dinamica": resultado_dinamico,
                "detalhes": resultado_dinamico.get("detalhes", ""),
                "feedback_alternativo": feedback_alternativo,
                "observacao": "Código funciona corretamente, mas usa abordagem alternativa."
            }

        # Se a análise estática falhou completamente
        if resultado_estatico["status"] == "REPROVADO":
            # Gerar dica inteligente para conceitos faltantes
            conceitos_faltantes = (resultado_estatico.get("conceitos_especificos_faltantes", []) +
                                 resultado_estatico.get("conceitos_gerais_faltantes", []))

            dica = self.dicas_inteligentes.gerar_dica_conceitos_faltantes(
                codigo_aluno, conceitos_faltantes,
                resultado_estatico.get("tipo_problema", "Desconhecido"),
                enunciado
            )

            return {
                "status": "REPROVADO_ESTATICO",
                "avaliacao_estatica": resultado_estatico,
                "avaliacao_dinamica": resultado_dinamico,
                "detalhes": "Código reprovado na análise estática. Verifique os conceitos faltantes.",
                "dica_inteligente": dica
            }

        # Caso padrão: retorna o status da análise dinâmica
        resultado_final = {
            "status": resultado_dinamico["status"],
            "avaliacao_estatica": resultado_estatico,
            "avaliacao_dinamica": resultado_dinamico,
            "detalhes": resultado_dinamico.get("detalhes", "")
        }

        # Preservar dados específicos do erro dinâmico (entrada, saída esperada, saída obtida)
        if resultado_dinamico["status"] == "RESPOSTA_ERRADA":
            resultado_final["entrada"] = resultado_dinamico.get("entrada", "") or ""
            resultado_final["saida_esperada"] = resultado_dinamico.get("saida_esperada", "") or ""
            resultado_final["saida_obtida"] = resultado_dinamico.get("saida_obtida", "") or ""

        return resultado_final

    def _gerar_feedback_alternativo(self, conceitos_faltantes, tipo_problema):
        """
        Gera feedback quando o aluno resolve o problema de forma alternativa.
        """
        feedback = []

        for conceito in conceitos_faltantes:
            if "printf" in conceito:
                feedback.append("Você resolveu o problema sem usar printf. Ótimo trabalho! "
                              "Para praticar, tente também usar printf() para saída formatada.")

            elif "scanf" in conceito:
                feedback.append("Você resolveu o problema sem usar scanf. Ótimo trabalho! "
                              "Para praticar, tente também usar scanf() para entrada de dados.")

            elif "if" in conceito:
                feedback.append("Você resolveu o problema sem usar estruturas condicionais. "
                              "Ótimo trabalho! Para praticar, tente também usar if/else.")

            elif "while" in conceito or "for" in conceito:
                feedback.append("Você resolveu o problema sem usar estruturas de repetição. "
                              "Ótimo trabalho! Para praticar, tente também usar while ou for.")

            elif "vetor" in conceito:
                feedback.append("Você resolveu o problema sem usar vetores. "
                              "Ótimo trabalho! Para praticar, tente também usar arrays.")

            elif "matriz" in conceito:
                feedback.append("Você resolveu o problema sem usar matrizes. "
                              "Ótimo trabalho! Para praticar, tente também usar matrizes.")

            elif "função" in conceito:
                feedback.append("Você resolveu o problema sem usar funções adicionais. "
                              "Ótimo trabalho! Para praticar, tente também criar funções.")

            else:
                feedback.append(f"Você resolveu o problema sem usar {conceito}. "
                              "Ótimo trabalho! Para praticar, tente também usar esse conceito.")

        return feedback


# Funções de conveniência para compatibilidade com código existente
def avaliador_estatico(codigo_aluno, enunciado):
    """Função de conveniência que usa a classe AvaliadorCodigo"""
    avaliador = AvaliadorCodigo()
    return avaliador.avaliar_estatico(codigo_aluno, enunciado)


def avaliador_dinamico(codigo_aluno, casos_de_teste):
    """Função de conveniência que usa a classe AvaliadorCodigo"""
    avaliador = AvaliadorCodigo()
    return avaliador.avaliar_dinamico(codigo_aluno, casos_de_teste)


def avaliador_completo(codigo_aluno, enunciado, casos_de_teste):
    """Função de conveniência que usa a classe AvaliadorCodigo"""
    avaliador = AvaliadorCodigo()
    return avaliador.avaliar_completo(codigo_aluno, enunciado, casos_de_teste)