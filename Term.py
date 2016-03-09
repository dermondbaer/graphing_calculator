# Pascal Mehnert
# 09.03.2016
# Speichern von konstanten und von variablen abhängingen Termen
# V 0.1


class Term(object):
    def __init__(self, expression, parsed_expression, variable=False):
        self.__expression = expression
        self.__parsed_expression = parsed_expression
        self.__variable = variable

    def get_expression(self):
        return self.__expression

    def get_parsed_expression(self):
        return self.__parsed_expression

    def get_variable(self):
        return self.__variable
