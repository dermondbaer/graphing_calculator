# Pascal Mehnert
# 09.03.2016
# Calculator for mathematical expressions
# V 0.1

import math_library
from operator import *
from math_parser import Parser
from parser_tree import ParserTree


class Calculator(object):
    parser = Parser()
    operators = {'+': add, '-': sub, '*': mul, '/': truediv, '^': pow}

    @staticmethod
    def calculate_expression(expression):
        """
        Calculates the solution of a mathematical expression.
        If there are variables in the expression, it is being simplified as far as possible.

        :arg expression: The expression to calculate.
        :type expression: str
        :rtype: ParserTree
        """
        print('{:<14}'.format('Calculating:'), expression, sep='')
        parser_tree = Calculator.parser.parse_expression(expression)        # Parsing the given expression
        print('{:<14}'.format('Postfix:'), end='')
        parser_tree.print()
        if parser_tree.get_root() is not None:
            Calculator._simplify(parser_tree.get_root())          # Calling the _simplify function
        print('{:<14}'.format('Result:'), end='')
        parser_tree.print()
        print()
        return parser_tree

    @staticmethod
    def calculate_function_value(parser_tree, **variables):
        """
        Calculates the solution of an already expression, that has already been parsed.
        All variables used in the expression have to be declared in the function call as variable=value.

        :arg parser_tree: The expression to calculate.
        :type parser_tree: ParserTree
        :arg variables: The variables used in the expression.
        :type variables: dict
        :rtype: float
        """
        if parser_tree.get_root() is not None:
            result = Calculator._calculate(parser_tree.get_root(), variables)
            return result
        else:
            return False

    @staticmethod
    def _simplify(node):
        """
        Simplifies a Node and its children by calculating their actual value.

        :arg node: The Node to simplify.
        :type node: Node
        :rtype: bool
        """
        can_be_simplified = True
        for child in node.get_child_list():     # Try to simplify each child
            if not Calculator._simplify(child):       # If one child can't be simplified
                can_be_simplified = False       # Then this Node can also be not simplified

        if node.is_variable():      # If this Node is a variable
            return False            # Then this Node and its parents can't be simplified

        if can_be_simplified:
            if node.is_operation():
                if node.get_value() in Calculator.operators:            # If this Node is an operator
                    operation = Calculator.operators[node.get_value()]  # Get the operator
                    operand_0 = node.get_child(0).get_value()       # Get the values of the children
                    operand_1 = node.get_child(1).get_value()
                    operands = (operand_0, operand_1)
                    value = operation(*operands)                    # Calculate the value of this node
                    node.set_value(value, is_number=True)           # Set the value of this node

                else:                                                   # If the Node is a function
                    arguments = []
                    for child in node.get_child_list():                 # Get the value  of each child
                        arguments.append(child.get_value())
                    function = getattr(math_library, node.get_value())
                    value = function(*arguments)                        # Calculate the value of this Node
                    node.set_value(value, is_number=True)               # Set the value of this Node

                return True

            elif node.is_number():      # If this Node is a number
                return True             # Do nothing and return

            elif node.is_constant():                    # If the Node is a constant
                value = vars(math_library)[node.get_value()]    # Get the value of the constant
                node.set_value(value, is_number=True)   # Set the value of this Node
                return True

        else:
            return False

    @staticmethod
    def _calculate(node, variables=None):
        """
        Calculates the value of a Node and returns it.

        :arg node: The Node to calculate the value of.
        :type node: Node
        :arg variables: A list of variables.
        :type variables: dict
        :rtype: float
        """
        if node.is_operation():
            if node.get_value() in Calculator.operators:            # If the Node is an operator
                operation = Calculator.operators[node.get_value()]  # Get the operator
                operand_1 = Calculator._calculate(node.get_child(0), variables=variables)
                operand_2 = Calculator._calculate(node.get_child(1), variables=variables)
                operands = (operand_1, operand_2)               # Calculate the values of both children
                value = operation(*operands)                    # Calculate the value of this Node
                return value

            else:                                                       # If the Node is a function
                function = getattr(math_library, node.get_value())              # Get the function
                arguments = []
                for child in node.get_child_list():                     # Calculate the value of each child
                    arguments.append(Calculator._calculate(child, variables=variables))
                value = function(*arguments)                            # Calculate the value of this Node
                return value

        elif node.is_number():          # If the Node is a number
            return node.get_value()     # Return the value of the Node

        elif node.is_variable():                    # If the Node is a variable
            value = variables[node.get_value()]     # Get the value of the Node from the dictionary
            return value                            # Return the value
