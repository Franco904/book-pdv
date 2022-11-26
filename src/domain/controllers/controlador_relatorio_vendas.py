from datetime import datetime, timedelta

import PySimpleGUI as sg
from src.data.dao.vendas_dao import VendasDAO
from src.domain.enums import FiltroRelatorioVendasIntervaloEnum
from src.domain.models.venda import Venda
from src.domain.views.relatorio_vendas.tela_mais_vendidos import TelaProdutosMaisVendidos
from src.domain.views.relatorio_vendas.tela_relatorio_vendas import TelaRelatorioVendas
from src.domain.views.relatorio_vendas.tela_venda_produtos import TelaVendaProdutos


class ControladorRelatorioVendas:
    def __init__(self, vendas_dao: VendasDAO) -> None:
        self.__vendas_dao = vendas_dao
        self.__tela_relatorio_vendas = TelaRelatorioVendas()
        self.__tela_venda_produtos = TelaVendaProdutos()
        self.__tela_produtos_mais_vendidos = TelaProdutosMaisVendidos()

    def get_vendas(self) -> dict:
        colunas = [
            'Código da venda',
            'Data',
            'Valor pago (R$)',
            'Valor de Troco (R$)',
            'Valor Total (R$)',
            'Observação da venda',
            'Nome do operador',
        ]

        vendas = self.__vendas_dao.get_all_with_products()

        vendas_week_ago = self.__vendas_dao.get_all_by_period_with_products()
        vendas_2_weeks_ago = self.__vendas_dao.get_all_by_period_with_products(
            f"'{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')}'"
        )

        diff_registros = self.__get_diff_registros(vendas_week_ago, vendas_2_weeks_ago)
        diff_receita = self.__get_diff_receita(vendas_week_ago, vendas_2_weeks_ago)
        operador_com_mais_vendas = self.__vendas_dao.get_operador_with_more_vendas_by_period()

        return {
            'colunas': colunas,
            'lista': vendas,
            'diff_registros': diff_registros,
            'diff_receita': diff_receita,
            'operador_com_mais_vendas': operador_com_mais_vendas,
        }

    def __handle_filter_change(self, filtroIntervalo: FiltroRelatorioVendasIntervaloEnum) -> None:
        pass

    def __get_diff_registros(self, vendas_this_period: [Venda], vendas_last_period: [Venda]) -> int:
        return len(vendas_this_period) - len(vendas_last_period)

    def __get_diff_receita(self, vendas_this_period: [Venda], vendas_last_period: [Venda]) -> int:
        receita_this_period = sum([v.valor_total() for v in vendas_this_period])
        receita_last_period = sum([v.valor_total() for v in vendas_last_period])

        return receita_this_period - receita_last_period

    def abre_produtos_venda(self) -> None:
        pass

    def abre_mais_vendidos(self) -> None:
        pass

    def abre_tela(self) -> None:
        opcoes = {
            'produtos_venda': self.abre_produtos_venda,
            'mais_vendidos': self.abre_mais_vendidos,
        }

        while True:
            dados_vendas = self.get_vendas()
            self.__tela_relatorio_vendas.init_components(dados_vendas, self.__handle_filter_change)

            opcao_escolhida = self.__tela_relatorio_vendas.open()

            if opcao_escolhida in ('voltar', None, sg.WIN_CLOSED):
                self.__tela_relatorio_vendas.close()
                break
            else:
                opcoes[opcao_escolhida]()
