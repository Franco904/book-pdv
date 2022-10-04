class CargoInvalidoException(Exception):
    def __init__(self):
        super().__init__("\nVocê deve selecionar pelo menos um cargo para continuar.\n")