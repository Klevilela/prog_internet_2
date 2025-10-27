from pydantic import BaseModel
from typing import Optional

class ArenaUpdate(BaseModel):
    nome:Optional[str] = None
    zona:Optional[str] = None