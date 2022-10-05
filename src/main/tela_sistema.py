class TelaSistema:
    def __init__(self):
        pass

    @staticmethod
    def show_options():
        print('=' * 40)
        print('[ 1 ] Funcionarios')
        print('[ 2 ] Início')
        print('[ 0 ] Fechar sistema')
        print('=' * 40)

        opcao = int(input('Opção: '))

        while opcao not in range(0, 3):
            opcao = int(input('Opção: '))

        return opcao

    @staticmethod
    def show_message(message):
        print(message)
