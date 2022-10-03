class CPFJaCadastradoException(Exception):
    def __init__(self, codigo: str):
        super().__init__(f"\nO CPF {codigo} já esta cadastrado!")