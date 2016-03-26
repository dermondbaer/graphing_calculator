# Pascal Mehnert
# 20.03.2016
# Data type that is used to save a parsed mathematical expression to it.
# V 1.0


class Node:
    """Represents either an operation, a number, a constant or a variable in a Parser Tree."""
    def __init__(self, value, is_operation=False, is_number=False, is_constant=False, is_variable=False):
        self.__child_list = []
        self.__value = value

        if is_operation ^ is_number ^ is_constant ^ is_variable:
            self.__is_operation = is_operation
            self.__is_number = is_number
            self.__is_constant = is_constant
            self.__is_variable = is_variable

    def get_child_list(self):
        """Returns a list, containing all child elements of this Node."""
        return self.__child_list

    def get_child(self, index):
        """Returns a specific child of this Node."""
        return self.__child_list[index]

    def get_value(self):
        """Returns the value of this Node."""
        return self.__value

    def is_operation(self):
        """Determines if this Node represents an operation."""
        return self.__is_operation

    def is_number(self):
        """Determines if this Node represents a number."""
        return self.__is_number

    def is_constant(self):
        """Determines if this Node represents a constant."""
        return self.__is_constant

    def is_variable(self):
        """Determines if  this Node represents a variable."""
        return self.__is_variable

    def add_child(self, child, reverse=False):
        """Adds a child element to this Node."""
        if reverse is False:
            self.__child_list.append(child)         # adding as most right child
        else:
            self.__child_list.insert(0, child)      # adding as most left child
        return child


class ParserTree:
    """Used to save a mathematical Expression as a Tree."""
    def __init__(self):
        self.__root = None

    def get_root(self):
        """Returns the root Node of this Parser Tree."""
        return self.__root

    def get_variables(self):
        """Returns all variables in this ParserTree. If there are none, returns False."""
        variable_list = []
        self.__is_variable(self.__root, variable_list)
        if not variable_list:       # Return False, if the list is empty
            return False
        else:                       # Else returns the list itself
            return variable_list

    def __is_variable(self, node, variable_list):
        """Checks if a Node is a variable and calls itself for every child of the Node."""
        if node.is_variable():
            variable_list.append(node.get_value())
        elif node.is_operation():
            for child in node.get_child_list():
                self.__is_variable(child, variable_list)

    def add_operation(self, value, reverse=True, parent=None):
        """Adds an operation as child of a Node."""
        return self.__add_node(value, is_operation=True, reverse=reverse, parent=parent)

    def add_number(self, value, reverse=True, parent=None):
        """Adds a value as child of a Node."""
        return self.__add_node(value, is_number=True, reverse=reverse, parent=parent)

    def add_constant(self, value, reverse=True, parent=None):
        """Adds a constant as child of a Node."""
        return self.__add_node(value, is_constant=True, reverse=reverse, parent=parent)

    def add_variable(self, value, reverse=True, parent=None):
        """Adds a variable as child of a Node."""
        return self.__add_node(value, is_variable=True, reverse=reverse, parent=parent)

    def __add_node(self, value, is_operation=False, is_number=False, is_constant=False, is_variable=False, reverse=True,
                   parent=None):
        """Adds a child to a Node in this Parser Tree."""
        if parent is None:              # Adding the Node as root
            if self.__root is None:
                self.__root = Node(value, is_operation=is_operation, is_number=is_number, is_constant=is_constant,
                                   is_variable=is_variable)
                return self.__root

        elif parent.is_operation():     # Adding the Node as child of an operation
            child = Node(value, is_operation=is_operation, is_number=is_number, is_constant=is_constant,
                         is_variable=is_variable)
            return parent.add_child(child, reverse=reverse)

        else:
            raise SyntaxError('Error while parsing the expression')

    def print(self):
        """Initializes the print for this Parser Tree."""
        if self.__root is not None:
            self.__print(self.__root)   # Calls the __print() function for the root of this Parser Tree
        print()

    def __print(self, node):
        """Prints the given Node and initializes the print for every child element."""
        if node is not None:
            value = node.get_value()
            for child in node.get_child_list():
                self.__print(child) # Calls the __print() function for every child element of this Node
            print(value, end=' ')
