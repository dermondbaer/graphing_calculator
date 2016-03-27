# Pascal Mehnert
# 09.03.2016
# Class that is used to save the infix notation and a parser tree of a mathematical expression
# V 0.1


class Expression(object):
    """A mathematical expression and its ParserTree."""
    def __init__(self, expression, parsed_expression):
        """
        :type expression: str
        :type parsed_expression: ParserTree()
        """
        self.__expression = expression
        self.__parsed_expression = parsed_expression

    def get_expression(self):
        return self.__expression

    def get_parsed_expression(self):
        return self.__parsed_expression

    @staticmethod
    def is_function():
        return False


class Function(Expression):
    """"""
    def __init__(self, expression, parsed_expression, simplified_parsed_expression):
        Expression.__init__(self, expression, parsed_expression)
        self.__simplified_parsed_expression = simplified_parsed_expression

    def get_simplified_parsed_expression(self):
        return self.__simplified_parsed_expression

    @staticmethod
    def is_function():
        return True
