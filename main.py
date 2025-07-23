from utils import carregarJson, tipoPerfil, sessaoAtiva, userLogado
from crud_perfis import Usuario, Estabelecimento
from filtros_recomendacoes import Recomendacoes
#importação dos modulos e classes

usuarios_json = 'usuarios.json'
estabelecimentos_json = 'estabelecimentos.json'


 

'''
Solicita o tipo de perfil, email e senha. Carrega os dados do JSON e itera sobre eles para encontrar uma correspondência do email e senha. 
Se o login for bem-sucedido, o perfil é salvo como logado e o usuário é direcionado para o seu menu principal. 
Caso aconteça algum erro, uma mensagem é exibida.
'''
def login():
    while True:
        print("=== LOGIN ===")
        tipo = tipoPerfil()
        email = input("Email: ").strip()
        senha = input("Senha: ").strip()

        if tipo == "usuario":
            dados_usuarios = carregarJson(usuarios_json)
            for usuario in dados_usuarios:
                if usuario['email'] == email and usuario['senha'] == senha:
                    print(f"\nLogin bem-sucedido! Bem-vindo, {usuario['nome']} (ID: {usuario['id']})")
                    usuario["tipo"] = "usuario"
                    userLogado(usuario)
                    menuUsuario()
                    return
                
            print("Email ou senha incorretos, tente novamente.")

        elif tipo == "estabelecimento":
            dados_estabelecimentos = carregarJson(estabelecimentos_json)
            for estabelecimento in dados_estabelecimentos:
                if estabelecimento['email'] == email and estabelecimento['senha'] == senha:
                    print(f"\nLogin bem-sucedido! Bem-vindo, {estabelecimento['nome']} (ID: {estabelecimento['id']})")
                    estabelecimento["tipo"] = "estabelecimento"
                    userLogado(estabelecimento)
                    menuEstabelecimentoP()
                    return estabelecimento
                
            print("Email ou senha incorretos, tente novamente.")



#Menu principal do usuario, carrega o perfil do usuario logado e inicializa as classes Usuario e Recomendacoes.
#Printa as opções disponiveis e encaminha para a função correspondente
def menuUsuario():
    """
    Exibe o menu principal exclusivo para o perfil de usuário.
    """
    while True:
        perfil = sessaoAtiva()
        cadastro = Usuario(usuarios_json)
        recomendador = Recomendacoes(perfil)

        print("\n=== MENU PRINCIPAL ===")
        print("\n1. 📜 Recomendações")
        print("\n2. <# Recomendações Locais")
        print("\n3. 🎲 Recomendações Aleatórias")
        print("\n4. <3 Lista Quero Conhecer ")
        print("\n5. 💾 Atualizar dados do perfil")
        print("\n6. ❗ Excluir Perfil")
        print("\n7. 📄 Ver meus dados")
        print("\n8. 🚪 Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            recomendador.recomendarEstabelecimentos()
        elif escolha == "2":
            recomendador.recomendacoesLocais()
        elif escolha == "3":
            recomendador.recomendacaoAleatoria()
        elif escolha == "4":
            cadastro.verQueroconhecer(perfil['id'])  
        elif escolha == "5":
            cadastro.atualizar(perfil['id'])                       
        elif escolha == "6":
            cadastro.excluirPerfil(perfil['id'])         
        elif escolha == "7":
            cadastro.verDados() 
        elif escolha == "8":
            print("Saindo...")
            exit()
        else:
            print("Opção inválida!")


#Menu principal dos estabelecimentos, similar aos dos usuarios, porem com menos opções.
def menuEstabelecimentoP():
    """
    Exibe o menu principal exclusivo para o perfil de estabelecimento.
    """
    while True:
        perfil = sessaoAtiva()
        cadastro = Estabelecimento(estabelecimentos_json)
        print("\n=== MENU DO ESTABELECIMENTO ===")
        print("\n1. 💾 Atualizar dados do perfil")
        print("\n2. ❗ Excluir Perfil")
        print("\n3. 📄 Ver meus dados")
        print("\n4. 🚪 Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            cadastro.atualizar(perfil['id'])
        elif escolha == "2":
            cadastro.excluirPerfil(perfil['id'])
        elif escolha == "3":
            cadastro.verDados()
        elif escolha == "4":
            print("Saindo...")
            exit()
        else:
            print("Opção inválida!")



#Menu inicial do projeto, apresenta as opções e com base na escolha, ela inicializa a classe de perfil correta(usuario ou estabelecimento)
def menuInicial():
    """
    Exibe o menu inicial para cadastro ou login.
    """
    while True:
        print("=== MENU INICIAL ===")
        print("\n1. 👤 Cadastrar Usuário")
        print("\n2. 🏪 Cadastrar Estabelecimento")
        print("\n3. 🔑 Login")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            cadastro = Usuario(usuarios_json)
            perfil = cadastro.cadastrar()
            perfil["tipo"] = "usuario"
            userLogado(perfil)
            menuUsuario()
            break
        elif escolha == "2":
            cadastro = Estabelecimento(estabelecimentos_json)
            perfil = cadastro.cadastrar()
            perfil["tipo"] = "estabelecimento"
            userLogado(perfil)
            menuEstabelecimentoP()
            break
        elif escolha == "3":
            login()
            break
        else:
            print("Opção inválida.")


#Inicia a aplicação
menuInicial()
