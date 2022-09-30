from src.data.database.database import Database
from src.main.system_view import SystemView


class SystemController:
    def __init__(self):
        self.__database = None
        self.__daos = {}
        self.__controllers = {}
        self.__views = {}
        self.__system_view = None

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
        self.__controllers = {}

    def init_system_view(self):
        self.__system_view = SystemView()

        options = {
            1: self.open_cadastro_usuario_view,
            2: self.open_login_view,
            0: self.close_system,
        }

        while True:
            try:
                options[self.__system_view.show_options()]()
            except ValueError:
                self.__system_view.show_message('Numeric values must be int')

    def open_cadastro_usuario_view(self):
        # self.__controllers['cadastro_usuario_controller'].open()
        pass

    def open_login_view(self):
        # self.__controllers['login_controller'].open()
        pass

    def close_system(self):
        self.__database.close()
        exit(0)
