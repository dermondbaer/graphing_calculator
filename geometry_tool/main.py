#   Pascal Mehnert
#   29.01.2016
#
#   V 0.1

from geometry_tool.gui import *
from Calculator import *


class Application(object):
    def __init__(self):
        self.__gui = Gui('Coordinate System', target_size_x=950, target_size_y=950)
        self.__calculator = Calculator()

    def start(self):
        self.__gui.start()

    def stop(self):
        self.__gui.stop()

    def test_calculator(self):
        test_file = open('test_files/test_calculator', mode='r')
        for line in test_file.read().splitlines():
            temp = line.split(';')
            expression = temp[0]
            expected_result = temp[1]
            self.__calculator.calculate_expression(expression)
            print('{:<14}'.format('Expected:'), expected_result, sep='')
            print()

    def test_parser(self):
        pass

    def test_geometry_tool(self):
        test_file = open('test_files/test_geometry_tool')
        for function in test_file.read().splitlines():
            self.__gui.create_function_graph(function)

app = Application()
app.test_geometry_tool()
app.test_calculator()
app.start()
