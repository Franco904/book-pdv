import datetime
import PySimpleGUI as sg

from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.extrato_caixa_dao import ExtratoCaixaDAO
from src.domain.exceptions.lista_vazia_exception import ListaVaziaException
from src.domain.models.extrato_caixa import ExtratoCaixa
from src.domain.models.operador_caixa import OperadorCaixa
from src.domain.views.abrir_caixa.tela_abrir_caixa import TelaAbrirCaixa
from src.domain.views.tela_confirmacao import TelaConfirmacao


class ControladorAbrirCaixa:
    def __init__(self, controlador_sistema, caixa_dao: CaixaDAO, extrato_caixa_dao: ExtratoCaixaDAO) -> None:
        self.__tela_caixa = TelaAbrirCaixa()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__controlador_sistema = controlador_sistema
        self.__caixa_dao = caixa_dao
        self.__extrato_caixa_dao = extrato_caixa_dao

        self.__caixas = self.__load_caixas_fisicos()
        self.__data_abertura = datetime.datetime.now().strftime("%d/%m/%Y")

    def __load_caixas_fisicos(self):
        return self.__caixa_dao.get_all()

    def abre_tela(self, operador_caixa: OperadorCaixa):
        while True:
            try:
                if len(self.__caixas) == 0:
                    raise ListaVaziaException

                caixas_ids = list(map(lambda caixa: caixa.id, self.__caixas))

                self.__tela_caixa.init_components(caixas_ids, self.__data_abertura)
                result = self.__tela_caixa.open(self.__caixas)

                if result["option"] == 0 or result["values"] is None or sg.WIN_CLOSED:
                    self.__tela_confirmacao.init_components()
                    botao_confirmacao = self.__tela_confirmacao.open()
                    self.__tela_confirmacao.close()

                    if botao_confirmacao == 'confirmar':
                        return self.retornar()
                    continue

                result["values"]["saldo_abertura"] = result["saldo_abertura"]

                self.abrir_caixa(result["values"], operador_caixa)
                break
            except ListaVaziaException as v:
                self.__tela_caixa.show_message("Lista de caixas vazia", v)
                self.retornar()

    def abrir_caixa(self, values, operador_caixa: OperadorCaixa):
        if values is None:
            return

        filtered = list(filter(lambda caixa: caixa.id == values["caixa_id"], self.__caixas))
        if filtered is None:
            return

        caixa = filtered[0]
        caixa.operador_caixa = operador_caixa

        # Atualiza no banco o caixa com o operador associado
        self.__caixa_dao.update_entity(caixa.id, "cpf_operador", operador_caixa.cpf)

        # Atualiza na memória os caixas disponíveis para abertura
        self.__caixas = list(
                filter(lambda caixa: caixa.operador_caixa is None or caixa.operador_caixa.cpf != operador_caixa.cpf,
                       self.__caixas)
            )

        extrato = ExtratoCaixa(
            caixa,
            self.__data_abertura,
            values["saldo_abertura"],
            values["observacoes"]
        )

        # self.__extrato_caixa_dao.persist_entity(extrato)

    def retornar(self):
        self.__tela_caixa.close()
        self.__controlador_sistema.controllers["inicio"].abre_tela(True)
