from abc import ABC, abstractmethod


class Funcionario(ABC):
    @abstractmethod
    def __init__(self, nome: str, cpf: str, email: str, telefone: str, senha: str, cargo: str):
        self.__nome = None
        self.__cpf = None
        self.__email = None
        self.__telefone = None
        self.__senha = None
        self.__cargo = None
        if isinstance(nome, str):
            self.__nome = nome
        if isinstance(cpf, str):
            self.__cpf = cpf
        if isinstance(email, str):
            self.__email = email
        if isinstance(telefone, str):
            self.__telefone = telefone
        if isinstance(senha, str):
            self.__senha = senha
        if isinstance(cargo, str):
            self.__cargo = cargo

    @abstractmethod
    def copy_with(self, nome: str = None, cpf: str = None, email: str = None, telefone: str = None):
        pass

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str) -> None:
        if isinstance(cpf, str):
            self.__cpf = cpf

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str) -> None:
        if isinstance(email, str):
            self.__email = email

    @property
    def cargo(self) -> str:
        return self.__cargo

    @cargo.setter
    def cargo(self, cargo: str) -> None:
        if isinstance(cargo, str):
            self.__cargo = cargo

    @property
    def telefone(self) -> str:
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone: str) -> None:
        if isinstance(telefone, str):
            self.__telefone = telefone

    @property
    def senha(self) -> str:
        return self.__senha

    @senha.setter
    def senha(self, senha: str) -> None:
        if isinstance(senha, str):
            self.__senha = senha
