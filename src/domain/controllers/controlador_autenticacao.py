from src.data.dao.autenticacao_dao import AutenticacaoDAO
from src.domain.exceptions.email_invalido_exception import EmailInvalidoException
from src.domain.exceptions.falha_login_exception import FalhaLoginException
from src.domain.exceptions.senha_atual_nao_correspondente_exception import SenhaAtualNaoCorrespondenteException
from src.domain.views.login.tela_autenticacao import TelaLogin
from src.domain.views.login.tela_cadastrar_senha import TelaCadastrarSenha
from src.domain.views.login.tela_inserir_senha import TelaInserirSenha
from src.domain.models.funcionario import Funcionario
import bcrypt


class ControladorAutenticacao:
    def __init__(
            self,
            controlador_sistema,
            autenticacao_dao: AutenticacaoDAO
    ) -> None:
        self.__tela_autenticacao = TelaLogin()
        self.__tela_inserir_senha = TelaInserirSenha()
        self.__tela_cadastrar_senha = TelaCadastrarSenha()
        self.__controlador_sistema = None
        self.__autenticacao_dao = None
        self.__controlador_sistema = controlador_sistema

        if isinstance(autenticacao_dao, AutenticacaoDAO):
            self.__autenticacao_dao = autenticacao_dao

    def abrir_tela_autenticacao(self) -> None:
        self.__tela_autenticacao.init_components()
        opcao, dados = self.__tela_autenticacao.open()

        if opcao is not None:
            if opcao == 'login':
                self.tratar_senha(dados['email'])

    def tratar_senha(self, email_funcionario: str) -> None:
        funcionario = self.__autenticacao_dao.get_by_email(email_funcionario)

        try:
            if funcionario is None:
                raise EmailInvalidoException

            has_password = funcionario.senha != ''

            if not has_password:
                self.abrir_cadastrar_senha(funcionario, editando=False)

            logged = self.abrir_inserir_senha(funcionario)

            if logged is not None:
                if logged:
                    self.__controlador_sistema.funcionario_logado = funcionario
                    self.__tela_inserir_senha.close()
                    self.abrir_tela_inicio()
                else:
                    raise FalhaLoginException

        except EmailInvalidoException as e:
            self.__tela_autenticacao.show_message("Email inválido", e)
            self.__tela_autenticacao.close()
        except FalhaLoginException as f:
            self.__tela_autenticacao.show_message("Falha durante o login", f)
            self.__tela_autenticacao.close()

    def abrir_cadastrar_senha(self, funcionario: Funcionario, editando: bool) -> None:
        while True:
            self.__tela_cadastrar_senha.init_components(editando)
            botao, dados = self.__tela_cadastrar_senha.open(editando)

            senha_atual = dados['senha_atual']
            senha_nova = dados['senha_nova']

            if botao == 'salvar':
                if editando:
                    try:
                        senha_atual = senha_atual.encode('utf-8')
                        result = bcrypt.checkpw(senha_atual, funcionario.senha.encode('ascii'))

                        if not result:
                            raise SenhaAtualNaoCorrespondenteException
                    except SenhaAtualNaoCorrespondenteException as s:
                        self.__tela_cadastrar_senha.show_message('Senha atual não é correspondente', s)
                        self.__tela_cadastrar_senha.close()
                        break

                bytes = senha_nova.encode('utf-8')
                salt = bcrypt.gensalt()
                hash_senha = bcrypt.hashpw(bytes, salt)

                self.__autenticacao_dao.update_password(funcionario.cpf, f"{hash_senha.decode('ascii')}")
                self.__tela_cadastrar_senha.close()
                self.tratar_senha(funcionario.email)
                break
            else:
                self.__tela_cadastrar_senha.close()
                break

    def abrir_inserir_senha(self, funcionario: Funcionario) -> bool | None:
        self.__tela_inserir_senha.init_components()
        evento, dados = self.__tela_inserir_senha.open()

        senha = dados['senha']
        if evento == 'alterar_senha':
            self.abrir_cadastrar_senha(funcionario, editando=True)

        if evento == 'login':
            bytes = senha.encode('utf-8')
            result = bcrypt.checkpw(bytes, funcionario.senha.encode('ascii'))
            return result

    def abrir_tela_inicio(self) -> None:
        self.__controlador_sistema.abrir_inicio()

    def retornar_home(self) -> None:
        self.__tela_autenticacao.close()
