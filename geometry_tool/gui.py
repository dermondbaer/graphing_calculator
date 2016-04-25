#   Pascal Mehnert
#   29.01.2016
#
#   V 0.1

from tkinter import *

from geometry_tool.coordinate_system import CoordinateSystem
from geometry_tool.user_input import UserInput
from geometry_tool.figures import Point, Distance, Line, Function


class Gui(object):
    """Graphical User Interface for a CoordinateSystem."""
    def __init__(self, window_title, target_size_x=1000, target_size_y=1000, default_units_x=10, default_units_y=10):
        """
        :arg window_title: The title to display for the coordinate system.
        :type window_title: str
        :arg target_size_x: The width of the coordinate system in Pixels.
        :type target_size_x: int
        :arg target_size_y: The height of the coordinate system in Pixels.
        :type target_size_y: int
        :arg default_units_x: The default amount of units on the x-axis.
        :type default_units_x: int
        :arg default_units_y: The default amount of units on the y-axis.
        :type default_units_y: int
        """
        dialog = InputDialog()
        units_x, units_y = dialog.get_gui_size()

        if not units_x:
            units_x = (-default_units_x, default_units_x)
        if not units_y:
            units_y = (-default_units_y, default_units_y)

        neg_units_x, pos_units_x = units_x
        neg_units_y, pos_units_y = units_y
        scale_x = target_size_x / (abs(neg_units_x) + abs(pos_units_x))
        scale_y = target_size_y / (abs(neg_units_y) + abs(pos_units_y))
        absolute_size_x = (scale_x * neg_units_x, scale_x * pos_units_x)
        absolute_size_y = (scale_y * neg_units_y, scale_y * pos_units_y)
        absolute_size = (absolute_size_x, absolute_size_y)

        print('Creating Coordinate System')
        print('X-target_size:', target_size_x)
        print('Y-target_size:', target_size_y)
        print('X-actual_size:', scale_x * (abs(neg_units_x) + pos_units_x))
        print('Y-actual_size:', scale_y * (abs(neg_units_y) + pos_units_y))
        print('X-range: ', neg_units_x, '; ', pos_units_x, sep='')
        print('Y-range: ', neg_units_y, '; ', pos_units_y, sep='')
        print('X-scale:', scale_x)
        print('Y-scale:', scale_y)
        print()

        self.__scale = (scale_x, scale_y)
        self.__units = (units_x, units_y)
        self.__figures = []
        self.__master = Tk()
        self.__master.wm_title(window_title)
        self.__master.resizable(0, 0)

        self.__menu = Menu(master=self.__master)
        self.__menu.add_command(label='Quit', command=self.stop)
        self.__menu.add_command(label='Clear', command=self.clear_figures)
        self.__master.config(menu=self.__menu)

        self.__in_out_container = Frame(self.__master)
        self.__in_out_container.pack(side=LEFT)

        self.__user_input = UserInput(self, self.__in_out_container)
        self.__user_input.create_point_input(0, 0)
        self.__user_input.create_function_input(0, 1)
        self.__user_input.create_distance_input(1, 0)
        self.__user_input.create_line_input(1, 1)

        # self.__gui_output = GuiOutput(self, self.__in_out_container)

        self.__coordinate_system = CoordinateSystem(self, self.__master, absolute_size)

    def start(self):
        """Calls the mainloop for the Gui."""
        self.__master.mainloop()

    def stop(self):
        """Destroys the Gui."""
        self.__master.destroy()
        del self

    def clear_figures(self):
        """Removes all figures from the coordinate system"""
        for figure in self.__figures:
            for tkinter_object in figure.get_tkinter_objects():
                self.__coordinate_system.del_tkinter_object(tkinter_object)
        self.__figures = []

    def get_units(self):
        """Returns the amount of units on the negative and positive parts of the x- and y-axis as
        ((negative_units_x, positive_units_x), (negative_units_y, positive_units_x))"""
        return self.__units

    def get_scale(self):
        """Returns the scale of the x- and y-axis as (scale_x, scale_y)."""
        return self.__scale

    def get_figures(self):
        """Returns a list of all figures in the GUI."""
        return self.__figures

    def get_master(self):
        """Returns the tkinter root of the GUI."""
        return self.__master

    def create_point(self, coordinates):
        """
        Creates a point in the coordinate system at the given coordinates.

        :arg coordinates: The coordinates of the Point.
        :type coordinates: tuple
        :rtype: Point
        """
        position, tkinter_object = self.__coordinate_system.create_point(coordinates)
        print('Creating Point')
        print('Coordinates:', coordinates)
        print('Position:', position)
        print()
        point = Point(coordinates, position, tkinter_object)
        self.__figures.append(point)
        return point

    def create_distance(self, coord_a, coord_b):
        """
        Creates a distance in the coordinate system from point a to point b.

        :arg coord_a: The coordinates for the beginning of the distance.
        :type coord_a: tuple
        :arg coord_b: The coordinates for the ending of the distance.
        :type coord_b: tuple
        :rtype: Distance
        """
        pos_a, pos_b, tkinter_objects = self.__coordinate_system.create_distance(coord_a, coord_b)
        print('Creating Distance')
        print('Coordinates Point A:', coord_a)
        print('Coordinates Point B:', coord_b)
        print('Position Point A:', pos_a)
        print('Position Point B:', pos_b)
        print()
        distance = Distance(coord_a, coord_b, pos_a, pos_b, tkinter_objects)
        self.__figures.append(distance)
        return distance

    def create_line(self, support_vector, direction_vector):
        """
        Creates a line in the coordinate system with a support and a direction vector.

        :arg support_vector: The support vector of the line.
        :type support_vector: tuple
        :arg direction_vector: The direction vector of the line.
        :type direction_vector: tuple
        :rtype: Line
        """
        pos_sup, pos_dir, tkinter = self.__coordinate_system.create_line(support_vector, direction_vector)
        line = Line(support_vector, direction_vector, pos_sup, pos_dir, tkinter)
        print('Creating Line')
        print('Coordinates Support Vector:', support_vector)
        print('Coordinates Direction Vector:', direction_vector)
        print('Position Support Vector:', pos_sup)
        print('Position Direction Vector:', pos_dir)
        print()
        self.__figures.append(line)
        return line

    def create_function_graph(self, function_term):
        """
        Creates a function graph in the coordinate system.

        :arg function_term: The corresponding term to the function graph.
        :type function_term: str
        :rtype: Function
        """
        print('Creating Function Graph')
        print('Function Term:', function_term)
        print()
        tkinter_objects = self.__coordinate_system.create_function_graph(function_term)
        function = Function(function_term, tkinter_objects)
        self.__figures.append(function)
        return function

    def del_point(self, point):
        """
        Deletes a point from the coordinate system.

        :arg point: The point to delete.
        :type point: Point
        """
        self.__figures.remove(point)
        self.__coordinate_system.del_tkinter_object(point.get_tkinter_objects())

    def del_distance(self, distance):
        """
        Deletes a distance form the coordinate system.

        :arg distance: The distance to delete.
        :type distance: Distance
        """
        self.__figures.remove(distance)
        for a in distance.get_tkinter_objects():
            self.__coordinate_system.del_tkinter_object(a)

    def del_line(self, line):
        """
        Deletes a line from the coordinate system.

        :arg line: The line to delete.
        :type line: Line
        """
        self.__figures.remove(line)
        self.__coordinate_system.del_tkinter_object(line.get_tkinter_objects())

    def del_function_graph(self, function):
        """
        Deletes a function graph from the coordinate system.

        :arg function: The function graph to delete.
        :type function: Function
        """
        self.__figures.remove(function)
        for a in function.get_tkinter_objects():
            self.__coordinate_system.del_tkinter_object(a)


class InputDialog(object):
    def __init__(self):
        def get_size():
            is_float = re.compile(r'^-?\d+(\.\d+)?$')

            x = y = False
            neg = self.validate_axis_size(is_float, input_neg_x)
            pos = self.validate_axis_size(is_float, input_pos_x)
            if neg and pos:
                x = True
            if not neg:
                input_neg_x.delete(0, END)
                x = False
            if not pos:
                input_pos_x.delete(0, END)

            neg = self.validate_axis_size(is_float, input_neg_y)
            pos = self.validate_axis_size(is_float, input_pos_y)
            if neg and pos:
                y = True
            if not neg:
                input_neg_y.delete(0, END)
                y = False
            if not pos:
                input_pos_y.delete(0, END)
                y = False

            if x and y:
                neg_x = -abs(float(input_neg_x.get()))
                pos_x = abs(float(input_pos_x.get()))
                self.__size_x = (neg_x, pos_x)

                neg_y = -abs(float(input_neg_y.get()))
                pos_y = abs(float(input_pos_y.get()))
                self.__size_y = (neg_y, pos_y)
                master.destroy()

        def call_get_size(event):
            get_size()

        self.__size_x = self.__size_y = False
        master = Tk()
        dialog = Frame(master)
        dialog.grid(pady=2)
        dialog.focus_set()

        Label(dialog, text='X: [ -').grid(row=1, column=0)
        Label(dialog, text=';  ').grid(row=1, column=2)
        Label(dialog, text=']').grid(row=1, column=4)

        input_neg_x = Entry(dialog, width=10)
        input_neg_x.bind('<Return>', call_get_size)
        input_neg_x.grid(row=1, column=1)
        input_pos_x = Entry(dialog, width=10)
        input_pos_x.bind('<Return>', call_get_size)
        input_pos_x.grid(row=1, column=3)

        Label(dialog, text='Y: [ -').grid(row=2, column=0, pady=2)
        Label(dialog, text=';  ').grid(row=2, column=2, pady=2)
        Label(dialog, text=']').grid(row=2, column=4, pady=2)

        input_neg_y = Entry(dialog, width=10)
        input_neg_y.bind('<Return>', call_get_size)
        input_neg_y.grid(row=2, column=1, pady=2)
        input_pos_y = Entry(dialog, width=10)
        input_pos_y.grid(row=2, column=3, pady=2)
        input_pos_y.bind('<Return>', call_get_size)
        button = Button(dialog, text='Create', command=get_size)
        button.bind('<Return>', call_get_size)
        button.grid(columnspan=5, pady=5)

        def on_closing():
            self.__size_x = self.__size_y = False
            master.destroy()

        master.protocol("WM_DELETE_WINDOW", on_closing)

        master.wait_window(dialog)

    def get_gui_size(self):
        return self.__size_x, self.__size_y

    @staticmethod
    def validate_axis_size(expression, entry_dialog):
        if expression.match(entry_dialog.get()):
            return True
        else:
            return False
