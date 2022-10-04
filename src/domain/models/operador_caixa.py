from funcionario import Funcionario

class OperadorCaixa(Funcionario):

    def __init__(self, nome: str, cpf: str, email: str, telefone: str, password: str):
        super().__init__(nome, cpf, email, telefone, password, "operador")
