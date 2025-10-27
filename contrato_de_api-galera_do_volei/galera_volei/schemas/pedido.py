from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Status(str, Enum):
    PENDENTE = 'pendente'
    ACEITO = 'aceito'
    REJEITADO = 'rejeitado'


class Pedido(BaseModel):
    id_pedido:int
    id_partida:int
    id_jogador:int
    status:Status = Field(default=Status.PENDENTE)
    moderador_id:Optional[int] = None