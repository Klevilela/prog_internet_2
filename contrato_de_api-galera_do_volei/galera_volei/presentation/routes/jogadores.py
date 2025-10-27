from fastapi import APIRouter
from presentation.controllers.jogadores import JogadoresControllers
from application.jogadores_services import JogadoresService


jogador_router = APIRouter()

# cria a instancia de jogadorcontroller passando jogadorservice como argumento no
#construtor
jogador_service = JogadoresService()
jogador_controller = JogadoresControllers(jogador_service)

jogador_router.post('/jogadores')(jogador_controller.incluir_jogador)
jogador_router.get('/jogadores')(jogador_controller.listar_jogadores)
jogador_router.get('/jogadores/{id}')(jogador_controller.listar_jogador_id)
jogador_router.delete('/jogadores/{id}')(jogador_controller.excluir_jogador)
jogador_router.put('/jogadores/{id}')(jogador_controller.alterar_jogador)
jogador_router.patch('/jogadores/{id}')(jogador_controller.alterar_atributo)



""" jogador_router.post('/jogadores')(jogador_controller.incluir_jogador)
jogador_router.post('/jogadores')(jogador_controller.incluir_jogador)
jogador_router.post('/jogadores')(jogador_controller.incluir_jogador)
 """


""" @app.post('/jogadores')
def incluir_jogador(nome: str, sexo: str, idade: int, categoria: str):
    global next_id_jogador
    jogador = {
        'id': next_id_jogador,
        'nome': nome,
        'sexo': sexo,
        'idade': idade,
        'categoria': categoria
    }
    jogadores.append(jogador)
    next_id_jogador += 1
    return jogador


@app.get('/jogadores')
def listar_jogadores():
    return jogadores


@app.get('/jogadores/{id}')
def listar_jogadores_id(id: int):
    for j in jogadores:
        if j['id'] == id:
            return j
    return {'erro': 'Jogador não encontrado'}


@app.delete('/jogadores/{id}')
def excluir_jogador(id: int):
    for j in jogadores:
        if j['id'] == id:
            jogadores.remove(j)
            return {'mensagem': f'Jogador {id} removido com sucesso!'}
    return {'erro': 'Jogador não existe'}


@app.put('/jogadores/{id}')
def atualizar_jogador(id: int, nome: str, sexo: str, idade: int, categoria: str):
    for j in jogadores:
        if j['id'] == id:
            j.update({
                'nome': nome,
                'sexo': sexo,
                'idade': idade,
                'categoria': categoria
            })
            return j
    return {'erro': 'Jogador não encontrado'}


@app.patch('/jogadores/{id}')
def alterar_jogador(id: int, nome: str = None, sexo: str = None, idade: int = None, categoria: str = None):
    for j in jogadores:
        if j['id'] == id:
            if nome:
                j['nome'] = nome
            if sexo:
                j['sexo'] = sexo
            if idade:
                j['idade'] = idade
            if categoria:
                j['categoria'] = categoria
            return j
    return {'erro': 'Jogador não encontrado'} """