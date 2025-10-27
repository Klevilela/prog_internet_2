from typing import List, Optional
from schemas.pedido import Pedido

from presentation.exceptions.HTTPException import AppException
from presentation.exceptions.HTTPNotFound import NotFoundException
from presentation.exceptions.BadRequestException import BadRequestException 

class PedidoService:
    def __init__(self):
        self.__pedidos: List[Pedido] = []

    def criar_pedido(self, pedido: Pedido) -> Pedido:
        self.__pedidos.append(pedido)
        return pedido

    def encontrar_pedido(self, id_pedido: int) -> Optional[Pedido]:
        for pedido in self.__pedidos:
            if pedido.id_pedido == id_pedido:
                return pedido
        return None

    def aceitar_pedido(self, id_pedido: int, id_moderador: int, status: str) -> Pedido:
        from presentation.routes.partidas import partida_service
        pedido = self.encontrar_pedido(id_pedido)
        if not pedido:
            raise NotFoundException('Pedido não encontrado.')

        # Checa se o moderador é válido na partida associada
        if pedido:
            id_pedido = pedido.id_partida
            moderador_id_da_partida = partida_service.encontrar_moderador(id_pedido, id_moderador)
            if moderador_id_da_partida != id_moderador:
                raise AppException('Moderador não autorizado a processar este pedido.')

            if status == 'aceito':
                pedido.status = status
                return {
                    'success': True,
                    'id_partida': pedido.id_partida,
                    'id_jogador': pedido.id_jogador
                }
            elif status == 'rejeitado':
                pedido.status = status
                raise AppException('Pedido explicitamente rejeitado.')

            raise  BadRequestException('Status de pedido inválido.')
