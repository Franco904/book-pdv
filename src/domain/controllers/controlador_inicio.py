import PySimpleGUI as sg

from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.funcionario_dao import FuncionarioDAO
from src.domain.controllers.controlador_abrir_caixa import ControladorAbrirCaixa
from src.domain.controllers.controlador_funcionarios import ControladorFuncionarios
from src.domain.exceptions.lista_vazia_exception import ListaVaziaException
from src.domain.models.funcionario import Funcionario
from src.domain.views.inicio.tela_inicio import TelaInicio
from src.domain.views.tela_confirmacao import TelaConfirmacao


class ControladorInicio:
    def __init__(
            self,
            controlador_sistema,
            controlador_funcionarios: ControladorFuncionarios,
            controlador_abrir_caixa: ControladorAbrirCaixa,
            funcionario_dao: FuncionarioDAO,
            caixa_dao: CaixaDAO,
            funcionario_logado: Funcionario,
    ) -> None:
        self.__tela_inicio = TelaInicio()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__controlador_sistema = controlador_sistema
        self.__controlador_funcionarios = None
        self.__controlador_abrir_caixa = None
        self.__funcionario_dao = None
        self.__caixa_dao = None
        self.__funcionario_logado = None

        if isinstance(controlador_funcionarios, ControladorFuncionarios):
            self.__controlador_funcionarios = controlador_funcionarios
        if isinstance(controlador_abrir_caixa, ControladorAbrirCaixa):
            self.__controlador_abrir_caixa = controlador_abrir_caixa
        if isinstance(funcionario_dao, FuncionarioDAO):
            self.__funcionario_dao = funcionario_dao
        if isinstance(caixa_dao, CaixaDAO):
            self.__caixa_dao = caixa_dao
        if isinstance(funcionario_logado, Funcionario):
            self.__funcionario_logado = funcionario_logado

    def abrir_caixas(self) -> None:
        # Cadastro de caixas físicos e visualização do histórico de aberturas
        pass

    def abrir_relatorio_vendas(self) -> None:
        # Visualização dos dados das vendas registradas
        pass

    def abrir_produtos(self) -> None:
        # Visualização dos dados dos produtos registrados (Operador) ou Módulo de produtos (Supervisor)
        pass

    def abrir_funcionarios(self) -> None:
        self.__controlador_funcionarios.abre_tela()

    def abrir_novo_caixa(self) -> None:
        has_caixas_to_open = len(self.__caixa_dao.get_all()) > 0

        try:
            if not has_caixas_to_open:
                raise ListaVaziaException

            # Redireciona para a tela de abertura de caixa com as opções de caixas disponíveis
            self.__controlador_abrir_caixa.abrir_tela()
        except ListaVaziaException as v:
            self.__tela_inicio.show_message("Lista de caixas vazia", v)
            self.__tela_inicio.close()

    def sair(self) -> None:
        self.__controlador_sistema.funcionario_logado = None
        self.__tela_inicio.close()

    def abrir_tela(self) -> None:
        opcoes_operador = {
            'produtos': self.abrir_produtos,
            'sair': self.sair,
            'novo': self.abrir_novo_caixa,
        }

        opcoes_supervisor = {
            'caixas': self.abrir_caixas,
            'relatorio_vendas': self.abrir_relatorio_vendas,
            'produtos': self.abrir_produtos,
            'funcionarios': self.abrir_funcionarios,
            'sair': self.sair,
        }

        while True:
            is_operador_caixa = self.__funcionario_logado.cargo == 'operador_caixa'

            # Inicializa componentes de início conforme o cargo do funcionário
            self.__tela_inicio.init_components(
                nome_funcionario=self.__funcionario_logado.nome,
                is_operador=is_operador_caixa,
            )

            opcao_escolhida = self.__tela_inicio.open()

            if opcao_escolhida in ('sair', None, sg.WIN_CLOSED):
                self.__tela_confirmacao.init_components()
                botao_confirmacao = self.__tela_confirmacao.open()
                self.__tela_confirmacao.close()

                if botao_confirmacao == 'confirmar':
                    self.sair()
                    break
            elif is_operador_caixa:
                opcoes_operador[opcao_escolhida]()
            else:
                opcoes_supervisor[opcao_escolhida]()
