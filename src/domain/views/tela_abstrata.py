from abc import ABC, abstractmethod
import PySimpleGUI as sg


class Tela(ABC):
    @abstractmethod
    def __init__(self, window: sg.Window, tamanho=None):
        self.__window = window
        if tamanho is not None:
            self.__window.set_min_size(tamanho)

    @abstractmethod
    def init_components(self):
        pass

    @abstractmethod
    def open(self):
        pass

    @property
    def window(self):
        return self.__window

    def close(self):
        self.__window.close()

    def show_message(self, titulo: str, msg):
        sg.Popup(titulo, msg)

    def show_form_confirmation(self, titulo: str, msg):
        return sg.PopupOKCancel(titulo, msg)

    def read(self):
        botao, valores = self.__window.read()
        return botao, valores

    def update(self, key: str, value):
        self.__window[key].update(value)
