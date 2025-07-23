from utils import carregarJson, salvarJson
#Importação de metodos do modulo utils


class Avaliacao:
    #Construtor inicializa a instancia do caminho do json que vai ser usado nos metodos
    def __init__(self, caminho_json):
        self.caminho_json = caminho_json

    #a função carregarJson ja tem tratamentos de erro
    def carregarEstabelecimentos(self):
        return carregarJson(self.caminho_json)


    def salvarEstabelecimentos(self, estabelecimentos):
        try:
            salvarJson(self.caminho_json, estabelecimentos)
        except Exception as e:
            print(f"Ocorreu um erro ao tentar salvar os dados: {e}")


    #Encontra um estabelecimento com base no id
    def encontrarEstabelecimento(self, id_):
        estabelecimentos = self.carregarEstabelecimentos()
        for estab in estabelecimentos:
            if estab.get("id") == id_:
                return estab, estabelecimentos.index(estab)
        return None, None


    '''
    Cria chaves que seram usadas, caso nao existam no estabelecimento, insere a nota dada pelo usuario
    e verifica se é um morador local se sim o valor de local é True, se não, false
    '''
    def registrarAvaliacao(self, id_estabeleci, usuario):
        estab, index = self.encontrarEstabelecimento(id_estabeleci)
        if estab is None:
            print("Não encontramos este estabelecimento :( ")
            return

        try:
            nota = int(input("Insira sua avaliação (1 a 5): "))
            if nota < 1 or nota > 5:
                print("Nota inválida. Use um número entre 1 e 5.")
                return
        except ValueError:
            print("Você inseriu uma entrada inválida!")
            return


        if "avaliacoes" not in estab:
            estab["avaliacoes"] = []
        if "avaliadores" not in estab:
            estab["avaliadores"] = []
        if "avaliacoes_detalhadas" not in estab:
            estab["avaliacoes_detalhadas"] = []


        if usuario['id'] in estab["avaliadores"]:
            print("Você já avaliou este estabelecimento.")
            return
        

        #usando get pra acessar os dados do dicionario evitando erros de KeyError
        local_usuario = usuario.get("localidade", "").lower()
        regiao_estab = estab.get("regiao", "").lower()
        local = local_usuario == regiao_estab


        estab["avaliadores"].append(usuario["id"])
        estab["avaliacoes"].append(nota)
        estab["avaliacoes_detalhadas"].append({
            "id_usuario": usuario["id"],
            "nota": nota,
            "local": local
        })


        estabelecimentos = self.carregarEstabelecimentos()
        estabelecimentos[index] = estab
        self.salvarEstabelecimentos(estabelecimentos)

        print("Avaliação registrada com sucesso!")
        print("Avaliação atual do estabelecimento:", self.exibirEstrelas(id_estabeleci))


    #verifica se avaliacoes é uma lista e calcula a media das notas do estabelecimento.
    def calcularMedia(self, id_):
        estab, _ = self.encontrarEstabelecimento(id_)
        avaliacoes = estab.get("avaliacoes", [])
        if not isinstance(avaliacoes, list) or not avaliacoes:
            return 0.0
        return sum(avaliacoes) / len(avaliacoes)


    #transforma a media em estrelas visuais
    def mediaEstrelas(self, media):
        cheias = int(media)
        meia = 1 if (media - cheias) >= 0.5 else 0
        vazias = 5 - cheias - meia

        return "★" * cheias + "½" * meia + "☆" * vazias
    
    
    #recebe o id de um estabelecimento, e exibe as estrelas dele.
    def exibirEstrelas(self, id_):
        try:
            media = self.calcularMedia(id_)
            if media == 0.0:
                return "Sem avaliações ainda."
            return self.mediaEstrelas(media)
        except Exception as e:
            print(f"Erro ao tentar exibir estrelas: {e}")
            return "Erro ao exibir avaliação."

    


