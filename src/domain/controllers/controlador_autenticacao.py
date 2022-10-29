import bcrypt

from src.data.dao.autenticacao_dao import AutenticacaoDAO
from src.data.dao.caixas_operadores_dao import CaixasOperadoresDAO
from src.domain.exceptions.email_invalido_exception import EmailInvalidoException
from src.domain.exceptions.falha_login_exception import FalhaLoginException
from src.domain.exceptions.senha_atual_nao_correspondente_exception import SenhaAtualNaoCorrespondenteException
from src.domain.views.login.tela_autenticacao import TelaLogin
from src.domain.views.login.tela_cadastrar_senha import TelaCadastrarSenha
from src.domain.views.login.tela_inserir_senha import TelaInserirSenha


class ControladorAutenticacao:
    def __init__(
            self,
            controlador_sistema,
            autenticacao_dao: AutenticacaoDAO,
            caixas_operadores_dao: CaixasOperadoresDAO,
    ) -> None:
        self.__tela_autenticacao = TelaLogin()
        self.__tela_inserir_senha = TelaInserirSenha()
        self.__tela_cadastrar_senha = TelaCadastrarSenha()

        self.__autenticacao_dao = None
        self.__caixas_operadores_dao = None

        self.__controlador_sistema = controlador_sistema
        self.__funcionario = None

        if isinstance(autenticacao_dao, AutenticacaoDAO):
            self.__autenticacao_dao = autenticacao_dao
        if isinstance(caixas_operadores_dao, CaixasOperadoresDAO):
            self.__caixas_operadores_dao = caixas_operadores_dao

    def abrir_tela_autenticacao(self) -> None:
        self.__tela_autenticacao.init_components()
        opcao, dados = self.__tela_autenticacao.open()

        if opcao is not None:
            if opcao == 'login':
                self.tratar_senha(dados['email'])

    def tratar_senha(self, email_funcionario: str) -> None:
        self.__funcionario = self.__autenticacao_dao.get_by_email(email_funcionario)

        try:
            if self.__funcionario is None:
                raise EmailInvalidoException

            has_password = self.__funcionario.senha != ''

            if not has_password:
                self.abrir_cadastrar_senha(editando=False)

            logged = self.abrir_inserir_senha()

            if logged is not None:
                if logged:
                    # Defini o funcionário autenticado como o utilizador do sistema
                    # Inicializa demais controladores do sistema para uso contínuo
                    self.__controlador_sistema.funcionario_logado = self.__funcionario

                    self.__tela_inserir_senha.close()

                    # Redireciona o funcionário para a tela relativa ao seu cargo
                    self.redirecionar_para_tela()
                else:
                    raise FalhaLoginException

        except EmailInvalidoException as e:
            self.__tela_autenticacao.show_message("Email inválido", e)
            self.__tela_autenticacao.close()
        except FalhaLoginException as f:
            self.__tela_autenticacao.show_message("Falha durante o login", f)
            self.__tela_autenticacao.close()

    def abrir_cadastrar_senha(self, editando: bool) -> None:
        while True:
            self.__tela_cadastrar_senha.init_components(editando)
            botao, dados = self.__tela_cadastrar_senha.open(editando)

            senha_atual = dados['senha_atual']
            senha_nova = dados['senha_nova']

            if botao == 'salvar':
                # Alteração de senha atual
                if editando:
                    try:
                        # Encripta a senha para comparação binária
                        senha_atual = senha_atual.encode('utf-8')
                        result = bcrypt.checkpw(senha_atual, self.__funcionario.senha.encode('ascii'))

                        if not result:
                            raise SenhaAtualNaoCorrespondenteException
                    except SenhaAtualNaoCorrespondenteException as s:
                        self.__tela_cadastrar_senha.show_message('Senha atual não é correspondente', s)
                        self.__tela_cadastrar_senha.close()
                        break

                # Definição de nova senha (criação/alteração)

                # Gera senha em formato binário
                bytes = senha_nova.encode('utf-8')
                salt = bcrypt.gensalt()
                hash_senha = bcrypt.hashpw(bytes, salt)

                # Atualiza no banco o funcionario com a nova senha na forma decodificada
                self.__autenticacao_dao.update_password(self.__funcionario.cpf, f"{hash_senha.decode('ascii')}")

                self.__tela_cadastrar_senha.close()

                # Redireciona o funcionário para a tela de inserção de senha (efetuar login)
                self.tratar_senha(self.__funcionario.email)
                break
            else:
                self.__tela_cadastrar_senha.close()
                break

    def abrir_inserir_senha(self) -> bool | None:
        self.__tela_inserir_senha.init_components()
        evento, dados = self.__tela_inserir_senha.open()

        senha = dados['senha']
        if evento == 'alterar_senha':
            self.abrir_cadastrar_senha(editando=True)

        if evento == 'login':
            # Encripta a senha para autenticação com comparação binária
            bytes = senha.encode('utf-8')
            result = bcrypt.checkpw(bytes, self.__funcionario.senha.encode('ascii'))

            return result

    def redirecionar_para_tela(self) -> None:
        caixa_operador_opened = self.__caixas_operadores_dao.get_caixa_opened_id(self.__funcionario.cpf)

        if caixa_operador_opened is None:
            self.__controlador_sistema.abrir_inicio()
        else:
            self.__controlador_sistema.abrir_painel_caixa(caixa_operador_opened)

    def retornar_home(self) -> None:
        self.__tela_autenticacao.close()
