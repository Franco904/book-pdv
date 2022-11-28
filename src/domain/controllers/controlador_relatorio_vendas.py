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
        vendas_week_ago = self.__vendas_dao.get_all_by_period_with_products()
        vendas_2_weeks_ago = self.__vendas_dao.get_all_by_period_with_products(
            (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        )

        colunas = [
            'Código',
            'Data da venda',
            'Valor pago (R$)',
            'Valor de Troco (R$)',
            'Valor Total (R$)',
            'Observação da venda',
            'Nome do operador',
        ]

        parsed_vendas = self.__parse_vendas_to_show(vendas_week_ago)

        diff_registros = self.__get_diff_registros(vendas_week_ago, vendas_2_weeks_ago)
        diff_receita = self.__get_diff_receita(vendas_week_ago, vendas_2_weeks_ago)
        operador_com_mais_vendas = self.__vendas_dao.get_operador_with_more_vendas_by_period()

        return {
            'colunas': colunas,
            'lista': parsed_vendas,
            'diff_registros': diff_registros,
            'diff_receita': diff_receita,
            'operador_com_mais_vendas': operador_com_mais_vendas,
        }

    def __handle_filter_change(self, filtroIntervalo: str) -> None:
        data_inicio = None
        periodo_enum = FiltroRelatorioVendasIntervaloEnum.ultima_semana

        if filtroIntervalo == 'Última semana':
            data_inicio = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        elif filtroIntervalo == 'Último mês':
            data_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            periodo_enum = FiltroRelatorioVendasIntervaloEnum.ultimo_mes

        elif filtroIntervalo == 'Últimos 3 meses':
            data_inicio = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            periodo_enum = FiltroRelatorioVendasIntervaloEnum.ultimos_3_meses

        elif filtroIntervalo == 'Último ano':
            data_inicio = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            periodo_enum = FiltroRelatorioVendasIntervaloEnum.ultimo_ano

        elif filtroIntervalo == 'Últimos 5 anos':
            data_inicio = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')
            periodo_enum = FiltroRelatorioVendasIntervaloEnum.ultimos_5_anos

        vendas_this_period = self.__vendas_dao.get_all_by_period_with_products(filtroIntervalo=periodo_enum)
        vendas_last_period = self.__vendas_dao.get_all_by_period_with_products(data_inicio, periodo_enum)

        # Formata vendas para mostrar na tabela
        parsed_vendas = self.__parse_vendas_to_show(vendas_this_period)

        operador_com_mais_vendas = self.__vendas_dao.get_operador_with_more_vendas_by_period(filtroIntervalo=periodo_enum)

        diff_registros = self.__get_diff_registros(vendas_this_period, vendas_last_period)
        diff_receita = self.__get_diff_receita(vendas_this_period, vendas_last_period)

        self.__tela_relatorio_vendas.update_component('vendas_table', parsed_vendas)

        self.__tela_relatorio_vendas.update_component(
            'diff_registros',
            f'{"+" if diff_registros > 0 else ""} {diff_registros}',
        )
        self.__tela_relatorio_vendas.update_component(
            'diff_receita',
            f'{"+" if diff_receita > 0 else ""} R$ {round(diff_receita, 2)}',
        )

        self.__tela_relatorio_vendas.update_component(
            'operador_nome',
            operador_com_mais_vendas['nome'] if operador_com_mais_vendas['nome'] is not None else '-',
        )
        self.__tela_relatorio_vendas.update_component(
            'operador_total',
            f" R$ {operador_com_mais_vendas['total']}" if round(operador_com_mais_vendas['total'], 2) is not None else ' R$ 0.0',
        )

    def __parse_vendas_to_show(self, vendas: list) -> list:
        return [[
            venda.id,
            venda.data_horario.strftime("%d/%m/%Y, %H:%M"),
            venda.valor_pago,
            venda.valor_troco,
            venda.valor_total(),
            'Nenhuma observação' if venda.observacao is not None else venda.observacao,
            venda.funcionario.nome,
        ] for venda in vendas]

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
            'venda_produtos': self.abre_produtos_venda,
            'mais_vendidos': self.abre_mais_vendidos,
        }

        while True:
            dados_vendas = self.get_vendas()
            self.__tela_relatorio_vendas.init_components(dados_vendas)

            opcao_escolhida = self.__tela_relatorio_vendas.open(self.__handle_filter_change)

            if opcao_escolhida in ('voltar', None, sg.WIN_CLOSED):
                self.__tela_relatorio_vendas.close()
                break
            else:
                opcoes[opcao_escolhida]()
