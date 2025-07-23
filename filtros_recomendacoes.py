import random
from utils import carregarJson, sessaoAtiva
from crud_perfis import Usuario
from avaliacoes import Avaliacao

usuarios_json = 'usuarios.json'
estabelecimentos_json = 'estabelecimentos.json'
dados_usuarios = carregarJson(usuarios_json)
dados_estabelecimentos = carregarJson(estabelecimentos_json)
#Importação de modulos e carregamento dos dados do json, para serem usados nas classes.


class Recomendacoes:
    #Construtor da classe associa o perfil logado, os estabelecimentos em variveis e cria uma instancia da classe Avaliacao para serem utilizados posteriormente
    def __init__(self, perfil_logado):
        self.perfil = perfil_logado
        self.estabelecimentos = dados_estabelecimentos
        self.avaliador = Avaliacao(estabelecimentos_json)


    '''
    Método que filtra os estabelecimentos por regiao e interesses em comum com o usuario logado, 
    transforma os interesses e regiao em conjuntos set para fazer uma comparação assim encontrando os matchs, se caso encontre um match
    retorna uma lista de dicionarios
    '''

    def filtrarEstabelecimentos(self):
        if not self.perfil:
            return []

        interesses_usuario = [i.strip().lower() for i in self.perfil['interesses']]
        regiao_usuario = self.perfil['regiao'].lower()
        recomendados = []

        for estabelecimento in self.estabelecimentos:
            regiao_estabelecimento = estabelecimento['regiao'].lower()
            interesses_estabelecimento = [i.lower() for i in estabelecimento['interesses']]

            if regiao_estabelecimento == regiao_usuario:
                interesses_em_comum = set(interesses_usuario) & set(interesses_estabelecimento)
                if interesses_em_comum:
                    recomendados.append({
                        'estabelecimento': estabelecimento,
                        'interesses_em_comum': list(interesses_em_comum),
                        'id': estabelecimento['id']
                    })
        return recomendados


    '''
    Utiliza o metodo filtrarEstabelecimentos para pegar os matchs entre o usuario e os estabelecimentos e exibe cada estabelecimento com seus respectivos 
    dados e enumera os estabelecimentos para acessar suas paginas posteriormente, por meio de seus indices.
    '''
    def recomendarEstabelecimentos(self):
        recomendados = self.filtrarEstabelecimentos()

        if not recomendados:
            print('\n⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘')
            print('\n(╥﹏╥) (╥﹏╥) (╥﹏╥) (╥﹏╥)')
            print("🥺 Não encontramos estabelecimentos compatíveis com seus interesses nessa região :( \nTente alterar seus interesses.")
            print('\n⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘')
            return

        print('\n✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦')
        print("\nEstabelecimentos recomendados com base em seus interesses: ")
        for i, rec in enumerate(recomendados, start=1):
            estrelas = self.avaliador.exibirEstrelas(rec['id'])
            print(f"\n🔖 {i}. {rec['estabelecimento']['nome']}")
            print(f"⭐ Avaliação: {estrelas}")
            print(f"💟 Interesses em comum: {', '.join(rec['interesses_em_comum']).capitalize()}")
            print(f"🗺️  Região: {rec['estabelecimento']['regiao']}")

        try:
            indice_recomendado = int(input('\nPressione o indice de um estabelecimento para acessar a pagina dele: '))
            if 1 <= indice_recomendado <= len(recomendados):
                selecionado = recomendados[indice_recomendado - 1]['estabelecimento']
                print(f"\n{selecionado['nome']}")
                print(f"{selecionado['bio']}")
                print(f"{', '.join(selecionado['interesses']).title()}")
                print(f"{selecionado['telefone']}")
                print(f"{selecionado['endereco']}")
                
                opcao = input("\n Desejar adicionar este estabelecimento a Lista de Quero Conhecer (Sim / Sair): ").lower()
                if opcao == "sim":
                    perfil = sessaoAtiva()
                    Usuario(usuarios_json).adicionarQueroconhecer(perfil['id'], selecionado['id'])
        except ValueError:
            print("Valor da entrada foi invalido.")

        print('\n✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦')



    #Utiliza o random para sortear 3 estabelecimentos que estão no json e printa cada um com suas respectivas informações
    def recomendacaoAleatoria(self):
        print('\n──── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ────')
        print('\nA vida é feita de novas experiências. Permita-se sair do óbvio e descubra lugares incríveis')
            
        if len(self.estabelecimentos) < 3:
            print("🥺 Não há estabelecimentos suficientes para fazer uma recomendação aleatória (mínimo de 3).")
            print('\n──── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ────')
            return

        estabelecimentos_sorteados = random.sample(self.estabelecimentos, k=3)
        for i in estabelecimentos_sorteados:
            estrelas = self.avaliador.exibirEstrelas(i['id'])
            print(f"\n 🔖 Nome: {i['nome']}")
            print(f"⭐ Avaliação: {estrelas}")
            print(f"💟 Interesses: {', '.join(i['interesses'])}")
            print(f"🗺️  Região: {i['regiao']}")
            print(f"📍 Endereço: {i['endereco']}")
            print(f"📞 Telefone: {i['telefone']}")
            print(f"📖 Bio: {i['bio']}")
            print('\n﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌')
        print('\n──── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ──────── ୨୧ ────')



    '''
    Utiliza o metodo filtrar para ter acesso aos matchs, se o estabelecimento tiver avaliação, procura um match entre o id de quem avaliou e a nota dele
    para ter acesso a esse usuario, assim verifica se ele mora na mesma regiao do estabelecimento, se caso for igual, adiciona a nota_locais
    calcula uma média apenas com as notas dadas por usuários da mesma localidade e os estabelecimentos são ordenados por essa média local.
    '''
    def recomendacoesLocais(self):
        recomendados_base = self.filtrarEstabelecimentos()
        
        if not recomendados_base:
            print("\n✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦"*3)
            print("\n🥺 Nenhum estabelecimento compatível foi encontrado para realizar as recomendações de moradores locais.")
            print("\n✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦"*3)
            return

        usuarios = carregarJson(usuarios_json)
        recomendados_finais = []

        for rec in recomendados_base:
            estab = rec['estabelecimento']
            notas_locais = []
            
            if 'avaliadores' in estab and 'avaliacoes' in estab:
                for uid, nota in zip(estab["avaliadores"], estab["avaliacoes"]):
                    user = next((u for u in usuarios if u["id"] == uid), None)
                    if user and user.get("localidade", "").strip().lower() == estab['regiao'].strip().lower():
                        notas_locais.append(nota)

            if notas_locais:
                media = sum(notas_locais) / len(notas_locais)
                recomendados_finais.append({
                    'estab': estab,
                    'interesses_em_comum': rec['interesses_em_comum'],
                    'media_local': media,
                    'estrelas': self.avaliador.mediaEstrelas(media),
                    'id': estab['id']
                })

        if not recomendados_finais:
            print("\n✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦" *3)
            print("\n🥺 Nenhum estabelecimento com avaliações de moradores locais encontrado.")
            print("\n✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦"*3)
            return

        recomendados_finais.sort(key=lambda x: x["media_local"], reverse=True)

        print("\n✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦")
        print("\n✨ Recomendação com base nas avaliações de moradores locais:")
        for i, rec in enumerate(recomendados_finais, 1):
            print(f"\n🔖 {i}. {rec['estab']['nome']}")
            print(f"⭐ Avaliação (locais): {rec['estrelas']} ({rec['media_local']:.1f})")
            print(f"💟 Interesses em comum: {', '.join(rec['interesses_em_comum']).capitalize()}")
            print(f"🗺️  Região: {rec['estab']['regiao']}")

        try:
            indice = int(input("\nEscolha um indice para abrir o perfil de um estabelecimento ou qualquer outra tecla para voltar: "))
            if 1 <= indice <= len(recomendados_finais):
                sel = recomendados_finais[indice - 1]["estab"]
                print(f"\n✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦")
                print(f"\n{sel['nome']}\n{sel['bio']}")
                print(f"\nInteresses: {', '.join(sel['interesses']).title()}")
                print(f"📞 {sel['telefone']}")
                print(f"📍 {sel['endereco']}")
                print("\n✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦ ✦·┈๑⋅⋯ ⋯⋅๑┈·✦")
                
                opcao = input("\nDeseja adicionar esse estabelecimento à Lista de Quero Conhecer? (Sim / Voltar): ").lower()
                if opcao == "sim":
                    perfil = sessaoAtiva()
                    Usuario(usuarios_json).adicionarQueroconhecer(perfil['id'], sel['id'])
        except ValueError:
            return
        

