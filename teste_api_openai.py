"""
Teste específico da API OpenAI
"""

import os
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def testar_api_openai():
    """
    Testa a conexão com a API OpenAI
    """
    print("🔍 TESTE DA API OPENAI")
    print("=" * 40)

    # Verificar se a chave está disponível
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("❌ Chave da API não encontrada!")
        print("Configure a variável OPENAI_API_KEY ou crie um arquivo .env")
        return False

    print(f"✅ Chave da API encontrada: {api_key[:20]}...")

    # Testar a API
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Você é um professor de programação C."},
            {"role": "user", "content": "Gere uma dica simples para um erro de compilação em C."}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }

    try:
        print("🔄 Testando conexão com a API...")
        response = requests.post(url, headers=headers, json=data, timeout=10)

        if response.status_code == 200:
            result = response.json()
            dica = result['choices'][0]['message']['content'].strip()
            print(f"✅ API funcionando! Dica gerada: {dica}")
            return True
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Erro ao conectar com a API: {e}")
        return False

if __name__ == "__main__":
    sucesso = testar_api_openai()
    if sucesso:
        print("\n🎉 API configurada corretamente!")
        print("Agora você pode executar: streamlit run interface_streamlit.py")
    else:
        print("\n⚠️ Verifique sua chave da API e conexão com a internet.")