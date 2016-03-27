# Pascal Mehnert
# 09.03.2016
# Calculator for mathematical expressions
# V 0.1

import math
import xml.etree.ElementTree as Et
from Parser import Parser


class Calculator(object):
    def __init__(self, xml_file):
        self.__parser = Parser(xml_file)
        self.__operators = []               # List of available operators
        self.__supported_functions = {}     # List of available functions
        self.__supported_constants = []     # List of available constants
        self.__supported_variables = []     # List of available variables
        self.__operations_xml = Et.parse(xml_file)
        self.__xml_root = self.__operations_xml.getroot()
        for child in self.__xml_root[0]:    # Iterating over the operators, defined in the XML-File
            attributes = child.attrib
            self.__operators.append(attributes['name'])

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
        parser_tree = self.__parser.parse_expression(expression)
        if parser_tree.get_root() is not None:
            self.__simplify(parser_tree.get_root())
        return parser_tree

    def calculate_function_value(self, parser_tree, **variables):
        if parser_tree.get_root() is not None:
            result = self.__calculate(parser_tree.get_root(), variables)
            return result
        else:
            return False

    def __calculate(self, node, variables=None):
        if node.is_operation():
            if node.get_value() in self.__operators:
                value = 0
                operator = node.get_value()
                operand_0 = self.__calculate(node.get_child(0), variables=variables)
                operand_1 = self.__calculate(node.get_child(1), variables=variables)
                if operator == '+':
                    value = operand_0 + operand_1

                elif operator == '-':
                    value = operand_0 - operand_1

                elif operator == '*':
                    value = operand_0 * operand_1

                elif operator == '/':
                    value = operand_0 / operand_1

                elif operator == '^':
                    value = pow(operand_0, operand_1)
                return value

            elif node.get_value() in self.__supported_functions:
                arguments = []
                for child in node.get_child_list():
                    arguments.append(self.__calculate(child, variables=variables))
                command = getattr(math, node.get_value())
                value = command(*arguments)
                return value

        elif node.is_number():
            return node.get_value()

        elif node.is_constant():
            constant = node.get_value()
            value = vars(math)[constant]
            return value

        elif node.is_variable():
            value = variables[node.get_value()]
            return value

    def __simplify(self, node):
        can_be_simplified = True
        for child in node.get_child_list():
            if not self.__simplify(child):
                can_be_simplified = False

        if node.is_variable():
            return False

        if can_be_simplified:
            if node.is_operation():
                if node.get_value() in self.__operators:
                    operator = node.get_value()
                    operands = [node.get_child(0).get_value(), node.get_child(1).get_value()]
                    if operator == '+':
                        value = operands[0] + operands[1]

                    elif operator == '-':
                        value = operands[0] - operands[1]

                    elif operator == '*':
                        value = operands[0] * operands[1]

                    elif operator == '/':
                        value = operands[0] / operands[1]

                    elif operator == '^':
                        value = pow(operands[0], operands[1])

                elif node.get_value() in self.__supported_functions:
                    arguments = []
                    for child in node.get_child_list():
                        arguments.append(child.get_value())
                    command = getattr(math, node.get_value())
                    value = command(*arguments)

                node.set_value(value, is_number=True)
                return True

            elif node.is_number():
                return True

            elif node.is_constant():
                constant = node.get_value()
                node.set_value(vars(math)[constant], is_number=True)
                return True

        else:
            return False
