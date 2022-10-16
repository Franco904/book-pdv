from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
from src.domain.models.operador_caixa import OperadorCaixa
from src.domain.models.supervisor import Supervisor
from src.domain.models.funcionario import Funcionario


class AutenticacaoDAO(AbstractDAO):
    def __init__(self, database: Database) -> None:
        super().__init__(database, 'access_control', 'funcionarios')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    def execute_query(self, query: str):
        super().execute_query(query)

    def get_by_email(self, email: str) -> Funcionario | None:
        row = super().get_by_pk("email", email)

        funcionario = None if row is None else AutenticacaoDAO.__parse_funcionario(row)
        return funcionario

    def update_password(self, cpf: str, password) -> None:
        super().update("cpf", cpf, "senha", f"'{password}'")

    @staticmethod
    def __parse_funcionario(row) -> Funcionario | None:
        if row is None:
            return None

        if row["cargo"] == "operador_caixa":
            return AutenticacaoDAO.__parse_operador_caixa(row)

        elif row["cargo"] == "supervisor":
            return AutenticacaoDAO.__parse_supervisor(row)

        else:
            raise Exception

    @staticmethod
    def __parse_operador_caixa(row) -> OperadorCaixa:
        nome = row["nome"]
        cpf = row["cpf"]
        email = row["email"]
        telefone = row["telefone"]
        senha = row["senha"]

        return OperadorCaixa(nome, cpf, email, telefone, senha)

    @staticmethod
    def __parse_supervisor(row) -> Supervisor:
        nome = row["nome"]
        cpf = row["cpf"]
        email = row["email"]
        telefone = row["telefone"]
        senha = row["senha"]

        return Supervisor(nome, cpf, email, telefone, senha)
