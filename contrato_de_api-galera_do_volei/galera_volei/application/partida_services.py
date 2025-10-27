from typing import List, Optional
from schemas.partida import Partida
from schemas.avaliacao import Avaliacao
from schemas.pagamento import Pagamento
from schemas.jogador import Jogador

from schemas.avaliacao_jogador import AvaliacaoJogador
from presentation.exceptions.HTTPException import AppException
from presentation.exceptions.HTTPNotFound import NotFoundException


import random

class PartidaService:
    def __init__(self):
        self.__partidas: List[Partida] = []

    def encontrar_partida(self, id: int) -> Optional[Partida]:
        for partida in self.__partidas:
            if partida.id == id:
                return partida
        return None

    def criar_partida(self, partida: Partida) -> Partida:
        self.__partidas.append(partida)
        return partida

    def listar_partidas(self) -> List[Partida]:
        return self.__partidas

    def listar_partida_id(self, id: int) -> Optional[Partida]:
        return self.encontrar_partida(id)

    def excluir_partida(self, id: int) -> Optional[Partida]:
        partida = self.encontrar_partida(id)
        if partida:
            self.__partidas.remove(partida)
            return partida
        return None
    
    def alterar_partida(self, id: int, dados: Partida) -> Optional[Partida]:
        partida = self.encontrar_partida(id)
        if not partida:
            return None

        for field, value in dados.model_dump().items():
            setattr(partida, field, value)
        return partida

    def alterar_atributo_partida(self, id: int, dados: dict) -> Optional[Partida]:
        partida = self.encontrar_partida(id)
        if not partida:
            return None

        for chave, valor in dados.items():
            if valor is not None:
                setattr(partida, chave, valor)
        return partida


    def adicionar_moderador(self, id_partida: int, id_jogador: int) -> Optional[Partida]:
        partida = self.encontrar_partida(id_partida)
        if partida and partida.moderador_id is None:
            partida.moderador_id = id_jogador
            return partida
        return None

    def encontrar_moderador(self, id_partida: int, id_jogador: int) -> Optional[int]:
        partida = self.encontrar_partida(id_partida)
        if partida and partida.moderador_id == id_jogador:
            return id_jogador
        return None

    def adicionar_participante_pendente(self, id_partida: int, id_jogador: int) -> Optional[List[int]]:
        partida = self.encontrar_partida(id_partida)
        if partida:
            if id_jogador not in partida.participantes_pendentes:
                partida.participantes_pendentes.append(id_jogador)
                return partida.participantes_pendentes
        return None

    def remover_participante_pendente(self, id_partida: int, id_jogador: int) -> Optional[List[int]]:
        partida = self.encontrar_partida(id_partida)
        if partida:
            if id_jogador in partida.participantes_pendentes:
                partida.participantes_pendentes.remove(id_jogador)
                return partida.participantes_pendentes
        return None

    def adicionar_participante_confirmado(self, id_partida: int, id_jogador: int) -> Optional[List[int]]:
        partida = self.encontrar_partida(id_partida)
        if partida:
            if id_jogador in partida.participantes_pendentes:
                self.remover_participante_pendente(id_partida, id_jogador)
            if id_jogador not in partida.participantes_confirmados:
                partida.participantes_confirmados.append(id_jogador)
            return partida.participantes_confirmados
        return None
    
    def avaliar_partida(self, id_partida:int, avaliacao:Avaliacao):
        partida = self.encontrar_partida(id_partida)

        if partida and avaliacao.id_jogador in partida.participantes_confirmados:
            partida.avaliacoes.append(avaliacao)
            return partida.avaliacoes
        
        return None
    
    def avaliar_jogador(self, id_partida: int, avaliacao: AvaliacaoJogador):
        partida = self.encontrar_partida(id_partida)
        if not partida:
            return None

        # só permite avaliação se ambos os jogadores estiverem confirmados
        if (avaliacao.id_jogador_avaliado not in partida.participantes_confirmados or
            avaliacao.id_jogador_avaliador not in partida.participantes_confirmados):
            return None

        # adiciona avaliação
        partida.avaliacoes_jogadores.append(avaliacao)
        return avaliacao
    
    def excluir_participante(self, id_partida: int, id_jogador: int, id_moderador: int):
        partida = self.encontrar_partida(id_partida)
        if not partida:
            return None

        if partida.moderador_id != id_moderador:
            return None  # não autorizado

        # remove jogador das listas, se estiver
        if id_jogador in partida.participantes_confirmados:
            partida.participantes_confirmados.remove(id_jogador)
        if id_jogador in partida.participantes_pendentes:
            partida.participantes_pendentes.remove(id_jogador)
        
        if id_jogador in partida.equipe_a:
            partida.equipe_a.remove(id_jogador)
        if id_jogador in partida.equipe_b:
            partida.equipe_b.remove(id_jogador)

        return partida
    
    def desistir_partida(self, id_partida: int, id_jogador: int):
        partida = self.encontrar_partida(id_partida)
        if not partida:
            return None

        if id_jogador not in partida.participantes_confirmados:
            return None  # jogador não está confirmado

        partida.participantes_confirmados.remove(id_jogador)
        
        if id_jogador in partida.equipe_a:
            partida.equipe_a.remove(id_jogador)
        if id_jogador in partida.equipe_b:
            partida.equipe_b.remove(id_jogador)

        return partida


    def alterar_equipe(self, id_partida: int, id_jogador: int):
        partida = self.encontrar_partida(id_partida)
        if not partida:
            return None

        if id_jogador not in partida.participantes_confirmados:
            return None  # só jogador confirmado pode mudar de equipe

        if id_jogador in partida.equipe_a:
            partida.equipe_a.remove(id_jogador)
            partida.equipe_b.append(id_jogador)
        elif id_jogador in partida.equipe_b:
            partida.equipe_b.remove(id_jogador)
            partida.equipe_a.append(id_jogador)
        else:
            return None  # jogador não está em nenhuma equipe

        return partida
    
    def efetuar_pagamento(self, id_partida:int, pagamento:Pagamento):
        from presentation.routes.partidas import pagamento_service
        partida = self.encontrar_partida(id_partida)
        

        if not partida:
            return None
        
        return pagamento_service.criar_pagamento(pagamento)
    
    def formar_equipes(self, partida: Partida, lista_jogadores: list[Jogador], criterio: str | None = None):
        if not partida:
            raise AppException("Partida não encontrada.")

        # Filtra jogadores confirmados
        jogadores_confirmados = [
            jogador for jogador in lista_jogadores
            if jogador.id in partida.participantes_confirmados
        ]

        # Aplica filtro se houver critério
        if criterio == "categoria":
            jogadores_confirmados = [
                j for j in jogadores_confirmados
                if j.categoria == partida.categoria
            ]
        elif criterio == "genero":
            jogadores_confirmados = [
                j for j in jogadores_confirmados
                if j.genero == partida.tipo
            ]

        n = len(jogadores_confirmados)

        # Checagem mínima, máxima e par
        if n < 4:
            raise AppException("Jogadores insuficientes para formar equipes.", status_code=400)
        if n > 12:
            raise AppException("Número máximo de jogadores excedido.", status_code=400)
        if n % 2 != 0:
            raise AppException("Número de jogadores precisa ser par.", status_code=400)


        # Embaralha e divide
        random.shuffle(jogadores_confirmados)
        metade = n // 2
        partida.equipe_a = [j.id for j in jogadores_confirmados[:metade]]
        partida.equipe_b = [j.id for j in jogadores_confirmados[metade:]]

        return {"equipe_a": partida.equipe_a, "equipe_b": partida.equipe_b}