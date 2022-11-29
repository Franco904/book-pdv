from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.funcionario_dao import FuncionarioDAO
from src.domain.controllers.controlador_abrir_caixa import ControladorAbrirCaixa
from src.domain.controllers.controlador_funcionarios import ControladorFuncionarios
from src.domain.controllers.controlador_gerir_caixas import ControladorGerirCaixas
from src.domain.controllers.controlador_produtos import ControladorProdutos
from src.domain.controllers.controlador_relatorio_vendas import ControladorRelatorioVendas
from src.domain.exceptions.lista_vazia_exception import ListaVaziaException
from src.domain.models.funcionario import Funcionario
from src.domain.views.inicio.tela_inicio import TelaInicio
from src.domain.views.shared.tela_confirmacao import TelaConfirmacao


class ControladorInicio:
    def __init__(
            self,
            controlador_sistema,
            controlador_funcionarios: ControladorFuncionarios,
            controlador_abrir_caixa: ControladorAbrirCaixa,
            controlador_gerir_caixas: ControladorGerirCaixas,
            controlador_produtos: ControladorProdutos,
            controlador_relatorio_vendas: ControladorRelatorioVendas,
            funcionario_dao: FuncionarioDAO,
            caixa_dao: CaixaDAO,
            funcionario_logado: Funcionario,
    ) -> None:
        self.__tela_inicio = TelaInicio()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__controlador_sistema = controlador_sistema
        self.__controlador_produtos = None
        self.__controlador_relatorio_vendas = None
        self.__controlador_funcionarios = None
        self.__controlador_abrir_caixa = None
        self.__controlador_gerir_caixas = None
        self.__funcionario_dao = None
        self.__caixa_dao = None
        self.__funcionario_logado = None

        if isinstance(controlador_funcionarios, ControladorFuncionarios):
            self.__controlador_funcionarios = controlador_funcionarios
        if isinstance(controlador_abrir_caixa, ControladorAbrirCaixa):
            self.__controlador_abrir_caixa = controlador_abrir_caixa
        if isinstance(controlador_gerir_caixas, ControladorGerirCaixas):
            self.__controlador_gerir_caixas = controlador_gerir_caixas
        if isinstance(controlador_produtos, ControladorProdutos):
            self.__controlador_produtos = controlador_produtos
        if isinstance(controlador_relatorio_vendas, ControladorRelatorioVendas):
            self.__controlador_relatorio_vendas = controlador_relatorio_vendas
        if isinstance(funcionario_dao, FuncionarioDAO):
            self.__funcionario_dao = funcionario_dao
        if isinstance(caixa_dao, CaixaDAO):
            self.__caixa_dao = caixa_dao
        if isinstance(funcionario_logado, Funcionario):
            self.__funcionario_logado = funcionario_logado

    def abrir_gerir_caixas(self) -> None:
        # Módulo de Gestão de Caixas
        self.__controlador_gerir_caixas.abre_tela()

    def abrir_relatorio_vendas(self) -> None:
        # Módulo de Relatório de Vendas
        self.__controlador_relatorio_vendas.abre_tela()

    def abrir_produtos(self) -> None:
        # Módulo de Produtos
        is_supervisor = self.__funcionario_logado.cargo == 'supervisor'
        self.__controlador_produtos.abre_tela(is_supervisor)

    def abrir_funcionarios(self) -> None:
        # Módulo de Funcionários
        self.__controlador_funcionarios.abre_tela()

    def abrir_novo_caixa(self) -> None:
        # Módulo de Abertura de Caixas
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

    def abrir_tela(self) -> None:
        opcoes_operador = {
            'produtos': self.abrir_produtos,
            'sair': self.sair,
            'novo': self.abrir_novo_caixa,
        }

        opcoes_supervisor = {
            'caixas': self.abrir_gerir_caixas,
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

            if opcao_escolhida == 'sair':
                self.__tela_confirmacao.init_components()
                botao_confirmacao = self.__tela_confirmacao.open()
                self.__tela_confirmacao.close()

                if botao_confirmacao == 'confirmar':
                    self.sair()
                    break
            elif opcao_escolhida is None:
                continue
            elif is_operador_caixa:
                opcoes_operador[opcao_escolhida]()
            else:
                opcoes_supervisor[opcao_escolhida]()
