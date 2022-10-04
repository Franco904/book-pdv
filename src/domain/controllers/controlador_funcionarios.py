import PySimpleGUI as sg
from src.domain.views.funcionarios.tela_funcionarios import TelaFuncionarios
from src.domain.views.funcionarios.tela_cadastrar_funcionario import TelaCadastroFuncionario
from src.domain.views.funcionarios.tela_busca_funcionario import TelaBuscaFuncionario
from src.domain.views.tela_confirmacao import TelaConfirmacao
from src.domain.views.tela_lista_entidades import TelaListaEntidades


class ControladorFuncionarios:
    def __init__(self, controlador_sistema) -> None:
        self.__tela_funcionarios = TelaFuncionarios()
        self.__tela_cadastro_funcionario = TelaCadastroFuncionario()
        self.__tela_busca_funcionario = TelaBuscaFuncionario()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__tela_lista_entidades = TelaListaEntidades()
        self.__controlador_sistema = controlador_sistema

    @property
    def funcionarios(self):
        """
            Method to get all employees from db and its attributes, in order to 
            list them in a table.
        """
        pass

    def cadastrar_funcionario(self):
        self.__tela_cadastro_funcionario.init_components()
        botao, dados = self.__tela_cadastro_funcionario.tela_opcoes()
        # dados: {'nome': '', 'cpf': '', 'email': '', 'telefone': '', 'operador': True, 'supervisor': False}
        print(botao, dados)

    def listar_funcionarios(self):
        # verificar a existencia de funcionarios no banco, se sim:
        # trazer a lista de funcionarios e preparar uma tabela [] e o nome das colunas ['Coluna x', 'Coluna y']
        # abrir a tela de listagem de entidades com os parametros lista de funcionarios, colunas e o titulo
        self.__tela_lista_entidades.init_components([['Jorge', '12345678912'],['Paulo', '98798765432']], ['Nome', 'CPF'], 'Lista de funcionarios')
        botao = self.__tela_lista_entidades.open()
        print(botao)

    def alterar_funcionario(self):
        self.__tela_busca_funcionario.init_components()
        botao_busca, cpf = self.__tela_busca_funcionario.open()

        if botao_busca == 'buscar' and cpf is not None:
            #buscar se o cpf existe no banco e então abrir tela para inserçao de novos dados (objeto com dados antigos)
            self.__tela_cadastro_funcionario.init_components(alterar=True)
            botao_cadastro, novos_dados = self.__tela_cadastro_funcionario.tela_opcoes()

            if botao_cadastro == 'enviar':
                self.__tela_confirmacao.init_components()
                botao_confirmacao = self.__tela_confirmacao.open()
                self.__tela_confirmacao.close()
                if botao_confirmacao == 'confirmar':
                    # persistir dados
                    # dados: {'nome': '', 'cpf': '', 'email': '', 'telefone': '', 'operador': True, 'supervisor': False}
                    print(botao_cadastro, novos_dados)

    def excluir_funcionario(self):
        self.__tela_busca_funcionario.init_components()
        botao_busca, cpf = self.__tela_busca_funcionario.open()

        if botao_busca == 'buscar' and cpf is not None:
            # comando para buscar no banco a existencia de um funcionario com o cpf digitado

            # se encontrou o funcionario -> solicita confirmacao:
            self.__tela_confirmacao.init_components()
            botao_confirmacao = self.__tela_confirmacao.open()
            self.__tela_confirmacao.close()
            if botao_confirmacao == 'confirmar':
                # comando para deletar funcionario no banco
                print(cpf)

    def retornar(self):
        self.__tela_funcionarios.close()

    def sair(self):
        exit(0)

    def abre_tela(self):
        opcoes = {1: self.cadastrar_funcionario, 2: self.listar_funcionarios,
                  3: self.alterar_funcionario, 4: self.excluir_funcionario,
                  5: self.retornar, 0: self.sair}

        while True:
            self.__tela_funcionarios.init_components()
            opcao_escolhida = self.__tela_funcionarios.open()
            self.__tela_funcionarios.close()

            if opcao_escolhida == 5 or opcao_escolhida is None or sg.WIN_CLOSED:
                self.__tela_funcionarios.close()
                break
            else:
                opcoes[opcao_escolhida]()
