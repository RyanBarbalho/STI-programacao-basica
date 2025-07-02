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


class AvaliadorCodigo:
    """
    Classe principal para avaliação de código C.
    Combina análise estática e dinâmica.
    """

    def __init__(self):
        self.BASE_DE_REGRAS = BASE_DE_REGRAS

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
                return {
                    "status": "ERRO_COMPILACAO",
                    "detalhes": compilacao.stderr,
                    "arquivo_compilado": caminho_arquivo_c
                }

            print("   ✅ Compilação bem-sucedida!")

            # 5. Executar os casos de teste
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
                    saida_obtida = execucao.stdout.strip()
                    saida_esperada = caso['saida_esperada'].strip()

                    print(f"   📤 Saída obtida: '{saida_obtida}'")
                    print(f"   📥 Saída esperada: '{saida_esperada}'")

                    # 7. Comparar saídas
                    if saida_obtida != saida_esperada:
                        # Limpar arquivos temporários antes de retornar
                        if os.path.exists(caminho_arquivo_c):
                            os.remove(caminho_arquivo_c)
                            print(f"   🗑️ Arquivo removido: {caminho_arquivo_c}")
                        if os.path.exists(caminho_executavel):
                            os.remove(caminho_executavel)
                            print(f"   🗑️ Executável removido: {caminho_executavel}")
                        return {
                            "status": "RESPOSTA_ERRADA",
                            "detalhes": f"Falhou no caso de teste {i+1}",
                            "entrada": caso['entrada'],
                            "saida_esperada": saida_esperada,
                            "saida_obtida": saida_obtida,
                            "arquivo_compilado": caminho_arquivo_c
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

        if resultado_estatico["status"] == "REPROVADO":
            return {
                "status": "REPROVADO_ESTATICO",
                "avaliacao_estatica": resultado_estatico,
                "avaliacao_dinamica": None,
                "detalhes": "Código reprovado na análise estática. Verifique os conceitos faltantes."
            }

        # 2. Avaliação dinâmica
        resultado_dinamico = self.avaliar_dinamico(codigo_aluno, casos_de_teste)

        return {
            "status": resultado_dinamico["status"],
            "avaliacao_estatica": resultado_estatico,
            "avaliacao_dinamica": resultado_dinamico,
            "detalhes": resultado_dinamico.get("detalhes", "")
        }


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