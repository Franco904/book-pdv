import PySimpleGUI as sg

from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.funcionario_dao import FuncionarioDAO
from src.domain.exceptions.lista_vazia_exception import ListaVaziaException
from src.domain.views.inicio.tela_inicio import TelaInicio
from src.domain.views.tela_confirmacao import TelaConfirmacao


class ControladorInicio:
    def __init__(self, controlador_sistema, funcionario_dao: FuncionarioDAO, caixa_dao: CaixaDAO) -> None:
        self.__tela_inicio = TelaInicio()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__controlador_sistema = controlador_sistema
        self.__funcionario = None
        self.__funcionario_dao = None
        self.__caixa_dao = None

        if isinstance(funcionario_dao, FuncionarioDAO):
            self.__funcionario_dao = funcionario_dao
        if isinstance(caixa_dao, CaixaDAO):
            self.__caixa_dao = caixa_dao

    def abre_caixas_abertos(self):
        # Visualização dos dados dos caixas que foram abertos
        pass

    def abre_relatorios(self):
        # Visualização dos dados das vendas registradas
        pass

    def abre_produtos(self):
        # Visualização dos dados dos produtos registrados
        pass

    def abre_funcionarios(self):
        self.__controlador_sistema.controllers["funcionarios"].abre_tela()

    def abre_caixa(self):
        has_caixas_to_open = len(self.__caixa_dao.get_all()) > 0

        try:
            if not has_caixas_to_open:
                raise ListaVaziaException

            self.__controlador_sistema.controllers["abrir_caixa"].abre_tela(self.__funcionario)
        except ListaVaziaException as v:
            self.__tela_inicio.show_message("Lista de caixas vazia", v)
            self.retornar()

    def retornar(self):
        self.__tela_inicio.close()

    def abre_tela(self, cpf_funcionario):
        opcoes_operador = {
            1: self.abre_caixas_abertos,
            2: self.retornar,
            3: self.abre_caixa,
        }

        opcoes_supervisor = {
            1: self.abre_relatorios,
            2: self.abre_produtos,
            3: self.abre_funcionarios,
            4: self.retornar,
        }

        while True:
            self.__funcionario = self.__funcionario_dao.get_by_cpf(cpf_funcionario)
            is_operador_caixa = self.__funcionario.cargo == "operador_caixa"

            self.__tela_inicio.init_components(
                nome_funcionario=self.__funcionario.nome,
                cargo_funcionario=self.__funcionario.cargo
            )

            opcao_escolhida = self.__tela_inicio.open()

            if opcao_escolhida in (0, None, sg.WIN_CLOSED):
                self.__tela_confirmacao.init_components()
                botao_confirmacao = self.__tela_confirmacao.open()
                self.__tela_confirmacao.close()

                if botao_confirmacao == 'confirmar':
                    self.retornar()
                    break
            elif is_operador_caixa:
                opcoes_operador[opcao_escolhida]()
            else:
                opcoes_supervisor[opcao_escolhida]()
