# Pascal Mehnert
# 11.03.2016
# Datentyp zum Speichern von geparsten Termen
# V 0.1


class Node:
    def __init__(self, value, is_operation=False, is_value=False, is_constant=False, is_variable=False):
        self.__child_list = []
        self.__value = value
        if is_operation ^ is_value ^ is_constant ^ is_variable:
            self.__is_operation = is_operation
            self.__is_value = is_value
            self.__is_constant = is_constant
            self.__is_variable = is_variable

    def get_child_list(self):
        return self.__child_list

    def get_child(self, index):
        return self.__child_list[index]

    def add_child(self, child, reverse=False):
        if reverse is False:
            self.__child_list.append(child)
        else:
            self.__child_list.insert(0, child)
        return child

    def get_child_count(self):
        return len(self.__child_list)

    def get_value(self):
        return self.__value

    def is_operation(self):
        return self.__is_operation

    def is_value(self):
        return self.__is_value

    def is_constant(self):
        return self.__is_constant

    def is_variable(self):
        return self.__is_variable


class ParserTree:
    def __init__(self):
        self.__root = None

    def get_root(self):
        return self.__root

    def add_operation(self, value, reverse=True, parent=None):
        if parent is None:
            self.__root = Node(value, is_operation=True)
            return self.__root

        elif parent.is_operation():
            return parent.add_child(Node(value, is_operation=True), reverse=reverse)

        else:
            raise SyntaxError('Error while parsing the expression')

    def add_value(self, value, reverse=True, parent=None):
        if parent is None:
            if self.__root is None:
                self.__root = Node(value, is_value=True)
                return self.__root

        elif parent.is_operation():
            return parent.add_child(Node(value, is_value=True), reverse=reverse)

        else:
            raise SyntaxError('Error while parsing the expression')

    def add_constant(self, value, reverse=True, parent=None):
        if parent is None:
            if self.__root is None:
                self.__root = Node(value, is_constant=True)
                return self.__root

        elif parent.is_operation():
            return parent.add_child(Node(value, is_constant=True), reverse=reverse)

        else:
            raise SyntaxError('Error while parsing the expression')

    def add_variable(self, value, reverse=True, parent=None):
        if parent is None:
            if self.__root is None:
                self.__root = Node(value, is_variable=True)
                return self.__root

        elif parent.is_operation():
            return parent.add_child(Node(value, is_variable=True), reverse=reverse)

        else:
            raise SyntaxError('Error while parsing the expression')

    def print(self):
        if self.__root is not None:
            self.__print(self.__root)

    def __print(self, node):
        if node is not None:
            value = node.get_value()
            for child in node.get_child_list():
                self.__print(child)
            print(value, end=' ')
