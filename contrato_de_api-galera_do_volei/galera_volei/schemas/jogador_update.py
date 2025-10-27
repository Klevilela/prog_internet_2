from pydantic import BaseModel
from typing import Optional

class JogadorUpdate(BaseModel):
    nome:Optional[str] = None
    sexo:Optional[str] = None
    categoria:Optional[str] = None