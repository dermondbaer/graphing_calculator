# Pascal Mehnert
# 20.03.2016
# Data type that is used to save a parsed mathematical expression to it.
# V 1.0


class Node(object):
    """Represents either an operation, a number, a constant or a variable in a Parser Tree."""
    def __init__(self, key, value, parent=None):
        self.__key = key
        self.__value = value
        self.__parent = parent

    def get_key(self):
        """Returns the key of this Node"""
        return self.__key

    def get_value(self):
        """Returns the value of this Node."""
        return self.__value

    def get_parent(self):
        """Returns the parent of this Node."""
        return self.__parent

    def set_key(self, key):
        """Changes the key of this Node."""
        self.__key = key

    def set_value(self, value):
        """Changes the value of this Node."""
        self.__value = value


class Constant(Node):
    def __init__(self, key, value, parent):
        Node.__init__(self, key, value, parent)


class Variable(Node):
    def __init__(self, key, parent):
        Node.__init__(self, key, key, parent)

class Number(Node):
    def __init__(self, key, value, parent):
        Node.__init__(self, key, value, parent)


class ParsedFunction(Node):
    def __init__(self, key, value, parent):
        Node.__init__(self, key, value, parent)


class Operation(Node):
    def __init__(self, key, value, parent):
        Node.__init__(self, key, value, parent)
        self.__child_list = []

    def get_child_list(self):
        return self.__child_list

    def get_child(self, index):
        return self.__child_list[index]

    def add_child(self, child):
        self.__child_list.insert(0, child)

    def replace_child(self, old, new):
        for index, child in enumerate(self.__child_list):
            if child == old:
                self.__child_list[index] = new
                break


class Operator(Operation):
    def __int__(self, key, value, parent):
        Operation.__init__(self, key, value, parent)


class Function(Operation):
    def __init__(self, key, value, parent):
        Operation.__init__(self, key, value, parent)


class ParserTree(object):
    def __init__(self, expression=False):
        """
        Used to save a mathematical Expression as a Tree.

        :arg expression: The expression saved in this ParserTree.
        :type expression: str
        """
        self.__root = None
        self.__expression = expression

    def get_root(self):
        """Returns the root Node of this Parser Tree."""
        return self.__root

    def set_root(self, node):
        self.__root = node

    def get_expression(self):
        """Returns the expression saved in this ParserTree"""
        return self.__expression

    def add_operator(self, key, value, parent=None):
        """Adds an operation as child of a Node."""
        if parent is None:
            self.__root = Operator(key, value, parent)
            return self.__root

        elif isinstance(parent, Operation):
            child = Operator(key, value, parent)
            parent.add_child(child)
            return child

        else:
            raise ValueError('Error while parsing the expression.')

    def add_function(self, key, value, parent=None):
        """Adds an operation as child of a Node."""
        if parent is None:
            self.__root = Function(key, value, parent)
            return self.__root

        elif isinstance(parent, Operation):
            child = Function(key, value, parent)
            parent.add_child(child)
            return child

        else:
            raise ValueError('Error while parsing the expression.')

    def add_number(self, key, value, parent=None):
        """Adds a value as child of a Node."""
        if parent is None:
            self.__root = Number(key, value, parent)
            return self.__root

        elif isinstance(parent, Operation):
            child = Number(key, value, parent)
            parent.add_child(child)
            return child

        else:
            raise ValueError('Error while parsing the expression.')

    def add_constant(self, key, value, parent=None):
        """Adds a constant as child of a Node."""
        if parent is None:
            self.__root = Constant(key, value, parent)
            return self.__root

        elif isinstance(parent, Operation):
            child = Constant(key, value, parent)
            parent.add_child(child)
            return child

        else:
            raise ValueError('Error while parsing the expression.')

    def add_variable(self, key, parent=None):
        """Adds a variable as child of a Node."""
        if parent is None:
            self.__root = Variable(key, parent)
            return self.__root

        elif isinstance(parent, Operation):
            child = Variable(key, parent)
            parent.add_child(child)
            return child

        else:
            raise ValueError('Error while parsing the expression.')

    def add_parsed_function(self, key, value, parent=None):
        if parent is None:
            self.__root = ParsedFunction(key, value, parent)
            return self.__root

        elif isinstance(parent, Operation):
            child = ParsedFunction(key, value, parent)
            parent.add_child(child)
            return child

        else:
            raise ValueError('Error while parsing the expression.')

    def get_variables(self):
        """Returns all variables in this ParserTree. If there are none, returns False."""
        variable_list = []
        if self.__root is not None:
            self._is_variable(self.__root, variable_list)   # Checks if there are variables in this ParserTree
        if not variable_list:                               # Return False, if the list is empty
            return False
        else:                                               # Else returns the list itself
            return variable_list

    def _is_variable(self, node, variable_list):
        """Checks if a Node is a variable and calls itself for every child of the Node."""
        if type(node) == Variable:
            variable_list.append(node.get_key())
        elif isinstance(node, Operation):
            for child in node.get_child_list():
                self._is_variable(child, variable_list)

    def print(self, precision=12):
        """Initializes the print for this Parser Tree."""
        if self.__root is not None:
            self._print(self.__root, precision)
        print()

    def _print(self, node, precision):
        """Prints the given Node and initializes the print for every child element."""
        if node is not None:
            key = ''
            if type(node)in (Number, Constant):
                key = round(node.get_value(), precision)
            elif type(node) == Variable:
                key = node.get_key()
            elif type(node) == ParsedFunction:
                key = node.get_key()
            elif isinstance(node, Operation):
                key = node.get_key()
                for child in node.get_child_list():
                    self._print(child, precision)
            key = str(key)
            key = key.rstrip('0').rstrip('.') if '.' in key else key
            print(key, end=' ')
