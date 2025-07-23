import json
#Importação do modulo json

#Carrega(ler) os dados de um json, se caso o json não for valido, não encontrado ou alguma outra exceção de erro, retorna uma lista vazia para o codigo não travar.
def carregarJson(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao tentar carregar '{caminho}': {e}")
        return []


#Salva os dados num json, abrindo o arquivo em modo escrita, os dados convertidos para json, ensure false para salvar as acentuações do português.
def salvarJson(caminho, dados):
    try:
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Erro ao tentar salvar {caminho}: {e}")


#Verificar qual é o tipo do perfil, de forma pratica.
def tipoPerfil():
    print("Qual o tipo do seu perfil?")
    print("1. Usuário")
    print("2. Estabelecimento")
    escolha = input("Digite 1 ou 2: ")
    if escolha == "1":
        return "usuario"
    elif escolha == "2":
        return "estabelecimento"
    else:
        print("\nTipo inválido, tente novamente.")
        return tipoPerfil()
    

#Grava os dados de quem esta logado
def userLogado(usuario):
    salvarJson('user_logado.json', usuario)


#Lê os dados do usuario logado.
def sessaoAtiva():
    try:
        dados = carregarJson('user_logado.json')
        return dados if dados else None
    except Exception as e:
        print(f"Erro ao tentar carregar a sessão: {e}")
        return None

