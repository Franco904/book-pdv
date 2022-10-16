class SenhaInvalidaException(Exception):
    def __init__(self):
        super().__init__("\nDigite uma senha válida:\nA senha deve conter entre 6 e 18 caracteres sendo números e letras.\n")