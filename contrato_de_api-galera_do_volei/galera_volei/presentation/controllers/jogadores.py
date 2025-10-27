from application.jogadores_services import JogadoresService
from schemas.jogador import Jogador
from schemas.jogador_update import JogadorUpdate
from presentation.exceptions.HTTPNotFound import NotFoundException

from presentation.exceptions.ConflictException import ConflictException

next_id_jogador = 1

class JogadoresControllers:
    def __init__(self, jogador_service: JogadoresService):
        self.__jogador_service = jogador_service

    def incluir_jogador(self, jogador: Jogador):
        global next_id_jogador
        # Cria um objeto Jogador real
        jogadores = self.listar_jogadores()

            

        for j in jogadores:
            if j.nome == jogador.nome and j.genero == jogador.genero and j.categoria == jogador.categoria:
                raise ConflictException('Já existe jogador o mesmo nome, gênero e categoria')

        novo_jogador = Jogador(
            id=next_id_jogador,
            nome=jogador.nome,
            genero=jogador.genero,
            categoria=jogador.categoria
        )
        self.__jogador_service.incluir_jogador(novo_jogador)
        next_id_jogador += 1
        return {'msg': 'Jogador incluído com sucesso', 'jogador': novo_jogador}

    def listar_jogadores(self):
        jogadores = self.__jogador_service.listar_jogadores()
        if not jogadores:
            return []
        return jogadores

    def listar_jogador_id(self, id: int):
        jogador = self.__jogador_service.listar_jogador_id(id)

        if not jogador:
            raise NotFoundException(f'Jogador {id} não encontrado')
        return jogador

    def excluir_jogador(self, id: int):
        jogador = self.__jogador_service.excluir_jogador(id)

        if not jogador:
            raise NotFoundException(f'Jogador {id} não encontrado')
        return {'msg': 'Jogador excluído com sucesso', 'jogador': jogador}

    def alterar_jogador(self, id: int, jogador: Jogador):
        # Atualiza com objeto Jogador real
        jogador_atualizado = self.__jogador_service.alterar_jogador(id, jogador)

        if not jogador_atualizado:
            raise NotFoundException(f'Jogador {id} não encontrado')
        return {'msg': 'Jogador atualizado com sucesso', 'jogador': jogador_atualizado}

    def alterar_atributo(self, id: int, dados: JogadorUpdate):
        jogador_existente = self.__jogador_service.encontrar_jogador(id)
        if not jogador_existente:
            raise NotFoundException(f'Jogador {id} não encontrado')
        
        
        self.__jogador_service.alterar_atributo(id, dados.model_dump(exclude_unset=True))
        jogador_atualizado = self.__jogador_service.encontrar_jogador(id)

        return {'msg': 'Atributos atualizados', 'jogador': jogador_atualizado}
