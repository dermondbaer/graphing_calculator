# Pascal Mehnert
# 11.03.2016
# Datentyp zum Speichern von geparsten Termen
# V 0.1


class Operation:
    def __init__(self, value):
        self.__left = None
        self.__right = None
        self.__value = value

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    def get_value(self):
        return self.__value

    def set_left(self, value):
        self.__left = value
        return value

    def set_right(self, value):
        self.__right = value
        return value


class Value:
    def __init__(self, value):
        self.__value = value
        self.__left = None
        self.__right = None

    def get_value(self):
        return self.__value

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right


class ParserTree:
    def __init__(self):
        self.__root = None

    def get_root(self):
        return self.__root

    def add_operation(self, value, root=None, side=None):
        if root is None:
            self.__root = Operation(value)
            return self.__root

        else:
            if side == 'l':
                if root.get_left() is None:
                    return root.set_left(Operation(value))
            elif side == 'r':
                if root.get_right() is None:
                    return root.set_right(Operation(value))

    def add_value(self, value, root=None, side=None):
        if root is None:
            if self.__root is None:
                self.__root = Value(value)
                return self.__root

        else:
            if side == 'l':
                if root.get_left() is None:
                    return root.set_left(Value(value))
            elif side == 'r':
                if root.get_right() is None:
                    return root.set_right(Value(value))

    def print(self):
        if self.__root is not None:
            self._print(self.__root)

    def _print(self, node):
        if node is not None:
            if node.get_left() is not None:
                self._print(node.get_left())
            print(node.get_value())
            if node.get_right() is not None:
                self._print(node.get_right())
