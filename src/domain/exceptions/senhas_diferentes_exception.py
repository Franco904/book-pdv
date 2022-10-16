class SenhasDiferentesException(Exception):
    def __init__(self):
        super().__init__("\nAs senhas devem ser iguais!\n")