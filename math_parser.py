# Pascal Mehnert
# 19.05.2016
# Multiple algorithms, used to restructure and parse mathematical expression.
# V 2.0

import re
import inspect
import operator as op
import math_library
import analysis_library
from decimal import *
from parser_tree import ParserTree


class Parser(object):
    operators = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv, '^': pow}
    operator_precedence = {'^': 4, '*': 3, '/': 3, '+': 2, '-': 2}
    operator_associativity = {'^': 'r', '*': 'l', '/': 'l', '+': 'l', '-': 'l'}
    supported_constants = ['e', 'pi']

    is_function_name = re.compile('^-?[a-zA-Z][a-zA-z0-9]+$')
    is_positive_function_name = re.compile('^[a-zA-Z][a-zA-z0-9]+$')
    is_negative_function_name = re.compile('^-[a-zA-Z][a-zA-z0-9]+$')
    is_number = re.compile('^-?\d+(\.\d+)?$')
    is_variable = re.compile('^-?[a-z]$')
    is_positive_variable = re.compile('^[a-z]$')
    is_negative_variable = re.compile('^-[a-z]$')

    @staticmethod
    def parse_expression(expression):
        """
        Parses a mathematical expression and returns it as ParserTree.

        :param expression: A mathematical expression, given in infix notation.
        :type expression: str
        :rtype: ParserTree
        """
        postfix = Parser._make_postfix(Parser.partition(expression))
        parser_tree = ParserTree()
        if postfix:
            if Parser._parse(postfix, current_token_index=len(postfix) - 1, parser_tree=parser_tree) == -1:
                return parser_tree
            else:
                raise ValueError('Error while Parsing the Expression.')
        else:
            return parser_tree

    @staticmethod
    def make_expression_postfix(expression):
        """
        Converts a mathematical expression from infix to postfix notation.

        :param expression: The expression to be converted to postfix notation.
        :type expression: str
        :rtype: str
        """
        infix = Parser.partition(expression)
        postfix = Parser._make_postfix(infix)
        postfix = ' '.join(postfix)
        return postfix

    @staticmethod
    def _make_postfix(expression):
        """
        Uses the shunting-yard algorithm to convert an expression from infix to postfix notation.

        :param expression: The expression to be converted into postfix notation.
        :type expression: list
        :rtype: list
        """
        is_function_name = Parser.is_function_name
        is_number = Parser.is_number
        is_variable = Parser.is_variable
        output_queue = []
        operator_stack = []

        for token in expression:
            if re.match(is_number, token):              # If the token is a number
                output_queue.append(token)              # Add it to the output queue

            elif token in Parser.supported_constants:   # If the token is a constant
                output_queue.append(token)              # Add it to the output queue

            elif re.match(is_variable, token):          # If the token is a variable (single lowercase)
                output_queue.append(token)              # Add it to the output queue

            elif re.match(is_function_name, token):     # If the token is a function name
                operator_stack.append(token)            # Add it to the operator stack

            elif token == ',':                          # If the token is a argument separator
                while operator_stack[-1] != '(':        # Until the top of the operator stack is a left parenthesis
                    operator = operator_stack.pop()     # Pop operators off the operator stack
                    output_queue.append(operator)       # Add them to the output queue
                    if len(operator_stack) == 0:        # If there are no left parenthesis, raise an Error
                        raise ValueError('Error while parsing the Expression: Parenthesis mismatched')

            elif token in Parser.operators:             # If the token is an operator
                if len(operator_stack) > 0:
                    while operator_stack[-1] in Parser.operators:   # While there are operators on the operator stack
                        if Parser.operator_associativity[token] == 'l':
                            if Parser.operator_precedence[token] <= Parser.operator_precedence[operator_stack[-1]]:
                                operator = operator_stack.pop()     # Pop them off the operator stack
                                output_queue.append(operator)       # Add them to the output queue
                            else:
                                break

                        if Parser.operator_associativity[token] == 'r':
                            if Parser.operator_precedence[token] < Parser.operator_precedence[operator_stack[-1]]:
                                operator = operator_stack.pop()     # Pop them off the operator stack
                                output_queue.append(operator)       # Add them to output queue
                            else:
                                break

                        if len(operator_stack) == 0:
                            break

                operator_stack.append(token)            # Add the token to the operator stack

            elif token == '(':                          # If the token is a left parenthesis
                operator_stack.append(token)            # Add it to the output queue

            elif token == ')':                          # If the token is a right parenthesis
                while operator_stack[-1] != '(':        # Until the top of the operator stack is a left parenthesis
                    operator = operator_stack.pop()     # Pop operator off the operator stack
                    output_queue.append(operator)       # Add them to the output queue
                    if len(operator_stack) == 0:        # If there are no left parenthesis, raise an Error
                        raise ValueError('Error while parsing the Expression: Parenthesis mismatched')

                operator_stack.pop()                    # Pop the left parenthesis off the stack

                if len(operator_stack) > 0:
                    if re.match(is_function_name, operator_stack[-1]):  # If the top of the operator stack is a function
                        operator = operator_stack.pop()                 # Pop it off the operator stack
                        output_queue.append(operator)                   # Add it to the output queue

        while len(operator_stack) > 0:              # While there are operators on the operator stack
            if operator_stack[-1] == '(':           # If there is a left parenthesis at the top of the operator stack
                raise ValueError('Error while parsing the Expression: Parenthesis mismatched')

            else:                                   # If there is an operator at the top of the operator stack
                operator = operator_stack.pop()     # Pop it off the operator stack
                output_queue.append(operator)       # Add it to the output queue

        return output_queue

    @staticmethod
    def _parse(expression, current_token_index, parser_tree, parent=None):
        """
        Parses an expression, given in postfix notation and saves it to a ParserTree.

        :param expression: The expression to parse.
        :type expression: list
        :parm current_token_index: The index of the current token.
        :type current_token_index: int
        :param parser_tree: The ParserTree, the expression is being written to.
        :type parser_tree: ParserTree
        :param parent: The Node that is parent to the current token.
        :type parent: Node
        :rtype: int
        """
        is_function_name = Parser.is_function_name
        is_number = Parser.is_number
        is_variable = Parser.is_variable

        if current_token_index >= 0:
            token = expression[current_token_index]
        else:
            return current_token_index

        if token in Parser.operators:
            value = Parser.operators[token]
            parent = parser_tree.add_operator(token, value, parent=parent)
            current_token_index -= 1
            current_token_index = Parser._parse(expression, current_token_index, parser_tree, parent=parent)
            current_token_index = Parser._parse(expression, current_token_index, parser_tree, parent=parent)

        elif token in Parser.supported_constants:
            value = vars(math_library)[token]
            parser_tree.add_constant(token, value, parent=parent)
            current_token_index -= 1

        elif re.match(is_function_name, token):
            try:
                function = getattr(math_library, token)
                parent = parser_tree.add_function(token, function, parent=parent)
                current_token_index -= 1
                argument_count = len(inspect.getfullargspec(function).args)
                for argument in range(0, argument_count):
                    current_token_index = Parser._parse(expression, current_token_index, parser_tree, parent=parent)

            except AttributeError:
                function = getattr(analysis_library, token)
                parent = parser_tree.add_function(token, function, parent=parent)
                current_token_index -= 1
                argument_count = len(inspect.getfullargspec(function).args)

                for argument in range(0, argument_count - 1):
                    current_token_index = Parser._parse(expression, current_token_index, parser_tree, parent=parent)

                temp_parser_tree = ParserTree()
                new_current_token_index = Parser._parse(expression, current_token_index, temp_parser_tree, parent=None)
                function_term = expression[new_current_token_index + 1:current_token_index + 1]
                function_term = ' '.join(function_term)
                parser_tree.add_parsed_function(function_term, temp_parser_tree, parent=parent)
                current_token_index = new_current_token_index

        elif re.match(is_variable, token):
            parser_tree.add_variable(token, parent)
            current_token_index -= 1

        elif re.match(is_number, token):
            parser_tree.add_number(token, Decimal(token), parent=parent)
            current_token_index -= 1

        return current_token_index

    @staticmethod
    def partition(expression):
        """
        Sequences a mathematical expression into logically separable parts.

        :arg expression: The expression to sequence.
        :type expression: str
        :rtype: list
        """
        is_function_name = Parser.is_function_name
        is_negative_function_name = Parser.is_negative_function_name
        is_number = Parser.is_number
        is_variable = Parser.is_variable
        is_negative_variable = Parser.is_negative_variable

        expression = expression.replace('-(', ' ## ')
        expression = expression.replace('(', ' ( ')
        expression = expression.replace('##', '-(')
        expression = expression.replace(')', ' ) ')
        expression = expression.replace(',', ' , ')
        expression = re.sub('\s+', ' ', expression)
        expression = expression.rstrip(' ').lstrip(' ')
        expression = expression.split(' ')

        for index in range(0, len(expression)):
            token = expression[index]
            if re.match('^\.\d+$', token):
                token = '0' + token             # Adding left out leading zeros in positive decimal digits
            if re.match('^-\.\d+$', token):
                token.replace('-', '-0')        # Adding left out leading zeros in negative decimal digits
            expression[index] = token

        stack = []
        for token in expression:
            if token in ('(', '-('):
                stack.append(token)
            elif token == ')':
                if len(stack) > 0:
                    stack.pop()
                else:
                    raise ValueError('Error while parsing the expression, check parenthesis.')
        if stack:
            for bracket in range(0, len(stack)):
                expression.append(')')          # Adding left out closing brackets at the end of the expression

        for index, token in enumerate(expression):
            if re.match(is_negative_function_name, token):
                expression[index] = expression[index][1:]
                expression.insert(index, '*')
                expression.insert(index, '-1')
            elif re.match(is_negative_variable, token):
                expression[index] = expression[index][1]
                expression.insert(index, '*')
                expression.insert(index, '-1')
            elif token == '-(':
                expression[index] = '('
                expression.insert(index, '*')
                expression.insert(index, '-1')

            next_index = index + 1
            if next_index == len(expression):
                break
            next_token = expression[index + 1]                          # Adding left out multiplication signs
            if re.match(is_number, token):                              # Between numbers and ...
                if next_token == '(':  # ... opening brackets
                    expression.insert(next_index, '*')
                elif next_token in Parser.supported_constants:          # ... constants
                    expression.insert(next_index, '*')
                elif re.match(is_variable, next_token):                 # ... variables
                    expression.insert(next_index, '*')
                elif re.match(is_function_name, next_token):            # ... functions
                    expression.insert(next_index, '*')

            elif token == ')':                                          # Between closing brackets and ...
                if next_token == '(':                                   # ... opening brackets
                    expression.insert(next_index, '*')
                elif re.match(is_number, next_token):                   # ... numbers
                    expression.insert(next_index, '*')
                elif next_token in Parser.supported_constants:          # ... constants
                    expression.insert(next_index, '*')
                elif re.match(is_variable, next_token):                 # ... variables
                    expression.insert(next_index, '*')
                elif re.match(is_function_name, next_token):            # ... functions
                    expression.insert(next_index, '*')

            elif token in Parser.supported_constants:                   # Between constants and ...
                if next_token == '(':                                   # ... opening brackets
                    expression.insert(next_index, '*')
                elif re.match(is_number, next_token):                   # ... numbers
                    expression.insert(next_index, '*')
                elif next_token in Parser.supported_constants:          # ... constants
                    expression.insert(next_index, '*')
                elif re.match(is_variable, next_token):                 # ... variables
                    expression.insert(next_index, '*')
                elif re.match(is_function_name, next_token):            # ... functions
                    expression.insert(next_index, '*')

            elif re.match(is_variable, token):                          # Between variables and ...
                if next_token == '(':                                   # ... opening brackets
                    expression.insert(next_index, '*')
                elif re.match(is_number, next_token):                   # ... numbers
                    expression.insert(next_index, '*')
                elif next_token in Parser.supported_constants:          # ... constants
                    expression.insert(next_index, '*')
                elif re.match(is_variable, next_token):                 # ... variables
                    expression.insert(next_index, '*')
                elif re.match(is_function_name, next_token):            # ... functions
                    expression.insert(next_index, '*')

        return expression
