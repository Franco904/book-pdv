class IDInvalidoException(Exception):
    def __init__(self):
        super().__init__("\nO campo ID produto deve deve conter apenas números.\n")