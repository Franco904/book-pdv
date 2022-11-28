from datetime import datetime, timedelta

import PySimpleGUI as sg

from src.data.dao.produto_dao import ProdutoDAO
from src.data.dao.vendas_dao import VendasDAO
from src.domain.enums import FiltroRelatorioVendasIntervaloEnum
from src.domain.exceptions.vendas.venda_nao_encontrada_exception import VendaNaoEncontradaException
from src.domain.models.produto_relatorio import ProdutoRelatorio
from src.domain.models.venda import Venda
from src.domain.models.venda_produtos import VendaProduto
from src.domain.views.relatorio_vendas.tela_mais_vendidos import TelaProdutosMaisVendidos
from src.domain.views.relatorio_vendas.tela_relatorio_vendas import TelaRelatorioVendas
from src.domain.views.relatorio_vendas.tela_venda_produtos import TelaVendaProdutos
from src.domain.views.tela_buscar_venda import TelaBuscaVenda


class ControladorRelatorioVendas:
    def __init__(self, vendas_dao: VendasDAO, produto_dao: ProdutoDAO) -> None:
        self.__vendas_dao = vendas_dao
        self.__produto_dao = produto_dao

        self.__tela_relatorio_vendas = TelaRelatorioVendas()
        self.__tela_venda_produtos = TelaVendaProdutos()
        self.__tela_produtos_mais_vendidos = TelaProdutosMaisVendidos()
        self.__tela_buscar_venda = TelaBuscaVenda()

        self.__current_filter = FiltroRelatorioVendasIntervaloEnum.ultima_semana

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
        self.__current_filter = FiltroRelatorioVendasIntervaloEnum.ultima_semana

        if filtroIntervalo == 'Última semana':
            data_inicio = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        elif filtroIntervalo == 'Último mês':
            data_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            self.__current_filter = FiltroRelatorioVendasIntervaloEnum.ultimo_mes

        elif filtroIntervalo == 'Últimos 3 meses':
            data_inicio = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            self.__current_filter = FiltroRelatorioVendasIntervaloEnum.ultimos_3_meses

        elif filtroIntervalo == 'Último ano':
            data_inicio = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            self.__current_filter = FiltroRelatorioVendasIntervaloEnum.ultimo_ano

        elif filtroIntervalo == 'Últimos 5 anos':
            data_inicio = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')
            self.__current_filter = FiltroRelatorioVendasIntervaloEnum.ultimos_5_anos

        vendas_this_period = self.__vendas_dao.get_all_by_period_with_products(filtroIntervalo=self.__current_filter)
        vendas_last_period = self.__vendas_dao.get_all_by_period_with_products(data_inicio, self.__current_filter)

        # Formata vendas para mostrar na tabela
        parsed_vendas = self.__parse_vendas_to_show(vendas_this_period)

        operador_com_mais_vendas = self.__vendas_dao.get_operador_with_more_vendas_by_period(filtroIntervalo=self.__current_filter)

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

    def abre_produtos_venda(self) -> None:
        self.__tela_buscar_venda.init_components()
        botao_busca, id_venda = self.__tela_buscar_venda.open()
        self.__tela_buscar_venda.close()

        if botao_busca == 'buscar' and id_venda is not None:
            venda: Venda = self.__vendas_dao.get_by_id_with_products(id_venda)

            try:
                if venda is None:
                    raise VendaNaoEncontradaException

                colunas = ['Código', 'Título', 'Descrição', 'Preço (R$)', 'Quantidade']
                parsed_produtos_venda = self.__parse_produtos_venda_to_show(venda.venda_produtos)

                while True:
                    self.__tela_venda_produtos.init_components({
                            'colunas': colunas,
                            'lista': parsed_produtos_venda,
                            'id_venda': venda.id,
                    })

                    opcao_escolhida = self.__tela_venda_produtos.open()
                    if opcao_escolhida in ('voltar', None, sg.WIN_CLOSED):
                        self.__tela_venda_produtos.close()
                        break

            except VendaNaoEncontradaException as v:
                self.__tela_buscar_venda.show_message('Venda não encontrada', v)

    def abre_mais_vendidos(self) -> None:
        colunas = ['Código', 'Título', 'Descrição', 'Receita Total (R$)', 'Quantidade']

        produtos: [ProdutoRelatorio] = self.__produto_dao.get_most_sold_in_period(filtroIntervalo=self.__current_filter)
        parsed_produtos = self.__parse_produtos_mais_vendidos_to_show(produtos)

        percentual_livros = (len([p for p in produtos if p.id_tipo_produto == 0]) / len(produtos)) * 100
        percentual_eletronicos = (len([p for p in produtos if p.id_tipo_produto == 1]) / len(produtos)) * 100

        while True:
            self.__tela_produtos_mais_vendidos.init_components({
                'colunas': colunas,
                'lista': parsed_produtos,
                'percentual_livros': round(percentual_livros, 2),
                'percentual_eletronicos': round(percentual_eletronicos, 2),
            })

            opcao_escolhida = self.__tela_produtos_mais_vendidos.open()
            if opcao_escolhida in ('voltar', None, sg.WIN_CLOSED):
                self.__tela_produtos_mais_vendidos.close()
                break

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

    def __parse_vendas_to_show(self, vendas: list) -> list:
        return [[
            venda.id,
            venda.data_horario.strftime("%d/%m/%Y, %H:%M"),
            round(venda.valor_pago, 2),
            round(venda.valor_troco, 2),
            round(venda.valor_total(), 2),
            'Nenhuma observação' if venda.observacao is not None else venda.observacao,
            venda.funcionario.nome,
        ] for venda in vendas]

    def __parse_produtos_venda_to_show(self, venda_produtos: [VendaProduto]) -> list:
        return [[
            venda_produto.produto.id_produto,
            venda_produto.produto.titulo,
            venda_produto.produto.descricao,
            round(venda_produto.produto.preco_final, 2),
            venda_produto.quantidade,
        ] for venda_produto in venda_produtos]

    def __parse_produtos_mais_vendidos_to_show(self, produtos: [ProdutoRelatorio]) -> list:
        return [[
            produto.id_produto,
            produto.titulo,
            produto.descricao,
            round(produto.receita_total, 2),
            produto.quantidade,
        ] for produto in produtos]

    def __get_diff_registros(self, vendas_this_period: [Venda], vendas_last_period: [Venda]) -> int:
        return len(vendas_this_period) - len(vendas_last_period)

    def __get_diff_receita(self, vendas_this_period: [Venda], vendas_last_period: [Venda]) -> int:
        receita_this_period = sum([v.valor_total() for v in vendas_this_period])
        receita_last_period = sum([v.valor_total() for v in vendas_last_period])

        return receita_this_period - receita_last_period
