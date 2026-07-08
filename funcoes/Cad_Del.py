import time
import json
import datetime
import os

# --- Classe Base Gerenciadora para operações JSON ---
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


# --- Classe GerenciadorUsuario ---
class GerenciadorUsuario(GerenciadorJson):
    # Atualizado para apontar para a subpasta "dados"
    def __init__(self, nome_arquivo=os.path.join('dados', 'dados_usuarios.json')):
        super().__init__(nome_arquivo)

    def adicionar_usuario(self):
        while True:
            novo_usuario = input("Digite o nome do novo usuário:\n").strip()
            if novo_usuario:
                break
            else:
                print("\033[1mUsuário não pode ser vazio\033[0m\n")
                time.sleep(1)

        while True:
            senha_novo_usuario = input("Digite uma senha para o novo usuário:\n").strip()
            if senha_novo_usuario:
                break
            else:
                print("\033[1mSenha não pode ser vazia\033[0m\n")
                time.sleep(1)

        proximo_id = 1
        if self.dados:
            proximo_id = max([usuario["id"] for usuario in self.dados]) + 1

        self.dados.append({"id": proximo_id, "usuario": novo_usuario, "senha": senha_novo_usuario})
        self._salvar_dados()
        print(f"\033[1mUsuário cadastrado com ID: {proximo_id}\033[0m\n")
        time.sleep(1)

    def deletar_usuario(self):
        if not self.dados:
            print("\033[1mNenhum usuário cadastrado para deletar.\033[0m\n")
            time.sleep(1)
            return

        try:
            id_usuario = int(input("Digite o ID do usuário que deseja deletar:\n").strip())
        except ValueError:
            print("\033[1mID inválido. Por favor, digite um número.\033[0m\n")
            time.sleep(1)
            return

        # Busca o usuário pelo ID
        usuario_para_deletar = next((usuario for usuario in self.dados if usuario["id"] == id_usuario), None)

        if usuario_para_deletar:
            self.dados.remove(usuario_para_deletar)
            self._salvar_dados()
            print(f"\033[1mUsuário com ID {id_usuario} deletado com sucesso.\033[0m\n")
        else:
            print(f"\033[1mUsuário com ID {id_usuario} não encontrado.\033[0m\n")
        time.sleep(1)


# --- Classe GerenciadorAtivo ---
class GerenciadorAtivo(GerenciadorJson):
    # Atualizado para apontar para a subpasta "dados"
    def __init__(self, nome_arquivo=os.path.join('dados', 'dados_ativos.json')):
        super().__init__(nome_arquivo)
        self.tipos_ativos_permitidos = [
            "Computador", "Servidor", "Roteador",
            "Impressora de rede", "Impressora"
        ]
        self.setores_permitidos = ["Rh", "Adm", "Financeiro", "Diretoria", "Logística"]
        self.marcas_permitidas = ["Samsung", "Dell", "Acer", "Epson"]

    def _validar_data(self, string_data):
        try:
            datetime.datetime.strptime(string_data, '%d/%m/%y')
            return True
        except ValueError:
            try:
                datetime.datetime.strptime(string_data, '%d/%m/%Y')
                return True
            except ValueError:
                return False

    def adicionar_ativo(self):
        while True:
            tipo_ativo = input(
                f"Digite o \033[1mtipo\033[0m de ativo a ser cadastrado ({', '.join(self.tipos_ativos_permitidos)}):\n"
            ).strip().capitalize()
            if tipo_ativo and tipo_ativo in self.tipos_ativos_permitidos:
                break
            elif not tipo_ativo:
                print("\033[1mTipo de ativo não pode ser vazio\033[0m\n")
                time.sleep(1)
            else:
                print(f"\033[1mTipo de ativo inválido. Escolha entre: {', '.join(self.tipos_ativos_permitidos)}\033[0m\n")
                time.sleep(1)

        while True:
            responsavel_ativo = input("Digite o responsável pelo novo ativo:\n").strip()
            if responsavel_ativo:
                if not responsavel_ativo.isdigit():
                    break
                else:
                    print("\033[1mResponsável não pode ser apenas números.\033[0m\n")
                    time.sleep(1)
            else:
                print("\033[1mResponsável não pode ser vazio\033[0m\n")
                time.sleep(1)

        while True:
            data_manutencao = input("Digite a data de aquisição ou última manutenção do ativo (DD/MM/YY ou DD/MM/YYYY):\n").strip()
            if data_manutencao:
                if self._validar_data(data_manutencao):
                    break
                else:
                    print("\033[1mFormato de data inválido. Use DD/MM/YY ou DD/MM/YYYY.\033[0m\n")
                    time.sleep(1)
            else:
                print("\033[1mData de aquisição ou última manutenção não pode ser vazia\033[0m\n")
                time.sleep(1)

        while True:
            setor_ativo = input(
                f"Digite o \033[1msetor\033[0m do ativo a ser cadastrado ({', '.join(self.setores_permitidos)}):\n"
            ).strip().capitalize()
            if setor_ativo and setor_ativo in self.setores_permitidos:
                break
            elif not setor_ativo:
                print("\033[1mSetor do ativo não pode ser vazio\033[0m\n")
                time.sleep(1)
            else:
                print(f"\033[1mSetor do ativo inválido. Escolha entre: {', '.join(self.setores_permitidos)}\033[0m\n")
                time.sleep(1)

        while True:
            marca_ativo = input(
                f"Digite a \033[1mmarca\033[0m do ativo a ser cadastrado ({', '.join(self.marcas_permitidas)}):\n"
            ).strip().capitalize()
            if marca_ativo and marca_ativo in self.marcas_permitidas:
                break
            elif not marca_ativo:
                print("\033[1mMarca do ativo não pode ser vazia\033[0m\n")
                time.sleep(1)
            else:
                print(f"\033[1mMarca do ativo inválida. Escolha entre: {', '.join(self.marcas_permitidas)}\033[0m\n")
                time.sleep(1)

        proximo_id_ativo = 1
        if self.dados:
            proximo_id_ativo = max([ativo['id_ativo'] for ativo in self.dados]) + 1

        self.dados.append({
            "id_ativo": proximo_id_ativo,
            "tipo_ativo": tipo_ativo,
            "resp_ativo": responsavel_ativo,
            "manutencao": data_manutencao,
            "setor": setor_ativo,
            "marca": marca_ativo
        })
        self._salvar_dados()
        print(f"\033[1mAtivo cadastrado com ID: {proximo_id_ativo}\033[0m\n")
        time.sleep(1)

    def deletar_ativo(self):
        if not self.dados:
            print("\033[1mNenhum ativo cadastrado para deletar.\033[0m\n")
            time.sleep(1)
            return

        try:
            id_ativo_remover = int(input("Digite o ID do ativo que deseja deletar:\n").strip())
        except ValueError:
            print("\033[1mID inválido. Por favor, digite um número.\033[0m\n")
            time.sleep(1)
            return

        # Busca o ativo pelo ID
        ativo_para_deletar = next((ativo for ativo in self.dados if ativo["id_ativo"] == id_ativo_remover), None)

        if ativo_para_deletar:
            self.dados.remove(ativo_para_deletar)
            self._salvar_dados()
            print(f"\033[1mAtivo com ID {id_ativo_remover} deletado com sucesso.\033[0m\n")
        else:
            print(f"\033[1mAtivo com ID {id_ativo_remover} não encontrado.\033[0m\n")
        time.sleep(1)

def cad_menu(g_usuario,g_ativo):
    cad = input("\n--- MENU DE CADASTRO ---\n"
        "1- Cadastrar Usuário\n"
        "2- Cadastrar Ativo\n").strip()
    match cad:
        case "1":
            g_usuario.adicionar_usuario()
        case "2":
           g_ativo.adicionar_ativo()

def del_menu(g_usuario,g_ativo):
    delet = input("\n--- DELETAR ---\n"
        "1- Deletar Usuário\n"
        "2- Deletar Ativo\n").strip()
    match delet:
        case "1":
            g_usuario.deletar_usuario()
        case "2":
           g_ativo.deletar_ativo()