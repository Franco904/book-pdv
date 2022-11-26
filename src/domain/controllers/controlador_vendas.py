import PySimpleGUI as sg
from src.domain.models.venda import Venda
from src.data.dao.vendas_dao import VendasDAO
from src.data.dao.vendas_produtos_dao import VendasProdutoDAO
from src.domain.views.tela_buscar_venda import TelaBuscaVenda
from src.domain.views.vendas.tela_cadastrar_venda import TelaCadastroVenda
from src.domain.views.vendas.tela_confirmacao_supervisor import TelaConfirmacaoSupervisor
from src.domain.views.vendas.tela_incluir_produto import TelaIncluirProduto
from src.domain.views.vendas.tela_inicial_vendas import TelaInicialVenda


class ControladorVendas:

    def __init__(self, vendas_dao: VendasDAO, vendas_produtos_dao: VendasProdutoDAO) -> None:
        self.__tela_inicial_vendas = TelaInicialVenda()
        self.__tela_incluir_produto = TelaIncluirProduto()
        self.__tela_confirmacao_supervisor = TelaConfirmacaoSupervisor()
        self.__tela_buscar_venda = TelaBuscaVenda()
        self.__tela_cadastrar_venda = TelaCadastroVenda()
        self.__vendas_dao = None
        self.__vendas_produtos_dao = None

        if isinstance(vendas_dao, VendasDAO):
            self.__vendas_dao = vendas_dao
        if isinstance(vendas_produtos_dao, VendasProdutoDAO):
            self.__vendas_produtos_dao = vendas_produtos_dao

    def cadastrar_venda(self):
        self.__tela_cadastrar_venda.init_components(alterar=False)  # revisar
        botao_cadastro, valores = self.__tela_cadastrar_venda.open(alterar=False)  # revisar

        if botao_cadastro == 'salvar':
            if valores is not None:
                venda = Venda(
                    valores['id'],
                    valores['id_caixa_operador'],
                    valores['data_horario'],
                    valores['valor_pago'],
                    valores['valor_troco'],
                    valores['observacao'],
                    valores['venda_produtos']
                )
                self.__vendas_dao.persist_entity(venda)
                self.__tela_cadastrar_venda.close()


    def alterar_venda(self):
        self.__tela_buscar_venda.init_components()
        botao_busca, id_venda = self.__tela_buscar_venda.open()
        self.__tela_buscar_venda.close()

        if botao_busca == 'buscar' and id_venda is not None:
            venda: Venda = self.__vendas_dao.get_by_id_with_products(id_venda)

        if venda is None:
            self.__tela_buscar_venda.show_message('Venda não encontrada',
                                                   'Não foi encontrada uma venda cadastrada com esse ID.')
        else:
            dados_venda = {

            }


    def cancelar_venda(self):
        pass

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
