# Pascal Mehnert
# 09.03.2016
# Multiple algorithms, used to restructure and parse mathematical expression.
# V 1.0

import re
import xml.etree.ElementTree as Et
from ParserTree import ParserTree


class Parser(object):
    def __init__(self, xml_file):
        self.__operators = []               # List of available operators
        self.__operator_precedence = {}     # List of available operators and their corresponding precedence
        self.__operator_associativity = {}  # List of available operators and their corresponding associativity
        self.__supported_functions = {}     # List of available functions
        self.__supported_constants = []     # List of available constants
        self.__supported_variables = []     # List of available variables
        self.__operations_xml = Et.parse(xml_file)
        self.__xml_root = self.__operations_xml.getroot()
        for child in self.__xml_root[0]:    # Iterating over the operators, defined in the XML-File
            attributes = child.attrib
            self.__operators.append(attributes['name'])
            self.__operator_precedence[attributes['name']] = attributes['precedence']
            self.__operator_associativity[attributes['name']] = attributes['associativity']

        for child in self.__xml_root[1]:    # Iterating over the functions, defined in the XML-File
            attributes = child.attrib
            self.__supported_functions[attributes['name']] = int(attributes['variables'])

        for child in self.__xml_root[2]:    # Iterating over the constants, defined in the XML-File
            attributes = child.attrib
            self.__supported_constants.append(attributes['name'])

        for child in self.__xml_root[3]:    # Iterating over the variables, defined in the XML-File
            attributes = child.attrib
            self.__supported_variables.append(attributes['name'])

    def parse_expression(self, expression):
        """
        Parses a mathematical expression and returns it as a ParserTree.  Its purpose is NOT graphic display.

        :arg expression: A mathematical expression, given in infix notation.
        :type expression: str
        :rtype: ParserTree
        """
        postfix = self._make_postfix(self.partition(expression))    # Converts the expression to postfix notation
        parser_tree = ParserTree(expression)
        if len(postfix) > 0:
            self._parse(postfix, current_token_index=len(postfix) - 1, parser_tree=parser_tree)
        return parser_tree

    def make_expression_postfix(self, expression):
        """
        Initializes the conversion of a mathematical from infix to postfix notation.

        :arg expression: The expression to be converted into postfix notation.
        :type expression: str
        :rtype: str
        """
        infix = self.partition(expression)      # Sequences the given expression
        postfix = self._make_postfix(infix)    # Invokes the actual conversion of the expression
        postfix = ' '.join(postfix)             # Joins the sequenced expression back together
        return postfix

    def _make_postfix(self, expression):
        """
        Uses the shunting-yard algorithm to convert from infix to postfix notation.

        :arg expression: The expression to be converted into postfix notation.
        :type expression: list
        :rtype: list
        """
        output_queue = []
        operator_stack = []
        for token in expression:
            if re.match('^-?\d+(\.\d+)?$', token):      # If the token is a number
                output_queue.append(token)              # Add it to the output queue

            elif token in self.__supported_constants:   # If the token is a constant
                output_queue.append(token)              # Add it to the output queue

            elif token in self.__supported_variables:   # If the token is a variable
                output_queue.append(token)              # Add it to the output queue

            elif token in self.__supported_functions:   # If the token is a function
                operator_stack.append(token)            # Add it to the operator stack

            elif token == ',':                          # If the token is a argument separator
                while operator_stack[-1] != '(':        # Until the top of the operator stack is a left parenthesis
                    operator = operator_stack.pop()     # Pop operators off the operator stack
                    output_queue.append(operator)       # Add them to the output queue
                    if len(operator_stack) == 0:        # If there are no left parenthesis, raise an Error
                        raise ValueError('Error while parsing the Expression: Parenthesis mismatched')

            elif token in self.__operators:             # If the token is an operator
                if len(operator_stack) > 0:
                    while operator_stack[-1] in self.__operators:   # While there are operators on the operator stack
                        if self.__operator_associativity[token] == 'l':
                            if self.__operator_precedence[token] <= self.__operator_precedence[operator_stack[-1]]:
                                operator = operator_stack.pop()     # Pop them off the operator stack
                                output_queue.append(operator)       # Add them to the output queue
                            else:
                                break

                        if self.__operator_associativity[token] == 'r':
                            if self.__operator_precedence[token] < self.__operator_precedence[operator_stack[-1]]:
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
                    if operator_stack[-1] in self.__supported_functions:    # If the top of the operator stack is a
                                                                            # function
                        operator = operator_stack.pop()                     # Pop it off the operator stack
                        output_queue.append(operator)                       # Add it to the output queue

        while len(operator_stack) > 0:              # While there are operators on the operator stack
            if operator_stack[-1] == '(':           # If there is a left parenthesis at the top of the operator stack
                raise ValueError('Error while parsing the Expression: Parenthesis mismatched')     # Raise an Error

            else:                                   # If there is an operator at the top of the operator stack
                operator = operator_stack.pop()     # Pop it off the operator stack
                output_queue.append(operator)       # Add it to the output queue

        return output_queue

    def _parse(self, expression, current_token_index, parser_tree, parent=None):
        """
        Parser an expression, given in postfix notation and writes it to a ParserTree.

        :arg expression: The expression to parse.
        :type expression: list
        :arg current_token_index: The index of the current token.
        :type current_token_index: int
        :arg parser_tree: The ParserTree, the expression is written to.
        :type parser_tree: ParserTree
        :arg parent: The Node that is parent to the current token.
        :type parent: Node
        :rtype: int
        """
        token = expression[current_token_index]
        if token in self.__operators:       # If the token is an operator
            parent = parser_tree.add_operation(token, parent=parent)
            current_token_index -= 1
            current_token_index = self._parse(expression, current_token_index, parser_tree, parent=parent)
            current_token_index = self._parse(expression, current_token_index, parser_tree, parent=parent)

        elif token in self.__supported_functions:                           # If the token is a function
            parent = parser_tree.add_operation(token, parent=parent)        # Add the token as Node
            current_token_index -= 1
            for argument in range(0, self.__supported_functions[token]):    # Add each argument as child
                current_token_index = self._parse(expression, current_token_index, parser_tree, parent=parent)

        elif token in self.__supported_constants:               # If the token is a constant
            parser_tree.add_constant(token, parent=parent)      # Add the token as Node
            current_token_index -= 1

        elif token in self.__supported_variables:               # If the token is a variable
            parser_tree.add_variable(token, parent=parent)      # Add the token as Node
            current_token_index -= 1

        elif re.match('^-?\d+(\.\d+)?$', token):                # If the token is a number
            parser_tree.add_number(float(token), parent=parent)        # Add the token as Node
            current_token_index -= 1

        return current_token_index          # Return the current token index

    @staticmethod
    def partition(expression):
        """
        Sequences a mathematical expression into logically separable parts.

        :arg expression: The expression to sequence.
        :type expression: str
        :rtype: list
        """
        expression = expression.replace('(', ' ( ')
        expression = expression.replace(')', ' ) ')
        expression = expression.replace(',', ' , ')
        expression = re.sub('\s+', ' ', expression)
        expression = expression.split(' ')
        if len(expression) > 0:
            while expression[-1] == '':
                expression.pop()
                if len(expression) == 0:
                    break
        return expression
