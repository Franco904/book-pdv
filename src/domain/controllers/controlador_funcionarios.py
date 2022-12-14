import PySimpleGUI as sg

from src.data.dao.funcionario_dao import FuncionarioDAO
from src.domain.exceptions.cpf_ja_cadastrado_exception import CPFJaCadastradoException
from src.domain.exceptions.excluir_funcionario_caixa_aberto_exception import ExcluirFuncionarioCaixaAbertoException
from src.domain.exceptions.excluir_funcionario_logado_exception import ExcluirFuncionarioLogadoException
from src.domain.exceptions.lista_vazia_exception import ListaVaziaException
from src.domain.models.funcionario import Funcionario
from src.domain.models.operador_caixa import OperadorCaixa
from src.domain.models.supervisor import Supervisor
from src.domain.views.funcionarios.tela_busca_funcionario import TelaBuscaFuncionario
from src.domain.views.funcionarios.tela_cadastrar_funcionario import TelaCadastroFuncionario
from src.domain.views.funcionarios.tela_funcionarios import TelaFuncionarios
from src.domain.views.shared.tela_confirmacao import TelaConfirmacao
from src.domain.views.shared.tela_lista_entidades import TelaListaEntidades


class ControladorFuncionarios:
    def __init__(
            self,
            controlador_sistema,
            funcionario_dao: FuncionarioDAO,
            funcionario_logado: Funcionario,
    ) -> None:
        self.__controlador_sistema = controlador_sistema
        self.__tela_funcionarios = TelaFuncionarios()
        self.__tela_cadastro_funcionario = TelaCadastroFuncionario()
        self.__tela_busca_funcionario = TelaBuscaFuncionario()
        self.__tela_confirmacao = TelaConfirmacao()
        self.__tela_lista_entidades = TelaListaEntidades()

        if isinstance(funcionario_dao, FuncionarioDAO):
            self.__funcionario_dao = funcionario_dao
        if isinstance(funcionario_logado, Funcionario):
            self.__funcionario_logado = funcionario_logado

    def cadastrar_funcionario(self) -> None:
        self.__tela_cadastro_funcionario.init_components()
        botao, dados = self.__tela_cadastro_funcionario.open()

        if botao == 'enviar':
            try:
                if self.__funcionario_dao.get_by_cpf(dados['cpf']) is not None:
                    raise CPFJaCadastradoException(dados['cpf'])
                else:
                    if dados['cargo'] == 'supervisor':
                        funcionario = Supervisor(
                            dados['nome'],
                            dados['cpf'],
                            dados['email'],
                            dados['telefone'],
                            ''
                        )
                    else:
                        funcionario = OperadorCaixa(
                            dados['nome'],
                            dados['cpf'],
                            dados['email'],
                            dados['telefone'],
                            ''
                        )
                    self.__tela_cadastro_funcionario.close()
                    self.__funcionario_dao.persist_entity(funcionario)
            except CPFJaCadastradoException as c:
                self.__tela_cadastro_funcionario.show_message('CPF j?? cadastrado', c)
                self.__tela_cadastro_funcionario.close()

    def listar_funcionarios(self) -> None:
        try:
            funcionarios: [Funcionario] = self.__funcionario_dao.get_all()
            if len(funcionarios) == 0:
                raise ListaVaziaException
            lista_funcionarios = []
            for funcionario in funcionarios:
                funcionario.cargo = ' '.join([word.capitalize() for word in funcionario.cargo.split(
                    '_')]) if 'operador' in funcionario.cargo else funcionario.cargo.capitalize()
                funcionario.cpf = funcionario.cpf[:3] + '.' + funcionario.cpf[3:6] + '.' + funcionario.cpf[6:9] + '-' + funcionario.cpf[9:11]

                lista_funcionarios.append(
                    [funcionario.nome, funcionario.telefone, funcionario.cargo, funcionario.email, funcionario.cpf])

            nomes_colunas = ['Nome', 'Telefone', 'Cargo', 'E-mail', 'CPF']

            self.__tela_lista_entidades.init_components(lista_funcionarios, nomes_colunas, 'Lista de funcionarios')
            self.__tela_lista_entidades.open()
        except ListaVaziaException as v:
            self.__tela_funcionarios.show_message('Lista vazia!', v)

    def alterar_funcionario(self) -> None:
        self.__tela_busca_funcionario.init_components()
        botao_busca, cpf = self.__tela_busca_funcionario.open()

        if botao_busca == 'buscar' and cpf is not None:
            # Busca se o cpf existe no banco e ent??o abre tela para inser????o de novos dados (objeto com dados antigos)
            funcionario: Funcionario = self.__funcionario_dao.get_by_cpf(cpf)

            if funcionario is None:
                self.__tela_busca_funcionario.show_message('Funcion??rio n??o encontrado',
                                                           'N??o foi encontrado um funcion??rio cadastrado com esse CPF.')
            else:
                dados_funcionario = [funcionario.nome, funcionario.cpf, funcionario.email, funcionario.telefone]
                self.__tela_cadastro_funcionario.init_components(alterar=True, dados_funcionario=dados_funcionario)
                botao_cadastro, novos_dados = self.__tela_cadastro_funcionario.open(alterar=True)

                if botao_cadastro == 'enviar':
                    self.__tela_cadastro_funcionario.close()
                    self.__tela_confirmacao.init_components()
                    botao_confirmacao = self.__tela_confirmacao.open()
                    self.__tela_confirmacao.close()

                    if botao_confirmacao == 'confirmar':
                        if novos_dados['nome'] != dados_funcionario[0]:
                            self.__funcionario_dao.update_entity(dados_funcionario[1], 'nome', novos_dados['nome'])
                        if novos_dados['cpf'] != dados_funcionario[1]:
                            self.__funcionario_dao.update_entity(dados_funcionario[1], 'cpf', novos_dados['cpf'])
                        if novos_dados['email'] != dados_funcionario[2]:
                            self.__funcionario_dao.update_entity(dados_funcionario[1], 'email', novos_dados['email'])
                        if novos_dados['telefone'] != dados_funcionario[3]:
                            self.__funcionario_dao.update_entity(dados_funcionario[1], 'telefone', novos_dados['telefone'])

                        self.__controlador_sistema.funcionario_logado = funcionario.copy_with(
                            nome=novos_dados['nome'],
                            cpf=novos_dados['cpf'],
                            email=novos_dados['email'],
                            telefone=novos_dados['telefone'],
                        )

    def excluir_funcionario(self) -> None:
        self.__tela_busca_funcionario.init_components()
        botao_busca, cpf = self.__tela_busca_funcionario.open()

        if botao_busca == 'buscar' and cpf is not None:
            try:
                if self.__funcionario_logado.cpf == cpf:
                    raise ExcluirFuncionarioLogadoException

                if self.__funcionario_dao.has_opened_caixa(cpf):
                    raise ExcluirFuncionarioCaixaAbertoException

                if self.__funcionario_dao.get_by_cpf(cpf) is not None:
                    # se encontrou o funcionario -> solicita confirmacao:
                    self.__tela_confirmacao.init_components()
                    botao_confirmacao = self.__tela_confirmacao.open()
                    self.__tela_confirmacao.close()

                    if botao_confirmacao == 'confirmar':
                        self.__funcionario_dao.delete_entity(cpf)

            except ExcluirFuncionarioLogadoException as e:
                self.__tela_funcionarios.show_message('Funcion??rio logado', e)
            except ExcluirFuncionarioCaixaAbertoException as e:
                self.__tela_funcionarios.show_message('Funcion??rio possui caixas abertos', e)

    def voltar(self) -> None:
        self.__tela_funcionarios.close()
        self.__controlador_sistema.abrir_inicio()

    def abre_tela(self):
        opcoes = {'cadastrar': self.cadastrar_funcionario, 'listar': self.listar_funcionarios,
                  'alterar': self.alterar_funcionario, 'excluir': self.excluir_funcionario,
                  'voltar': self.voltar}

        while True:
            self.__tela_funcionarios.init_components()
            opcao_escolhida = self.__tela_funcionarios.open()
            self.__tela_funcionarios.close()

            if opcao_escolhida == 'voltar' or opcao_escolhida is None or sg.WIN_CLOSED:
                self.__tela_funcionarios.close()
                break
            else:
                opcoes[opcao_escolhida]()
