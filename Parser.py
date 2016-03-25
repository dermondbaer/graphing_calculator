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
        for child in self.__xml_root[0]:    # Iterating over the operators defined in the XML-File
            attributes = child.attrib
            self.__operators.append(attributes['name'])
            self.__operator_precedence[attributes['name']] = attributes['precedence']
            self.__operator_associativity[attributes['name']] = attributes['associativity']

        for child in self.__xml_root[1]:    # Iterating over the functions defined in the XML-File
            attributes = child.attrib
            self.__supported_functions[attributes['name']] = int(attributes['variables'])

        for child in self.__xml_root[2]:    # Iterating over the constants defined in the XML-File
            attributes = child.attrib
            self.__supported_constants.append(attributes['name'])

        for child in self.__xml_root[3]:    # Iterating over the variables defined in the XML-File
            attributes = child.attrib
            self.__supported_variables.append(attributes['name'])

    def parse_expression(self, expression):
        """Parses a """
        parser_tree = ParserTree()
        infix = self.partition(expression)
        postfix = self.__make_postfix(infix)
        self.__parse(postfix, current_token_index=len(postfix)-1, parser_tree=parser_tree)
        return parser_tree

    def make_expression_postfix(self, expression):
        infix = self.partition(expression)
        postfix = self.__make_postfix(infix)
        postfix = ' '.join(postfix)
        return postfix

    def __make_postfix(self, expression):
        output_queue = []
        operator_stack = []
        for token in expression:
            if re.match('^-?\d+(\.\d+)?$', token):
                output_queue.append(token)

            elif token in self.__supported_constants:
                output_queue.append(token)

            elif token in self.__supported_variables:
                output_queue.append(token)

            elif token in self.__supported_functions:
                operator_stack.append(token)

            elif token == ',':
                while operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                    if len(operator_stack) == 0:
                        raise SyntaxError('Error while parsing the Expression: Parenthesis mismatched')

            elif token in self.__operators:
                if len(operator_stack) > 0:
                    while operator_stack[-1] in self.__operators:
                        if self.__operator_associativity[token] == 'l':
                            if self.__operator_precedence[token] <= self.__operator_precedence[operator_stack[-1]]:
                                output_queue.append(operator_stack.pop())
                            else:
                                break

                        if self.__operator_associativity[token] == 'r':
                            if self.__operator_precedence[token] < self.__operator_precedence[operator_stack[-1]]:
                                output_queue.append(operator_stack.pop())
                            else:
                                break

                        if len(operator_stack) == 0:
                            break

                operator_stack.append(token)

            elif token == '(':
                operator_stack.append(token)

            elif token == ')':
                while operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                    if len(operator_stack) == 0:
                        raise SyntaxError('Error while parsing the Expression: Parenthesis mismatched')

                operator_stack.pop()

                if operator_stack[-1] in self.__supported_functions:
                    output_queue.append(operator_stack.pop())

        while len(operator_stack) > 0:
            if operator_stack[-1] == '(':
                raise SyntaxError('Error while parsing the Expression: Parenthesis mismatched')

            else:
                output_queue.append(operator_stack.pop())

        return output_queue

    def __parse(self, expression, current_token_index, parser_tree, parent=None):
        token = expression[current_token_index]
        if token in self.__operators:
            parent = parser_tree.add_operation(token, parent=parent)
            current_token_index -= 1
            current_token_index = self.__parse(expression, current_token_index, parser_tree, parent=parent)
            current_token_index = self.__parse(expression, current_token_index, parser_tree, parent=parent)

        elif token in self.__supported_functions:
            parent = parser_tree.add_operation(token, parent=parent)
            current_token_index -= 1
            for argument in range(0, self.__supported_functions[token]):
                current_token_index = self.__parse(expression, current_token_index, parser_tree, parent=parent)

        elif token in self.__supported_constants:
            parser_tree.add_constant(token, parent=parent)
            current_token_index -= 1

        elif token in self.__supported_variables:
            parser_tree.add_variable(token, parent=parent)
            current_token_index -= 1

        elif re.match('^-?\d+(\.\d+)?$', token):
            parser_tree.add_number(token, parent=parent)
            current_token_index -= 1

        return current_token_index

    @staticmethod
    def partition(expression):
        expression = expression.replace('(', ' ( ')
        expression = expression.replace(')', ' ) ')
        expression = expression.replace(',', ' , ')
        expression = re.sub('\s+', ' ', expression)
        expression = expression.split(' ')
        while expression[-1] == '':
            expression.pop()

        return expression

p = Parser('supported.xml')
p.parse_expression('6 - cos(-3 * 5)').print()
