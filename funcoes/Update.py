import time
import datetime
import os

class GerenciadorAtualizacao:
    def __init__(self, gerenciador_usuario, gerenciador_ativo, gerenciador_vulnerabilidade):
        self.gerenciador_usuario = gerenciador_usuario
        self.gerenciador_ativo = gerenciador_ativo
        self.gerenciador_vulnerabilidade = gerenciador_vulnerabilidade

    def executar_menu_atualizacao(self):
        while True:
            opcao = input("\n--- MENU DE ATUALIZAÇÃO ---\n"
                          "1- Atualizar Senha de Usuário\n"
                          "2- Atualizar Responsável por Ativo\n"
                          "3- Atualizar Data de Manutenção\n"
                          "4- Marcar Vulnerabilidade como Tratada\n"
                          "\nAperte Enter para voltar ao Menu Principal\n").strip()
            
            if not opcao: break
            
            match opcao:
                case "1": self._atualizar_senha()
                case "2": self._atualizar_responsavel()
                case "3": self._atualizar_manutencao()
                case "4": self._tratar_vulnerabilidade()
                case _: print("\033[1mOpção inválida.\033[0m")

    def _atualizar_senha(self):
        user_id = input("Digite o ID do usuário para atualizar a senha: ")
        try:
            user_id = int(user_id)
            user = next((u for u in self.gerenciador_usuario.dados if u['id'] == user_id), None)
            if user:
                user['senha'] = input(f"Nova senha para {user['usuario']}: ")
                self.gerenciador_usuario._salvar_dados()
                # Atualiza vulnerabilidades relacionadas
                for vuln in self.gerenciador_vulnerabilidade.dados:
                    if vuln.get('id_ativo') is None and f"Usuário ID {user_id}" in vuln['descricao']:
                        vuln['status'] = 'Tratado'
                self.gerenciador_vulnerabilidade._salvar_dados()
                print("\033[1mSenha atualizada com sucesso!\033[0m")
            else:
                print("Usuário não encontrado.")
        except ValueError: print("ID inválido.")

    def _atualizar_responsavel(self):
        ativo_id = input("Digite o ID do ativo para atualizar o responsável: ")
        try:
            ativo_id = int(ativo_id)
            ativo = next((a for a in self.gerenciador_ativo.dados if a['id_ativo'] == ativo_id), None)
            if ativo:
                ativo['resp_ativo'] = input("Novo responsável: ")
                self.gerenciador_ativo._salvar_dados()
                print("\033[1mResponsável atualizado com sucesso!\033[0m")
            else: print("Ativo não encontrado.")
        except ValueError: print("ID inválido.")

    def _atualizar_manutencao(self):
        ativo_id = input("Digite o ID do ativo para atualizar a manutenção: ")
        try:
            ativo_id = int(ativo_id)
            ativo = next((a for a in self.gerenciador_ativo.dados if a['id_ativo'] == ativo_id), None)
            if ativo:
                nova_data = input("Nova data (DD/MM/AAAA): ")
                # Validação simples
                datetime.datetime.strptime(nova_data, '%d/%m/%Y')
                ativo['manutencao'] = nova_data
                self.gerenciador_ativo._salvar_dados()
                # Resolve vulnerabilidades de manutenção
                for vuln in self.gerenciador_vulnerabilidade.dados:
                    if vuln.get('id_ativo') == ativo_id and "Manutenção atrasada" in vuln['descricao']:
                        vuln['status'] = 'Tratado'
                self.gerenciador_vulnerabilidade._salvar_dados()
                print("\033[1mData atualizada com sucesso!\033[0m")
            else: print("Ativo não encontrado.")
        except ValueError: print("Data ou ID inválido.")

    def _tratar_vulnerabilidade(self):
        print("\n\033[1mVulnerabilidades Não Tratadas:\033[0m")
        pendentes = [v for v in self.gerenciador_vulnerabilidade.dados if v['status'] == 'Não tratado']
        if not pendentes:
            print("Nenhuma pendência.")
            return
        
        for v in pendentes:
            print(f"ID: {v['id_vulnerabilidade']} - {v['descricao']}")
            
        vuln_id = input("Digite o ID da vulnerabilidade para tratar (ou 'n' para cancelar): ")
        if vuln_id.lower() == 'n': return
        try:
            vuln = next((v for v in self.gerenciador_vulnerabilidade.dados if v['id_vulnerabilidade'] == int(vuln_id)), None)
            if vuln:
                vuln['status'] = 'Tratado'
                self.gerenciador_vulnerabilidade._salvar_dados()
                print("Vulnerabilidade marcada como tratada.")
        except ValueError: print("ID inválido.")