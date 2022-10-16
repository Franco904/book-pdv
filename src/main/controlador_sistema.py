from src.data.dao.autenticacao_dao import AutenticacaoDAO
from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.extrato_caixa_dao import ExtratoCaixaDAO
from src.data.database.database import Database
from src.domain.controllers.controlador_abrir_caixa import ControladorAbrirCaixa
from src.domain.controllers.controlador_autenticacao import ControladorAutenticacao
from src.domain.controllers.controlador_funcionarios import ControladorFuncionarios
from src.domain.controllers.controlador_inicio import ControladorInicio
from src.domain.models.caixa import Caixa
from src.data.dao.funcionario_dao import FuncionarioDAO
from src.domain.models.funcionario import Funcionario
from src.main.tela_home import TelaHome
import PySimpleGUI as sg


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
        self.init_controladores()

    def init_sistema(self) -> None:
        self.init_database()
        self.init_daos()
        # self.init_inserts()
        self.init_controlador_autenticacao()
        self.abrir_tela_home()

    def init_database(self) -> None:
        # Cria instância global do banco de dados
        self.__database = Database()

    def init_daos(self) -> None:
        # Cria instâncias globais dos DAOs
        self.__daos = {
            "autenticacao_dao": AutenticacaoDAO(self.__database),
            "funcionario_dao": FuncionarioDAO(self.__database),
            "caixa_dao": CaixaDAO(self.__database),
            "extrato_caixa_dao": ExtratoCaixaDAO(self.__database),
        }

    def init_controlador_autenticacao(self) -> None:
        self.__controladores["autenticacao"] = ControladorAutenticacao(self, self.__daos["autenticacao_dao"])

    def init_controladores(self) -> None:
        # Cria instâncias globais dos controladores
        self.__controladores['funcionarios'] = ControladorFuncionarios(
            self.__daos["funcionario_dao"],
        )
        self.__controladores['abrir_caixa'] = ControladorAbrirCaixa(
            self.__daos["caixa_dao"],
            self.__daos['extrato_caixa_dao'],
            self.__funcionario_logado,
        ),
        self.__controladores["inicio"] = ControladorInicio(
            self,
            self.__controladores['funcionarios'],
            self.__controladores['abrir_caixa'],
            self.__daos['funcionario_dao'], self.__daos['caixa_dao'],
            self.__funcionario_logado,
        )

    def init_inserts(self) -> None:
        self.__daos['caixa_dao'].delete_all()
        self.__daos['caixa_dao'].persist_entity(Caixa(1))
        self.__daos['caixa_dao'].persist_entity(Caixa(2))
        self.__daos['caixa_dao'].persist_entity(Caixa(3))
        self.__daos['caixa_dao'].persist_entity(Caixa(4))
        self.__daos['caixa_dao'].persist_entity(Caixa(5))

    def entrar(self):
        self.__controladores['autenticacao'].abrir_tela_autenticacao()

    def fechar(self):
        exit(0)

    def abrir_tela_home(self):
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
