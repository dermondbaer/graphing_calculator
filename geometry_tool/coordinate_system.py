#   Pascal Mehnert
#   19.05.2016
#   V 1.0

from tkinter import *
from decimal import *
from math_calculator import Calculator
from geometry_tool.coordinate_system_canvas import CoordinateSystemCanvas
from geometry_tool.figures import Point, Distance, Line, Function
from geometry_tool.figure_dialog import PointDialog, DistanceInput, LineInput


class CoordinateSystem(Frame):
    """Class that is used to interact between the underlying program and the CoordinateSystemCanvas."""
    def __init__(self, master, target_size_x=1000, target_size_y=1000, default_units_x=10, default_units_y=10):
        """
        :arg master: The parent tkinter element of this CoordinateSystem.
        :arg target_size_x: The estimated width of the CoordinateSystem in Pixels.
        :arg target_size_y: The estimated height of the CoordinateSystem in Pixels.
        :arg default_units_x: The default amount of units on the x-axis.
        :arg default_units_y: The default amount of units on the y-axis.
        """
        self.__default_unit_count = (Decimal(default_units_x), Decimal(default_units_y))
        target_size_x, target_size_y = Decimal(target_size_x), Decimal(target_size_y)
        self.__target_size = (target_size_x, target_size_y)
        self.__master = master
        self.__figures = []

        # Binding keys to important functionalities of the CoordinateSystem.
        self.__master.bind('<F5>', lambda event: self.restart())
        self.__master.bind('<Delete>', lambda event: self.clear_figures())
        self.__master.bind('<Escape>', lambda event: self.stop())

        units_x = (-default_units_x, default_units_x)
        units_y = (-default_units_y, default_units_y)

        # Calculating the scale of the CoordinateSystem.
        neg_units_x, pos_units_x = units_x
        neg_units_y, pos_units_y = units_y
        scale_x = target_size_x / (abs(neg_units_x) + abs(pos_units_x))
        scale_y = target_size_y / (abs(neg_units_y) + abs(pos_units_y))

        if scale_x > 1:
            scale_x = round(scale_x, 3)
        if scale_y > 1:
            scale_y = round(scale_y, 3)

        # Calculating the absolute size of this CoordinateSystems Canvas in pixels.
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
        Frame.__init__(self)
        self.grid()
        self.__master.lift()
        self.__master.focus_force()

        # Creating a menu bar.
        # self.__menu = Menu(master=self)
        # self.__menu.add_command(label='Quit (ESC)', command=self.stop)
        # self.__menu.add_command(label='Clear (DEL)', command=self.clear_figures)
        # self.__menu.add_command(label='Restart (F5)', command=self.restart)
        # self.__master.config(menu=self.__menu)

        # Creating the CoordinateSystemCanvas.
        self.__coordinate_system_canvas = CoordinateSystemCanvas(self, absolute_size)

    def start(self):
        """Calls the mainloop for this CoordinateSystem."""
        self.__master.mainloop()

    def restart(self, resize=True):
        """Destroys the CoordinateSystemCanvas and asks the user to reenter the size of the CoordinateSystem.
        The CoordinateSystemCanvas is then being recreated. Previously existent figures are being redrawn."""
        units_x = units_y = False
        if resize:
            dialog = InputDialog(self.__units)
            units_x, units_y = dialog.get_gui_size()

        default_units_x, default_units_y = self.__default_unit_count
        target_size_x, target_size_y = self.__target_size
        if not units_x:
            units_x = (-default_units_x, default_units_x)
        if not units_y:
            units_y = (-default_units_y, default_units_y)

        # Recalculating the scale and the absolute size of this CoordinateSystem.
        neg_units_x, pos_units_x = units_x
        neg_units_y, pos_units_y = units_y
        scale_x = target_size_x / (abs(neg_units_x) + abs(pos_units_x))
        scale_y = target_size_y / (abs(neg_units_y) + abs(pos_units_y))

        if scale_x > 1:
            scale_x = round(scale_x, 3)
        if scale_y > 1:
            scale_y = round(scale_y, 3)

        absolute_size_x = (scale_x * neg_units_x, scale_x * pos_units_x)
        absolute_size_y = (scale_y * neg_units_y, scale_y * pos_units_y)
        absolute_size = (absolute_size_x, absolute_size_y)

        self.__scale = (scale_x, scale_y)
        self.__units = (units_x, units_y)
        self.__coordinate_system_canvas.destroy()
        self.__coordinate_system_canvas = CoordinateSystemCanvas(self, absolute_size)

        print('Recreating Coordinate System')
        print('X-target_size:', target_size_x)
        print('Y-target_size:', target_size_y)
        print('X-actual_size:', scale_x * (abs(neg_units_x) + pos_units_x))
        print('Y-actual_size:', scale_y * (abs(neg_units_y) + pos_units_y))
        print('X-range: ', neg_units_x, '; ', pos_units_x, sep='')
        print('Y-range: ', neg_units_y, '; ', pos_units_y, sep='')
        print('X-scale:', scale_x)
        print('Y-scale:', scale_y)
        print()

        # Redrawing all figures previously existent in the CoordinateSystem.
        figures = self.__figures
        self.__figures = []
        for figure in figures:
            if type(figure) == Point:
                self.create_point(figure.get_coordinates())
            elif type(figure) == Distance:
                self.create_distance(figure.get_coordinates_a(), figure.get_coordinates_b())
            elif type(figure) == Line:
                self.create_line(figure.get_coordinates_support_vector(), figure.get_coordinates_direction_vector())
            elif type(figure) == Function:
                self.create_function_graph(figure.get_function_term())

    def stop(self):
        """Destroys this Gui."""
        self.__master.destroy()
        del self

    def clear_figures(self):
        """Removes all figures from the CoordinateSystem."""
        for figure in self.__figures:
            for tkinter_object in figure.get_tkinter_objects():
                self.__coordinate_system_canvas.del_tkinter_object(tkinter_object)
        self.__figures = []

    def clear_non_graph_figures(self):
        """Removes all figures from the CoordinateSystem, wich are no function graphs."""
        figure_list = self.__figures
        for figure in figure_list:
            if type(figure) != Function:
                self.__figures.remove(figure)
                for tkinter_object in figure.get_tkinter_objects():
                    self.__coordinate_system_canvas.del_tkinter_object(tkinter_object)

    def get_default_unit_count(self):
        """Returns the default number of units on the x-and y-axis."""
        return self.__default_unit_count

    def get_target_size(self):
        """Returns the size, the CoordinateSystem should match."""
        return self.__target_size

    def get_units(self):
        """Returns the amount of units on the negative and positive x-and y-axis."""
        return self.__units

    def get_scale(self):
        """Returns the scale of the x-and y-axis.."""
        return self.__scale

    def get_figures(self):
        """Returns a list of all figures in this Gui."""
        return self.__figures

    def get_master(self):
        """Returns the parent tkinter element of this CoordinateSystem."""
        return self.__master

    def create_point(self, coordinates=False, debug_output=False):
        """Creates a point in this CoordinateSystem at the given coordinates."""
        if not coordinates:
            dialog = PointDialog()
            coordinates = dialog.get_coordinates()
        if coordinates:
            position, tkinter_object = self.__coordinate_system_canvas.create_point(coordinates)

            if debug_output:
                print('Creating Point')
                print('Coordinates:', coordinates)
                print('Position:', position)
                print()

            point = Point(coordinates, position, tkinter_object)
            self.__figures.append(point)
            return point
        else:
            return False

    def create_distance(self, coord_a=False, coord_b=False, debug_output=False):
        """Creates a distance in this CoordinateSystem from point a to point b."""
        if not coord_a or not coord_b:
            dialog = DistanceInput()
            coord_a, coord_b = dialog.get_coordinates()
        if coord_a and coord_b:
            pos_a, pos_b, tkinter_objects = self.__coordinate_system_canvas.create_distance(coord_a, coord_b)

            if debug_output:
                print('Creating Distance')
                print('Coordinates Point A:', coord_a)
                print('Coordinates Point B:', coord_b)
                print('Position Point A:', pos_a)
                print('Position Point B:', pos_b)
                print()

            distance = Distance(coord_a, coord_b, pos_a, pos_b, tkinter_objects)
            self.__figures.append(distance)
            return distance
        else:
            return False

    def create_line(self, support_vector=False, direction_vector=False, debug_output=False):
        """Creates a line in this CoordinateSystem with a support vector and a direction vector."""
        if not support_vector or not direction_vector:
            dialog = LineInput()
            support_vector, direction_vector = dialog.get_coordinates()
        if support_vector and direction_vector:
            pos_sup, pos_dir, tkinter = self.__coordinate_system_canvas.\
                create_vector_line(support_vector, direction_vector)

            if debug_output:
                print('Creating Line')
                print('Coordinates Support Vector:', support_vector)
                print('Coordinates Direction Vector:', direction_vector)
                print('Position Support Vector:', pos_sup)
                print('Position Direction Vector:', pos_dir)
                print()
            line = Line(support_vector, direction_vector, pos_sup, pos_dir, tkinter)
            self.__figures.append(line)
            return line
        else:
            return False

    def create_function_graph(self, function_term, debug_output=False):
        """Creates a function graph in this CoordinateSystem."""
        if debug_output:
            print('Creating Function Graph')
            print('Function Term:', function_term)
            print()

        tkinter_objects = self.__coordinate_system_canvas.create_function_graph(function_term, debug_output)
        function = Function(function_term, tkinter_objects)
        self.__figures.append(function)
        return function

    def del_figure(self, figure):
        """Deletes a figure from this CoordinateSystem."""
        self.__figures.remove(figure)
        for tkinter_object in figure.get_tkinter_objects():
            self.__coordinate_system_canvas.del_tkinter_object(tkinter_object)


class InputDialog(object):
    """Dialog that enables the user the enter the size of a CoordinateSystem."""
    def __init__(self, displayed_size):
        """
        :param displayed_size: The values that should be displayed in the Entry fields.
        :type displayed_size: tuple
        """
        displayed_size_x, displayed_size_y = displayed_size
        neg_x, pos_x = displayed_size_x
        neg_y, pos_y = displayed_size_y
        display_list = list((neg_x, pos_x, neg_y, pos_y))

        for index, item in enumerate(display_list):
            temp = str(abs(item))
            display_list[index] = temp.rstrip('0').rstrip('.') if '.' in temp else temp

        displayed_size_neg_x, displayed_size_pos_x, displayed_size_neg_y, displayed_size_pos_y = display_list

        def get_size():
            """Grabs the entries, entered into the input fields and validates whether they are correct."""
            # Validate the values, entered into the input fields.
            x = y = False
            negative_x = self.validate_axis_size(input_neg_x)
            positive_x = self.validate_axis_size(input_pos_x)
            if negative_x and positive_x:
                x = True
            if not negative_x:
                input_neg_x.delete(0, END)
                x = False
            if not positive_x:
                input_pos_x.delete(0, END)

            negative_y = self.validate_axis_size(input_neg_y)
            positive_y = self.validate_axis_size(input_pos_y)
            if negative_y and positive_y:
                y = True
            if not negative_y:
                input_neg_y.delete(0, END)
                y = False
            if not positive_y:
                input_pos_y.delete(0, END)
                y = False

            # If the values for x and y are correctly entered, set the __size_x and __size_y instance variables.
            if x and y:
                negative_x = -abs(Calculator.calculate_function_value(negative_x, {}))
                positive_x = abs(Calculator.calculate_function_value(positive_x, {}))
                self.__size_x = (negative_x, positive_x)

                negative_y = -abs(Calculator.calculate_function_value(negative_y, {}))
                positive_y = abs(Calculator.calculate_function_value(positive_y, {}))
                self.__size_y = (negative_y, positive_y)

                # Then destroy the tkinter master.
                master.destroy()

        self.__size_x = self.__size_y = False
        master = Tk()
        master.lift()
        master.attributes("-topmost", True)
        master.focus_force()
        dialog = Frame(master)
        dialog.grid(pady=2)
        dialog.focus_set()

        Label(dialog, text='X: [ -').grid(row=1, column=0)
        Label(dialog, text=';  ').grid(row=1, column=2)
        Label(dialog, text=']').grid(row=1, column=4)

        input_neg_x = Entry(dialog, width=10)
        input_neg_x.bind('<Return>', lambda event: get_size())
        input_neg_x.grid(row=1, column=1)
        input_neg_x.insert(0, displayed_size_neg_x)
        input_neg_x.focus()
        input_neg_x.selection_range(0, END)

        input_pos_x = Entry(dialog, width=10)
        input_pos_x.bind('<Return>', lambda event: get_size())
        input_pos_x.grid(row=1, column=3)
        input_pos_x.insert(0, displayed_size_pos_x)

        Label(dialog, text='Y: [ -').grid(row=2, column=0, pady=2)
        Label(dialog, text=';  ').grid(row=2, column=2, pady=2)
        Label(dialog, text=']').grid(row=2, column=4, pady=2)

        input_neg_y = Entry(dialog, width=10)
        input_neg_y.bind('<Return>', lambda event: get_size())
        input_neg_y.grid(row=2, column=1, pady=2)
        input_neg_y.insert(0, displayed_size_neg_y)

        input_pos_y = Entry(dialog, width=10)
        input_pos_y.grid(row=2, column=3, pady=2)
        input_pos_y.bind('<Return>', lambda event: get_size())
        input_pos_y.insert(0, displayed_size_pos_y)

        button = Button(dialog, text='Create', command=get_size, relief='groove')
        button.bind('<Return>', lambda event: get_size())
        button.grid(columnspan=5, pady=5)

        def on_closing():
            self.__size_x = self.__size_y = False
            master.destroy()

        # Call the on_closing function if the tkinter master is being forced to close by the user.
        master.protocol("WM_DELETE_WINDOW", on_closing)

        # Wait for the tkinter master to be destroyed
        master.wait_window(master)

    def get_gui_size(self):
        """Returns the values entered into the Entry fields."""
        return self.__size_x, self.__size_y

    @staticmethod
    def validate_axis_size(entry_dialog):
        """Parses the string entered into an Entry field and returns it as ParserTree.
        Returns False, if the string cannot be parsed."""
        try:
            return Calculator.parse_expression(entry_dialog.get())
        except (ValueError, IndexError):
            return False
