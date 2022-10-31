import PySimpleGUI as sg
from src.data.dao.produto_dao import ProdutoDAO
from src.domain.views.produtos.tela_inicial_produtos import TelaIncialProdutos


class ControladorProdutos:
    def __init__(self, produto_dao: ProdutoDAO) -> None:
        self.__produto_dao = produto_dao
        self.__tela_inicial_produtos = TelaIncialProdutos()

    def iniciar_modulo_produtos(self):
        pass

    def cadastrar_produto(self) -> None:
        pass

    def aplicar_desconto(self) -> None:
        pass

    def alterar_produto(self) -> None:
        pass

    def excluir_produto(self) -> None:
        pass

    def voltar(self) -> None:
        pass

    def abre_tela(self):
        opcoes = {'cadastrar': self.cadastrar_produto, 'desconto': self.aplicar_desconto,
                  'alterar': self.alterar_produto, 'excluir': self.excluir_produto,
                  'voltar': self.voltar}

        while True:
            self.__tela_inicial_produtos.init_components()
            opcao_escolhida = self.__tela_inicial_produtos.open()

            if opcao_escolhida == 'voltar' or opcao_escolhida is None or sg.WIN_CLOSED:
                self.__tela_inicial_produtos.close()
                break
            else:
                opcoes[opcao_escolhida]()
