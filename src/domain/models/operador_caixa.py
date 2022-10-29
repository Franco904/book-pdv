from src.domain.models.funcionario import Funcionario


class OperadorCaixa(Funcionario):
    def __init__(self, nome: str, cpf: str, email: str, telefone: str, senha: str):
        super().__init__(nome, cpf, email, telefone, senha, "operador_caixa")

    def copy_with(self, nome: str = None, cpf: str = None, email: str = None, telefone: str = None):
        return OperadorCaixa(
            nome if nome is not None else self.__nome,
            cpf if cpf is not None else self.__cpf,
            email if email is not None else self.__email,
            telefone if telefone is not None else self.__telefone,
            '',
        )
