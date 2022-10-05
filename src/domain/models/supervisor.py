from funcionario import Funcionario

class Supervisor(Funcionario):

    def __init__(self, nome: str, cpf: str, email: str, telefone: str, senha: str):
        super().__init__(nome, cpf, email, telefone, senha, "supervisor")
