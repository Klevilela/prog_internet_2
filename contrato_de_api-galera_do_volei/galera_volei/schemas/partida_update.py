from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from schemas.jogador import Jogador

class PartidaUpdate(BaseModel):
    data: Optional[date] = None
    id_local: Optional[int] = None
    tipo:Optional[str] = None
    categoria:Optional[str] = None

    participantes:Optional[List[Jogador]] = None
    equipe_a:Optional[List[Jogador]] = None
    equipe_b:Optional[List[Jogador]] = None
    moderador_id:Optional[int] = None