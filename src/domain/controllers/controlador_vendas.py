import PySimpleGUI as sg

from src.data.dao.vendas_dao import VendasDAO
from src.domain.views.vendas.tela_cadastrar_venda import TelaCadastroVenda
from src.domain.views.vendas.tela_confirmacao_supervisor import TelaConfirmacaoSupervisor
from src.domain.views.vendas.tela_incluir_produto import TelaIncluirProduto
from src.domain.views.vendas.tela_inicial_vendas import TelaInicialVenda

class ControladorVendas:

    def __init__(self, controlador_sistema, vendas_dao: VendasDAO) -> None:
        self.__controlador_sistema = controlador_sistema
        self.__tela_inicial_vendas = TelaInicialVenda()
        self.__tela_incluir_produto = TelaIncluirProduto()
        self.__tela_confirmacao_supervisor = TelaConfirmacaoSupervisor()
        self.__tela_cadastrar_venda = TelaCadastroVenda()

        if isinstance(vendas_dao, VendasDAO):
            self.__vendas_dao = vendas_dao

    def cadastrar_venda(self):
        self.__tela_cadastrar_venda.init_components(alterar = False) #revisar
        botao_cadastro, valores = self.__tela_cadastrar_venda.open(alterar=False) #revisar

    def alterar_venda(self):
        pass

    def cancelar_venda(self):
        pass

    def voltar(self) -> None:
        self.__tela_inicial_vendas.close()
        self.__controlador_sistema.abrir_painel_caixa() #tem que passar como parametro o operador de caixa

    def abre_tela(self):
        opcoes = {'cadastrar': self.cadastrar_venda,
                  'alterar': self.alterar_venda, 'cancelar': self.cancelar_venda,
                  'voltar': self.voltar}

        while True:
            self.__tela_inicial_vendas.init_components()
            opcao_escolhida = self.__tela_inicial_vendas.open()
            self.__tela_inicial_vendas.close()

            if opcao_escolhida == 'voltar' or opcao_escolhida is None or sg.WIN_CLOSED:
                self.__tela_inicial_vendas.close()
                break
            else:
                opcoes[opcao_escolhida]()
