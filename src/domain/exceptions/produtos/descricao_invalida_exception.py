class DescricaoInvalidaException(Exception):
    def __init__(self):
        super().__init__("\nA descrição deve conter entre 2 e 50 caracteres.\n A descrição não deve conter apenas números.")