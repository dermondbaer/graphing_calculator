# Pascal Mehnert
# 09.03.2016
# Calculator for mathematical expressions
# V 0.1

import math
import time
import xml.etree.ElementTree as Et
from operator import *
from Parser import Parser
from ParserTree import ParserTree


class Calculator(object):
    def __init__(self, xml_file):
        self.__parser = Parser(xml_file)
        self.__operators = {'+': add, '-': sub, '*': mul, '/': truediv, '^': pow}
        self.__supported_functions = {}     # List of available functions
        self.__supported_constants = []     # List of available constants
        self.__supported_variables = []     # List of available variables
        self.__operations_xml = Et.parse(xml_file)
        self.__xml_root = self.__operations_xml.getroot()

        for child in self.__xml_root[1]:    # Iterating over the functions, defined in the XML-File
            attributes = child.attrib
            self.__supported_functions[attributes['name']] = int(attributes['variables'])

        for child in self.__xml_root[2]:    # Iterating over the constants, defined in the XML-File
            attributes = child.attrib
            self.__supported_constants.append(attributes['name'])

        for child in self.__xml_root[3]:    # Iterating over the variables, defined in the XML-File
            attributes = child.attrib
            self.__supported_variables.append(attributes['name'])

    def calculate_expression(self, expression):
        """
        Calculates the solution of a mathematical expression.
        If there are variables in the expression, it is being simplified as far as possible.

        :arg expression: The expression to calculate.
        :type expression: str
        :rtype: ParserTree
        """
        print('{:<14}'.format('Calculating:'), expression, sep='')
        parser_tree = self.__parser.parse_expression(expression)        # Parsing the given expression
        print('{:<14}'.format('Postfix:'), end='')
        parser_tree.print()
        if parser_tree.get_root() is not None:
            self._simplify(parser_tree.get_root())          # Calling the _simplify function
        print('{:<14}'.format('Result:'), end='')
        parser_tree.print()
        print()
        return parser_tree

    def calculate_function_value(self, parser_tree, **variables):
        """
        Calculates the solution of an already expression, that has already been parsed.
        All variables used in the expression have to be declared in the function call as variable=value.

        :arg parser_tree: The expression to calculate.
        :type parser_tree: ParserTree
        :arg variables: The variables used in the expression.
        :type variables: dict
        :rtype: float
        """
        print('{:<14}'.format('Calculating:'), parser_tree.get_expression(), sep='')
        print('{:<14}'.format('Variables:'), end='')
        first = True
        for variable in variables:
            if first:
                print(variable, '=', variables[variable], sep=' ', end='')
                first = False
            else:
                print(';', variable, '=', variables[variable], sep=' ', end='')
                pass
        print()
        if parser_tree.get_root() is not None:
            result = self._calculate(parser_tree.get_root(), variables)
            print('{:<14}'.format('Result:'), result, sep='')
            print()
            return result
        else:
            print('Error')
            print()
            return False

    def _simplify(self, node):
        """
        Simplifies a Node and its children by calculating their actual value.

        :arg node: The Node to simplify.
        :type node: Node
        :rtype: bool
        """
        can_be_simplified = True
        if node.is_operation():
            if node.get_value() in self.__operators:                # If this Node is an operator
                operator = self.__operators[node.get_value()]       # Get the actual operator
                node.set_value(operator, is_operation=True)         # Set the value of this Node

            elif node.get_value() in self.__supported_functions:    # If this Node is a function
                function = getattr(math, node.get_value())          # Get the actual function
                node.set_value(function, is_operator=True)          # Set the value of this Node

        elif node.is_constant():
            if node.get_value() in self.__supported_constants:      # If this Node is a constant
                constant = vars(math)[node.get_value()]             # Get the value of the constant
                node.set_value(constant, is_number=True)            # Set the value of this Node

        for child in node.get_child_list():     # Try to simplify each child
            if not self._simplify(child):       # If one child can't be simplified
                can_be_simplified = False       # Then this Node can also be not simplified

        if node.is_variable():      # If this Node is a variable
            return False            # Then this Node and its parents can't be simplified

        if can_be_simplified:
            if node.is_operation():
                if node.get_value() in self.__operators:            # If this Node is an operator
                    operation = node.get_value()                    # Get the operator
                    operand_0 = node.get_child(0).get_value()       # Get the values of the children
                    operand_1 = node.get_child(1).get_value()
                    operands = (operand_0, operand_1)
                    value = operation(*operands)                    # Calculate the value of this node
                    node.set_value(value, is_number=True)           # Set the value of this node

                elif node.get_value() in self.__supported_functions:    # If this Node is a function
                    arguments = []
                    for child in node.get_child_list():                 # Get the value  of each child
                        arguments.append(child.get_value())
                    function = node.get_value()
                    value = function(*arguments)                        # Calculate the value of this Node
                    node.set_value(value, is_number=True)               # Set the value of this Node

                return True

            elif node.is_number():      # If this Node is a number
                return True             # Do nothing and return

        else:
            return False

    def _calculate(self, node, variables=None):
        """
        Calculates the value of a Node and returns it.

        :arg node: The Node to calculate the value of.
        :type node: Node
        :arg variables: A list of variables.
        :type variables: dict
        :rtype: float
        """
        if node.is_operation():
            if node.get_value() in self.__operators:        # If the Node is an operator
                operation = node.get_value()                # Get the operator
                operand_1 = self._calculate(node.get_child(0), variables=variables)
                operand_2 = self._calculate(node.get_child(1), variables=variables)
                operands = (operand_1, operand_2)           # Calculate the values of both children
                value = operation(*operands)                # Calculate the value of this Node
                return value

            elif node.get_value() in self.__supported_functions:        # If the Node is a function
                function = node.get_value()                             # Get the function
                arguments = []
                for child in node.get_child_list():                     # Calculate the value of each child
                    arguments.append(self._calculate(child, variables=variables))
                value = function(*arguments)                            # Calculate the value of this Node
                return value

        elif node.is_number():          # If the Node is a number
            return node.get_value()     # Return the value of the Node

        elif node.is_variable():                    # If the Node is a variable
            value = variables[node.get_value()]     # Get the value of the Node from the dictionary
            return value                            # Return the value``
