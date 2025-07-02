#!/usr/bin/env python3
"""
Script para verificar se o GCC está instalado e fornecer instruções de instalação
"""

import os
import subprocess


def verificar_gcc():
    """Verifica se o GCC está disponível no sistema"""
    
    print("🔍 Verificando se o GCC está instalado...")
    
    try:
        # Tentar executar gcc --version
        resultado = subprocess.run(['gcc', '--version'], 
                                 capture_output=True, text=True, timeout=5)
        
        if resultado.returncode == 0:
            print("✅ GCC encontrado!")
            print(f"   Versão: {resultado.stdout.split('\n')[0]}")
            return True
        else:
            print("❌ GCC não encontrado")
            return False
            
    except FileNotFoundError:
        print("❌ GCC não encontrado no PATH")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar GCC: {e}")
        return False

def instrucoes_instalacao():
    """Fornece instruções para instalar o GCC"""
    
    print("\n📋 INSTRUÇÕES PARA INSTALAR O GCC:")
    print("=" * 50)
    
    if os.name == 'nt':  # Windows
        print("1. Instalar MSYS2:")
        print("   - Baixe em: https://www.msys2.org/")
        print("   - Ou use: winget install MSYS2.MSYS2")
        print()
        print("2. Abra o MSYS2 e execute:")
        print("   pacman -S mingw-w64-x86_64-gcc")
        print()
        print("3. Adicione ao PATH do usuário:")
        print("   C:\\msys64\\mingw64\\bin")
        print()
        print("4. Reinicie o terminal e teste:")
        print("   gcc --version")
    else:  # Linux/Mac
        print("1. Ubuntu/Debian:")
        print("   sudo apt update && sudo apt install gcc")
        print()
        print("2. CentOS/RHEL:")
        print("   sudo yum install gcc")
        print()
        print("3. macOS:")
        print("   xcode-select --install")

def testar_compilacao():
    """Testa se o GCC consegue compilar um código simples"""
    
    print("\n🧪 Testando compilação...")
    
    # Código C simples para teste
    codigo_teste = """
#include <stdio.h>

int main() {
    printf("Teste de compilacao OK!\\n");
    return 0;
}
"""
    
    try:
        # Salvar código de teste
        with open("teste_gcc.c", "w") as f:
            f.write(codigo_teste)
        
        # Compilar
        resultado = subprocess.run(
            ['gcc', 'teste_gcc.c', '-o', 'teste_gcc'],
            capture_output=True, text=True, timeout=10
        )
        
        if resultado.returncode == 0:
            print("✅ Compilação de teste bem-sucedida!")
            
            # Executar
            execucao = subprocess.run(
                ['./teste_gcc'] if os.name != 'nt' else ['teste_gcc'],
                capture_output=True, text=True, timeout=5
            )
            
            if execucao.returncode == 0:
                print("✅ Execução de teste bem-sucedida!")
                print(f"   Saída: {execucao.stdout.strip()}")
            else:
                print("❌ Erro na execução de teste")
                
        else:
            print("❌ Erro na compilação de teste")
            print(f"   Erro: {resultado.stderr}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    finally:
        # Limpar arquivos de teste
        try:
            if os.path.exists("teste_gcc.c"):
                os.remove("teste_gcc.c")
            if os.path.exists("teste_gcc"):
                os.remove("teste_gcc")
            if os.name == 'nt' and os.path.exists("teste_gcc.exe"):
                os.remove("teste_gcc.exe")
        except:
            pass

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 VERIFICADOR DE GCC PARA SISTEMA DE AVALIAÇÃO")
    print("=" * 60)
    
    if verificar_gcc():
        testar_compilacao()
        print("\n🎉 GCC está funcionando corretamente!")
        print("   O sistema de avaliação dinâmica deve funcionar.")
    else:
        instrucoes_instalacao()
        print("\n⚠️  Instale o GCC para usar a avaliação dinâmica.")
        print("   A avaliação estática continuará funcionando.")
    
    print("\n" + "=" * 60) 