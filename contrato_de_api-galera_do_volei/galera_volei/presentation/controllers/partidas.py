from typing import Optional
from application import pagamento_services
from application.partida_services import PartidaService
from application.arena_services import ArenaService
from application.jogadores_services import JogadoresService
from application.pedido_services import PedidoService
from schemas.avaliacao_jogador import AvaliacaoJogador
from schemas.pagamento import Pagamento
from schemas.pedido import Pedido
from schemas.partida import Partida
from schemas.partida_update import PartidaUpdate
from schemas.pedido import Status
from schemas.avaliacao import Avaliacao
from schemas.jogador import Jogador

from presentation.exceptions.HTTPNotFound import NotFoundException
from presentation.exceptions.ConflictException import ConflictException
from presentation.exceptions.HTTPException import AppException

from fastapi import Body, Query

global next_id_partida
next_id_partida = 1

global next_id_pedido
next_id_pedido = 1

global next_id_avaliacao
next_id_avaliacao = 1

global next_id_avaliacao_jogador
next_id_avaliacao = 1

class PartidaController:
    def __init__(self, partida_service: PartidaService, arena_service: ArenaService,
                 jogador_service: JogadoresService, pedido_service: PedidoService):
        self.__partida_service = partida_service
        self.__arena_service = arena_service
        self.__jogador_service = jogador_service
        self.__pedido_service = pedido_service

    # ---------------------- PARTIDAS ----------------------
    def criar_partida(self, partida: Partida):
        global next_id_partida
        arena = self.__arena_service.encontrar_arena(partida.id_local)
        partidas = self.__partida_service.listar_partidas()

        if not arena:
            raise NotFoundException('Não é possível criar uma partida, arena inexistente')
        
        for p in partidas:
            if p.data == partida.data and p.id_local == partida.id_local and p.tipo == partida.tipo and p.categoria == partida.categoria:
                raise ConflictException('Já existe uma partida cadastrada com essa data, arena, tipo e categoria')


        nova_partida = Partida(
            id=next_id_partida,
            data=partida.data,
            id_local=partida.id_local,
            tipo=partida.tipo,
            categoria=partida.categoria
        )

        next_id_partida += 1
        self.__partida_service.criar_partida(nova_partida)

        return {'msg': 'Partida criada com sucesso', 'partida': nova_partida}

    def listar_partidas(self):
        partidas = self.__partida_service.listar_partidas()

        if not partidas:
            return []
        return partidas

    def listar_partida_id(self, id: int):
        partida = self.__partida_service.encontrar_partida(id)
        if not partida:
            raise NotFoundException(f'Partida {id} não encontrada')
        return partida

    def excluir_partida(self, id: int):
        partida = self.__partida_service.encontrar_partida(id)
        if not partida:
            raise NotFoundException(f'Partida {id} não encontrada')

        self.__partida_service.excluir_partida(id)
        return {'msg': 'Partida excluída com sucesso!', 'partida': partida}

    def alterar_partida(self, id: int, dados: Partida):
        partida = self.__partida_service.encontrar_partida(id)
        if not partida:
            raise NotFoundException('Partida não encontrada')
        
        partida_atualizada = self.__partida_service.alterar_partida(id, dados)
        return {'msg': 'Partida alterada com sucesso!', 'partida': partida_atualizada}
        

    def alterar_atributo_partida(self, id: int, dados: PartidaUpdate):
        partida = self.__partida_service.encontrar_partida(id)

        if not partida:
            raise NotFoundException('Partida não encontrada')
        
        partida_atualizada = self.__partida_service.alterar_atributo_partida(
            id, dados.model_dump(exclude_unset=True)
        )
        if partida_atualizada:
            return {'msg': 'Partida atualizada parcialmente!', 'partida': partida_atualizada}
        

    # ---------------------- MODERADOR ----------------------
    def adicionar_moderador(self, id_partida: int, dados: PartidaUpdate):
        partida = self.__partida_service.encontrar_partida(id_partida)
        if not partida:
            raise NotFoundException("Partida não encontrada.")

        if not dados.moderador_id:
            raise AppException("É necessário informar o moderador_id.")

        jogador = self.__jogador_service.encontrar_jogador(dados.moderador_id)
        if not jogador:
            raise NotFoundException("Jogador não encontrado.")

        if partida.moderador_id is not None:
            return AppException("Esta partida já possui um moderador.")

        partida_atualizada = self.__partida_service.alterar_atributo_partida(
            id_partida, dados.model_dump(exclude_unset=True)
        )
        return {"msg": "Moderador adicionado com sucesso!", "partida": partida_atualizada}

    # ---------------------- PEDIDOS ----------------------
    def fazer_pedido(self, pedido: Pedido):
        global next_id_pedido
        jogador = self.__jogador_service.encontrar_jogador(pedido.id_jogador)
        partida = self.__partida_service.encontrar_partida(pedido.id_partida)

        if not partida:
            raise NotFoundException('Partida não encontrada.')
        if not jogador:
            raise NotFoundException('Jogador não encontrado.')

        
        pedido.id_pedido = next_id_pedido
        next_id_pedido += 1

        self.__pedido_service.criar_pedido(pedido)

        # Adiciona o jogador como participante pendente e salva o retorno
        pendentes = self.__partida_service.adicionar_participante_pendente(
            pedido.id_partida, pedido.id_jogador
        )

        return {
            'msg': 'Solicitação de participação em partida criada com sucesso!',
            'pedido': pedido,
            'jogadores_pendentes': pendentes
        }

    def aceitar_pedido(
            self,
            id_pedido: int,
            id_moderador: int,
            status: Status = Body(default=Status.PENDENTE, embed=True)
        ):
        pedido = self.__pedido_service.aceitar_pedido(id_pedido, id_moderador, status)
        if pedido:
            self.__partida_service.remover_participante_pendente(
                pedido['id_partida'], pedido['id_jogador']
            )
            self.__partida_service.adicionar_participante_confirmado(
                pedido['id_partida'], pedido['id_jogador']
            )
            return {'msg': 'Pedido aceito e jogador confirmado com sucesso!'}
        #return {'msg': 'Pedido não encontrado ou moderador não autorizado.'}
        return pedido
    

    def avaliar_partida(self, id_partida:int, avaliacao:Avaliacao):
        partida = self.__partida_service.encontrar_partida(id_partida)

        if not partida:
            raise NotFoundException('Partida não encontrada.')
        
        if avaliacao.id_jogador not in partida.participantes_confirmados:
            raise NotFoundException('Jogador não participou da partida')

        
        avaliacao = Avaliacao(
            id = next_id_avaliacao,
            id_jogador = avaliacao.id_jogador,
            avaliacao = avaliacao.avaliacao
        )
        next_id_avaliacao += 1

        self.__partida_service.avaliar_partida(id_partida, avaliacao)
        return {'msg':'Avaliação incluída com sucesso !', 'avaliacao':avaliacao}
        
    def avaliar_jogador(self, id_partida: int, avaliacao: AvaliacaoJogador):
        avaliacao = AvaliacaoJogador(
            id=next_id_avaliacao_jogador,
            id_partida=id_partida,
            id_jogador_avaliado=avaliacao.id_jogador_avaliado,
            id_jogador_avaliador=avaliacao.id_jogador_avaliador,
            comentario=avaliacao.comentario,
            nota=avaliacao.nota
        )
        next_id_avaliacao_jogador += 1
        

        resultado = self.avaliar_jogador(id_partida, avaliacao)
        if not resultado:
          raise NotFoundException("Jogador não participante ou partida não encontrada")

        return {"msg": "Avaliação do jogador incluída com sucesso!", "avaliacao": resultado}
    

    def excluir_participante(self, 
        id_partida: int,
        id_jogador: int = Body(..., embed=True),
        id_moderador: int = Body(..., embed=True)
    ):
        partida = self.__partida_service.encontrar_partida(id_partida)
        if not partida:
            raise NotFoundException("Partida não encontrada")

        if partida.moderador_id != id_moderador:
            raise AppException("Ação não autorizada: não é moderador", 403)

        self.__partida_service.excluir_participante(id_partida, id_jogador)
        return {"msg": f"Jogador {id_jogador} removido da partida {id_partida}"}
    

    def desistir_partida(self, id_partida:int, id_jogador:int):
        partida = self.__partida_service.encontrar_partida(id_partida)
        jogador = self.__jogador_service.encontrar_jogador(id_jogador)

        if not partida:
            raise NotFoundException(f'Partida {id} não encontrada.')
        
        if not jogador:
            raise NotFoundException(f'Jogador {id} não encontrado.')
        
        jogador_desistente = self.__partida_service.desistir_partida(id_partida, id_jogador)
        return jogador_desistente
    
    def alterar_equipe(self, id_partida: int, jogador_id:int =  Body(..., embed=True)):
        
        partida = self.__partida_service.encontrar_partida(id_partida)
        jogador = self.__jogador_service.encontrar_jogador(jogador_id)

        if not partida:
            raise NotFoundException("Partida não encontrada")
        if not jogador:
            raise NotFoundException("Jogador não encontrado")

        
        partida_alterada = self.__partida_service.alterar_equipe(id_partida, jogador_id)
        return partida_alterada


    def efetuar_pagamento(self, id_partida:int, pagamento: Pagamento):
        partida = self.__partida_service.encontrar_partida(id_partida)

        if not partida:
            raise NotFoundException('Partida não encontrada')
        
        if pagamento.id_jogador not in partida.participantes_confirmados:
            raise AppException('Jogador não confirmado na partida', 400)
        
        pagamento = self.__partida_service.efetuar_pagamento(pagamento)
        return {'msg':'Pagamento efetuado com sucesso',"pagamento": pagamento}
    
    def formar_equipes(
            self,
            id_partida: int,
            criterio: Optional[str] = Query(None, description="Opção: 'categoria' ou 'genero'")
    ):
    # Busca a partida
        partida = self.__partida_service.encontrar_partida(id_partida)
        if not partida:
            raise NotFoundException("Partida não encontrada")

        # Busca todos os jogadores
        jogadores = self.__jogador_service.listar_jogadores()

        # Chama o método de formar equipes do service
        resultado = self.__partida_service.formar_equipes(partida, jogadores, criterio)
        return resultado