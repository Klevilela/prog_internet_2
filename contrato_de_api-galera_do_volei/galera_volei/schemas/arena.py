from pydantic import BaseModel

class Arena(BaseModel):
    id: int
    nome:str = None
    zona:str = None
