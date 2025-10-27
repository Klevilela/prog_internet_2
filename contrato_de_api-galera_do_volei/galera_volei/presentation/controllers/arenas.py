from application.arena_services import ArenaService
from presentation.exceptions.ConflictException import ConflictException
from schemas.arena import Arena
from schemas.arena_update import ArenaUpdate

from presentation.exceptions.HTTPNotFound import NotFoundException

next_id_arena = 1

class ArenaControllers:
    def __init__(self, arena_service: ArenaService):
        self.__arena_service = arena_service
    
    def criar_arena(self, arena: Arena):
        global next_id_arena

        # Lista todas as arenas existentes
        arenas_existentes = self.__arena_service.listar_arenas()

        # Verifica se já existe arena com mesmo nome e zona
        for a in arenas_existentes:
            if a.nome == arena.nome and a.zona == arena.zona:
                raise ConflictException('Já existe uma arena com esse nome nesta zona.')

        # Cria a nova arena com ID incremental
        nova_arena = Arena(
            id=next_id_arena,
            nome=arena.nome,
            zona=arena.zona
        )

        self.__arena_service.criar_arena(nova_arena)
        next_id_arena += 1
        return {'msg': 'Arena criada com sucesso', 'arena': nova_arena}


    def listar_arenas(self):
        arenas = self.__arena_service.listar_arenas()
        if not arenas:
            return []
        return arenas
    
    def listar_arenas_id(self, id: int):
        arena = self.__arena_service.encontrar_arena(id)
        if not arena:
            raise NotFoundException(f"Arena {id} não encontrada")
        return arena

    def excluir_arena(self, id: int):
        arena = self.__arena_service.encontrar_arena(id)
        if not arena:
            raise NotFoundException(f"Arena {id} não encontrada")
        
        self.__arena_service.excluir_arena(id)
        return {'msg': f"Arena {id} excluída com sucesso", 'arena': arena}
    
    def alterar_arena(self, id: int, arena: Arena):
        # Atualiza com objeto Arena real
        arena_atualizada = self.__arena_service.alterar_arena(id, arena)
        if not arena_atualizada:
            raise NotFoundException(f"Arena {id} não encontrada")
        
        return {'msg': 'Arena atualizada', 'arena': arena_atualizada}

    def alterar_atributo(self, id: int, dados: ArenaUpdate):
        arena_existente = self.__arena_service.encontrar_arena(id)
        if not arena_existente:
            raise NotFoundException(f"Arena {id} não encontrada")
        
        # Atualiza apenas os campos fornecidos
        arena_atualizada = self.__arena_service.alterar_atributo(id, dados.model_dump(exclude_unset=True))
        return {'msg': 'Arena parcialmente atualizada', 'arena': arena_atualizada}
