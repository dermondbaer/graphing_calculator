# Pascal Mehnert
# 11.03.2016
# Datentyp zum Speichern von gerparsten Termen
# V 0.1


class Operation:
    def __init__(self, value):
        self.__left = None
        self.__right = None
        self.__operation = value

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    def get_operation(self):
        return self.__operation

    def set_left(self, value):
        self.__left = value

    def set_right(self, value):
        self.__right = value


class Value:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value


class ParserTree:
    def __init__(self):
        self.__root = None

    def get_root(self):
        return self.__root

    def add_operation(self, value, root=None, side=False):
        if root is None:
            self.__root = Operation(value)
            return self.__root

        else:
            if side == 'left':
                if root.get_left() is None:
                    return root.set_left(Operation(value))
            elif side == 'right':
                if root.get_right() is None:
                    return root.set_right(Operation(value))

    def add_value(self, value, root=None, side=False):
        if root is None:
            self.__root = Value(value)
            return self.__root

        else:
            if side == 'left':
                if root.get_left() is None:
                    return root.set_left(Value(value))
            elif side == 'right':
                if root.get_right() is None:
                    return root.set_right(Value(value))
