from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from schemas.jogador import Categoria

from enum import Enum

class TipoPartida(str, Enum):
    mista = "mista"
    feminina = "feminina"
    masculina = "masculina"

class Partida(BaseModel):
    id: int
    data: datetime
    id_local: int
    tipo: TipoPartida = TipoPartida.mista  # padrão = mista
    categoria: Categoria = Categoria.amador  # padrão = amador

    participantes_pendentes: List[int] = []
    participantes_confirmados: List[int] = []
    equipe_a: List[int] = []
    equipe_b: List[int] = []
    moderador_id: Optional[int] = None
    avaliacoes: List = []
