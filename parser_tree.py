# Pascal Mehnert
# 29.05.2016
# Collections of classes, that are used to save a mathematical expression as a Tree.
# V 2.0

import re


class Node(object):
    """Represents any type of Node in a ParserTree"""
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
    """Represents a constant, like 'pi' or 'e' in a ParserTree."""
    def __init__(self, key, value, parent):
        """
        :type key: str
        :type value: Decimal
        :type parent: Node
        """
        Node.__init__(self, key, value, parent)


class Variable(Node):
    """Represents a variable in a ParserTree."""
    def __init__(self, key, parent):
        """
        :type key: str
        :type parent: Node
        """
        Node.__init__(self, key, key, parent)


class Number(Node):
    """Represents a number in a ParserTree."""
    def __init__(self, key, value, parent):
        """
        :type key: str
        :type value: Decimal
        :type parent: Node
        """
        Node.__init__(self, key, value, parent)


class ParsedFunction(Node):
    """Represents a function in a ParserTree, that has already been parsed."""
    def __init__(self, key, value, parent):
        """
        :type key: str
        :type value: ParserTree
        :type parent: Node
        """
        Node.__init__(self, key, value, parent)


class Operation(Node):
    """Represents any kind of mathematical operation in a ParserTree."""
    def __init__(self, key, value, parent):
        Node.__init__(self, key, value, parent)
        self.__child_list = []

    def get_child_list(self):
        """Returns all children of this Node as a list."""
        return self.__child_list

    def get_child(self, index):
        """Returns a specific child of this Node."""
        return self.__child_list[index]

    def add_child(self, child):
        """Adds a child to this Node."""
        self.__child_list.insert(0, child)

    def replace_child(self, old, new):
        """Replaces a child of this Node with a new one."""
        for index, child in enumerate(self.__child_list):
            if child == old:
                self.__child_list[index] = new
                break


class Operator(Operation):
    """Represents a mathematical operator, like '+' or '-' in a ParserTree."""
    def __int__(self, key, value, parent):
        """
        :type key: str
        :type value: function
        :type parent: Node
        """
        Operation.__init__(self, key, value, parent)


class Function(Operation):
    """Represents a mathematical function, like 'sin' or 'log' in a ParserTree."""
    def __init__(self, key, value, parent):
        """
        :type key: str
        :type value: function
        :type parent: Node
        """
        Operation.__init__(self, key, value, parent)


class ParserTree(object):
    """A class that is used to save a mathematical expression as interpretable object."""
    def __init__(self):
        self.__root = None

    def __str__(self):
        return self.to_string()

    def get_root(self):
        """Returns the root of this Parser Tree."""
        return self.__root

    def set_root(self, node):
        """Sets the root of this ParserTree."""
        self.__root = node
        return node

    def add_operator(self, key, value, parent=None):
        """Adds an operator as child of a Node in this ParserTree."""
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
        """Adds a function as child of a Node in this ParserTree."""
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
        """Adds a number as child of a Node in this ParserTree."""
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
        """Adds a constant as child of a Node in this ParserTree."""
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
        """Adds a variable as child of a Node in this ParserTree."""
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
        """Adds a function, that has already been parsed, as child of a Node in this ParserTree."""
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
        """Returns a list of all variables in this ParserTree."""
        variable_list = []
        if self.__root is not None:
            self._is_variable(self.__root, variable_list)
        return variable_list

    def _is_variable(self, node, variable_list):
        """Checks if the given Node represents a variable. If so, the variable is added to the given list."""
        if type(node) == Variable:
            variable_list.append(node.get_key())
        elif isinstance(node, Operation):
            for child in node.get_child_list():
                self._is_variable(child, variable_list)

    def print(self, precision=12):
        """Prints every Node of this ParserTree to the given precision."""
        if self.__root is not None:
            self._print_node(self.__root, precision)
        print()

    def _print_node(self, node, precision):
        """Prints the Node to the given precision. Then it calls itself for every child of the Node."""
        key = str()
        if type(node) in (Number, Constant):
            key = node.get_value()
            if key != 0:
                key = round(key, precision)
        elif type(node) in (Variable, ParsedFunction):
            key = node.get_key()
        elif isinstance(node, Operation):
            key = node.get_key()
            for child in node.get_child_list():
                self._print_node(child, precision)
        key = str(key)
        key = key.rstrip('0').rstrip('.') if '.' in key else key
        print(key, end=' ')

    def to_string(self, precision=12):
        """Returns all Nodes of this ParserTree, to the given precision as String."""
        string = str()
        if self.__root is not None:
            string = self._node_to_string(self.__root, precision)
            string = string.lstrip(' ').rstrip('')
            return string
        else:
            return string

    def _node_to_string(self, node, precision, string=''):
        """Returns the Node and its children as String. Decimals are rounded to the given precision."""
        key = str()
        if type(node) in (Number, Constant):
            key = node.get_value()
            if key != 0:
                key = round(key, precision)
        elif type(node) in (Variable, ParsedFunction):
            key = node.get_key()
        elif isinstance(node, Operation):
            for child in node.get_child_list():
                key += ' ' + self._node_to_string(child, precision, string)
            key += ' ' + node.get_key()
        key = str(key)
        key = key.rstrip('0').rstrip('.') if '.' in key else key
        key = re.sub('\s+', ' ', key)

        return key

    def is_empty(self):
        return self.__root is None
