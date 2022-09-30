class SystemView:
    def __init__(self):
        pass

    @staticmethod
    def show_options():
        print('='*40)
        print('[ 1 ] Cadastro Option')
        print('[ 2 ] Login Option')
        print('[ 0 ] Close system')
        print('=' * 40)

        opcao = int(input('Option: '))
        while opcao not in range(0, 2):
            opcao = int(input('Option: '))

        return opcao

    @staticmethod
    def show_message(message):
        print(message)
