from src.data.database.database import Database
from src.domain.controllers.controlador_abrir_caixa import ControladorAbrirCaixa
from src.domain.controllers.controlador_funcionarios import ControladorFuncionarios
from src.domain.controllers.controlador_inicio import ControladorInicio
from src.main.tela_sistema import TelaSistema


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
        self.init_views()
        self.init_presenters()
        self.init_system_view()

    def init_database(self):
        # Create database global instance
        self.__database = Database()
        self.__database.create()

    def init_daos(self):
        # Create daos global instances
        self.__daos = {}

    def init_views(self):
        # Create views global instances
        self.__views = {}

    def init_presenters(self):
        # Create presenters global instances
        self.__controllers = {
            "funcionarios": ControladorFuncionarios(self),
            "inicio": ControladorInicio(self),
            "caixa": ControladorAbrirCaixa(self),
        }

    def init_system_view(self):
        self.__tela_sistema = TelaSistema()

        options = {
            1: self.abre_inicio,
            2: self.abre_funcionarios,
            0: self.close_system
        }

        while True:
            try:
                options[self.__tela_sistema.show_options()]()
            except ValueError:
                self.__tela_sistema.show_message('Valores númericos devem ser inteiros!')

    def abre_inicio(self):
        # Move this to Login Controller later
        self.__controllers["inicio"].abre_tela(True)

    def abre_funcionarios(self):
        self.__controllers['funcionarios'].abre_tela()

    def close_system(self):
        self.__database.close()
        exit(0)
