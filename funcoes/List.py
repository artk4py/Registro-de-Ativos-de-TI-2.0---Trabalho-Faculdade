import time
import os

class GerenciadorListagem:
    def __init__(self):
        pass

    def listar_todos(self, gerenciador_usuario, gerenciador_ativo, gerenciador_vulnerabilidade):
        """Lista usuários, ativos e vulnerabilidades."""
        print("\n--- LISTAGEM GERAL ---")
        
        # Listar Usuários
        print("\033[1mUsuários:\033[0m")
        if not gerenciador_usuario.dados:
            print("  Nenhum usuário cadastrado.")
        for user in gerenciador_usuario.dados:
            print(f"  ID: {user['id']}, Usuário: {user['usuario']}")
        
        time.sleep(0.5)

        # Listar Ativos
        print("\n\033[1mAtivos:\033[0m")
        if not gerenciador_ativo.dados:
            print("  Nenhum ativo cadastrado.")
        for ativo in gerenciador_ativo.dados:
            print(f"  ID: {ativo['id_ativo']}, Tipo: {ativo['tipo_ativo']}, Responsável: {ativo['resp_ativo']}, Setor: {ativo['setor']}")
            
        time.sleep(0.5)
        
        # Listar Vulnerabilidades
        print("\n\033[1mVulnerabilidades:\033[0m")
        if not gerenciador_vulnerabilidade.dados:
            print("  Nenhuma vulnerabilidade cadastrada.")
        for vuln in gerenciador_vulnerabilidade.dados:
            print(f"  ID: {vuln['id_vulnerabilidade']}, Descrição: {vuln['descricao'][:50]}..., Status: {vuln['status']}")
        
        time.sleep(1)

    def procurar_item(self, gerenciador_usuario, gerenciador_ativo, gerenciador_vulnerabilidade):
        """Menu para busca específica."""
        while True:
            procurar_opcao = input("\nDeseja procurar um item específico? (s/n): ").strip().lower()
            if procurar_opcao == 's':
                tipos_permitidos = ["Usuario", "Ativo", "Vulnerabilidade"]
                tipo = input(f"Escolha o que deseja procurar ({', '.join(tipos_permitidos)}): ").capitalize()
                
                if tipo not in tipos_permitidos:
                    print("\033[1mOpção inválida.\033[0m")
                    continue

                try:
                    id_busca = int(input(f"Digite o ID do(a) {tipo} que deseja procurar: "))
                    
                    if tipo == "Usuario":
                        item = next((u for u in gerenciador_usuario.dados if u['id'] == id_busca), None)
                        if item: print(f"\nEncontrado: {item}")
                    elif tipo == "Ativo":
                        item = next((a for a in gerenciador_ativo.dados if a['id_ativo'] == id_busca), None)
                        if item: print(f"\nEncontrado: {item}")
                    elif tipo == "Vulnerabilidade":
                        item = next((v for v in gerenciador_vulnerabilidade.dados if v['id_vulnerabilidade'] == id_busca), None)
                        if item: print(f"\nEncontrado: {item}")
                    
                    if not item:
                        print(f"\033[1m{tipo} com ID {id_busca} não encontrado.\033[0m")
                        
                except ValueError:
                    print("\033[1mID inválido. Digite um número.\033[0m")
                
                break
            elif procurar_opcao == 'n':
                break
            else:
                print("\033[1mOpção inválida.\033[0m")