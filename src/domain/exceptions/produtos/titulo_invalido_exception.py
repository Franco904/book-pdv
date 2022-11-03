class TituloInvalidoException(Exception):
    def __init__(self):
        super().__init__("\nO campo título deve conter entre 2 e 20 caracteres.\n O título não deve conter apenas números.")