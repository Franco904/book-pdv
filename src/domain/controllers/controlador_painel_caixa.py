from src.data.dao.caixa_dao import CaixaDAO
from src.data.dao.caixas_operadores_dao import CaixasOperadoresDAO
from src.domain.models.caixa_operador import CaixaOperador
from src.domain.models.funcionario import Funcionario
from src.domain.views.painel_caixa.tela_painel_caixa import TelaPainelCaixa
from src.domain.views.tela_confirmacao import TelaConfirmacao


class ControladorPainelCaixa:
    def __init__(
            self,
            controlador_sistema,
            caixa_dao: CaixaDAO,
            caixas_operadores_dao: CaixasOperadoresDAO,
            funcionario_logado: Funcionario,
    ) -> None:
        self.__tela_painel_caixa = TelaPainelCaixa()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__controlador_sistema = controlador_sistema
        self.__caixa_dao = None
        self.__caixas_operadores_dao = None

        self.__caixa_operador = None
        self.__funcionario_logado = None

        if isinstance(caixa_dao, CaixaDAO):
            self.__caixa_dao = caixa_dao
        if isinstance(caixas_operadores_dao, CaixasOperadoresDAO):
            self.__caixas_operadores_dao = caixas_operadores_dao
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

    def fechar_caixa(self) -> bool:
        self.__tela_painel_caixa.close()

        self.__tela_confirmacao.init_components()
        botao_confirmacao = self.__tela_confirmacao.open()
        self.__tela_confirmacao.close()

        if botao_confirmacao == 'confirmar':
            self.__caixa_dao.update_entity(self.__caixa_operador.caixa.id, 'aberto', False)
            self.sair()
            return True

    def sair(self) -> None:
        self.__controlador_sistema.abrir_inicio()
        self.__tela_painel_caixa.close()

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
