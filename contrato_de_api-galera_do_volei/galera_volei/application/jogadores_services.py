from typing import List, Optional
from schemas.jogador import Jogador  # seu modelo Pydantic

class JogadoresService:
    def __init__(self):
        self.__jogadores: List[Jogador] = []

    # Busca por ID
    def encontrar_jogador(self, id: int) -> Optional[Jogador]:
        for jogador in self.__jogadores:
            if jogador.id == id:
                return jogador
        return None

    # Retorna ID se existir
    def retornar_id(self, id: int) -> Optional[int]:
        jogador = self.encontrar_jogador(id)
        if jogador:
            return id
        return None

    # Adiciona um jogador (objeto Jogador)
    def incluir_jogador(self, jogador: Jogador) -> Jogador:
        self.__jogadores.append(jogador)
        return jogador

    # Lista todos
    def listar_jogadores(self) -> List[Jogador]:
        return self.__jogadores

    # Lista um por ID
    def listar_jogador_id(self, id: int) -> Optional[Jogador]:
        return self.encontrar_jogador(id)

    # Remove um jogador por ID
    def excluir_jogador(self, id: int) -> Optional[Jogador]:
        jogador = self.encontrar_jogador(id)
        if jogador:
            self.__jogadores.remove(jogador)
            return jogador
        return None

    # Atualiza atributos passando um dicionário
    def alterar_jogador(self, id: int, dados: dict) -> Optional[Jogador]:
        jogador = self.encontrar_jogador(id)
        if not jogador:
            return None
        jogador.update(dados)
        return jogador

    # Alias para atualização parcial (mesmo comportamento)
    def alterar_atributo(self, id: int, dados: dict) -> Optional[Jogador]:
        jogador = self.encontrar_jogador(id)

        if jogador:
            for chave, valor in dados.items():
                if valor is not None:
                    jogador[chave] = valor
                    return jogador
            return None
