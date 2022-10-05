from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
from src.domain.models.funcionario import Funcionario  # Apagar

from src.domain.models.operador_caixa import OperadorCaixa
from src.domain.models.supervisor import Supervisor


class FuncionarioDAO(AbstractDAO):
    def __init__(self, database: Database):
        super().__init__(database, 'access_control', 'funcionarios')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    def execute_query(self, query: str):
        super().execute_query(query)

    def get_all(self):
        rows = super().get_all()
        funcionarios = list(map(lambda row: FuncionarioDAO.__parse_funcionario(row), rows))

        return funcionarios

    def get_by_cpf(self, cpf: str):
        row = super().get_by_pk("cpf", cpf)

        funcionario = None if row is None else FuncionarioDAO.__parse_funcionario(row)
        return funcionario

    def persist_entity(self, funcionario: Funcionario):
        table = super().get_table()
        columns = "cpf, nome, email, telefone, senha, cargo"

        super().persist(
            f""" INSERT INTO {table} ({columns}) VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                funcionario.cpf,
                funcionario.nome,
                funcionario.email,
                funcionario.telefone,
                funcionario.senha,
                funcionario.cargo,
            ),
        )

    def delete_entity(self, cpf: str):
        super().delete("cpf", cpf)

    def update_entity(self, cpf: str, attribute, value):
        super().update("cpf", cpf, attribute, value)

    @staticmethod
    def __parse_funcionario(row):
        if row is None:
            return None

        if row["cargo"] == "operador_caixa":
            return FuncionarioDAO.__parse_operador_caixa(row)

        elif row["cargo"] == "supervisor":
            return FuncionarioDAO.__parse_supervisor(row)

        else:
            raise Exception

    @staticmethod
    def __parse_operador_caixa(row):
        nome = row["nome"]
        cpf = row["cpf"]
        email = row["email"]
        telefone = row["telefone"]
        senha = row["senha"]

        return OperadorCaixa(nome, cpf, email, telefone, senha)

    @staticmethod
    def __parse_supervisor(row):
        nome = row["nome"]
        cpf = row["cpf"]
        email = row["email"]
        telefone = row["telefone"]
        senha = row["senha"]

        return Supervisor(nome, cpf, email, telefone, senha)


