from pydantic import BaseModel
from enum import Enum

class Genero(str, Enum):
    masculino = "masculino"
    feminino = "feminino"

class Categoria(str, Enum):
    amador = "amadora"
    profissional = "profissional"

class Jogador(BaseModel):
    id: int
    nome: str
    genero: Genero
    categoria: Categoria
