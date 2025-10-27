from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class FormaPagamento(str, Enum):
    dinheiro = 'dinheiro'
    pix = 'pix'
    cartao = 'cartao'


class Pagamento(BaseModel):
    id: int = None
    id_partida: int
    id_jogador: int
    valor: float
    forma: FormaPagamento
    valor: float = None
    parcelas: Optional[int] = Field(gt=0, le=10)