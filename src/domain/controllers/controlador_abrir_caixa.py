import datetime
from random import randint

import PySimpleGUI as sg

from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.caixas_operadores_dao import CaixasOperadoresDAO
from src.domain.controllers.controlador_painel_caixa import ControladorPainelCaixa
from src.domain.enums import StatusCaixaAberto
from src.domain.models.caixa import Caixa
from src.domain.models.caixa_operador import CaixaOperador
from src.domain.models.funcionario import Funcionario
from src.domain.views.abrir_caixa.tela_abrir_caixa import TelaAbrirCaixa
from src.domain.views.tela_confirmacao import TelaConfirmacao


class ControladorAbrirCaixa:
    def __init__(
            self,
            controlador_painel_caixa: ControladorPainelCaixa,
            caixa_dao: CaixaDAO,
            caixas_operadores_dao: CaixasOperadoresDAO,
            funcionario_logado: Funcionario,
    ) -> None:
        self.__tela_caixa = TelaAbrirCaixa()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__controlador_painel_caixa = None
        self.__caixa_dao = None
        self.__caixas_operadores_dao = None

        self.__data_horario_abertura = datetime.datetime.now()
        self.__caixas = []
        self.__funcionario_logado = None

        if isinstance(controlador_painel_caixa, ControladorPainelCaixa):
            self.__controlador_painel_caixa = controlador_painel_caixa
        if isinstance(caixa_dao, CaixaDAO):
            self.__caixa_dao = caixa_dao
        if isinstance(caixas_operadores_dao, CaixasOperadoresDAO):
            self.__caixas_operadores_dao = caixas_operadores_dao
        if isinstance(funcionario_logado, Funcionario):
            self.__funcionario_logado = funcionario_logado

    def __load_caixas_to_open(self) -> [Caixa]:
        return self.__caixa_dao.get_all_to_open()

    def abrir_tela(self) -> None:
        self.__caixas = self.__load_caixas_to_open()

        while True:
            caixas_ids = list(map(lambda caixa: caixa.id, self.__caixas))

            self.__tela_caixa.init_components(caixas_ids, self.__data_horario_abertura.strftime("%d/%m/%Y, %H:%M"))
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

        # Atualiza no banco o caixa aberto
        self.__caixa_dao.update_entity(caixa.id, 'aberto', True)

        # Atualiza na memória os caixas disponíveis para abertura
        self.__caixas = list(filter(lambda caixa: caixa.id != dados['caixa_id'], self.__caixas))

        caixa_operadores_ids = [co.id for co in self.__caixas_operadores_dao.get_all()]

        random_integers = [i for i in range(150)]
        chooseble_ids = [ri for ri in random_integers if ri not in caixa_operadores_ids]

        caixa_operador = CaixaOperador(
            randint(1, len(chooseble_ids) - 1),
            caixa,
            self.__funcionario_logado,
            self.__data_horario_abertura,
            None,
            caixa.saldo,
            float(),
            StatusCaixaAberto.positivo,
            dados['observacao_abertura'],
            '',
            '',
        )

        # Persiste no banco as informações do caixa no momento da abertura
        self.__caixas_operadores_dao.persist_entity(caixa_operador)

        # Redireciona operador de caixa para o painel do caixa
        self.__controlador_painel_caixa.abrir_tela(caixa_operador)

    def retornar(self) -> None:
        self.__tela_caixa.close()
