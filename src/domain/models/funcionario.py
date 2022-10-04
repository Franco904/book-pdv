from abc import ABC, abstractmethod

class Funcionario(ABC):

    @abstractmethod
    def __init__(self, nome: str, cpf: str, email:str, telefone:str, password:str, cargo: str):
        self.__nome = None
        self.__cpf = None
        self.__email = None
        self.__telefone = None
        self.__password = None
        self.__cargo = None
        if isinstance(nome, str):
            self.__nome = nome
        if isinstance(cpf, str):
            self.__cpf = cpf
        if isinstance(email, str):
            self.__email = email
        if isinstance(telefone, str):
            self.__telefone = telefone
        if isinstance(password, str):
            self.__password = password
        if isinstance(cargo, str):
            self.__cargo = cargo

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, nome: str):
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def cpf(self):
        return self.__cpf
    @cpf.setter
    def cpf(self, cpf: str):
        if isinstance(cpf, str):
            self.__cpf = cpf

    @property
    def email(self):
        return self.__email
    @email.setter
    def email(self, email: str):
        if isinstance(email, str):
            self.__email = email

    @property
    def cargo(self):
        return self.__cargo
    @cargo.setter
    def cargo(self, cargo: str):
        if isinstance(cargo, str):
            self.__cargo = cargo

    @property
    def telefone(self):
        return self.__telefone
    @telefone.setter
    def telefone(self, telefone: str):
        if isinstance(telefone, str):
            self.__telefone = telefone

    @property
    def password(self):
        return self.__password
    @password.setter
    def password(self, password: str):
        if isinstance(password, str):
            self.__password = password