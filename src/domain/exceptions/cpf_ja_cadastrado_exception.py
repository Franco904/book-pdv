class CPFJaCadastradoException(Exception):
    def __init__(self, cpf: str):
        super().__init__(f"\nO CPF {cpf} já esta cadastrado!")