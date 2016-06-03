#   Pascal Mehnert
#   29.01.2016
#
#   V 1.0

from geometry_tool.coordinate_system import *
from math_calculator import *


class TestApplication(Calculator, CoordinateSystem):
    def __init__(self):
        Calculator.__init__(self)
        self.__master = Tk()
        self.__master.resizable(0, 0)
        CoordinateSystem.__init__(self, self.__master, target_size_x=900, target_size_y=900, debug=True)

        # Creating a menu bar.
        self.__menu = Menu(master=self)
        self.__menu.add_command(label='Quit (ESC)', command=self.stop)
        self.__menu.add_command(label='Clear (DEL)', command=self.clear_figures)
        self.__menu.add_command(label='Restart (F5)', command=self.restart)
        self.__master.config(menu=self.__menu)

    def test_calculator(self):
        test_file = open('test_files/test_calculator', mode='r')
        for line in test_file.read().splitlines():
            if line[0:2] != '# ':
                temp = line.split(';')
                expression = temp[0]
                expected_result = temp[1]
                self.calculate_expression(expression, True)
                print('{:<14}'.format('Expected:'), expected_result, sep='')
                print()
                print()

    def test_geometry_tool(self):
        test_file = open('test_files/test_geometry_tool')
        for function in test_file.read().splitlines():
            if function[0:2] != '# ':
                self.create_function_graph(function, True)


app = TestApplication()
# app.test_geometry_tool()
# app.test_calculator()
# app.create_point((1, 2))
# app.create_distance((-3, -2), (-7, -1))
# app.create_line((1, 2), (5, 7))
app.start()
