class CaixaJaCadastradoException(Exception):
    def __init__(self, codigo: str):
        super().__init__(f"\nUm caixa com o código {codigo} já está cadastrado!")
