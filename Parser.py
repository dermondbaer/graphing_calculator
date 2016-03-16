# Pascal Mehnert
# 09.03.2016
# Algorithmus zum analysieren und aufgliedern von mathematischen Ausdrücken
# V 0.1

from ParserTree import ParserTree


class Parser(object):
    def parse_expression(self, expression):
        parser_tree = ParserTree()
        expression = expression.replace(" ", "")
        self._parse_expression(expression, parser_tree)

    def _parse_expression(self, expression, parser_tree, side, parent=None):
        brackets = 0
        cut_index = False
        for index, char in enumerate(expression):
            if char == '(':
                brackets += 1
            elif char == ')':
                brackets -= 1
            elif brackets == 0:
                if char == '+' or char == '-':
                    cut_index = index
                    break
                if char == '*' or char == '/' and cut_index is False:
                    cut_index = index

        if cut_index:
            node = parser_tree.add_operation(expression[cut_index], parent=parent, side=side)
            self._parse_expression(expression[0:cut_index], parser_tree, 'left', node)
            self._parse_expression(expression[cut_index+1:len(expression)], parser_tree, 'right', node)

        else:
            for char, index in enumerate(expression):
                pass

