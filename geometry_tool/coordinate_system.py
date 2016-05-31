#   Pascal Mehnert
#   29.01.2016
#   V 2.0

from tkinter import *
from decimal import *
from math_calculator import Calculator


class CoordinateSystem(object):
    def __init__(self, gui, master, axis_size):
        """
        :arg gui: The Gui, the CoordinateSystem belongs to.
        :arg master: The Tkinter master widget.
        :arg axis_size: The absolute axis size of the CoordinateSystem.
        """
        self.__gui = gui
        self.__master = master
        self.__calculator = Calculator()

        size_x, size_y = axis_size
        neg_size_x, pos_size_x = size_x
        neg_size_y, pos_size_y = size_y
        self.__axis_size = axis_size

        origin_x = abs(neg_size_x)
        origin_y = abs(pos_size_y)
        self.__origin = (origin_x, origin_y)

        canvas_width = pos_size_x + abs(neg_size_x) + 1
        canvas_height = pos_size_y + abs(neg_size_y) + 1
        self.__canvas_size = (canvas_width, canvas_height)

        self.__canvas = Canvas(self.__master, width=canvas_width, height=canvas_height, highlightthickness=0,
                               bg='white')
        self.__mouse_position = self.__canvas.create_text(canvas_width-3, canvas_height-1, text='0; 0', anchor='se')

        def set_mouse_position(event):
            coordinate_x, coordinate_y = self.get_coordinates((event.x, event.y))
            coordinate_x, coordinate_y = round(coordinate_x, 3), round(coordinate_y, 3)
            self.__canvas.itemconfig(self.__mouse_position, text='{0}; {1}'.format(coordinate_x, coordinate_y))

        # When the mouse is moved, the set_mouse_position function is being executed.
        self.__canvas.bind('<Motion>', set_mouse_position)
        self.__canvas.pack()

        # Draw the lines, representing the x-and y-axis.
        self.__canvas.create_line((abs(neg_size_x), 0), (abs(neg_size_x), canvas_height))
        self.__canvas.create_line((0, pos_size_y), (canvas_width, pos_size_y))

        self.__unit_size = self.__gui.get_scale()
        unit_size_x, unit_size_y = self.__unit_size

        # Calculate an appropriate scaling for the x-and y-axis, based on the unit size of the respective axis.
        if unit_size_x < 20:
            multiplicand_x = 10
            while unit_size_x * multiplicand_x < 20:
                multiplicand_x *= 10
            unit_size_x *= multiplicand_x
        elif unit_size_x > 100:
            multiplicand_x = Decimal('0.1')
            while unit_size_x * multiplicand_x > 100:
                multiplicand_x /= 10
            unit_size_x *= multiplicand_x
        else:
            multiplicand_x = 1

        if unit_size_y < 20:
            multiplicand_y = 10
            while unit_size_y * multiplicand_y < 20:
                multiplicand_y *= 10
            unit_size_y *= multiplicand_y
        elif unit_size_y > 100:
            multiplicand_y = Decimal('0.1')
            while unit_size_y * multiplicand_y > 100:
                multiplicand_y /= 10
            unit_size_y *= multiplicand_y
        else:
            multiplicand_y = 1

        units = self.__gui.get_units()
        units_x, units_y = units
        neg_units_x, pos_units_x = units_x
        neg_units_y, pos_units_y = units_y

        # Calculate the number of units displayed on the x-and y-axis, based on the scaling previously computed.
        neg_units_x = abs(int(neg_units_x / multiplicand_x))
        pos_units_x = abs(int(pos_units_x / multiplicand_x))
        neg_units_y = abs(int(neg_units_y / multiplicand_y))
        pos_units_y = abs(int(pos_units_y / multiplicand_y))

        # Draw the scaling on the negative x-axis.
        for unit in range(0, neg_units_x + 1):
            margin = origin_x - (unit * unit_size_x)
            self.__canvas.create_line((margin, origin_y + 6), (margin, origin_y - 7))
            if unit > 0:
                self.__canvas.create_text((margin, origin_y - 15), text=(-unit * multiplicand_x), font="arial 7")
            margin = origin_x - ((unit + Decimal('0.5')) * unit_size_x)
            self.__canvas.create_line((margin, origin_y + 4), (margin, origin_y - 5))

        # Draw the scaling on the positive x-axis.
        for unit in range(0, pos_units_x + 1):
            margin = origin_x + (unit * unit_size_x)
            self.__canvas.create_line((margin, origin_y + 6), (margin, origin_y - 7))
            if unit > 0:
                self.__canvas.create_text((margin, origin_y + 15), text=(unit * multiplicand_x), font="arial 7")
            margin = origin_x + ((unit + Decimal('0.5')) * unit_size_x)
            self.__canvas.create_line((margin, origin_y + 4), (margin, origin_y - 5))

        # Draw the scaling on the negative y-axis.
        for unit in range(0, neg_units_y + 1):
            margin = origin_y + (unit * unit_size_y)
            self.__canvas.create_line((origin_x + 6, margin), (origin_x - 7, margin))
            if unit > 0:
                self.__canvas.create_text((origin_x-10, margin), text=(-unit*multiplicand_y), font="arial 7", anchor='e')
            margin = origin_y + ((unit + Decimal('0.5')) * unit_size_y)
            self.__canvas.create_line((origin_x + 4, margin), (origin_x - 5, margin))

        # Draw the scaling on the positive y-axis.
        for unit in range(0, pos_units_y + 1):
            margin = origin_y - (unit * unit_size_y)
            self.__canvas.create_line((origin_x + 6, margin), (origin_x - 7, margin))
            if unit > 0:
                self.__canvas.create_text((origin_x+10, margin), text=(unit*multiplicand_y), font="arial 7", anchor='w')
            margin = origin_y - ((unit + Decimal('0.5')) * unit_size_y)
            self.__canvas.create_line((origin_x + 4, margin), (origin_x - 5, margin))

    def get_gui(self):
        return self.__gui

    def get_axis_size(self):
        return self.__axis_size

    def get_canvas_size(self):
        return self.__canvas_size

    def get_origin(self):
        return self.__origin

    def get_master(self):
        return self.__master

    def get_canvas(self):
        return self.__canvas

    def get_absolute_position(self, coordinates):
        x, y = coordinates
        origin_x, origin_y = self.__origin
        scale_x, scale_y = self.__unit_size
        abs_pos_x = origin_x + (x * scale_x)
        abs_pos_y = origin_y - (y * scale_y)

        return abs_pos_x, abs_pos_y

    def get_coordinates(self, position):
        position_x, position_y = position
        origin_x, origin_y = self.__origin
        unit_size_x, unit_size_y = self.__unit_size

        delta_x = position_x - origin_x
        coordinate_x = delta_x / unit_size_x

        delta_y = origin_y - position_y
        coordinate_y = delta_y / unit_size_y

        return coordinate_x, coordinate_y

    def create_point(self, coordinates):
        x, y = self.get_absolute_position(coordinates)
        tkinter = self.__canvas.create_line((x - 3, y), (x + 3, y), (x, y), (x, y - 3), (x, y + 4), fill='red')
        return (x, y), tkinter

    def create_distance(self, coord_a, coord_b):
        tkinter_objects = []

        pos_a = self.get_absolute_position(coord_a)
        pos_b = self.get_absolute_position(coord_b)

        tkinter = self.__canvas.create_line(pos_a, pos_b)
        tkinter_objects.append(tkinter)

        x, y = pos_a
        tkinter = self.__canvas.create_line((x - 3, y), (x + 3, y), (x, y), (x, y - 3), (x, y + 4), fill='red')
        tkinter_objects.append(tkinter)

        x, y = pos_b
        tkinter = self.__canvas.create_line((x - 3, y), (x + 3, y), (x, y), (x, y - 3), (x, y + 4), fill='red')
        tkinter_objects.append(tkinter)

        return pos_a, pos_b, tkinter_objects

    def create_line(self, coord_sup, coord_dir):
        pos_sup_vec = self.get_absolute_position(coord_sup)
        pos_dir_vec = self.get_absolute_position(coord_dir)
        coord_sup_x, coord_sup_y = coord_sup
        coord_dir_x, coord_dir_y = coord_dir
        units_x, units_y = self.__gui.get_units()
        neg_units_x, pos_units_x = units_x
        neg_units_y, pos_units_y = units_y

        bound_x = max(pos_units_x, abs(neg_units_x))
        bound_y = max(pos_units_y, abs(neg_units_y))

        x = y = 0
        t = 1

        while abs(x) < bound_x and abs(y) < bound_y:
            x = coord_sup_x + t * coord_dir_x
            y = coord_sup_y + t * coord_dir_y
            t *= 2
        point_a = (x, y)

        x = y = 0
        t = -1

        while abs(x) < bound_x and abs(y) < bound_y:
            x = coord_sup_x + t * coord_dir_x
            y = coord_sup_y + t * coord_dir_y
            t *= 2
        point_b = (x, y)

        pos_a = self.get_absolute_position(point_a)
        pos_b = self.get_absolute_position(point_b)

        tkinter_object = self.__canvas.create_line(pos_a, pos_b)

        return pos_sup_vec, pos_dir_vec, tkinter_object

    def create_function_graph(self, function_term):
        parsed_function = self.__calculator.calculate_expression(function_term)

        canvas_size_x, canvas_size_y = self.__canvas_size
        overhang = canvas_size_y * 2

        units_x, units_y = self.__gui.get_units()
        neg_units_x, pos_units_x = units_x
        scale_x, scale_y = self.__gui.get_scale()
        full_graph = []
        current_graph_section = []

        if scale_x <= 1:
            for x in range(int(neg_units_x), int(pos_units_x+1)):
                dec_x = Decimal(x)
                try:
                    y = self.__calculator.calculate_function_value(parsed_function, {'x': dec_x})
                    position_x, position_y = self.get_absolute_position((dec_x, y))
                    if position_y < -overhang:
                        if current_graph_section:
                            current_graph_section.append((position_x, -overhang))
                            full_graph.append(current_graph_section)
                            current_graph_section = []
                    elif position_y > canvas_size_y + overhang:
                        if current_graph_section:
                            current_graph_section.append((position_x, canvas_size_y + overhang))
                            full_graph.append(current_graph_section)
                            current_graph_section = []
                    else:
                        current_graph_section.append((position_x, position_y))

                except (ZeroDivisionError, ValueError, OverflowError, InvalidOperation):
                    if current_graph_section:
                        full_graph.append(current_graph_section)
                        current_graph_section = []

        else:
            for unit in range(int(neg_units_x), int(pos_units_x)+1):
                dec_unit = Decimal(unit)
                for fraction in range(0, int(scale_x)):
                    dec_fraction = Decimal(fraction)
                    x = unit + (fraction / int(scale_x))
                    dec_x = dec_unit + (dec_fraction / int(scale_x))
                    try:
                        y = self.__calculator.calculate_function_value(parsed_function, {'x': dec_x})
                        position_x, position_y = self.get_absolute_position((dec_x, y))
                        if position_y < -overhang:
                            if current_graph_section:
                                current_graph_section.append((position_x, -overhang))
                                full_graph.append(current_graph_section)
                                current_graph_section = []
                        elif position_y > canvas_size_y + overhang:
                            if current_graph_section:
                                current_graph_section.append((position_x, canvas_size_y + overhang))
                                full_graph.append(current_graph_section)
                                current_graph_section = []
                        else:
                            current_graph_section.append((position_x, position_y))

                    except (ZeroDivisionError, ValueError, OverflowError, InvalidOperation):
                        if current_graph_section:
                            full_graph.append(current_graph_section)
                            current_graph_section = []

        if current_graph_section:
            full_graph.append(current_graph_section)

        tkinter_objects = []
        for a in full_graph:
            tkinter_objects.append(self.__canvas.create_line(a, fill='black'))

        return tkinter_objects

    def del_tkinter_object(self, tkinter_object):
        self.__canvas.delete(tkinter_object)
