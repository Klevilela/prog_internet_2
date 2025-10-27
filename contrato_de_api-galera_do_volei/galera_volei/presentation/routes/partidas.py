from fastapi import APIRouter
from presentation.controllers.partidas import PartidaController

# Importa apenas as classes de service (não as instâncias)
from application.partida_services import PartidaService
from application.pedido_services import PedidoService
from application.pagamento_services import PagamentoService

from presentation.routes.jogadores import jogador_service
from presentation.routes.arenas import arena_service


# Criação das instâncias de cada service

partida_service = PartidaService()
pedido_service = PedidoService()
pagamento_service = PagamentoService()

# Injeta tudo no controller
partida_controller = PartidaController(
    partida_service,
    arena_service,
    jogador_service,
    pedido_service
)

# Criação do router
partida_router = APIRouter()

# Rotas
partida_router.post('/partidas')(partida_controller.criar_partida)
partida_router.get('/partidas')(partida_controller.listar_partidas)
partida_router.get('/partidas/{id}')(partida_controller.listar_partida_id)
partida_router.put('/partidas/{id}')(partida_controller.alterar_partida)
partida_router.patch('/partidas/{id}')(partida_controller.alterar_atributo_partida)
partida_router.delete('/partidas/{id}')(partida_controller.excluir_partida)

partida_router.post('/partidas/pedido')(partida_controller.fazer_pedido)
partida_router.patch('/partidas/aceitar_pedido/{id_pedido}/{id_moderador}')(partida_controller.aceitar_pedido)
partida_router.patch('/partidas/{id_partida}/moderador')(partida_controller.adicionar_moderador)
partida_router.post('/partidas/{id_partida}/avaliar')(partida_controller.avaliar_partida)
