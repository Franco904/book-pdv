from funcionario import Funcionario

class Supervisor(Funcionario):

    def __init__(self, nome: str, cpf: int):
        super().__init__(nome, cpf, "supervisor")