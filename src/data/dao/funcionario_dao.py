from src.data.dao.abstract_dao import AbstractDAO
from src.data.database.database import Database
from src.domain.enums import CargoEnum
from src.domain.models.funcionario import Funcionario  # Apagar

from src.domain.models.operador_caixa import OperadorCaixa
from src.domain.models.supervisor import Supervisor


class FuncionarioDAO(AbstractDAO):
    def __init__(self, database: Database) -> None:
        super().__init__(database, 'access_control', 'funcionarios')
        self.__database = database
        self.__schema = super().schema
        self.__table = super().table

    def execute_query(self, query: str):
        super().execute_query(query)

    def get_all(self, custom_query="") -> [Funcionario]:
        rows = super().get_all()
        funcionarios = list(map(lambda row: FuncionarioDAO.parse_funcionario(row), rows))

        return funcionarios

    def get_by_cpf(self, cpf: str) -> Funcionario | None:
        row = super().get_by_pk("cpf", cpf)

        funcionario = None if row is None else FuncionarioDAO.parse_funcionario(row)
        return funcionario

    def has_opened_caixa(self, cpf: str) -> bool:
        table = super().get_table()
        custom_query = f"""
                            SELECT * FROM {table} AS f
                            INNER JOIN access_control.caixas_operadores AS co
                            ON f.cpf = co.cpf_operador
                            WHERE co.cpf_operador = '{cpf}'
                        """

        rows = super().get_all(custom_query)

        has_opened_caixa = False if len(rows) == 0 else True
        return has_opened_caixa

    def persist_entity(self, funcionario: Funcionario) -> None:
        table = super().get_table()
        columns = "cpf, nome, email, telefone, senha, id_cargo"

        id_cargo = CargoEnum.operador_caixa.value if funcionario.cargo == "operador_caixa" \
            else CargoEnum.supervisor.value

        super().persist(
            f""" INSERT INTO {table} ({columns}) VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                funcionario.cpf,
                funcionario.nome,
                funcionario.email,
                funcionario.telefone,
                funcionario.senha,
                id_cargo,
            ),
        )

    def delete_entity(self, cpf: str) -> None:
        super().delete("cpf", cpf)

    def update_entity(self, cpf: str, attribute, value) -> None:
        super().update("cpf", cpf, attribute, value)

    @staticmethod
    def parse_funcionario(row) -> Funcionario | None:
        if row is None:
            return None

        if row["id_cargo"] == CargoEnum.operador_caixa.value:
            return FuncionarioDAO.__parse_operador_caixa(row)

        elif row["id_cargo"] == CargoEnum.supervisor.value:
            return FuncionarioDAO.__parse_supervisor(row)

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
