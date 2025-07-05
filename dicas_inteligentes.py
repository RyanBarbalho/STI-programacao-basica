"""
Sistema de Dicas Inteligentes usando LLM
Gera dicas personalizadas baseadas no erro do aluno
"""

import os
import json
import requests
from typing import Dict, List, Optional

# Carregar variáveis de ambiente do arquivo .env se existir
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class DicasInteligentes:
    """
    Classe para gerar dicas inteligentes usando LLM
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1/chat/completions"

    def gerar_dica_erro_compilacao(self, codigo: str, erro: str, tipo_problema: str) -> str:
        """
        Gera dica específica para erro de compilação
        """
        # Tentar usar API primeiro
        prompt = f"""
        Você é um professor experiente de programação C. O aluno cometeu um erro de compilação.

        TIPO DE PROBLEMA: {tipo_problema}
        CÓDIGO DO ALUNO:
        {codigo}

        ERRO DE COMPILAÇÃO:
        {erro}

        Gere uma dica específica e útil (máximo 2 frases) que ajude o aluno a corrigir o erro.
        Seja direto e específico. Não dê a resposta completa, apenas uma dica.

        Responda apenas com a dica, sem formatação adicional.
        """

        dica_api = self._chamar_llm(prompt)

        # Se a API falhou, usar análise local
        if dica_api == self._dica_padrao():
            return self._gerar_dica_inteligente_local(codigo, "compilacao", {"erro": erro})

        return dica_api

    def gerar_dica_resposta_errada(self, codigo: str, entrada: str, saida_esperada: str,
                                  saida_obtida: str, tipo_problema: str) -> str:
        """
        Gera dica específica para resposta incorreta
        """
        # Tentar usar API primeiro
        prompt = f"""
        Você é um professor experiente de programação C. O aluno resolveu o problema, mas a saída está incorreta.

        TIPO DE PROBLEMA: {tipo_problema}
        CÓDIGO DO ALUNO:
        {codigo}

        ENTRADA: {entrada if entrada else "(sem entrada)"}
        SAÍDA ESPERADA: {saida_esperada}
        SAÍDA OBTIDA: {saida_obtida if saida_obtida else "(saída vazia)"}

        Analise a diferença entre a saída esperada e a obtida. Gere uma dica específica (máximo 2 frases)
        que ajude o aluno a identificar e corrigir o problema.

        Seja direto e específico. Não dê a resposta completa, apenas uma dica.

        Responda apenas com a dica, sem formatação adicional.
        """

        dica_api = self._chamar_llm(prompt)

        # Se a API falhou, usar análise local
        if dica_api == self._dica_padrao():
            contexto = {
                "entrada": entrada,
                "saida_esperada": saida_esperada,
                "saida_obtida": saida_obtida
            }
            return self._gerar_dica_inteligente_local(codigo, "resposta_errada", contexto)

        return dica_api

    def gerar_dica_conceitos_faltantes(self, codigo: str, conceitos_faltantes: List[str],
                                     tipo_problema: str, enunciado: str) -> str:
        """
        Gera dica para conceitos faltantes
        """
        # Tentar usar API primeiro
        conceitos_str = ", ".join(conceitos_faltantes)

        prompt = f"""
        Você é um professor experiente de programação C. O aluno não usou alguns conceitos necessários.

        TIPO DE PROBLEMA: {tipo_problema}
        ENUNCIADO: {enunciado}
        CÓDIGO DO ALUNO:
        {codigo}

        CONCEITOS FALTANTES: {conceitos_str}

        Gere uma dica específica (máximo 2 frases) que oriente o aluno sobre quais conceitos usar
        para resolver o problema corretamente.

        Seja direto e específico. Não dê a resposta completa, apenas uma dica.

        Responda apenas com a dica, sem formatação adicional.
        """

        dica_api = self._chamar_llm(prompt)

        # Se a API falhou, usar análise local
        if dica_api == self._dica_padrao():
            contexto = {"conceitos_faltantes": conceitos_faltantes}
            return self._gerar_dica_inteligente_local(codigo, "conceitos_faltantes", contexto)

        return dica_api

    def gerar_dica_geral(self, codigo: str, tipo_problema: str, enunciado: str, pergunta: str = "") -> str:
        """
        Gera dica geral para o problema ou responde perguntas específicas
        """
        if pergunta:
            # Se há uma pergunta específica, responder a ela
            prompt = f"""
            Você é um professor experiente de programação C. O aluno fez uma pergunta sobre um problema.

            TIPO DE PROBLEMA: {tipo_problema}
            ENUNCIADO: {enunciado}
            CÓDIGO DO ALUNO:
            {codigo}

            PERGUNTA DO ALUNO: {pergunta}

            Responda à pergunta do aluno de forma clara e específica (máximo 3 frases).
            Seja direto e útil. Se a pergunta for sobre não entender o enunciado, explique de forma simples.

            Responda apenas com a resposta, sem formatação adicional.
            """
        else:
            # Dica geral (comportamento original)
            prompt = f"""
            Você é um professor experiente de programação C. O aluno está tentando resolver um problema.

            TIPO DE PROBLEMA: {tipo_problema}
            ENUNCIADO: {enunciado}
            CÓDIGO DO ALUNO:
            {codigo}

            Gere uma dica geral e motivacional (máximo 2 frases) que ajude o aluno a pensar sobre
            como resolver o problema.

            Seja encorajador e direto. Não dê a resposta completa, apenas uma orientação.

            Responda apenas com a dica, sem formatação adicional.
            """

        dica_api = self._chamar_llm(prompt)

        # Se a API falhou, usar análise local
        if dica_api == self._dica_padrao():
            contexto = {"pergunta": pergunta}
            return self._gerar_dica_inteligente_local(codigo, "geral", contexto)

        return dica_api

    def _chamar_llm(self, prompt: str) -> str:
        """
        Chama a API da OpenAI para gerar dicas
        """
        if not self.api_key:
            return self._dica_padrao()

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "Você é um professor de programação C experiente e paciente."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 150,
                "temperature": 0.7
            }

            response = requests.post(self.base_url, headers=headers, json=data, timeout=10)

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                return self._dica_padrao()

        except Exception as e:
            print(f"Erro ao chamar LLM: {e}")
            return self._dica_padrao()

    def _dica_padrao(self) -> str:
        """
        Retorna dicas padrão quando a LLM não está disponível
        """
        dicas = [
            "💡 Revise o código e verifique se todos os conceitos necessários estão sendo usados.",
            "🔍 Compare sua saída com a esperada e identifique as diferenças.",
            "📚 Lembre-se de usar as estruturas de controle apropriadas para este tipo de problema.",
            "✅ Verifique se a sintaxe está correta e se todas as chaves estão balanceadas.",
            "🎯 Foque nos conceitos principais deste tipo de problema."
        ]
        import random
        return random.choice(dicas)

    def _gerar_dica_inteligente_local(self, codigo: str, tipo_erro: str, contexto: dict) -> str:
        """
        Gera dicas inteligentes usando análise local do código
        """
        codigo_lower = codigo.lower()

        # Verificar se há uma pergunta específica no contexto
        pergunta = contexto.get('pergunta', '').lower() if contexto else ''

        # Responder perguntas conceituais comuns
        if pergunta:
            if 'estrutura de controle' in pergunta:
                return "Uma estrutura de controle em C é um comando como if, else, while ou for que controla o fluxo de execução do programa."
            elif 'printf' in pergunta:
                return "printf() é uma função em C usada para exibir texto na tela. Exemplo: printf('Olá mundo!');"
            elif 'scanf' in pergunta:
                return "scanf() é uma função em C usada para ler dados do teclado. Exemplo: scanf('%d', &numero);"
            elif 'enunciado' in pergunta or 'não entendi' in pergunta:
                return "O enunciado descreve o que seu programa deve fazer. Leia com atenção e identifique o que precisa ser feito."
            elif 'main' in pergunta:
                return "main() é a função principal em C. Todo programa deve ter uma função main() que é onde a execução começa."
            elif 'include' in pergunta:
                return "#include é usado para incluir bibliotecas. stdio.h é a biblioteca padrão para entrada/saída."
            elif 'variável' in pergunta:
                return "Uma variável é um espaço na memória para armazenar dados. Em C, declare com: int nome;"
            elif 'loop' in pergunta or 'repetição' in pergunta:
                return "Loops repetem ações. Use while() para repetir enquanto uma condição for verdadeira, ou for() para repetir um número específico de vezes."
            elif 'condicional' in pergunta or 'if' in pergunta:
                return "Estruturas condicionais (if/else) permitem tomar decisões no programa baseado em condições."

        if tipo_erro == "compilacao":
            # Análise específica de erros de compilação
            if "'" in codigo and '"' not in codigo:
                return "💡 Você está usando aspas simples (') para strings. Em C, use aspas duplas (\") para strings."

            if "printf" in codigo_lower and ";" not in codigo:
                return "💡 Lembre-se de terminar os comandos com ponto e vírgula (;)."

            if "main" not in codigo_lower:
                return "💡 Todo programa C precisa ter uma função main()."

            if "#include" not in codigo_lower:
                return "💡 Não esqueça de incluir as bibliotecas necessárias com #include."

            return "💡 Verifique a sintaxe do código. Erros comuns: chaves desbalanceadas, ponto e vírgula faltando, aspas incorretas."

        elif tipo_erro == "resposta_errada":
            entrada = contexto.get('entrada', '')
            saida_esperada = contexto.get('saida_esperada', '')
            saida_obtida = contexto.get('saida_obtida', '')

            # Análise de diferenças específicas
            if saida_esperada and saida_obtida:
                if len(saida_esperada) != len(saida_obtida):
                    return f"💡 Sua saída tem {len(saida_obtida)} caracteres, mas deveria ter {len(saida_esperada)}. Verifique espaços e pontuação."

                if saida_esperada.lower() == saida_obtida.lower():
                    return "💡 A saída está correta, mas verifique maiúsculas/minúsculas e pontuação."

                if not saida_obtida:
                    return "💡 Sua saída está vazia. Verifique se está usando printf() corretamente."

            return "💡 Compare sua saída com a esperada. Verifique espaços, pontuação e formatação."

        elif tipo_erro == "conceitos_faltantes":
            conceitos = contexto.get('conceitos_faltantes', [])

            dicas_especificas = []
            for conceito in conceitos:
                if "printf" in conceito.lower():
                    dicas_especificas.append("Use printf() para exibir texto na tela")
                elif "scanf" in conceito.lower():
                    dicas_especificas.append("Use scanf() para ler dados do teclado")
                elif "if" in conceito.lower():
                    dicas_especificas.append("Use if/else para tomar decisões no programa")
                elif "while" in conceito.lower() or "for" in conceito.lower():
                    dicas_especificas.append("Use while ou for para repetir ações")
                elif "vetor" in conceito.lower() or "array" in conceito.lower():
                    dicas_especificas.append("Use arrays para armazenar múltiplos valores")
                elif "função" in conceito.lower():
                    dicas_especificas.append("Crie funções para organizar seu código")

            if dicas_especificas:
                return f"💡 Para este problema, você precisa: {', '.join(dicas_especificas)}."

            return "💡 Revise os conceitos necessários para este tipo de problema."

        return "💡 Analise o código e identifique o que precisa ser corrigido."


# Função de conveniência para uso rápido
def gerar_dica_erro_compilacao(codigo: str, erro: str, tipo_problema: str) -> str:
    """Função de conveniência para gerar dica de erro de compilação"""
    dicas = DicasInteligentes()
    return dicas.gerar_dica_erro_compilacao(codigo, erro, tipo_problema)

def gerar_dica_resposta_errada(codigo: str, entrada: str, saida_esperada: str,
                              saida_obtida: str, tipo_problema: str) -> str:
    """Função de conveniência para gerar dica de resposta incorreta"""
    dicas = DicasInteligentes()
    return dicas.gerar_dica_resposta_errada(codigo, entrada, saida_esperada, saida_obtida, tipo_problema)

def gerar_dica_conceitos_faltantes(codigo: str, conceitos_faltantes: List[str],
                                 tipo_problema: str, enunciado: str) -> str:
    """Função de conveniência para gerar dica de conceitos faltantes"""
    dicas = DicasInteligentes()
    return dicas.gerar_dica_conceitos_faltantes(codigo, conceitos_faltantes, tipo_problema, enunciado)