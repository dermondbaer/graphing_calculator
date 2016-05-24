#   Pascal Mehnert
#   19.05.2016
#   V 1.0

from tkinter import *
from decimal import *
from geometry_tool.coordinate_system import CoordinateSystem
from geometry_tool.figures import Point, Distance, Line, Function


class Gui(object):
    """Graphical User Interface for a CoordinateSystem. Interface between user and the Coordinate System."""
    def __init__(self, master, target_size_x=1000, target_size_y=1000, default_units_x=10, default_units_y=10):
        """
        :arg master: The parent tkinter element of the Gui.
        :arg target_size_x: The width of the coordinate system in Pixels.
        :arg target_size_y: The height of the coordinate system in Pixels.
        :arg default_units_x: The default amount of units on the x-axis.
        :arg default_units_y: The default amount of units on the y-axis.
        """
        def call_restart(event):
            self.restart()

        def call_clear(event):
            self.clear_figures()

        def call_stop(event):
            self.stop()

        self.__default_unit_count = (Decimal(default_units_x), Decimal(default_units_y))
        target_size_x, target_size_y = Decimal(target_size_x), Decimal(target_size_y)
        self.__target_size = (target_size_x, target_size_y)
        self.__master = master
        self.__master.bind('<F5>', call_restart)
        self.__master.bind('<Delete>', call_clear)
        self.__master.bind('<Escape>', call_stop)
        self.__figures = []

        # Creating the InputDialog and waiting for it to be closed.
        # dialog = InputDialog(((default_units_x, default_units_x), (default_units_y, default_units_y)))
        # units_x, units_y = dialog.get_gui_size()

        # if not units_x:
        #    units_x = (-default_units_x, default_units_x)
        # if not units_y:
        #    units_y = (-default_units_y, default_units_y)

        units_x = (-default_units_x, default_units_x)
        units_y = (-default_units_y, default_units_y)

        # Calculating the scale of the Gui.
        neg_units_x, pos_units_x = units_x
        neg_units_y, pos_units_y = units_y
        scale_x = target_size_x / (abs(neg_units_x) + abs(pos_units_x))
        scale_y = target_size_y / (abs(neg_units_y) + abs(pos_units_y))

        if scale_x > 1:
            scale_x = round(scale_x, 3)
        if scale_y > 1:
            scale_y = round(scale_y, 3)

        # Calculating the absolute of the CoordinateSystem im pixels.
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
        self.__frame = Frame(self.__master)
        self.__frame.pack()
        self.__master.lift()
        self.__master.focus_force()

        # Creating the menu bar.
        self.__menu = Menu(master=self.__frame, bg='red')
        self.__menu.add_command(label='Quit (ESC)', command=self.stop)
        self.__menu.add_command(label='Clear (DEL)', command=self.clear_figures)
        self.__menu.add_command(label='Restart (F5)', command=self.restart)
        self.__master.config(menu=self.__menu)

        self.__coordinate_system = CoordinateSystem(self, self.__frame, absolute_size)

    def start(self):
        """Calls the mainloop for the Gui."""
        self.__master.mainloop()

    def restart(self, resize=True):
        """Destroys the Coordinate System and asks the user to input the size of the Coordinate System,
        that is then being recreated. Previously added figures are being redrawn."""
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

        # Recalculating scale and absolute size of the CoordinateSystem.
        neg_units_x, pos_units_x = units_x
        neg_units_y, pos_units_y = units_y
        scale_x = target_size_x / (abs(neg_units_x) + abs(pos_units_x))
        scale_y = target_size_y / (abs(neg_units_y) + abs(pos_units_y))
        absolute_size_x = (scale_x * neg_units_x, scale_x * pos_units_x)
        absolute_size_y = (scale_y * neg_units_y, scale_y * pos_units_y)
        absolute_size = (absolute_size_x, absolute_size_y)

        if scale_x > 1:
            scale_x = round(scale_x, 3)
        if scale_y > 1:
            scale_y = round(scale_y, 3)

        absolute_size_x = (scale_x * neg_units_x, scale_x * pos_units_x)
        absolute_size_y = (scale_y * neg_units_y, scale_y * pos_units_y)
        absolute_size = (absolute_size_x, absolute_size_y)

        self.__scale = (scale_x, scale_y)
        self.__units = (units_x, units_y)
        self.__coordinate_system.get_canvas().destroy()
        self.__coordinate_system = CoordinateSystem(self, self.__frame, absolute_size)

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
        """Destroys the Gui."""
        self.__master.destroy()
        del self

    def clear_figures(self):
        """Removes all figures from the coordinate system"""
        for figure in self.__figures:
            for tkinter_object in figure.get_tkinter_objects():
                self.__coordinate_system.del_tkinter_object(tkinter_object)
        self.__figures = []

    def get_default_unit_count(self):
        """Returns the default number of units on the x- and y-axis."""
        return self.__default_unit_count

    def get_target_size(self):
        """Returns the size, the CoordinateSystem should match."""
        return self.__target_size

    def get_units(self):
        """Returns the amount of units on the negative and positive parts of the x- and y-axis as"""
        return self.__units

    def get_scale(self):
        """Returns the scale of the x- and y-axis as (scale_x, scale_y)."""
        return self.__scale

    def get_figures(self):
        """Returns a list of all figures in the Gui."""
        return self.__figures

    def get_master(self):
        """Returns the parent tkinter element of the GUI."""
        return self.__master

    def get_frame(self):
        """Returns the main frame of the Gui"""
        return self.__frame

    def create_point(self, coordinates, debug_output=False):
        """Creates a point in the coordinate system at the given coordinates."""
        position, tkinter_object = self.__coordinate_system.create_point(coordinates)
        if debug_output:
            print('Creating Point')
            print('Coordinates:', coordinates)
            print('Position:', position)
            print()

        point = Point(coordinates, position, tkinter_object)
        self.__figures.append(point)
        return point

    def create_distance(self, coord_a, coord_b, debug_output=False):
        """Creates a distance in the coordinate system from point a to point b."""
        pos_a, pos_b, tkinter_objects = self.__coordinate_system.create_distance(coord_a, coord_b)
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

    def create_line(self, support_vector, direction_vector, debug_output=False):
        """Creates a line in the coordinate system with a support and a direction vector."""
        pos_sup, pos_dir, tkinter = self.__coordinate_system.create_line(support_vector, direction_vector)
        line = Line(support_vector, direction_vector, pos_sup, pos_dir, tkinter)
        if debug_output:
            print('Creating Line')
            print('Coordinates Support Vector:', support_vector)
            print('Coordinates Direction Vector:', direction_vector)
            print('Position Support Vector:', pos_sup)
            print('Position Direction Vector:', pos_dir)
            print()

        self.__figures.append(line)
        return line

    def create_function_graph(self, function_term, debug_output=False):
        """Creates a function graph in the coordinate system."""
        if debug_output:
            print('Creating Function Graph')
            print('Function Term:', function_term)
            print()

        tkinter_objects = self.__coordinate_system.create_function_graph(function_term)
        function = Function(function_term, tkinter_objects)
        self.__figures.append(function)
        return function

    def del_figure(self, figure):
        """Deletes a figure from the CoordinateSystem."""
        self.__figures.remove(figure)
        for tkinter_object in figure.get_tkinter_objects():
            self.__coordinate_system.del_tkinter_object(tkinter_object)


class InputDialog(object):
    """Dialog that enables the user the enter the size of a CoordinateSystem."""
    def __init__(self, displayed_size):
        displayed_size_x, displayed_size_y = displayed_size
        display_list = list((*displayed_size_x, *displayed_size_y))

        for index, item in enumerate(display_list):
            temp = str(abs(item))
            display_list[index] = temp.rstrip('0').rstrip('.') if '.' in temp else temp

        displayed_size_neg_x, displayed_size_pos_x, displayed_size_neg_y, displayed_size_pos_y = display_list

        # Grabs the entries, entered into the input fields and validates whether they are correct.
        def get_size(event=None):
            is_decimal = re.compile(r'^-?\d+(\.\d+)?$')

            # Validate the values, entered into the input fields.
            x = y = False
            neg = self.validate_axis_size(is_decimal, input_neg_x)
            pos = self.validate_axis_size(is_decimal, input_pos_x)
            if neg and pos:
                x = True
            if not neg:
                input_neg_x.delete(0, END)
                x = False
            if not pos:
                input_pos_x.delete(0, END)

            neg = self.validate_axis_size(is_decimal, input_neg_y)
            pos = self.validate_axis_size(is_decimal, input_pos_y)
            if neg and pos:
                y = True
            if not neg:
                input_neg_y.delete(0, END)
                y = False
            if not pos:
                input_pos_y.delete(0, END)
                y = False

            # If the values for x and y are correctly entered, set the __size_x and __size_y instance variables.
            if x and y:
                neg_x = -abs(Decimal(input_neg_x.get()))
                pos_x = abs(Decimal(input_pos_x.get()))
                self.__size_x = (neg_x, pos_x)

                neg_y = -abs(Decimal(input_neg_y.get()))
                pos_y = abs(Decimal(input_pos_y.get()))
                self.__size_y = (neg_y, pos_y)

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
        input_neg_x.bind('<Return>', get_size)
        input_neg_x.grid(row=1, column=1)
        input_neg_x.insert(0, displayed_size_neg_x)
        input_neg_x.focus()
        input_neg_x.selection_range(0, END)

        input_pos_x = Entry(dialog, width=10)
        input_pos_x.bind('<Return>', get_size)
        input_pos_x.grid(row=1, column=3)
        input_pos_x.insert(0, displayed_size_pos_x)

        Label(dialog, text='Y: [ -').grid(row=2, column=0, pady=2)
        Label(dialog, text=';  ').grid(row=2, column=2, pady=2)
        Label(dialog, text=']').grid(row=2, column=4, pady=2)

        input_neg_y = Entry(dialog, width=10)
        input_neg_y.bind('<Return>', get_size)
        input_neg_y.grid(row=2, column=1, pady=2)
        input_neg_y.insert(0, displayed_size_neg_y)

        input_pos_y = Entry(dialog, width=10)
        input_pos_y.grid(row=2, column=3, pady=2)
        input_pos_y.bind('<Return>', get_size)
        input_pos_y.insert(0, displayed_size_pos_y)

        button = Button(dialog, text='Create', command=get_size, relief='groove')
        button.bind('<Return>', get_size)
        button.grid(columnspan=5, pady=5)

        def on_closing():
            self.__size_x = self.__size_y = False
            master.destroy()

        # Call the on_closing function if the tkinter master is being forced to close by the user.
        master.protocol("WM_DELETE_WINDOW", on_closing)

        # Wait for the tkinter master to be destroyed
        master.wait_window(master)

    def get_gui_size(self):
        return self.__size_x, self.__size_y

    @staticmethod
    def validate_axis_size(expression, entry_dialog):
        if expression.match(entry_dialog.get()):
            return True
        else:
            return False
