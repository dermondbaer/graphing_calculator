# Pascal Mehnert
# 09.03.2016
# Class that is used to save the infix notation and a parser tree of a mathematical expression
# V 0.1


class Expression(object):
    def __init__(self, expression, parsed_expression, variables=False):
        """
        :type expression: str
        :type parsed_expression: ParserTree()
        :type variables: list
        """
        self.__expression = expression
        self.__parsed_expression = parsed_expression
        self.__variables = variables

    def get_expression(self):
        return self.__expression

    def get_parsed_expression(self):
        return self.__parsed_expression

    def get_variable_list(self):
        return self.__variables
