from schemas.pagamento import FormaPagamento, Pagamento


class PagamentoService:
    def __init__(self):
        self.__pagamentos = []
        self.next_id = 1
        self.VALOR_FIXO = 50.0  # valor fixo preliminar

    def criar_pagamento(self, pagamento: Pagamento):
        # valida parcelas apenas para cartão
        if pagamento.forma == FormaPagamento.cartao:
            if pagamento.parcelas is None:
                return None  # precisa informar número de parcelas
        else:
            pagamento.parcelas = None  # para dinheiro e pix, não deve ter parcelas

        # atribui id automático
        pagamento.id = self.next_id
        self.next_id += 1
        pagamento.valor = self.VALOR_FIXO

        self.__pagamentos.append(pagamento)
        return pagamento

    def listar_por_partida(self, id_partida: int):
        return [p for p in self.__pagamentos if p.id_partida == id_partida]

    def listar_por_jogador(self, id_jogador: int):
        return [p for p in self.__pagamentos if p.id_jogador == id_jogador]
