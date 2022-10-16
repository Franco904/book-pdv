class SenhaNovaIgualAtualException(Exception):
    def __init__(self):
        super().__init__("\nA nova senha não deve ser igual a atual.\n")