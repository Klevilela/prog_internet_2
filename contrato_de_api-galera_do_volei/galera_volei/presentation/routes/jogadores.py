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