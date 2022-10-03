import PySimpleGUI as sg
from view.tela_funcionarios import TelaFuncionarios

class ControladorFuncionarios():

    def __init__(self, controlador_sistema) -> None:
        self.__tela_funcionarios = TelaFuncionarios()
        self.__controlador_sistema = controlador_sistema


    @property
    def funcionarios(self):
        """
            Method to get all employees from db and its attributes, in order to 
            list them in a table.
        """        
        pass

    def cadastrar_funcionario(self):
        pass

    def listar_funcionarios(self):
        pass

    def alterar_funcionarios(self):
        pass

    def excluir_funcionarios(self):
        pass


    def retornar(self):
        self.__tela_funcionarios.close()

    def sair(self):
        exit(0)

    def abre_tela(self):
        opcoes = {1: self.cadastrar_funcionario, 2: self.listar_funcionarios,
                  3: self.alterar_funcionario, 4: self.excluir_funcionario,
                  5: self.voltar, 0: self.sair}

        while True:
            self.__tela_funcionarios.init_components()
            opcao_escolhida = self.__tela_funcionarios.tela_opcoes()
            self.__tela_funcionarios.close()

            if opcao_escolhida == 5 or opcao_escolhida == None or sg.WIN_CLOSED:
                self.__tela_funcionarios.close()
                break
            else:
                opcoes[opcao_escolhida]()