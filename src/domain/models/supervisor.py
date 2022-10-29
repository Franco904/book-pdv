from src.domain.models.funcionario import Funcionario


class Supervisor(Funcionario):
    def __init__(self, nome: str, cpf: str, email: str, telefone: str, senha: str):
        super().__init__(nome, cpf, email, telefone, senha, "supervisor")

    def copy_with(self, nome: str = None, cpf: str = None, email: str = None, telefone: str = None):
        return Supervisor(
            nome if nome is not None else self.__nome,
            cpf if cpf is not None else self.__cpf,
            email if email is not None else self.__email,
            telefone if telefone is not None else self.__telefone,
            '',
        )
