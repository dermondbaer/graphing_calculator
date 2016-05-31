#   Pascal Mehnert
#   29.01.2016
#
#   V 1.0

from geometry_tool.gui import *
from math_calculator import *


class TestApplication(object):
    def __init__(self):
        self.__master = Tk()
        self.__master.resizable(0, 0)
        self.__gui = Gui(self.__master, target_size_x=900, target_size_y=900)
        self.__calculator = Calculator()

    def start(self):
        self.__gui.start()

    def stop(self):
        self.__gui.stop()

    def test_calculator(self):
        test_file = open('test_files/test_calculator', mode='r')
        for line in test_file.read().splitlines():
            if line[0:2] != '# ':
                temp = line.split(';')
                expression = temp[0]
                expected_result = temp[1]
                self.__calculator.calculate_expression(expression)
                print('{:<14}'.format('Expected:'), expected_result, sep='')
                print()
                print()

    def test_geometry_tool(self):
        test_file = open('test_files/test_geometry_tool')
        for function in test_file.read().splitlines():
            if function[0:2] != '# ':
                self.__gui.create_function_graph(function)


app = TestApplication()
app.test_geometry_tool()
app.test_calculator()
app.start()
