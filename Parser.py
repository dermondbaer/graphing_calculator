# Pascal Mehnert
# 09.03.2016
# Algorithmus zum analysieren und aufgliedern von mathematischen Ausdrücken
# V 0.1

import re
import xml.etree.ElementTree as Et
from ParserTree import ParserTree


class Parser(object):
    def __init__(self):
        self.__supported_operations = {}
        self.__operations_xml = Et.parse('supported_operations.xml')
        self.__xml_root = self.__operations_xml.getroot()
        for child in self.__xml_root:
            attributes = child.attrib
            self.__supported_operations[attributes['name']] = attributes['variables']

        self.__regex = re.compile('\d+\.\d+|\d+|[+-/*(),]|[a-z]+')

    def parse_expression(self, expression):
        parser_tree = ParserTree()
        expression = expression.replace(" ", "")

        expression = self.__regex.findall(expression)
        self.__parse_expression(expression, parser_tree)
        parser_tree.print()

    def __parse_expression(self, expression, parser_tree, side=None, parent=None):
        brackets = 0
        parsed_index = False
        for index, section in enumerate(expression):
            if section == '(':
                brackets += 1

            elif section == ')':
                brackets -= 1

            elif brackets == 0:
                if section in ['+', '-']:
                    parsed_index = index
                    break

                elif section in ['*', '/'] and parsed_index is False:
                    parsed_index = index

        if parsed_index is not False:
            value = expression[parsed_index]
            parent = parser_tree.add_operation(value, parent=parent, side=side)
            self.__parse_expression(expression[0:parsed_index], parser_tree, side='l', parent=parent)
            self.__parse_expression(expression[parsed_index+1:len(expression)], parser_tree, side='r', parent=parent)

        else:
            value = expression[0]
            if len(expression) == 1:
                parser_tree.add_value(value, parent=parent, side=side)

            elif re.match(r'^[a-z]+$', value):
                parent = parser_tree.add_operation(value, parent=parent, side=side)
                self.__parse_expression(expression[1:len(expression)], parser_tree, side='l', parent=parent)


parser = Parser()
# parser.parse_expression("5.34-456+456*4753/6")
