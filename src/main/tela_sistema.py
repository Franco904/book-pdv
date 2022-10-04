class TelaSistema:
    def __init__(self):
        pass

    @staticmethod
    def show_options():
        print('=' * 40)
        print('[ 1 ] Início')
        print('[ 2 ] Funcionarios')
        print('[ 0 ] Fechar sistema')
        print('=' * 40)

        opcao = int(input('Option: '))

        while opcao not in range(0, 3):
            opcao = int(input('Option: '))

        return opcao

    @staticmethod
    def show_message(message):
        print(message)
