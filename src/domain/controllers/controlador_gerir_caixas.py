from datetime import datetime

import PySimpleGUI as sg

from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.caixas_operadores_dao import CaixasOperadoresDAO
from src.domain.exceptions.caixas.caixa_ja_cadastrado_exception import CaixaJaCadastradoException
from src.domain.exceptions.lista_vazia_exception import ListaVaziaException
from src.domain.models.caixa import Caixa
from src.domain.views.gerir_caixa.tela_aberturas_caixa import TelaAberturasCaixa
from src.domain.views.gerir_caixa.tela_busca_caixa import TelaBuscarCaixa
from src.domain.views.gerir_caixa.tela_cadastro_caixa import TelaCadastroCaixa
from src.domain.views.gerir_caixa.tela_gerir_caixa import TelaGerirCaixas
from src.domain.views.shared.tela_confirmacao import TelaConfirmacao
from src.domain.views.shared.tela_movimentacoes_caixa import TelaMovimentacoesCaixa


class ControladorGerirCaixas:
    def __init__(
            self,
            caixa_dao: CaixaDAO,
            caixas_operadores_dao: CaixasOperadoresDAO,
    ) -> None:
        self.__caixa_dao = None
        self.__caixas_operadores_dao = None

        self.__tela_gerir_caixas = TelaGerirCaixas()
        self.__tela_cadastro_caixa = TelaCadastroCaixa()
        self.__tela_buscar_caixa = TelaBuscarCaixa()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__tela_movimentacoes_caixa = TelaMovimentacoesCaixa()
        self.__tela_aberturas_caixa = TelaAberturasCaixa()

        if isinstance(caixa_dao, CaixaDAO):
            self.__caixa_dao = caixa_dao
        if isinstance(caixas_operadores_dao, CaixasOperadoresDAO):
            self.__caixas_operadores_dao = caixas_operadores_dao

    def cadastrar_caixa(self) -> None:
        data_horario_criacao = datetime.now()

        self.__tela_cadastro_caixa.init_components(data_horario_criacao.strftime("%d/%m/%Y, %H:%M"))
        botao, dados = self.__tela_cadastro_caixa.open()

        if botao == 'enviar':
            try:
                if self.__caixa_dao.get_by_id(dados['id']) is not None:
                    raise CaixaJaCadastradoException(dados['id'])
                else:
                    caixa = Caixa(
                        dados['id'],
                        data_horario_criacao,
                        dados['saldo'],
                    )

                    self.__tela_cadastro_caixa.close()
                    self.__caixa_dao.persist_entity(caixa)
            except CaixaJaCadastradoException as c:
                self.__tela_cadastro_caixa.show_message('Caixa já cadastrado', c)
                self.__tela_cadastro_caixa.close()

    def inativar_caixa(self) -> None:
        self.__tela_buscar_caixa.init_components()
        botao_busca, id = self.__tela_buscar_caixa.open()

        if botao_busca == 'buscar' and id is not None and self.__caixa_dao.get_by_id(id) is not None:
            # Se encontrou o caixa -> Solicita confirmação:
            self.__tela_confirmacao.init_components()
            botao_confirmacao = self.__tela_confirmacao.open()
            self.__tela_confirmacao.close()

            if botao_confirmacao == 'confirmar':
                self.__caixa_dao.inactivate_entity(id)

    def abrir_aberturas_caixa(self) -> None:
        self.__tela_buscar_caixa.init_components()
        botao_busca, id = self.__tela_buscar_caixa.open()

        if botao_busca == 'buscar' and id is not None and self.__caixa_dao.get_by_id(id) is not None:
            while True:
                self.__tela_aberturas_caixa.init_components()

                opcao_escolhida = self.__tela_aberturas_caixa.open()
                if opcao_escolhida in ('voltar', None, sg.WIN_CLOSED):
                    self.__tela_aberturas_caixa.close()
                    break

    def abrir_movimentacoes_caixa(self) -> None:
        self.__tela_buscar_caixa.init_components()
        botao_busca, id = self.__tela_buscar_caixa.open()

        if botao_busca == 'buscar' and id is not None and self.__caixa_dao.get_by_id(id) is not None:
            while True:
                self.__tela_movimentacoes_caixa.init_components()

                opcao_escolhida = self.__tela_aberturas_caixa.open()
                if opcao_escolhida in ('voltar', None, sg.WIN_CLOSED):
                    self.__tela_aberturas_caixa.close()
                    break

    def abre_tela(self):
        opcoes = {
            'cadastrar': self.cadastrar_caixa,
            'inativar': self.inativar_caixa,
            'aberturas': self.abrir_aberturas_caixa,
            'movimentacoes': self.abrir_movimentacoes_caixa,
        }

        while True:
            self.__tela_gerir_caixas.init_components()
            opcao_escolhida = self.__tela_gerir_caixas.open()
            self.__tela_gerir_caixas.close()

            if opcao_escolhida == 'voltar' or opcao_escolhida is None or sg.WIN_CLOSED:
                self.__tela_gerir_caixas.close()
                break
            else:
                opcoes[opcao_escolhida]()
