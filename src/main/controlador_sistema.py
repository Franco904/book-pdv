import PySimpleGUI as sg

from src.data.dao.autenticacao_dao import AutenticacaoDAO
from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.caixas_operadores_dao import CaixasOperadoresDAO
from src.data.dao.cargos_dao import CargosDAO
from src.data.dao.funcionario_dao import FuncionarioDAO
from src.data.dao.produto_dao import ProdutoDAO
from src.data.dao.sangrias_dao import SangriasDAO
from src.data.dao.tipos_produto_dao import TiposProdutoDAO
from src.data.dao.vendas_dao import VendasDAO
from src.data.dao.vendas_produtos_dao import VendasProdutoDAO
from src.data.database.database import Database
from src.domain.controllers.controlador_abrir_caixa import ControladorAbrirCaixa
from src.domain.controllers.controlador_autenticacao import ControladorAutenticacao
from src.domain.controllers.controlador_funcionarios import ControladorFuncionarios
from src.domain.controllers.controlador_inicio import ControladorInicio
from src.domain.controllers.controlador_painel_caixa import ControladorPainelCaixa
from src.domain.controllers.controlador_produtos import ControladorProdutos
from src.domain.controllers.controlador_vendas import ControladorVendas
from src.domain.models.caixa_operador import CaixaOperador
from src.domain.models.funcionario import Funcionario
from src.main.tela_home import TelaHome


class ControladorSistema:
    def __init__(self):
        self.__database = None
        self.__daos = {}
        self.__controladores = {}
        self.__tela_home = TelaHome()
        self.__funcionario_logado = None

    @property
    def controladores(self) -> {}:
        return self.__controladores

    @property
    def funcionario_logado(self) -> Funcionario:
        return self.__funcionario_logado

    @funcionario_logado.setter
    def funcionario_logado(self, funcionario_logado: Funcionario) -> None:
        self.__funcionario_logado = funcionario_logado

        # Inicializa demais controladores se houver funcionário logado
        if self.__funcionario_logado is not None:
            self.init_controladores()

    def init_sistema(self) -> None:
        self.init_database()
        self.init_daos()
        # self.init_inserts()

        # Inicializa controlador de autenticação -> Abre tela Home
        self.init_controlador_autenticacao()
        self.abrir_tela_home()

    def init_database(self) -> None:
        # Cria instância global do banco de dados
        self.__database = Database()

    def init_daos(self) -> None:
        # Cria instâncias globais dos DAOs
        self.__daos = {
            'autenticacao_dao': AutenticacaoDAO(self.__database),
            'funcionario_dao': FuncionarioDAO(self.__database),
            'caixa_dao': CaixaDAO(self.__database),
            'caixas_operadores_dao': CaixasOperadoresDAO(self.__database),
            'sangrias_dao': SangriasDAO(self.__database),
            'cargos_dao': CargosDAO(self.__database),
            'tipos_produto_dao': TiposProdutoDAO(self.__database),
            'produto_dao': ProdutoDAO(self.__database),
            'vendas_dao': VendasDAO(self.__database),
            'vendas_produtos_dao': VendasProdutoDAO(self.__database)
        }

    def init_controlador_autenticacao(self) -> None:
        self.__controladores['autenticacao'] = ControladorAutenticacao(
            self,
            self.__daos['autenticacao_dao'],
            self.__daos['caixas_operadores_dao'],
        )

    def init_controladores(self) -> None:
        # Cria instâncias globais dos controladores
        self.__controladores['funcionarios'] = ControladorFuncionarios(
            self,
            self.__daos['funcionario_dao'],
            self.__funcionario_logado,
        )
        self.__controladores['vendas'] = ControladorVendas(
            self.__daos['vendas_dao'],
            self.__daos['vendas-produtos_dao'],
        )
        self.__controladores['painel_caixa'] = ControladorPainelCaixa(
            self,
            self.__daos["caixa_dao"],
            self.__daos['caixas_operadores_dao'],
            self.__daos['sangrias_dao'],
            self.__funcionario_logado,
        )
        self.__controladores['abrir_caixa'] = ControladorAbrirCaixa(
            self.__controladores['painel_caixa'],
            self.__daos["caixa_dao"],
            self.__daos['caixas_operadores_dao'],
            self.__funcionario_logado,
        )
        self.__controladores['produtos'] = ControladorProdutos(self.__daos['produto_dao'])
        self.__controladores["inicio"] = ControladorInicio(
            self,
            self.__controladores['funcionarios'],
            self.__controladores['abrir_caixa'],
            self.__controladores['produtos'],
            self.__daos['funcionario_dao'],
            self.__daos['caixa_dao'],
            self.__funcionario_logado,
        )

    def init_inserts(self) -> None:
        # self.__daos['cargos_dao'].persist_entity(CargoEnum.operador_caixa)
        # self.__daos['cargos_dao'].persist_entity(CargoEnum.supervisor)

        # self.__daos['tipos_produto_dao'].persist_entity(TipoProdutoEnum.livro)
        # self.__daos['tipos_produto_dao'].persist_entity(TipoProdutoEnum.eletronico)
        pass

    def entrar(self) -> None:
        self.__controladores['autenticacao'].abrir_tela_autenticacao()

    def fechar(self) -> None:
        exit(0)

    def abrir_tela_home(self) -> None:
        opcoes = {'entrar': self.entrar, 'fechar': self.fechar}
        while True:
            self.__tela_home.init_components()
            opcao_escolhida = self.__tela_home.open()
            self.__tela_home.close()

            if opcao_escolhida is None or sg.WIN_CLOSED:
                self.fechar()
                break
            else:
                opcoes[opcao_escolhida]()

    def abrir_inicio(self) -> None:
        self.__controladores['inicio'].abrir_tela()

    def abrir_painel_caixa(self, caixa_operador: CaixaOperador) -> None:
        self.__controladores['painel_caixa'].abrir_tela(caixa_operador)
