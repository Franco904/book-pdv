class QuantidadeInvalidaException(Exception):
    def __init__(self):
        super().__init__("\nVocê deve digitar uma quantidade válida.\n")