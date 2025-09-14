from fastapi import FastAPI

app = FastAPI()

list_partidas = []
jogadores = []
pedidos = []

next_id_jogador = 1
next_id_partida = 1
next_id_pedido = 1

# ------------------- JOGADORES -------------------

@app.post('/jogadores')
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
    return {'erro': 'Jogador não encontrado'}

# ------------------- PARTIDAS -------------------

@app.get('/partidas')
def partidas():
    return list_partidas


@app.post('/partidas')
def criar_partida(data: str, local: str, tipo: str, categoria: str):
    global next_id_partida
    partida = {
        'id': next_id_partida,
        'data': data,
        'local': local,
        'tipo': tipo,
        'categoria': categoria,
        'jogadores': []  # já cria com lista de jogadores
    }
    list_partidas.append(partida)
    next_id_partida += 1
    return partida


@app.delete('/partidas/{id}')
def excluir_partida(id: int):
    for p in list_partidas:
        if p['id'] == id:
            list_partidas.remove(p)
            return {'mensagem': f'Partida {id} removida com sucesso!'}
    return {'erro': 'Partida inexistente'}

# ------------------- PARTICIPAR -------------------

@app.post('/partidas/participar/{id_jogador}/{id_partida}')
def participar_partida(id_jogador: int, id_partida: int):
    global next_id_pedido

    jogador = next((j for j in jogadores if j['id'] == id_jogador), None)
    partida = next((p for p in list_partidas if p['id'] == id_partida), None)

    if not jogador:
        return {'erro': 'Jogador não encontrado'}
    if not partida:
        return {'erro': 'Partida não encontrada'}

    pedido = {
        'id': next_id_pedido,
        'id_jogador': id_jogador,
        'id_partida': id_partida,
        'status': 'pendente'
    }
    pedidos.append(pedido)
    next_id_pedido += 1

    return pedido


@app.post('/partidas/aceitar/{id_pedido}')
def aceitar_pedido(id_pedido: int):
    pedido = next((p for p in pedidos if p['id'] == id_pedido), None)
    if not pedido:
        return {'erro': 'Pedido não encontrado'}

    jogador = next((j for j in jogadores if j['id'] == pedido['id_jogador']), None)
    partida = next((p for p in list_partidas if p['id'] == pedido['id_partida']), None)

    if not jogador or not partida:
        return {'erro': 'Jogador ou partida não encontrados'}

    pedido['status'] = 'aceito'
    partida['jogadores'].append(jogador)
    return {'mensagem': f"Jogador {jogador['nome']} aceito na partida {partida['id']}"}


@app.post('/partidas/recusar/{id_pedido}')
def recusar_pedido(id_pedido: int):
    pedido = next((p for p in pedidos if p['id'] == id_pedido), None)
    if not pedido:
        return {'erro': 'Pedido não encontrado'}

    pedido['status'] = 'recusado'
    return {'mensagem': f"Pedido {id_pedido} recusado"}
