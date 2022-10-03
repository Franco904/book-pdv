from funcionario import Funcionario

class OperadorCaixa(Funcionario):

    def __init__(self, nome: str, cpf: int):
        super().__init__(nome, cpf, "operador")
