from utils import carregarJson, salvarJson, sessaoAtiva
from validacoes import emailValido, senhaValida, telefoneValido
from avaliacoes import Avaliacao

usuarios_json = 'usuarios.json'
estabelecimentos_json = 'estabelecimentos.json'
#Importações dos modulos e variaveis com os caminhos do json


'''
Classe que tem todos os metodos que ambos os perfis(Usario e Estabelecimento) usam.
'''
class Perfil:
    def __init__(self, caminho_json):
        self.perfil = None
        self.caminho_json = caminho_json
        self.dados = self.carregar_json()

    def carregar_json(self):
        return carregarJson(self.caminho_json)


    def salvar_json(self, todos):
        salvarJson(self.caminho_json, todos)


    def inputNome(self):
        return input("Nome: ")


    def inputEmail(self):
        while True:
            email = input("Email (@gmail.com ou @hotmail.com, sem espaços): ")
            if not emailValido(email):
                print("Email inválido.")
            elif any(p['email'] == email for p in self.dados):
                print("Este email já está cadastrado.")
            else:
                return email


    def inputSenha(self):
        while True:
            senha = input("Senha (8+ caracteres, letras, números, sem espaços): ")
            if not senhaValida(senha):
                print("Senha inválida.")
            else:
                return senha


    def inputInteresses(self):
        self.exibirCategorias()
        print("Escolha três interesses")
        i1 = input("Digite seu primeiro interesse: ")
        i2 = input("Digite seu segundo interesse: ")
        i3 = input("Digite seu terceiro interesse: ")
        interesses = [i1.strip(), i2.strip(), i3.strip()] 
        return interesses


    def inputRegiao(self):
        while True:
            regiao = input("Região de interesse (Ex: Recife - Pernambuco): ")
            if ' - ' not in regiao or len(regiao.split(' - ')) != 2:
                print("Formato inválido. Ex: Recife - Pernambuco")
            else:
                return regiao


    def exibirCategorias(self):
        print("""
                === ESTILOS & AMBIENTES ===
                * Alternativo          * Cultural           * Regional
                * Ar Livre             * Tranquilo          * Vista
                * Íntimo               * Temático           * Popular
                * LGBT                 * Pet-Friendly       * Vegano

                === MÚSICA & ENTRETENIMENTO ===
                * Ao Vivo              * Samba              * Forró
                * Rock                 * MPB                * Jazz
                * Sertanejo            * Reggae             * Eletrônico
                * Pop                  * DJ                 * Vinil
                *Techno
              
                === LAZER & CONVIVÊNCIA ===
                * Boteco               * Café               * Happy Hour
                * Dança                * Comédia            * Sinuca
                * Jogos                * Karaokê            * Grupos
                * Drinks               * Petiscos           * Vinhos
                * Sucos                * Saudável           * Geek

                === EXPERIÊNCIAS LOCAIS & COMUNITÁRIAS ===
                * Comida de rua        * Batalha de Rap     * Roda de Samba
                * Blocos de Carnaval   * Tour em favelas    * Bebidas Artesanais
                * Empreendedorismo Negro
        """)


    def gerarId(self):
        if not self.dados:
            return 1
        return max(p['id'] for p in self.dados) + 1
    

    #Descobre de quem é o id fazendo um for 
    def encontrarId(self, id_):
        todos = self.carregar_json()
        for i, p in enumerate(todos):
            if p['id'] == id_:
                return i, p
        return -1, None


    #Exibe os dados do perfil logado carregado com a função sessaoAtiva().
    def verDados(self):
        perfil = sessaoAtiva()
        print("✦·┈๑⋅⋯ ⋯⋅๑┈·✦ Dados Cadastrados ✦·┈๑⋅⋯ ⋯⋅๑┈·✦")
        for chave, valor in perfil.items():
            if chave == "conhecer":
                continue

            if isinstance(valor, list):
                conversao_string = ', '.join(map(str, valor))
                print(f"{chave.capitalize()}: {conversao_string}")
            else:
                print(f"{chave.capitalize()}: {valor}")
    

    def excluirPerfil(self, id_):
        index, _ = self.encontrarId(id_)
        if index == -1:
            print("Perfil não encontrado.")
            return
        todos = self.carregar_json()
        confirm = input("Tem certeza que deseja excluir esse perfil? (s/n): ")
        if confirm.lower() == 's':
            del todos[index]
            self.salvar_json(todos)
            print("Perfil excluído com sucesso.")
        else:
            print("Operação cancelada.")





#Classe filha de Perfil, contendo a maiora dos metodos que os usuarios precisam.
class Usuario(Perfil):
    #Metodo de cadastro do usuario
    def cadastrar(self):
        print("=== Cadastro de Usuário ===")
        nome = self.inputNome()
        email = self.inputEmail()
        senha = self.inputSenha()
        interesses = self.inputInteresses()
        regiao = self.inputRegiao()
        localidade = self.inputLocalidade()
        novo_id = self.gerarId()

        self.perfil = {
            'id': novo_id,
            'nome': nome,
            'email': email,
            'senha': senha,
            'interesses': interesses,
            'regiao': regiao,
            'localidade': localidade
        }
        self.salvar()
        print(f"Usuário cadastrado! Seu ID é: {novo_id}")
        return self.perfil



    def inputLocalidade(self):
        while True:
            localidade = input("Localidade, onde você mora (formato: Cidade - Estado): ")
            if ' - ' not in localidade or len(localidade.split(' - ')) != 2:
                print("Formato inválido. Ex: Recife - Pernambuco")
            else:
                return localidade


    def salvar(self):
        dados = carregarJson(self.caminho_json)
        dados.append(self.perfil)
        salvarJson(self.caminho_json, dados)


    #Atualização do perfil com base no id, após as entradas de dados, salva no JSON e no user_logado que tambem é um JSON.
    def atualizar(self, id_):
        index, usuario = self.encontrarId(id_)
        if usuario is None:
            print("Usuário não foi encontrado.")
            return

        print("=== Atualização de Perfil ===")
        nome = input(f"Nome ({usuario['nome']}), pressione Enter para manter o mesmo: ") or usuario['nome']

        email_input = input(f"Email ({usuario['email']}), pressione Enter para manter o mesmo: ") or usuario['email']
        email = email_input or usuario['email']
        if email != usuario['email']:
            if not emailValido(email):
                print("Esse email é inválido.")
                return
            if any(user['email'] == email for user in self.dados):
                print("Esse email já está em uso.")
                return
        
        senha = input(f"Senha ({usuario['senha']}), pressione Enter para manter a mesma: ") or usuario['senha']

        print("Interesses atuais:", ', '.join(usuario['interesses']))
        i1 = input("1º Interesse (ou Enter para manter o mesmo): ").strip()
        i2 = input("2º Interesse (ou Enter para manter o mesmo): ").strip()
        i3 = input("3º Interesse (ou Enter para manter o mesmo): ").strip()
        interesses = [
            i if i else usuario['interesses'][j]
            for j, i in enumerate([i1, i2, i3])]

        regiao = input(f"Região ({usuario['regiao']}): ") or usuario['regiao']
        localidade = input(f"Localidade ({usuario['localidade']}): ") or usuario['localidade']

        todos = self.carregar_json()
        todos[index].update({
            'nome': nome,
            'email': email,
            'senha': senha,
            'interesses': interesses,
            'regiao': regiao,
            'localidade': localidade
        })

        self.salvar_json(todos)
        salvarJson("user_logado.json", todos[index])
        print("Perfil atualizado com sucesso.")



    #Adiciona o ID do estabelecimento a lista 'conhecer' do usuario, se nao tiver a lista, ela é criada e verifica se esse usuario ja avaliou
    def adicionarQueroconhecer(self, id_usuario, id_estabelecimento):
        index, usuario = self.encontrarId(id_usuario)

        if 'conhecer' not in usuario:
            usuario['conhecer'] = []

        if id_estabelecimento in usuario['conhecer']:
            print("Este estabelecimento já está na sua lista de Quero Conhecer.")
            return

        usuario['conhecer'].append(id_estabelecimento)

        todos = self.carregar_json()
        todos[index] = usuario
        self.salvar_json(todos)
        salvarJson("user_logado.json", usuario)
        print("⭐ Estabelecimento adicionado a sua lista de Quero Conhecer com sucesso! ⭐")



    '''
    Exibe cada estabelecimento e suas respectivas informações, que estam na lista 'conhecer' do usuario, e oferece um menu interativo 
    para que o usuário possa escolher um estabelecimento para avaliar (usando a classe Avaliacao) ou removê-lo da lista "Quero Conhecer".
    '''
    def verQueroconhecer(self, id_):
        usuario_index, usuario = self.encontrarId(id_)
        if usuario is None:
            print("Usuário não encontrado.")
            return

        conhecer = usuario.get("conhecer", [])
        if not conhecer:
            print("Você ainda não tem estabelecimentos na lista de Quero Conhecer.")
            return

        estabelecimentos = carregarJson(estabelecimentos_json)
        conhecer_lista = []

        print("=== Lista de Quero Conhecer ===\n")
        for i, estabelecimento_id in enumerate(conhecer, 1):
            estabeleci = next((e for e in estabelecimentos if e['id'] == estabelecimento_id), None)
            if estabeleci:
                conhecer_lista.append(estabeleci)
                print(f"{i}. 📍 {estabeleci['nome']}")
                print(f"   📌 Interesses: {', '.join(estabeleci['interesses'])}")
                print(f"   📍 Endereço: {estabeleci['endereco']}")
                print(f"   📞 Telefone: {estabeleci['telefone']}")
                print(f"   📝 Bio: {estabeleci['bio']}\n")


        escolha = input("Digite o indice de um estabelecimento para abrir o menu ou digite 'voltar' para sair. ").strip().lower()

        if escolha == 'voltar':
            return


        avaliador = Avaliacao(estabelecimentos_json)
        try:
            indice = int(escolha)
            if not (1 <= indice <= len(conhecer_lista)):
                print("Você digitou um índice invalido!")
                return
        except ValueError:
                print('Entrada invalida, por favor, digite um numero que corresponda a um indice.')
                return
        

        estabelec_selecionado = conhecer_lista[indice - 1]

        while True:
            try:
                nome = estabelec_selecionado.get('nome', 'Estabelecimento')
                print(f"\n=== Menu {nome} ===")
                print("1. Avaliar estabelecimento")
                print("2. Remover da lista de Quero Conhecer")
                print("3. Voltar")
                opcao = input('Escolha uma opção: ').strip()

                if opcao == '1':
                    usuario_logado = sessaoAtiva()
                    if not usuario_logado:
                        print("Ocorreu um erro, nenhum usuario esta logado.")
                        return
                    avaliador.registrarAvaliacao(estabelec_selecionado['id'], usuario_logado)
                elif opcao == '2':
                    print(f"\n{estabelec_selecionado['nome']} foi removido dos seus favoritos.")
                    usuario['conhecer'].remove(estabelec_selecionado['id'])
                    todos_usuarios = self.carregar_json()
                    todos_usuarios[usuario_index] = usuario
                    self.salvar_json(todos_usuarios)
                    salvarJson("user_logado.json", usuario)
                    break
                elif opcao == '3':
                    break
                else:
                    print('Opção inválida, tente novamente.')
            except KeyboardInterrupt:
                print('\n Você interrompeu o programa.')





#Classe filha de Perfil para os estabelecimentos.
class Estabelecimento(Perfil):
    #Solicita o telefone do estabelecimento, algo que o usuario não precisa.
    def inputTelefone(self):
        while True:
            telefone = input("Telefone (DDD + número): ")
            if not telefoneValido(telefone):
                print("Telefone inválido. Deve conter 11 dígitos.")
            else:
                return telefone

    #Metodo de cadastro do estabelecimento
    def cadastrar(self):
        print("=== Cadastro de Estabelecimento ===")
        nome = self.inputNome()
        email = self.inputEmail()
        senha = self.inputSenha()
        endereco = input("Endereço: ")
        interesses = self.inputInteresses()
        bio = input("Bio (Descrição sobre seu Estabelecimento): ")
        telefone = self.inputTelefone()
        regiao = self.inputRegiao()
        novo_id = self.gerarId()

        self.perfil = {
            'id': novo_id,
            'nome': nome,
            'email': email,
            'senha': senha,
            'endereco': endereco,
            'interesses': interesses,
            'bio': bio,
            'telefone': telefone,
            'regiao': regiao
        }
        self.salvar()
        print(f"Estabelecimento cadastrado! Seu ID é: {novo_id}")
        return self.perfil


    def salvar(self):
        dados = carregarJson(self.caminho_json)
        dados.append(self.perfil)
        salvarJson(self.caminho_json, dados)


    #Atualização do perfil com base no id, após as entradas de dados, salva no JSON e no user_logado que tambem é um JSON.
    def atualizar(self, id_):
        index, estabelecimento = self.encontrarId(id_)
        if estabelecimento is None:
            print("Estabelecimento não encontrado.")
            return

        print("=== Atualização de Estabelecimento ===")
        nome = input(f"Nome ({estabelecimento['nome']}): ") or estabelecimento['nome']
        email = input(f"Email ({estabelecimento['email']}): ") or estabelecimento['email']
        senha = input("Senha (ou Enter para manter): ") or estabelecimento['senha']
        endereco = input(f"Endereço ({estabelecimento['endereco']}): ") or estabelecimento['endereco']
        bio = input(f"Bio ({estabelecimento['bio']}): ") or estabelecimento['bio']
        telefone = input(f"Telefone ({estabelecimento['telefone']}): ") or estabelecimento['telefone']
        regiao = input(f"Região ({estabelecimento['regiao']}): ") or estabelecimento['regiao']

        interesses = input("Interesses separados por vírgula (ou Enter para manter): ")
        if interesses:
            interesses = [i.strip() for i in interesses.split(',')]
        else:
            interesses = estabelecimento['interesses']

        todos = self.carregar_json()
        todos[index].update({
            'nome': nome,
            'email': email,
            'senha': senha,
            'endereco': endereco,
            'bio': bio,
            'telefone': telefone,
            'regiao': regiao,
            'interesses': interesses
        })

        self.salvar_json(todos)
        salvarJson("user_logado.json", todos[index])
        print("Estabelecimento atualizado com sucesso.")

