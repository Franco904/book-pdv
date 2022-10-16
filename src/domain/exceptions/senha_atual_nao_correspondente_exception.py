class SenhaAtualNaoCorrespondenteException(Exception):
    def __init__(self):
        super().__init__("\nA senha atual não corresponde às credenciais deste funcionário.\n")