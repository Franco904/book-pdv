from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.extrato_caixa_dao import ExtratoCaixaDAO
from src.data.database.database import Database
from src.domain.controllers.controlador_abrir_caixa import ControladorAbrirCaixa
from src.domain.controllers.controlador_funcionarios import ControladorFuncionarios
from src.domain.controllers.controlador_inicio import ControladorInicio
from src.domain.models.caixa import Caixa
from src.main.tela_sistema import TelaSistema
from src.data.dao.funcionario_dao import FuncionarioDAO


class ControladorSistema:
    def __init__(self):
        self.__database = None
        self.__daos = {}
        self.__controllers = {}
        self.__views = {}
        self.__tela_sistema = None

    @property
    def controllers(self):
        return self.__controllers

    def init_system(self):
        self.init_database()
        self.init_daos()
        self.init_inserts()
        self.init_views()
        self.init_controllers()
        self.init_system_view()

    def init_database(self):
        # Create database global instance
        self.__database = Database()

    def init_daos(self):
        # Create daos global instances
        self.__daos = {
            "funcionario_dao": FuncionarioDAO(self.__database),
            "caixa_dao": CaixaDAO(self.__database),
            "extrato_caixa_dao": ExtratoCaixaDAO(self.__database),
        }

    def init_views(self):
        # Create views global instances
        self.__views = {}

    def init_controllers(self):
        # Create controllers global instances
        self.__controllers = {
            "funcionarios": ControladorFuncionarios(self, self.__daos["funcionario_dao"]),
            "inicio": ControladorInicio(self),
            "abrir_caixa": ControladorAbrirCaixa(self, self.__daos["caixa_dao"], self.__daos["extrato_caixa_dao"]),
        }

    def init_inserts(self):
        self.__daos["caixa_dao"].delete_all()
        self.__daos["caixa_dao"].persist_entity(Caixa(1))
        self.__daos["caixa_dao"].persist_entity(Caixa(2))
        self.__daos["caixa_dao"].persist_entity(Caixa(3))

    def init_system_view(self):
        self.__tela_sistema = TelaSistema()

        options = {
            1: self.abre_funcionarios,
            2: self.abre_inicio,
            0: self.close_system
        }

        while True:
            try:
                options[self.__tela_sistema.show_options()]()
            except ValueError:
                self.__tela_sistema.show_message("Valores númericos devem ser inteiros!")

    def abre_funcionarios(self):
        self.__controllers["funcionarios"].abre_tela()

    # TODO: Mover método para controlador de login
    def abre_inicio(self):
        self.__controllers["inicio"].abre_tela()

    def close_system(self):
        self.__database.close()
        exit(0)
