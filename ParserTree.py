# Pascal Mehnert
# 11.03.2016
# Datentyp zum Speichern von geparsten Termen
# V 0.1


class Node:
    def __init__(self, value, is_operation=False, is_value=False, is_variable=False):
        self.__children = []
        self.__value = value
        if is_operation ^ is_value ^ is_variable:
            self.__is_operation = is_operation
            self.__is_value = is_value
            self.__is_variable = is_variable

    def get_child_list(self):
        return self.__children

    def get_child(self, index):
        return self.__children[index]

    def add_child(self, child):
        self.__children.append(child)
        return child

    def get_child_count(self):
        return len(self.__children)

    def get_value(self):
        return self.__value

    def is_operation(self):
        return self.__is_operation

    def is_value(self):
        return self.__is_value

    def is_variable(self):
        return self.__is_variable


class ParserTree:
    def __init__(self):
        self.__root = None

    def get_root(self):
        return self.__root

    def add_operation(self, value, parent=None):
        if parent is None:
            self.__root = Node(value, is_operation=True)
            return self.__root

        elif parent.is_operation():
            return parent.add_child(Node(value, is_operation=True))

        else:
            raise SyntaxError('Error while parsing the expression')

    def add_value(self, value, parent=None):
        if parent is None:
            if self.__root is None:
                self.__root = Node(value, is_value=True)
                return self.__root

        elif parent.is_operation():
            return parent.add_child(Node(value, is_value=True))

        else:
            raise SyntaxError('Error while parsing the expression')

    def add_variable(self, value, parent=None):
        if parent is None:
            if self.__root is None:
                self.__root = Node(value, is_variable=True)
                return self.__root

        elif parent.is_operation():
            return parent.add_child(Node(value, is_variable=True))

        else:
            raise SyntaxError('Error while parsing the expression')

'''
    def print(self):
        if self.__root is not None:
            self.__print(self.__root)

    def __print(self, node):
        if node is not None:
            value = node.get_value()
            if node.is_operation():
                if value in ['+', '-', '*', '/']:
                    if node.is_factored_out():
                        print('(', end='')

                    for index, child in enumerate(node.get_child_list()):
                        if index == 0:
                            is_first_child = True
                        else:
                            is_first_child = False
                            
                        if is_first_child:
                            self.__print(child)
                        else:
                            print('', value, end=' ')
                            self.__print(child)

                    if node.is_factored_out():
                        print(')', end='')
                else:
                    print(value, end='(')

                    for index, child in enumerate(node.get_child_list()):
                        if index == 0:
                            is_first_child = True
                        else:
                            is_first_child = False
                            
                        if is_first_child:
                            self.__print(child)
                        else:
                            print(', ', end='')
                            self.__print(child)

                    print(')', end='')

            elif not node.is_operation():
                if node.is_factored_out():
                    print('(', value, ')', sep='', end='')

                else:
                    print(value, end='')
'''
