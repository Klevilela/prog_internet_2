from typing import List, Optional
from schemas.arena import Arena  # seu modelo Pydantic

class ArenaService:
    def __init__(self):
        self.__arenas: List[Arena] = []

    # Busca por ID
    def encontrar_arena(self, id: int) -> Optional[Arena]:
        for arena in self.__arenas:
            if arena.id == id:
                return arena
        return None

    # Retorna ID se existir
    def retornar_id(self, id: int) -> Optional[int]:
        arena = self.encontrar_arena(id)
        if arena:
            return id
        return None

    # Cria uma nova arena
    def criar_arena(self, arena: Arena) -> Arena:
        self.__arenas.append(arena)
        return arena

    # Lista todas
    def listar_arenas(self) -> List[Arena]:
        return self.__arenas

    # Lista uma por ID
    def listar_arenas_id(self, id: int) -> Optional[Arena]:
        return self.encontrar_arena(id)

    # Remove por ID
    def excluir_arena(self, id: int) -> Optional[Arena]:
        arena = self.encontrar_arena(id)
        if arena:
            self.__arenas.remove(arena)
            return arena
        return None

    # Atualiza atributos usando dict
    def alterar_arena(self, id: int, dados: dict) -> Optional[Arena]:
        arena = self.encontrar_arena(id)
        if not arena:
            return None
        
        arena.update(dados)
        return arena

    # Alias para atualização parcial
    def alterar_atributo(self, id: int, dados: dict) -> Optional[Arena]:
        arena = self.encontrar_arena(id)

        if arena:
            for chave, valor in dados.items():
                if valor is not None:
                    arena[chave] = valor
                    return arena
            return None
