import time
import json
import sys
import os

def login():
    # Define o caminho do arquivo na subpasta "dados"
    caminho_arquivo = os.path.join('dados', 'dados_usuarios.json')
    
    # Verifica se o arquivo existe antes de tentar abrir
    if not os.path.exists(caminho_arquivo):
        print(f"\033[1mErro: O arquivo {caminho_arquivo} não foi encontrado.\033[0m")
        sys.exit()

    with open(caminho_arquivo, 'r', encoding='utf-8') as arq_user:
        dados_usuarios = json.load(arq_user)
        
    while True:
        print(f"\n{"─" * 8} [Enter] Para Encerrar Programa {"─" * 8}\n")
        usuario_input = input(f"\nRealize o Login para ter acesso ao Menu Principal\nDigite o usuario: \n")
        
        if usuario_input == "":
            print("\033[1mEncerrando o programa...\033[0m")
            time.sleep(2)
            sys.exit()
            
        senha_input = input(f"Digite sua senha:\n")
   
        found = False
        for usuario in dados_usuarios:
            if usuario["usuario"] == usuario_input and usuario["senha"] == senha_input:
                found = True
                break

        if found:
            print(f"\n\033[1mAcesso concedido\033[0m\n")
            time.sleep(1)
            break
        else:
            print(f"\033[1mUsuário ou senha incorretos, tente novamente\033[0m\n")
            time.sleep(1)