"""
Configuração de APIs para o Sistema de Dicas Inteligentes
"""

import os
from typing import Optional

def configurar_api_key():
    """
    Configura a chave da API OpenAI
    """
    # Verificar se já existe uma variável de ambiente
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("🤖 Sistema de Dicas Inteligentes")
        print("=" * 50)
        print("Para usar dicas inteligentes personalizadas, você precisa de uma chave da API OpenAI.")
        print("Se você não tiver uma chave, o sistema usará dicas padrão.")
        print()

        # Perguntar se o usuário quer configurar
        resposta = input("Deseja configurar a API key agora? (s/n): ").lower().strip()

        if resposta in ['s', 'sim', 'y', 'yes']:
            print()
            print("📝 Para obter uma chave da API OpenAI:")
            print("1. Acesse: https://platform.openai.com/api-keys")
            print("2. Faça login ou crie uma conta")
            print("3. Clique em 'Create new secret key'")
            print("4. Copie a chave gerada")
            print()

            api_key = input("Cole sua chave da API OpenAI aqui: ").strip()

            if api_key:
                # Salvar em arquivo .env
                with open('.env', 'w') as f:
                    f.write(f'OPENAI_API_KEY={api_key}\n')

                # Definir variável de ambiente
                os.environ['OPENAI_API_KEY'] = api_key

                print("✅ Chave da API configurada com sucesso!")
                print("💡 A chave foi salva no arquivo .env")
                return True
            else:
                print("❌ Nenhuma chave foi fornecida.")
                return False
        else:
            print("ℹ️ Sistema configurado para usar dicas padrão.")
            return False

    return True

def obter_api_key() -> Optional[str]:
    """
    Obtém a chave da API OpenAI
    """
    return os.getenv('OPENAI_API_KEY')

def verificar_configuracao():
    """
    Verifica se a API está configurada
    """
    api_key = obter_api_key()
    if api_key:
        print("🤖 Sistema de Dicas Inteligentes: ATIVO")
        return True
    else:
        print("🤖 Sistema de Dicas Inteligentes: MODO PADRÃO")
        return False

if __name__ == "__main__":
    configurar_api_key()
    verificar_configuracao()