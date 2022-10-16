import datetime
import PySimpleGUI as sg

from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.extrato_caixa_dao import ExtratoCaixaDAO
from src.domain.models.extrato_caixa import ExtratoCaixa
from src.domain.models.funcionario import Funcionario
from src.domain.models.caixa import Caixa
from src.domain.views.abrir_caixa.tela_abrir_caixa import TelaAbrirCaixa
from src.domain.views.tela_confirmacao import TelaConfirmacao


class ControladorAbrirCaixa:
    def __init__(
            self,
            caixa_dao: CaixaDAO,
            extrato_caixa_dao: ExtratoCaixaDAO,
            funcionario_logado: Funcionario,
    ) -> None:
        self.__tela_caixa = TelaAbrirCaixa()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__caixa_dao = None
        self.__extrato_caixa_dao = None

        self.__data_abertura = datetime.datetime.now().strftime("%d/%m/%Y")
        self.__caixas = []
        self.__funcionario_logado = None

        if isinstance(caixa_dao, CaixaDAO):
            self.__caixa_dao = caixa_dao
        if isinstance(extrato_caixa_dao, ExtratoCaixaDAO):
            self.__extrato_caixa_dao = extrato_caixa_dao
        if isinstance(funcionario_logado, Funcionario):
            self.__funcionario_logado = funcionario_logado

    def __load_caixas_fisicos(self) -> [Caixa]:
        return self.__caixa_dao.get_all()

    def abre_tela(self) -> None:
        self.__caixas = self.__load_caixas_fisicos()

        while True:
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

            self.abrir_caixa(result["values"])
            break

    def abrir_caixa(self, values: {}) -> None:
        if values is None:
            return

        filtered = list(filter(lambda caixa: caixa.id == values["caixa_id"], self.__caixas))
        if filtered is None:
            return

        caixa: Caixa = filtered[0]
        caixa.operador_caixa = self.__funcionario_logado

        # Atualiza no banco o caixa com o operador associado
        self.__caixa_dao.update_entity(caixa.id, "cpf_operador", self.__funcionario_logado.cpf)

        # Atualiza na memória os caixas disponíveis para abertura
        self.__caixas = self.__load_caixas_fisicos()

        extrato = ExtratoCaixa(
            caixa,
            self.__data_abertura,
            values["saldo_abertura"],
            values["observacoes"]
        )

        self.__extrato_caixa_dao.persist_entity(extrato)

    def retornar(self) -> None:
        self.__tela_caixa.close()
