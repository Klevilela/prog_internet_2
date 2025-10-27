from fastapi import APIRouter
from presentation.controllers.arenas import ArenaControllers
from application.arena_services import ArenaService

arena_router = APIRouter()

arena_service = ArenaService()
arena_controller = ArenaControllers(arena_service)

arena_router.get('/arenas')(arena_controller.listar_arenas)
arena_router.get('/arenas/{id}')(arena_controller.listar_arenas_id)
arena_router.post('/arenas')(arena_controller.criar_arena)
arena_router.put('/arenas/{id}')(arena_controller.alterar_arena)
arena_router.patch('/arenas/{id}')(arena_controller.alterar_atributo)
arena_router.delete('/arenas/{id}')(arena_controller.excluir_arena)
