from pydantic import BaseModel

class AvaliacaoJogador(BaseModel):
    id: int
    id_partida: int
    id_jogador_avaliado: int  
    id_jogador_avaliador: int
    comentario: str = None
    nota: int = None
