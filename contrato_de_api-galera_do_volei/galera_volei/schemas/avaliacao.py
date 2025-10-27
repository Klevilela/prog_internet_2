from pydantic import BaseModel

class Avaliacao(BaseModel):
    id:int
    id_jogador:int
    avaliacao:str = None