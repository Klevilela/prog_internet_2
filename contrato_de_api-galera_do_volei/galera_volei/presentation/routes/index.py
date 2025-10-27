from fastapi import APIRouter
from presentation.routes.jogadores import jogador_router
from presentation.routes.arenas import arena_router
from presentation.routes.partidas import partida_router

router = APIRouter()

router.include_router(jogador_router)
router.include_router(arena_router)
router.include_router(partida_router)