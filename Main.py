import time
import sys
import os

from funcoes.Cad_Del import GerenciadorUsuario, GerenciadorAtivo
from funcoes.List import GerenciadorListagem
from funcoes.Update import GerenciadorAtualizacao
from funcoes.Vulnerabilidades import GerenciadorVulnerabilidade
from funcoes.login import login

class AplicativoConsole:
    def __init__(self):
        self.g_usuario = GerenciadorUsuario()
        self.g_ativo = GerenciadorAtivo()
        self.g_vuln = GerenciadorVulnerabilidade()
        self.listagem = GerenciadorListagem()
        self.atualizador = GerenciadorAtualizacao(self.g_usuario, self.g_ativo, self.g_vuln)

    def executar(self):
        while True:
            login()
            
            print("\n" + "═" * 40)
            print("        SISTEMA DE GESTÃO DE TI  ")
            print("═" * 40)
            
            while True:
                print("\n" + "╭" + "─" * 38 + "╮")
                print(f"{"SELECIONE UMA OPERAÇÃO": ^38}")
                print(f"├" + "─" * 38 + "┤")
                print(f"{"├[1]  Cadastrar (Usuário/Ativo)": <38}")
                print(f"{"├[2]  Listar e Procurar": <38}")
                print(f"{"├[3]  Auditoria (Vulnerabilidades)": <38}")
                print(f"{"├[4]  Atualizar Dados": <38}")
                print(f"{"├[5]  Deletar (Usuário/Ativo) ": <38}")
                print(f"{"├" + "─" * 38 + "┤"}")
                print(f"{"├[Enter] Sair / Logout ": <38}")
                print(f"╰" + "─" * 38 + "╯")
                
                opcoes = input("   >> ").strip()

                if not opcoes: 
                    print("\n Realizando Logout...\n\n")
                    time.sleep(2)
                    break

                print("-" * 40)
                match opcoes:
                    case "1": self.g_usuario.adicionar_usuario()
                    case "2":
                        self.listagem.listar_todos(self.g_usuario, self.g_ativo, self.g_vuln)
                        self.listagem.procurar_item(self.g_usuario, self.g_ativo, self.g_vuln)
                    case "3": self.g_vuln.executar_auditoria_completa(self.g_usuario, self.g_ativo)
                    case "4": self.atualizador.executar_menu_atualizacao()
                    case "5": self.g_usuario.deletar_usuario()
                    case _:
                        print(" \033[31mComando desconhecido! Tente novamente.\033[0m")
                        time.sleep(1)

if __name__ == '__main__':
    app = AplicativoConsole()
    app.executar()