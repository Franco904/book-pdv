class ISBNInvalidoException(Exception):
    def __init__(self):
        super().__init__("\nO campo ISBN deve conter um valor válido. Ex: 978-3-16-148410-0 \n")