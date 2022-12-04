import datetime

import PySimpleGUI as sg

from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.caixas_operadores_dao import CaixasOperadoresDAO
from src.data.dao.sangrias_dao import SangriasDAO
from src.domain.controllers.controlador_vendas import ControladorVendas
from src.domain.models.caixa_operador import CaixaOperador
from src.domain.models.funcionario import Funcionario
from src.domain.models.movimentacao_caixa import MovimentacaoCaixa
from src.domain.views.painel_caixa.tela_fechar_caixa import TelaFecharCaixa
from src.domain.views.painel_caixa.tela_painel_caixa import TelaPainelCaixa
from src.domain.views.shared.tela_movimentacoes_caixa import TelaMovimentacoesCaixa
from src.domain.views.sangrias.tela_cadastrar_sangria import TelaCadastrarSangrias
from src.domain.views.shared.tela_confirmacao import TelaConfirmacao
from src.domain.models.sangria import Sangria


class ControladorPainelCaixa:
    def __init__(
            self,
            controlador_sistema,
            caixa_dao: CaixaDAO,
            caixas_operadores_dao: CaixasOperadoresDAO,
            sangrias_dao: SangriasDAO,
            funcionario_logado: Funcionario,
            controlador_vendas: ControladorVendas
    ) -> None:
        self.__tela_painel_caixa = TelaPainelCaixa()
        self.__tela_fechar_caixa = TelaFecharCaixa()
        self.__tela_movimentacoes_caixa = TelaMovimentacoesCaixa()
        self.__tela_sangrias = TelaCadastrarSangrias()
        self.__tela_confirmacao = TelaConfirmacao()

        self.__controlador_sistema = controlador_sistema
        self.__controlador_vendas = None

        self.__caixa_dao = None
        self.__caixas_operadores_dao = None
        self.__sangrias_dao = None

        self.__caixa_operador: CaixaOperador | None = None
        self.__funcionario_logado: Funcionario | None = None
        self.__movimentacoes_todas = []

        if isinstance(caixa_dao, CaixaDAO):
            self.__caixa_dao = caixa_dao
        if isinstance(caixas_operadores_dao, CaixasOperadoresDAO):
            self.__caixas_operadores_dao = caixas_operadores_dao
        if isinstance(sangrias_dao, SangriasDAO):
            self.__sangrias_dao = sangrias_dao
        if isinstance(funcionario_logado, Funcionario):
            self.__funcionario_logado = funcionario_logado
        if isinstance(controlador_vendas, ControladorVendas):
            self.__controlador_vendas = controlador_vendas

    def abrir_vendas(self) -> None:
        # Abre módulo de vendas
        self.__controlador_vendas.abre_tela()
        pass

    def realizar_sangrias(self) -> None:
        data_atual = datetime.datetime.now()
        data_string = data_atual.strftime("%Y-%m-%d %H:%M:%S")

        # Necessario buscar o saldo atualizado a cada sangria nova, por isso a query
        saldo_atual = self.__caixa_dao.get_by_id(self.__caixa_operador.caixa.id).saldo

        self.__tela_sangrias.init_components(data_string, saldo_atual)
        botao, valores = self.__tela_sangrias.open(saldo_atual)
        self.__tela_sangrias.close()

        if botao == 'enviar':
            if valores is not None:
                self.__tela_confirmacao.init_components()
                botao_confirmacao = self.__tela_confirmacao.open()
                self.__tela_confirmacao.close()
                if botao_confirmacao == 'confirmar':
                    new_id = self.__sangrias_dao.get_max_id() + 1
                    nova_sangria = Sangria(
                        new_id,
                        self.__caixa_operador.id,
                        data_string,
                        valores['valor_sangria'],
                        valores['observacao_sangria']
                    )

                    self.__sangrias_dao.persist_entity(nova_sangria)
                    novo_saldo = saldo_atual - valores['valor_sangria']
                    self.__caixa_dao.update_entity(self.__caixa_operador.caixa.id, 'saldo', novo_saldo)

    def abrir_movimentacoes(self) -> None:
        movimentacoes = self.__caixas_operadores_dao.get_movimentacoes_by_caixa_id(self.__caixa_operador.caixa.id)

        colunas = [
            'Tipo',
            'Código',
            'Data de fechamento',
            'Total movimentado (R$)',
            'Observação',
        ]

        self.__movimentacoes_todas = self.__parse_movimentacoes_to_show(movimentacoes)

        while True:
            self.__tela_movimentacoes_caixa.init_components({
                'colunas': colunas,
                'lista': self.__movimentacoes_todas,
            })

            opcao_escolhida = self.__tela_movimentacoes_caixa.open(self.__handle_movimentacao_filter_change)

            if opcao_escolhida in ('voltar', None, sg.WIN_CLOSED):
                self.__tela_movimentacoes_caixa.close()
                break

    def __handle_movimentacao_filter_change(self, filtroMovimentacao: str) -> None:
        if filtroMovimentacao == 'Todas':
            return self.__tela_movimentacoes_caixa.update_component('movimentacoes_table', self.__movimentacoes_todas)

        movimentacoes = self.__movimentacoes_todas
        movimentacoes_filtered = [m for m in movimentacoes if f'{m[0]}s' == filtroMovimentacao]

        self.__tela_movimentacoes_caixa.update_component('movimentacoes_table', movimentacoes_filtered)

    def fechar_caixa(self) -> bool | None:
        # Fechamento de caixa
        dados_caixa = {
            'id_caixa': self.__caixa_operador.caixa.id,
            'data_horario_fechamento': datetime.datetime.now(),
            'saldo_fechamento': round(self.__caixas_operadores_dao.get_saldo_fechamento(
                self.__caixa_operador.id,
                self.__caixa_operador.saldo_abertura,
            ), 2)
        }

        self.__tela_fechar_caixa.init_components(dados_caixa)

        while True:
            opcao, dados_tela = self.__tela_fechar_caixa.open()

            if opcao == 'fechar_caixa':
                botao_confirmacao = self.__tela_fechar_caixa.show_form_confirmation('Desejas fechar o caixa?', '')

                if botao_confirmacao == 'OK':
                    # Fecha o caixa
                    self.__caixa_dao.update_entity(self.__caixa_operador.caixa.id, 'aberto', False)

                    # Atualiza o saldo do caixa
                    if self.__caixa_operador.caixa.saldo != dados_caixa['saldo_fechamento']:
                        self.__caixa_dao.update_entity(self.__caixa_operador.caixa.id, 'saldo',
                                                       dados_caixa['saldo_fechamento'])

                    # Atualiza restante das propriedades do registro de caixa
                    self.persist_caixa_operador_data(dados_caixa, dados_tela)

                    # Redireciona para a tela de início
                    self.sair()
                    return True

            else:
                self.__tela_fechar_caixa.close()
                break

    def persist_caixa_operador_data(self, dados_caixa, dados_tela) -> None:
        # Atualiza data/horário de fechamento e saldo de fechamento
        self.__caixas_operadores_dao.update_entity(self.__caixa_operador.id, 'data_horario_fechamento',
                                                   dados_caixa['data_horario_fechamento'])
        self.__caixas_operadores_dao.update_entity(self.__caixa_operador.id, 'saldo_fechamento',
                                                   dados_caixa['saldo_fechamento'])

        # Atualiza o status para *negativo* caso o saldo de fechamento for menor que o saldo de
        # abertura e não houverem sangrias registradas
        num_sangrias_caixa = len(self.__sangrias_dao.get_all_by_caixa_operador(self.__caixa_operador.id))

        if dados_caixa['saldo_fechamento'] < self.__caixa_operador.saldo_abertura and num_sangrias_caixa == 0:
            self.__caixas_operadores_dao.update_entity(self.__caixa_operador.id, 'status', 'negativo')
            self.__caixas_operadores_dao.update_entity(
                self.__caixa_operador.id,
                'erros',
                'Caixa fechou com saldo menor do que o de abertura, mesmo sem ocorrerem retiradas de dinheiro',
            )

        # Adiciona observação de fechamento se houver
        if dados_tela['observacao_fechamento'] is not None:
            self.__caixas_operadores_dao.update_entity(self.__caixa_operador.id, 'observacao_fechamento',
                                                       dados_tela['observacao_fechamento'])

    def sair(self) -> None:
        self.__tela_fechar_caixa.close()
        self.__controlador_sistema.abrir_inicio()

    def abrir_tela(self, caixa_operador: CaixaOperador) -> None:
        self.__caixa_operador = caixa_operador

        opcoes = {
            'vendas': self.abrir_vendas,
            'sangrias': self.realizar_sangrias,
            'movimentacoes': self.abrir_movimentacoes,
            'fechar_caixa': self.fechar_caixa,
        }

        while True:
            self.__tela_painel_caixa.init_components(
                nome_operador=caixa_operador.operador_caixa.nome,
                id_caixa=caixa_operador.caixa.id,
            )

            # Passar esses parâmetros aqui não é a melhor abordagem, revisar depois!!!
            opcao_escolhida = self.__tela_painel_caixa.open(
                nome_operador=caixa_operador.operador_caixa.nome,
                id_caixa=caixa_operador.caixa.id,
            )
            saiu = opcoes[opcao_escolhida]()

            if saiu:
                break

    def __parse_movimentacoes_to_show(self, movimentacoes: [MovimentacaoCaixa]) -> list:
        return [[
            movimentacao.tipo,
            movimentacao.id,
            movimentacao.data_horario,
            round(movimentacao.movimentacao_total, 2),
            ' - ' if movimentacao.observacao in ('', None) else movimentacao.observacao,
        ] for movimentacao in movimentacoes]
