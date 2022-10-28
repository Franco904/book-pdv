import datetime

import PySimpleGUI as sg

from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.caixas_operadores_dao import CaixasOperadoresDAO
from src.domain.enums import StatusCaixaAberto
from src.domain.models.caixa import Caixa
from src.domain.models.caixa_operador import CaixaOperador
from src.domain.models.funcionario import Funcionario
from src.domain.views.abrir_caixa.tela_abrir_caixa import TelaAbrirCaixa
from src.domain.views.tela_confirmacao import TelaConfirmacao


class ControladorAbrirCaixa:
    def __init__(
            self,
            caixa_dao: CaixaDAO,
            caixas_operadores_dao: CaixasOperadoresDAO,
            funcionario_logado: Funcionario,
    ) -> None:
        self.__tela_caixa = TelaAbrirCaixa()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__caixa_dao = None
        self.__caixas_operadores_dao = None

        self.__data_horario_abertura = datetime.datetime.now()
        self.__caixas = []
        self.__funcionario_logado = None

        if isinstance(caixa_dao, CaixaDAO):
            self.__caixa_dao = caixa_dao
        if isinstance(caixas_operadores_dao, CaixasOperadoresDAO):
            self.__caixas_operadores_dao = caixas_operadores_dao
        if isinstance(funcionario_logado, Funcionario):
            self.__funcionario_logado = funcionario_logado

    def __load_caixas_fisicos(self) -> [Caixa]:
        return self.__caixa_dao.get_all()

    def abrir_tela(self) -> None:
        self.__caixas = self.__load_caixas_fisicos()

        while True:
            caixas_ids = list(map(lambda caixa: caixa.id, self.__caixas))

            self.__tela_caixa.init_components(caixas_ids, self.__data_horario_abertura.strftime("%d/%m/%Y"))
            opcao, dados = self.__tela_caixa.open(self.__caixas)

            if opcao == 'voltar' or dados is None or sg.WIN_CLOSED:
                self.__tela_confirmacao.init_components()
                botao_confirmacao = self.__tela_confirmacao.open()
                self.__tela_confirmacao.close()

                if botao_confirmacao == 'confirmar':
                    return self.retornar()
                continue

            self.abrir_caixa(dados)
            break

    def abrir_caixa(self, dados: {}) -> None:
        if dados is None:
            return

        caixa_filtered = list(filter(lambda caixa: caixa.id == dados['caixa_id'], self.__caixas))
        if caixa_filtered is None:
            return

        caixa: Caixa = caixa_filtered[0]

        # Atualiza na memória os caixas disponíveis para abertura
        self.__caixas = self.__load_caixas_fisicos()

        caixa_operador = CaixaOperador(
            int(),
            caixa,
            self.__funcionario_logado,
            self.__data_horario_abertura,
            None,
            dados['saldo_abertura'],
            float(),
            StatusCaixaAberto.positivo,
            dados['observacoes'],
            '',
        )

        # Persiste no banco as informações do caixa no momento da abertura
        self.__caixas_operadores_dao.persist_entity(caixa_operador)

    def retornar(self) -> None:
        self.__tela_caixa.close()
