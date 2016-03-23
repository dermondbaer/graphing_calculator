# Pascal Mehnert
# 20.03.2016
# Datentyp zum Speichern von geparsten Termen
# V 1.0


class Node:
    def __init__(self, value, is_operation=False, is_value=False, is_constant=False, is_variable=False):
        """
        :param value: The value of the Node.
        :type value: string
        :param is_operation: Defines whether the Node represents an operation.
        :type is_operation: Bool
        :param is_value: Defines whether the Node represents a value.
        :type is_value: Bool
        :param is_constant: Defines whether the Node represents a constant.
        :type is_constant: Bool
        :param is_variable: Defines whether the Node represents a variable.
        :type is_variable: Bool
        :return: The Node that has been created.
        :rtype: Node
        """
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

    def add_child(self, child, reverse=False):
        """
        Adds an child element to a Node

        :param child: The value to add as a child
        :type child: Node
        :param reverse: If True: Adds the child as new left child; Else: Adds the child as new right child
        :type reverse: Bool
        :return: The value that was added as child
        :rtype: Node
        """

        if reverse is False:
            self.__child_list.append(child)
        else:
            self.__child_list.insert(0, child)
        return child


class ParserTree:
    def __init__(self):
        self.__root = None

    def get_root(self):
        return self.__root

    def add_operation(self, value, reverse=True, parent=None):
        return self.__add_node(value, is_operation=True, reverse=reverse, parent=parent)

    def add_value(self, value, reverse=True, parent=None):
        return self.__add_node(value, is_value=True, reverse=reverse, parent=parent)

    def add_constant(self, value, reverse=True, parent=None):
        return self.__add_node(value, is_constant=True, reverse=reverse, parent=parent)

    def add_variable(self, value, reverse=True, parent=None):
        return self.__add_node(value, is_variable=True, reverse=reverse, parent=parent)

    def __add_node(self, value, is_operation=False, is_value=False, is_constant=False, is_variable=False, reverse=True,
                   parent=None):
        if parent is None:
            if self.__root is None:
                self.__root = Node(value, is_operation=is_operation, is_value=is_value, is_constant=is_constant,
                                   is_variable=is_variable)
                return self.__root

        elif parent.is_operation():
            child = Node(value, is_operation=is_operation, is_value=is_value, is_constant=is_constant,
                         is_variable=is_variable)
            return parent.add_child(child, reverse=reverse)

        else:
            raise SyntaxError('Error while parsing the expression')

    def print(self):
        if self.__root is not None:
            self.__print(self.__root)
        print()

    def __print(self, node):
        if node is not None:
            value = node.get_value()
            for child in node.get_child_list():
                self.__print(child)
            print(value, end=' ')
