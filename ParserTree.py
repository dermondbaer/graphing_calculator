# Pascal Mehnert
# 11.03.2016
# Datentyp zum Speichern von geparsten Termen
# V 0.1


class Node:
    def __init__(self, value, is_operation=True, factored_out=False):
        self.__left = None
        self.__right = None
        self.__value = value
        self.__is_operation = is_operation
        self.__factored_out = factored_out

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    def set_left(self, value):
        self.__left = value
        return value

    def set_right(self, value):
        self.__right = value
        return value

    def get_value(self):
        return self.__value

    def is_operation(self):
        return self.__is_operation

    def is_factored_out(self):
        return self.__factored_out


class ParserTree:
    def __init__(self):
        self.__root = None

    def get_root(self):
        return self.__root

    def add_operation(self, value, parent=None, side=None, factored_out=False):
        if parent is None:
            self.__root = Node(value, factored_out=factored_out)
            return self.__root

        if parent.is_operation():
            if side == 'l':
                if parent.get_left() is None:
                    return parent.set_left(Node(value, factored_out=factored_out))
            elif side == 'r':
                if parent.get_right() is None:
                    return parent.set_right(Node(value, factored_out=factored_out))

    def add_value(self, value, parent=None, side=None, factored_out=False):
        if parent is None:
            if self.__root is None:
                self.__root = Node(value, is_operation=False)
                return self.__root

        else:
            if side == 'l':
                if parent.get_left() is None:
                    return parent.set_left(Node(value, is_operation=False, factored_out=factored_out))
            elif side == 'r':
                if parent.get_right() is None:
                    return parent.set_right(Node(value, is_operation=False, factored_out=factored_out))

    def print(self):
        if self.__root is not None:
            self._print(self.__root)

    def _print(self, node):
        if node is not None:
            if node.is_factored_out():
                print('(', end='')

            if node.get_left() is not None:
                self._print(node.get_left())

            if node.is_operation():
                print(' ', node.get_value(), ' ', sep='', end='')
            else:
                print(node.get_value(), end='')

            if node.get_right() is not None:
                self._print(node.get_right())

            if node.is_factored_out():
                print(')', end='')

t = ParserTree()
op1 = t.add_operation('+')
op2 = t.add_operation('/', op1, 'l')
op3 = t.add_operation('*', op1, 'r', True)
val1 = t.add_value(5, op2, 'l')
val2 = t.add_value(27, op2, 'r')
val3 = t.add_value(567, op3, 'l')
val4 = t.add_value(5459, op3, 'r')

t.print()
