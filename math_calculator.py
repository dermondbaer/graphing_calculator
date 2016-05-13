# Pascal Mehnert
# 09.03.2016
# Calculator for mathematical expressions
# V 0.1

import math_library
from operator import *
from decimal import *
from math_parser import *
from parser_tree import *


class Calculator:
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
            Calculator._simplify(parser_tree, parser_tree.get_root())       # Calling the _simplify function
        print('{:<14}'.format('Result:'), end='')
        parser_tree.print()
        print()
        return parser_tree

    @staticmethod
    def calculate_function_value(parser_tree, variables):
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
    def _simplify(parser_tree, node):
        """
        Simplifies a Node and its children by calculating their actual value.

        :arg node: The Node to simplify.
        :rtype: bool
        """
        if node.is_variable():                              # If this Node is a variable
            return False                                    # Then this Nodes parent can't be simplified

        elif node.is_number() or node.is_constant():        # If this Node is Number or a Constant
            return True                                     # Then this Nodes parent can be simplified

        else:
            for child in node.get_child_list():             # Try to simplify each child
                if not Calculator._simplify(parser_tree, child):         # If one child can't be simplified
                    return False                            # Then this Node can also be not simplified

            parent = node.get_parent()
            if node.is_operator():
                operation = node.get_value()
                operand_0 = node.get_child(0).get_value()               # Get the values of the children
                operand_1 = node.get_child(1).get_value()
                operands = (operand_0, operand_1)
                value = operation(*operands)                            # Calculate the value of this node
                if parent is not None:
                    parent.replace_child(node, Number(str(value), value, parent))
                else:
                    parser_tree.set_root(Number(str(value), value, parent))

            elif node.is_function():
                function = node.get_value()
                arguments = []
                for child in node.get_child_list():                     # Get the value  of each child
                    arguments.append(child.get_value())
                value = function(*arguments)                            # Calculate the value of this Node
                if parent is not None:
                    parent.replace_child(node, Number(str(value), value, parent))
                else:
                    parser_tree.set_root(Number(str(value), value, parent))

            return True

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
        if node.is_operator():
            operation = node.get_value()
            operand_1 = Calculator._calculate(node.get_child(0), variables=variables)
            operand_2 = Calculator._calculate(node.get_child(1), variables=variables)
            value = operation(operand_1, operand_2)

        elif node.is_function():
            function = node.get_value()
            arguments = []
            for child in node.get_child_list():
                arguments.append(Calculator._calculate(child, variables=variables))
            value = function(*arguments)

        elif node.is_number() or node.is_constant():
            value = node.get_value()

        elif node.is_variable():
            value = Decimal(variables[node.get_key()])

        return value
