from colorama import Fore, Back, init
import os
import requests
import json

# Inicializa o colorama para funcionar corretamente
init(autoreset=True)

class sos:
    def __init__(self):
        self.name = "user"
        self.cmds = {
            "text": "",
            "custom_commands": {}  # Para armazenar comandos personalizados
        }
        self.memory = 20  # em GB
        self.variables = {}  # Dicionário para armazenar variáveis
        self.advanced_mode = False  # Modo avançado desativado inicialmente
        self.load_memory()  # Carrega a memória do sistema ao iniciar

    def boot(self):
        print(Back.BLUE + Fore.YELLOW + "SmakOs!")
        print(self.ini())
        while True:
            hh = os.getcwd()  # Obtém o diretório de trabalho atual
            user_input = input(self.cm(hh))
            spui = user_input.split()  # Divide o input em uma lista de palavras
            
            try:
                if user_input.lower() == "exit":
                    self.save_memory()  # Salva a memória antes de sair
                    print("Saindo...")
                    break
                elif user_input.lower() == "help":  # Comando de ajuda
                    self.show_help()
                elif spui[0] == "user" and len(spui) > 1:  # Sistema de usuários
                    self.name = spui[1]
                    print(f"Usuário alterado para '{self.name}'.")
                elif spui[0] == "text" and len(spui) > 1:
                    print(" ".join(spui[1:]))
                elif spui[0] == "exe" and len(spui) > 1:
                    os.system(f"python {spui[1]}")
                elif spui[0] == "cd" and len(spui) > 1:  # Comando para mudar diretório
                    try:
                        os.chdir(spui[1])
                    except FileNotFoundError:
                        print(f"Diretório '{spui[1]}' não encontrado.")
                    except NotADirectoryError:
                        print(f"'{spui[1]}' não é um diretório.")
                elif spui[0] == "ls":  # Comando para listar arquivos
                    files = os.listdir(hh)
                    print("\n".join(files))
                elif spui[0] == "smsn" and len(spui) > 2:  # Comando para adicionar comandos personalizados
                    command_name = spui[1]
                    command_action = " ".join(spui[2:])
                    self.cmds['custom_commands'][command_name] = command_action
                    print(f"Comando '{command_name}' adicionado.")
                elif spui[0] == "rm" and len(spui) > 1:  # Comando para remover comandos personalizados
                    command_name = spui[1]
                    if command_name in self.cmds['custom_commands']:
                        del self.cmds['custom_commands'][command_name]
                        print(f"Comando '{command_name}' removido.")
                    else:
                        print(f"Comando '{command_name}' não encontrado.")
                elif spui[0] == "inc":  # Comando para instalar comandos personalizados
                    if len(spui) < 3:
                        print("Uso: inc -o <pacote>")
                    elif spui[1] == "-o":
                        self.install_command(spui[2])  # Chama a função de instalação
                elif spui[0] == "am":  # Ativar modo avançado
                    if not self.advanced_mode:
                        self.advanced_mode = True
                        print("Modo avançado ativado.")
                    else:
                        print("Modo avançado já está ativado.")
                elif spui[0] == "download" and len(spui) > 1:  # Novo comando para baixar pacotes
                    self.download_package(spui[1])
                elif spui[0] == "shell" and len(spui) > 1:  # Comando shell para executar comandos
                    shell_command = " ".join(spui[1:])
                    os.system(shell_command)
                elif spui[0] in self.cmds['custom_commands']:  # Executa comandos personalizados
                    os.system(self.cmds['custom_commands'][spui[0]])
                elif spui[0] == "mem":  # Comando para mostrar memória
                    print(f"Memória disponível: {self.memory}GB")
                elif spui[0] == "set" and len(spui) == 3:  # Comando para definir uma variável
                    var_name = spui[1]
                    var_value = spui[2]
                    self.variables[var_name] = var_value
                    print(f"Variável '{var_name}' definida como '{var_value}'.")
                elif spui[0] == "get" and len(spui) == 2:  # Comando para obter o valor de uma variável
                    var_name = spui[1]
                    if var_name in self.variables:
                        print(f"{var_name} = {self.variables[var_name]}")
                    else:
                        print(f"Variável '{var_name}' não encontrada.")
                elif spui[0] == "if" and len(spui) > 4 and spui[2] == "then":  # Comando if
                    condition = spui[1]
                    action = " ".join(spui[3:])
                    if condition in self.variables:  # Verifica se a variável existe
                        print(f"A condição '{condition}' é verdadeira, executando ação: {action}")
                        os.system(action)  # Executa a ação
                    else:
                        print(f"A condição '{condition}' é falsa.")
                elif spui[0] == "elif" and len(spui) > 4 and spui[2] == "then":  # Comando elif
                    condition = spui[1]
                    action = " ".join(spui[3:])
                    if condition in self.variables:  # Verifica se a variável existe
                        print(f"A condição '{condition}' é verdadeira, executando ação: {action}")
                        os.system(action)  # Executa a ação
                elif spui[0] == "else":  # Comando else
                    action = " ".join(spui[1:])
                    print(f"Executando ação do else: {action}")
                    os.system(action)  # Executa a ação
                elif spui[0] == "memory":  # Novo comando para gerenciar memória
                    self.memory_management(spui)
            except Exception as e:
                print(f"Erro: {e}")

    def show_help(self):
        help_text = """
        Comandos disponíveis:
        - text <mensagem>: Exibe a mensagem.
        - exe <arquivo.py>: Executa um arquivo Python.
        - cd <diretório>: Muda o diretório atual.
        - ls: Lista os arquivos no diretório atual.
        - smsn <nome> <comando>: Adiciona um comando personalizado.
        - rm <nome>: Remove um comando personalizado.
        - user <usuario>: Altera o usuário atual.
        - inc -o <pacote>: Instala um pacote online.
        - download <url>: Baixa um pacote a partir de uma URL.
        - shell <comando>: Executa um comando no shell.
        - am: Ativa o modo avançado.
        - mem: Mostra a memória disponível.
        - set <variável> <valor>: Define uma variável.
        - get <variável>: Obtém o valor de uma variável.
        - if <condição> then <comando>: Executa um comando se a condição for verdadeira.
        - elif <condição> then <comando>: Executa um comando se a condição for verdadeira após um if.
        - else <comando>: Executa um comando se a condição do if não for verdadeira.
        - memory: Gerencia memória e exibe informações.
        - help: Exibe esta ajuda.
        - exit: Sai do sistema.
        """
        print(help_text)

    def download_package(self, url):
        # Nome do arquivo a ser salvo
        filename = url.split('/')[-1]
        file_path = os.path.join('packages', filename)
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lança um erro se o download falhar
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Pacote '{filename}' baixado com sucesso!")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar pacote: {e}")

    def install_command(self, package):
        print(f"Instalando pacote '{package}'...")  # Implementação da instalação do pacote

    def load_memory(self):
        # Implementação para carregar a memória do sistema
        if os.path.exists('memory.json'):
            with open('memory.json', 'r') as f:
                data = json.load(f)
                self.memory = data.get("memory", self.memory)
                self.variables = data.get("variables", self.variables)
                print("Memória carregada.")

    def save_memory(self):
        # Implementação para salvar a memória do sistema
        with open('memory.json', 'w') as f:
            json.dump({
                "memory": self.memory,
                "variables": self.variables
            }, f)
        print("Memória salva.")

    def memory_management(self, args):
        # Função para gerenciar a memória
        if args[1] == "add" and len(args) == 3:
            amount = int(args[2])
            self.memory += amount
            print(f"Adicionado {amount}GB. Memória total: {self.memory}GB.")
        elif args[1] == "remove" and len(args) == 3:
            amount = int(args[2])
            if amount > self.memory:
                print("Memória insuficiente para remoção.")
            else:
                self.memory -= amount
                print(f"Removido {amount}GB. Memória total: {self.memory}GB.")
        else:
            print("Uso: memory add <quantidade> ou memory remove <quantidade>.")

    def ini(self):
        return "Inicializando o sistema..."

    def cm(self, hh):
        return f"{self.name}@SmakOs:{hh} $ "  # Prompt do shell

