# Pascal Mehnert
# 19.05.2016
# Functions used to simplify and calculate mathematical expressions
# V 2.0

import math_library
import analysis_library
import decimal
import math_parser
from parser_tree import *

decimal.getcontext().prec = 64


class Calculator(math_parser.Parser):
    @staticmethod
    def calculate_expression(expression):
        """
        Calculates the solution of a mathematical expression.
        If there are variables in the expression, it is being simplified as far as possible.

        :param expression: The expression to calculate.
        :type expression: str
        :rtype: ParserTree
        """
        print('{:<14}'.format('Calculating:'), expression, sep='')

        parser_tree = Calculator.parse_expression(expression)

        print('{:<14}'.format('Postfix:'), end='')
        parser_tree.print()

        if parser_tree.get_root() is not None:
            Calculator._simplify(parser_tree, parser_tree.get_root())

        print('{:<14}'.format('Result:'), end='')
        parser_tree.print()
        print()

        return parser_tree

    @staticmethod
    def calculate_function_value(parser_tree, variables):
        """
        Calculates the solution of an expression, that has already been parsed.
        All variables used in the expression have to be declared in the function call as variable=value.

        :param parser_tree: The expression to calculate.
        :type parser_tree: ParserTree
        :param variables: The variables used in the expression.
        :type variables: dict
        :rtype: Decimal
        """
        if parser_tree.get_root() is not None:
            return Calculator._calculate(parser_tree.get_root(), variables)

        else:
            return False

    @staticmethod
    def _simplify(parser_tree, node):
        """
        Simplifies a Node and its children by calculating their actual value.

        :arg node: The Node to simplify.
        :rtype: bool
        """
        if type(node) == Variable:                                  # If this Node is a variable
            return False                                            # Then this Nodes parent can't be simplified

        elif type(node)in (Number, Constant, ParsedFunction):       # If this Node is Number or a Constant
            return True                                             # Then this Nodes parent can be simplified

        else:
            for child in node.get_child_list():                     # Try to simplify each child
                if not Calculator._simplify(parser_tree, child):    # If one child can't be simplified
                    return False                                    # Then this Node can't be simplified as well

            parent = node.get_parent()
            if type(node) == Operator:
                operation = node.get_value()
                operand_0 = node.get_child(0).get_value()           # Get the value of each children
                operand_1 = node.get_child(1).get_value()
                value = operation(operand_0, operand_1)             # Calculate the value of this Node
                if parent is not None:
                    parent.replace_child(node, Number(str(value), value, parent))
                else:
                    parser_tree.set_root(Number(str(value), value, parent))

            elif type(node) == Function:
                function = node.get_value()
                arguments = []
                for child in node.get_child_list():                 # Get the value of each child
                    arguments.append(child.get_value())
                value = function(*arguments)                        # Calculate the value of this Node
                if parent is not None:
                    parent.replace_child(node, Number(str(value), value, parent))
                else:
                    parser_tree.set_root(Number(str(value), value, parent))

            return True

    @staticmethod
    def _calculate(node, variables=None):
        """
        Calculates the value of a Node and returns it.

        :param node: The Node to calculate the value of.
        :type node: Constant, Variable, Number, ParsedFunction, Operator or Function
        :param variables: A list of variables.
        :type variables: dict
        :rtype: Decimal
        """
        value = decimal.Decimal()
        if type(node) == Operator:
            operation = node.get_value()
            operand_1 = Calculator._calculate(node.get_child(0), variables=variables)
            operand_2 = Calculator._calculate(node.get_child(1), variables=variables)
            value = operation(operand_1, operand_2)

        elif type(node) == Function:
            function = node.get_value()
            arguments = []
            for child in node.get_child_list():
                arguments.append(Calculator._calculate(child, variables=variables))
            value = function(*arguments)

        elif type(node) in (Number, Constant, ParsedFunction):
            value = node.get_value()

        elif type(node) == Variable:
            value = variables[node.get_key()]

        return value
