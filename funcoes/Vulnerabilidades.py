import time
import datetime
import os
import json

class GerenciadorJson:
    def __init__(self, nome_arquivo, dados_padrao=None):
        self.nome_arquivo = nome_arquivo
        self.dados = []
        self._garantir_arquivo_existe(dados_padrao)
        self._carregar_dados()

    def _garantir_arquivo_existe(self, dados_padrao):
        # Extrai o diretório (pasta) do caminho do arquivo
        diretorio = os.path.dirname(self.nome_arquivo)
        
        # Se houver um diretório especificado e ele não existir, cria a pasta
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)

        # Se o arquivo não existir, cria um novo
        if not os.path.exists(self.nome_arquivo):
            with open(self.nome_arquivo, 'w', encoding='utf-8') as arquivo:
                json.dump(dados_padrao if dados_padrao is not None else [], arquivo, indent=4, ensure_ascii=False)

    def _carregar_dados(self):
        with open(self.nome_arquivo, 'r', encoding='utf-8') as arquivo:
            self.dados = json.load(arquivo)

    def _salvar_dados(self):
        with open(self.nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(self.dados, arquivo, indent=4, ensure_ascii=False)

class GerenciadorVulnerabilidade(GerenciadorJson):
    def __init__(self, nome_arquivo=os.path.join('dados', 'vulnerabilidades_cadastradas.json')):
        super().__init__(nome_arquivo)

    def _obter_proximo_id(self):
        """Método auxiliar para gerar o ID sequencial da vulnerabilidade."""
        if self.dados:
            return max([vuln["id_vulnerabilidade"] for vuln in self.dados]) + 1
        return 1

    def verificar_senhas_fracas(self, dados_usuarios):
        print("\033[1mVerificando senhas fracas...\033[0m")
        for usuario in dados_usuarios:
            descricao_senha_fraca = f"Usuário ID {usuario['id']} ({usuario['usuario']}): Senha fraca ou padrão ('{usuario['senha']}')"
            
            # Verifica se já existe uma vulnerabilidade não tratada idêntica
            existindo_vuln = next((vuln for vuln in self.dados if 
                                   vuln['descricao'] == descricao_senha_fraca and 
                                   vuln['status'] == 'Não tratado'), None)
            
            if (usuario['senha'] == '1234' or len(usuario['senha']) < 4) and not existindo_vuln:
                self.dados.append({
                    "id_vulnerabilidade": self._obter_proximo_id(),
                    "descricao": descricao_senha_fraca,
                    "severidade": "Baixa",
                    "status": "Não tratado",
                    "id_ativo": None
                })
                self._salvar_dados()
        time.sleep(1)

    def verificar_manutencao_atrasada(self, dados_ativos):
        print("\033[1mVerificando falta de manutenção em ativos...\033[0m")
        data_atual = datetime.datetime.now()
        
        for ativo in dados_ativos:
            try:
                manutencao_data_str = ativo['manutencao']
                try:
                    manutencao_data = datetime.datetime.strptime(manutencao_data_str, '%d/%m/%y')
                except ValueError:
                    manutencao_data = datetime.datetime.strptime(manutencao_data_str, '%d/%m/%Y')

                descricao_manut_atrasada = f"Ativo ID {ativo['id_ativo']} ({ativo['tipo_ativo']}): Manutenção atrasada (última manutenção: {ativo['manutencao']})"
                
                existindo_vuln = next((vuln for vuln in self.dados if
                                       vuln['descricao'] == descricao_manut_atrasada and
                                       vuln['status'] == 'Não tratado'), None)
                
                if manutencao_data < data_atual - datetime.timedelta(days=30) and not existindo_vuln:
                    self.dados.append({
                        "id_vulnerabilidade": self._obter_proximo_id(),
                        "descricao": descricao_manut_atrasada,
                        "severidade": "Média",
                        "status": "Não tratado",
                        "id_ativo": ativo['id_ativo']
                    })
                    self._salvar_dados()
                    
            except ValueError:
                descricao_data_invalida = f"Ativo ID {ativo['id_ativo']} ({ativo['tipo_ativo']}): Data de manutenção inválida ou em formato incorreto ('{ativo['manutencao']}')"
                
                existindo_vuln = next((vuln for vuln in self.dados if
                                       vuln['descricao'] == descricao_data_invalida and
                                       vuln['status'] == 'Não tratado'), None)
                
                if not existindo_vuln:
                    self.dados.append({
                        "id_vulnerabilidade": self._obter_proximo_id(),
                        "descricao": descricao_data_invalida,
                        "severidade": "Média", 
                        "status": "Não tratado",
                        "id_ativo": ativo['id_ativo']
                    })
                    self._salvar_dados()
        time.sleep(1)

    def cadastrar_vulnerabilidade_manual(self, dados_ativos):
        while True:
            manual_vulnerabilidade = input("\nDeseja cadastrar uma vulnerabilidade manualmente? (s/n): \n").strip().lower()
            
            if manual_vulnerabilidade == 's':
                id_ativo_vulnerabilidade = None
                while True:
                    time.sleep(1)
                    id_ativo_input = input("\nDigite o ID do ativo ao qual a vulnerabilidade se refere (ou 'n' para sem ativo específico): \n").strip()
                    
                    if id_ativo_input.lower() == 'n':
                        id_ativo_vulnerabilidade = None
                        break
                    try:
                        id_ativo_vulnerabilidade = int(id_ativo_input)
                        ativo_existente = any(ativo['id_ativo'] == id_ativo_vulnerabilidade for ativo in dados_ativos)
                        if ativo_existente:
                            break
                        else:
                            print(f"\033[1mAtivo com ID: {id_ativo_vulnerabilidade} não encontrado. Por favor, digite um ID válido ou 'n'.\033[0m")
                    except ValueError:
                        print("\033[1mID inválido. Por favor, digite um número ou 'n'.\033[0m")

                descricao = input("Descreva a vulnerabilidade manualmente cadastrada: ").strip()
                severidade_manual = ''
                niveis_severidade = ['Baixa', 'Média', 'Alta']
                
                while severidade_manual not in niveis_severidade:
                    severidade_manual = input("Digite a severidade da vulnerabilidade (Baixa, Média, Alta): ").strip().capitalize()
                    if severidade_manual not in niveis_severidade:
                        print(f"\033[1mSeveridade inválida. Escolha entre: {', '.join(niveis_severidade)}.\033[0m")

                self.dados.append({
                    "id_vulnerabilidade": self._obter_proximo_id(),
                    "descricao": descricao,
                    "severidade": severidade_manual,
                    "status": "Não tratado",
                    "id_ativo": id_ativo_vulnerabilidade
                })
                self._salvar_dados()
                print(f"\033[1mVulnerabilidade manual cadastrada com ID: {self.dados[-1]['id_vulnerabilidade']}\033[0m")

            elif manual_vulnerabilidade == 'n':
                break
            else:
                print("\033[1mOpção inválida. Digite 's' para sim ou 'n' para não.\033[0m")

    def listar_nao_tratadas(self):
        vulnerabilidades_nao_tratadas = [vuln for vuln in self.dados if vuln['status'] == 'Não tratado']
        print("\n\033[1mVulnerabilidades Encontradas (Não Tratadas):\033[0m")
        
        if vulnerabilidades_nao_tratadas:
            for vuln in vulnerabilidades_nao_tratadas:
                ativo_info = f" (Ativo ID: {vuln['id_ativo']})" if vuln['id_ativo'] is not None else ""
                print(f"- ID: {vuln['id_vulnerabilidade']}, Severidade: {vuln['severidade']}, {vuln['descricao']}{ativo_info}")
        else:
            print("Nenhuma vulnerabilidade não tratada encontrada. Nenhum problema interno aparente.")
        time.sleep(2)

    def executar_auditoria_completa(self, gerenciador_usuario, gerenciador_ativo):
        """
        Método orquestrador que conecta tudo. 
        Recebe as instâncias dos outros gerenciadores para acessar seus dados.
        """
        self.verificar_senhas_fracas(gerenciador_usuario.dados)
        self.verificar_manutencao_atrasada(gerenciador_ativo.dados)
        self.cadastrar_vulnerabilidade_manual(gerenciador_ativo.dados)
        self.listar_nao_tratadas()