import os
import shutil

def remover_pycache(diretorio):
    """Remove todos os diretórios __pycache__ recursivamente."""
    for root, dirs, files in os.walk(diretorio):
        for d in dirs:
            if d == "__pycache__":
                caminho_pycache = os.path.join(root, d)
                shutil.rmtree(caminho_pycache)

def listar_estrutura_pastas(diretorio, nivel=0):
    """Lista a estrutura de pastas do diretório especificado."""
    indentacao = ' ' * 4 * nivel
    print(f"{indentacao}{os.path.basename(diretorio)}/")
    for item in os.listdir(diretorio):
        caminho_completo = os.path.join(diretorio, item)
        if os.path.isdir(caminho_completo):
            listar_estrutura_pastas(caminho_completo, nivel + 1)
        else:
            print(f"{indentacao}    {item}")

# Caminho do diretório raiz do seu projeto
diretorio_raiz = '/home/max-alves/Área de trabalho/supermercado_api/app'

# Executa a remoção de __pycache__ e depois exibe a estrutura
remover_pycache(diretorio_raiz)
listar_estrutura_pastas(diretorio_raiz)
