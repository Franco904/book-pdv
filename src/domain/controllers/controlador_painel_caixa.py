import datetime

from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.caixas_operadores_dao import CaixasOperadoresDAO
from src.data.dao.sangrias_dao import SangriasDAO
from src.domain.models.caixa_operador import CaixaOperador
from src.domain.models.funcionario import Funcionario
from src.domain.views.painel_caixa.tela_fechar_caixa import TelaFecharCaixa
from src.domain.views.painel_caixa.tela_painel_caixa import TelaPainelCaixa
from src.domain.views.tela_confirmacao import TelaConfirmacao


class ControladorPainelCaixa:
    def __init__(
            self,
            controlador_sistema,
            caixa_dao: CaixaDAO,
            caixas_operadores_dao: CaixasOperadoresDAO,
            sangrias_dao: SangriasDAO,
            funcionario_logado: Funcionario,
    ) -> None:
        self.__tela_painel_caixa = TelaPainelCaixa()
        self.__tela_fechar_caixa = TelaFecharCaixa()
        self.__tela_confirmacao = TelaConfirmacao()

        self.__controlador_sistema = controlador_sistema
        self.__caixa_dao = None
        self.__caixas_operadores_dao = None
        self.__sangrias_dao = None

        self.__caixa_operador: CaixaOperador | None = None
        self.__funcionario_logado: Funcionario | None = None

        if isinstance(caixa_dao, CaixaDAO):
            self.__caixa_dao = caixa_dao
        if isinstance(caixas_operadores_dao, CaixasOperadoresDAO):
            self.__caixas_operadores_dao = caixas_operadores_dao
        if isinstance(sangrias_dao, SangriasDAO):
            self.__sangrias_dao = sangrias_dao
        if isinstance(funcionario_logado, Funcionario):
            self.__funcionario_logado = funcionario_logado

    def abrir_vendas(self) -> None:
        # Abre módulo de vendas
        pass

    def abrir_sangrias(self) -> None:
        # Abre módulo de sangrias
        pass

    def abrir_movimentacoes(self) -> None:
        # Abre visualização das movimentações do caixa (Novo caso de uso?)
        pass

    def fechar_caixa(self) -> None:
        dados_caixa = {
            'id_caixa': self.__caixa_operador.caixa.id,
            'data_horario_fechamento': datetime.datetime.now(),
            'saldo_fechamento': self.__caixas_operadores_dao.get_saldo_fechamento(
                self.__caixa_operador.caixa.id,
                self.__caixa_operador.saldo_abertura,
            )
        }

        while True:
            self.__tela_fechar_caixa.init_components(dados_caixa)
            opcao, dados_tela = self.__tela_fechar_caixa.open()
            self.__tela_fechar_caixa.open()

            if opcao == 'voltar':
                return self.__tela_fechar_caixa.close()

            elif opcao == 'fechar_caixa':
                self.__tela_confirmacao.init_components()
                botao_confirmacao = self.__tela_confirmacao.open()

                # self.__tela_confirmacao.close()

                if botao_confirmacao == 'confirmar':
                    self.__tela_fechar_caixa.close()

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

        # Adiciona observação de fechamento se houver
        if dados_tela['observacao_fechamento'] is not None:
            self.__caixas_operadores_dao.update_entity(self.__caixa_operador.id, 'observacao_fechamento',
                                                       dados_tela['observacao_fechamento'])

    def sair(self) -> None:
        self.__controlador_sistema.abrir_inicio()

    def abrir_tela(self, caixa_operador: CaixaOperador) -> None:
        self.__caixa_operador = caixa_operador

        opcoes = {
            'vendas': self.abrir_vendas,
            'sangrias': self.abrir_sangrias,
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
