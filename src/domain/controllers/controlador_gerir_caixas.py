from datetime import datetime

import PySimpleGUI as sg

from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.caixas_operadores_dao import CaixasOperadoresDAO
from src.data.dao.funcionario_dao import FuncionarioDAO
from src.domain.enums import CargoEnum
from src.domain.exceptions.caixas.caixa_ativo_nao_encontrado_exception import CaixaAtivoNaoEncontradoException
from src.domain.exceptions.caixas.caixa_ja_cadastrado_exception import CaixaJaCadastradoException
from src.domain.exceptions.caixas.caixa_nao_encontrado_exception import CaixaNaoEncontradoException
from src.domain.exceptions.caixas.saldo_invalido_exception import SaldoInvalidoException
from src.domain.exceptions.codigo_invalido_exception import CodigoInvalidoException
from src.domain.models.caixa import Caixa
from src.domain.models.caixa_operador import CaixaOperador
from src.domain.models.funcionario import Funcionario
from src.domain.models.movimentacao_caixa import MovimentacaoCaixa
from src.domain.views.gerir_caixas.tela_aberturas_caixa import TelaAberturasCaixa
from src.domain.views.gerir_caixas.tela_busca_caixa import TelaBuscarCaixa
from src.domain.views.gerir_caixas.tela_cadastro_caixa import TelaCadastroCaixa
from src.domain.views.gerir_caixas.tela_gerir_caixas import TelaGerirCaixas
from src.domain.views.shared.tela_confirmacao import TelaConfirmacao
from src.domain.views.shared.tela_movimentacoes_caixa import TelaMovimentacoesCaixa


class ControladorGerirCaixas:
    def __init__(
            self,
            caixa_dao: CaixaDAO,
            caixas_operadores_dao: CaixasOperadoresDAO,
            funcionario_dao: FuncionarioDAO,
    ) -> None:
        self.__caixa_dao = None
        self.__caixas_operadores_dao = None
        self.__funcionario_dao = None

        self.__tela_gerir_caixas = TelaGerirCaixas()
        self.__tela_cadastro_caixa = TelaCadastroCaixa()
        self.__tela_buscar_caixa = TelaBuscarCaixa()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__tela_movimentacoes_caixa = TelaMovimentacoesCaixa()
        self.__tela_aberturas_caixa = TelaAberturasCaixa()

        self.__movimentacoes_todas = []

        if isinstance(caixa_dao, CaixaDAO):
            self.__caixa_dao = caixa_dao
        if isinstance(caixas_operadores_dao, CaixasOperadoresDAO):
            self.__caixas_operadores_dao = caixas_operadores_dao
        if isinstance(funcionario_dao, FuncionarioDAO):
            self.__funcionario_dao = funcionario_dao

    def cadastrar_caixa(self) -> None:
        data_horario_criacao = datetime.now()

        self.__tela_cadastro_caixa.init_components(data_horario_criacao.strftime("%d/%m/%Y, %H:%M"))
        botao, dados = self.__tela_cadastro_caixa.open()

        if botao == 'enviar':
            try:
                if not dados['id'].isnumeric():
                    raise CodigoInvalidoException('caixa')
                elif not dados['saldo'].isnumeric():
                    raise SaldoInvalidoException
                elif self.__caixa_dao.get_by_id(dados['id']) is not None:
                    raise CaixaJaCadastradoException(dados['id'])
                else:
                    caixa = Caixa(
                        int(dados['id']),
                        data_horario_criacao,
                        float(dados['saldo']),
                    )

                    self.__tela_cadastro_caixa.close()
                    self.__caixa_dao.persist_entity(caixa)
            except CodigoInvalidoException as c:
                self.__tela_cadastro_caixa.show_message('Código de caixa inválido', c)
                self.__tela_cadastro_caixa.close()
            except SaldoInvalidoException as s:
                self.__tela_cadastro_caixa.show_message('Saldo de caixa inválido', s)
                self.__tela_cadastro_caixa.close()
            except CaixaJaCadastradoException as c:
                self.__tela_cadastro_caixa.show_message('Caixa já foi cadastrado', c)
                self.__tela_cadastro_caixa.close()

    def inativar_caixa(self) -> None:
        self.__tela_buscar_caixa.init_components()
        botao_busca, id = self.__tela_buscar_caixa.open()
        self.__tela_buscar_caixa.close()

        if botao_busca == 'buscar' and id is not None:
            caixa: Caixa = self.__caixa_dao.get_ativo_by_id(id)

            try:
                if caixa is None:
                    raise CaixaAtivoNaoEncontradoException

                # Se encontrou o caixa -> Solicita confirmação:
                self.__tela_confirmacao.init_components()
                botao_confirmacao = self.__tela_confirmacao.open()
                self.__tela_confirmacao.close()

                if botao_confirmacao == 'confirmar':
                    self.__caixa_dao.inactivate_entity(id)
            except CaixaAtivoNaoEncontradoException as c:
                self.__tela_buscar_caixa.show_message('Caixa ativo não encontrado', c)

    def abrir_aberturas_caixa(self) -> None:
        self.__tela_buscar_caixa.init_components()
        botao_busca, id = self.__tela_buscar_caixa.open()
        self.__tela_buscar_caixa.close()

        if botao_busca == 'buscar' and id is not None:
            caixa: Caixa = self.__caixa_dao.get_by_id(id)

            try:
                if caixa is None:
                    raise CaixaNaoEncontradoException

                operadores = self.__funcionario_dao.get_all_by_cargo(CargoEnum.operador_caixa.value)
                caixa_operadores = self.__caixas_operadores_dao.get_all_by_caixa_id(id)

                filtros = ['Todos']
                filtros.extend([o.nome for o in operadores])

                colunas = [
                    'Data de abertura',
                    'Data de fechamento',
                    'Saldo de abertura (R$)',
                    'Saldo de fechamento (R$)',
                    'Status',
                    'Mensagem',
                    'Observação (abertura)',
                    'Observação (fechamento)',
                ]

                parsed_aberturas = self.__parse_aberturas_to_show(caixa_operadores)

                while True:
                    self.__tela_aberturas_caixa.init_components({
                        'filtros': filtros,
                        'colunas': colunas,
                        'lista': parsed_aberturas,
                    })

                    opcao_escolhida = self.__tela_aberturas_caixa.open(
                        self.__handle_operador_filter_change,
                        operadores,
                        id,
                    )

                    if opcao_escolhida in ('voltar', None, sg.WIN_CLOSED):
                        self.__tela_aberturas_caixa.close()
                        break
            except CaixaNaoEncontradoException as c:
                self.__tela_buscar_caixa.show_message('Caixa não encontrado', c)

    def __handle_operador_filter_change(self, filtroOperador: str, operadores: [Funcionario], id_caixa: int) -> None:
        operadores_filtered: [str | None] = [o.cpf for o in operadores if o.nome == filtroOperador]

        operador_cpf = operadores_filtered[0] if len(operadores_filtered) > 0 else None
        aberturas_operador = self.__caixas_operadores_dao.get_all_by_caixa_id_and_cpf(id_caixa, operador_cpf)

        # Formata aberturas de caixa do operador para mostrar na tabela
        parsed_aberturas = self.__parse_aberturas_to_show(aberturas_operador)

        self.__tela_aberturas_caixa.update_component('aberturas_table', parsed_aberturas)

    def abrir_movimentacoes_caixa(self) -> None:
        self.__tela_buscar_caixa.init_components()
        botao_busca, id = self.__tela_buscar_caixa.open()
        self.__tela_buscar_caixa.close()

        if botao_busca == 'buscar' and id is not None:
            caixa: Caixa = self.__caixa_dao.get_by_id(id)

            try:
                if caixa is None:
                    raise CaixaNaoEncontradoException

                movimentacoes = self.__caixas_operadores_dao.get_movimentacoes_by_caixa_id(id)

                colunas = [
                    'Tipo',
                    'Código',
                    'Data',
                    'Total movimentado (R$)',
                    'Observação',
                    'Operador',
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
            except CaixaNaoEncontradoException as c:
                self.__tela_buscar_caixa.show_message('Caixa não encontrado', c)

    def __handle_movimentacao_filter_change(self, filtroMovimentacao: str) -> None:
        if filtroMovimentacao == 'Todas':
            return self.__tela_movimentacoes_caixa.update_component('movimentacoes_table', self.__movimentacoes_todas)

        movimentacoes = self.__movimentacoes_todas
        movimentacoes_filtered = [m for m in movimentacoes if f'{m[0]}s' == filtroMovimentacao]

        self.__tela_movimentacoes_caixa.update_component('movimentacoes_table', movimentacoes_filtered)

    def abre_tela(self):
        opcoes = {
            'cadastrar': self.cadastrar_caixa,
            'inativar': self.inativar_caixa,
            'aberturas': self.abrir_aberturas_caixa,
            'movimentacoes': self.abrir_movimentacoes_caixa,
        }

        while True:
            self.__tela_gerir_caixas.init_components()
            opcao_escolhida = self.__tela_gerir_caixas.open()
            self.__tela_gerir_caixas.close()

            if opcao_escolhida == 'voltar' or opcao_escolhida is None or sg.WIN_CLOSED:
                self.__tela_gerir_caixas.close()
                break
            else:
                opcoes[opcao_escolhida]()

    def __parse_aberturas_to_show(self, caixa_operadores: [CaixaOperador]) -> list:
        return [[
            caixa_operador.data_horario_abertura.strftime("%d/%m/%Y, %H:%M"),
            ' - ' if caixa_operador.data_horario_fechamento is None
            else caixa_operador.data_horario_fechamento.strftime("%d/%m/%Y, %H:%M"),
            caixa_operador.saldo_abertura,
            ' - ' if caixa_operador.saldo_fechamento is None else caixa_operador.saldo_fechamento,
            caixa_operador.status,
            ' - ' if caixa_operador.erros in ('', None) else caixa_operador.erros,
            ' - ' if caixa_operador.observacao_abertura in ('', None) else caixa_operador.observacao_abertura,
            ' - ' if caixa_operador.observacao_fechamento in ('', None) else caixa_operador.observacao_fechamento,
        ] for caixa_operador in caixa_operadores]

    def __parse_movimentacoes_to_show(self, movimentacoes: [MovimentacaoCaixa]) -> list:
        return [[
            movimentacao.tipo,
            movimentacao.id,
            movimentacao.data_horario,
            round(movimentacao.movimentacao_total, 2),
            ' - ' if movimentacao.observacao in ('', None) else movimentacao.observacao,
            movimentacao.operador.nome,
        ] for movimentacao in movimentacoes]
