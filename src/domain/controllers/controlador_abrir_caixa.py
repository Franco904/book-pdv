import datetime

from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.extrato_caixa_dao import ExtratoCaixaDAO
from src.domain.models.caixa import Caixa
from src.domain.models.extrato_caixa import ExtratoCaixa
from src.domain.models.operador_caixa import OperadorCaixa
from src.domain.views.caixa.tela_abrir_caixa import TelaAbrirCaixa


class ControladorAbrirCaixa:
    def __init__(self, controlador_sistema, caixa_dao: CaixaDAO, extrato_caixa_dao: ExtratoCaixaDAO) -> None:
        self.__tela_caixa = TelaAbrirCaixa()
        self.__controlador_sistema = controlador_sistema
        self.__caixa_dao = caixa_dao
        self.__extrato_caixa_dao = extrato_caixa_dao

        self.__caixas = [Caixa(1), Caixa(2), Caixa(3)]
        self.__data_abertura = datetime.datetime.now().strftime("%d/%m/%Y")

    def __load_caixas_fisicos(self):
        return self.__caixa_dao.get_all()

    def abre_tela(self, operador_caixa: OperadorCaixa):
        caixas_disponiveis = list(
            filter(lambda caixa: caixa.operador_caixa is None or caixa.operador_caixa.cpf != operador_caixa.cpf,
                   self.__caixas)
        )
        caixas_ids = list(map(lambda caixa: caixa.id, caixas_disponiveis))

        self.__tela_caixa.init_components(caixas_ids, self.__data_abertura)
        result = self.__tela_caixa.open(caixas_disponiveis)

        if result["option"] == 0 or result["values"] is None:
            return self.retornar()

        result["values"]["saldo_abertura"] = result["saldo_abertura"]

        self.abrir_caixa(result["values"], operador_caixa)

    def abrir_caixa(self, values, operador_caixa: OperadorCaixa):
        if values is None:
            return

        filtered = list(filter(lambda caixa: caixa.id == values["caixa_id"], self.__caixas))
        if filtered is None:
            return

        caixa = filtered[0]

        caixa.operador_caixa = operador_caixa
        self.__caixa_dao.update_entity(caixa.id, caixa.operador_caixa.cpf, operador_caixa.cpf)

        extrato = ExtratoCaixa(
            caixa,
            self.__data_abertura,
            values["saldo_abertura"],
            values["observacoes"]
        )

        self.__extrato_caixa_dao.persist_entity(extrato)

    def retornar(self):
        self.__tela_caixa.close()
        self.__controlador_sistema.controllers["inicio"].abre_tela(True)
