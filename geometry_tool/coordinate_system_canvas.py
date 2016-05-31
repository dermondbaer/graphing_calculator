#   Pascal Mehnert
#   29.05.2016
#   V 2.0

from tkinter import *
from decimal import *
from math_calculator import Calculator


class CoordinateSystemCanvas(Canvas):
    def __init__(self, coordinate_system, axis_size):
        """
        :arg coordinate_system: The CoordinateSystem, this Canvas belongs to.
        :arg axis_size: The absolute axis size of this CoordinateSystemCanvas.
        """
        self.__coordinate_system = coordinate_system
        self.__master = coordinate_system.get_frame()
        self.__calculator = Calculator()

        self.__axis_size = axis_size
        size_x, size_y = self.__axis_size
        neg_size_x, pos_size_x = size_x
        neg_size_y, pos_size_y = size_y

        # Calculate the absolute position of the coordinate origin.
        origin_x = abs(neg_size_x)
        origin_y = abs(pos_size_y)
        self.__origin = (origin_x, origin_y)

        # Calculate the absolute width of the Canvas in pixels.
        canvas_width = pos_size_x + abs(neg_size_x) + 1
        canvas_height = pos_size_y + abs(neg_size_y) + 1
        self.__canvas_size = (canvas_width, canvas_height)

        Canvas.__init__(self, self.__master, width=canvas_width, height=canvas_height, highlightthickness=0)
        self.__mouse_position = self.create_text(canvas_width-3, canvas_height-1, text='0; 0', anchor='se')

        def set_mouse_position(event):
            """Displays the current mouse position in the bottom right of the Canvas"""
            coordinate_x, coordinate_y = self.get_coordinates((event.x, event.y))
            coordinate_x, coordinate_y = round(coordinate_x, 3), round(coordinate_y, 3)
            self.itemconfig(self.__mouse_position, text='{0}; {1}'.format(coordinate_x, coordinate_y))

        # When the mouse is moved, the set_mouse_position function is being executed.
        self.bind('<Motion>', set_mouse_position)
        self.pack()

        # Draw the lines, representing the x-and y-axis.
        self.create_line((abs(neg_size_x), 0), (abs(neg_size_x), canvas_height))
        self.create_line((0, pos_size_y), (canvas_width, pos_size_y))

        self.__unit_size = self.__coordinate_system.get_scale()
        unit_size_x, unit_size_y = self.__unit_size
        units_x, units_y = self.__coordinate_system.get_units()
        units_x = abs(units_x[0]) + abs(units_x[1])
        units_y = abs(units_y[0]) + abs(units_y[1])

        # Calculate an appropriate scaling for the x-and y-axis, based on the number of units on the respective axis.
        multiplicand_x = 1
        while units_x / multiplicand_x > 40:
            multiplicand_x *= 10
        while units_x / multiplicand_x <= 4:
            multiplicand_x *= Decimal('0.1')
        unit_size_x *= multiplicand_x

        multiplicand_y = 1
        while units_y / multiplicand_y > 40:
            multiplicand_y *= 10
        while units_y / multiplicand_y <= 4:
            multiplicand_y *= Decimal('0.1')
        unit_size_y *= multiplicand_y

        units = self.__coordinate_system.get_units()
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
            self.create_line((margin, origin_y + 6), (margin, origin_y - 7))
            if unit > 0:
                self.create_text((margin, origin_y - 7), text=(-unit * multiplicand_x), font="arial 7", anchor='s')
            margin = origin_x - ((unit + Decimal('0.5')) * unit_size_x)
            self.create_line((margin, origin_y + 4), (margin, origin_y - 5))

        # Draw the scaling on the positive x-axis.
        for unit in range(0, pos_units_x + 1):
            margin = origin_x + (unit * unit_size_x)
            self.create_line((margin, origin_y + 6), (margin, origin_y - 7))
            if unit > 0:
                self.create_text((margin, origin_y - 7), text=(unit * multiplicand_x), font="arial 7", anchor='s')
            margin = origin_x + ((unit + Decimal('0.5')) * unit_size_x)
            self.create_line((margin, origin_y + 4), (margin, origin_y - 5))

        # Draw the scaling on the negative y-axis.
        for unit in range(0, neg_units_y + 1):
            margin = origin_y + (unit * unit_size_y)
            self.create_line((origin_x + 6, margin), (origin_x - 7, margin))
            if unit > 0:
                self.create_text((origin_x + 10, margin), text=(-unit*multiplicand_y), font="arial 7", anchor='w')
            margin = origin_y + ((unit + Decimal('0.5')) * unit_size_y)
            self.create_line((origin_x + 4, margin), (origin_x - 5, margin))

        # Draw the scaling on the positive y-axis.
        for unit in range(0, pos_units_y + 1):
            margin = origin_y - (unit * unit_size_y)
            self.create_line((origin_x + 6, margin), (origin_x - 7, margin))
            if unit > 0:
                self.create_text((origin_x + 10, margin), text=(unit*multiplicand_y), font="arial 7", anchor='w')
            margin = origin_y - ((unit + Decimal('0.5')) * unit_size_y)
            self.create_line((origin_x + 4, margin), (origin_x - 5, margin))

    def get_axis_size(self):
        """Returns the absolute size of the negative and positive x-and y-axis as two dimensional tuple."""
        return self.__axis_size

    def get_canvas_size(self):
        """Returns the absolute height and width of the Canvas as one dimensional tuple."""
        return self.__canvas_size

    def get_origin(self):
        """Returns the absolute position of the coordinate origin as one dimensional tuple."""
        return self.__origin

    def get_master(self):
        """Returns the tkinter master element of this CoordinateSystem."""
        return self.__master

    def get_absolute_position(self, coordinates):
        """Calculates the exact position of a point given in coordinates."""
        x, y = coordinates
        return self._get_absolute_x_position(x), self._get_absolute_y_position(y)

    def _get_absolute_x_position(self, coordinate):
        """Calculates the absolute position of a coordinate on the x-axis."""
        origin_x = self.__origin[0]
        scale_x = self.__unit_size[0]
        return origin_x + (coordinate * scale_x)

    def _get_absolute_y_position(self, coordinate):
        """Calculates the absolute position of a coordinate on the y-axis."""
        origin_y = self.__origin[1]
        scale_y = self.__unit_size[1]
        return origin_y - (coordinate * scale_y)

    def get_coordinates(self, position):
        """Calculates the coordinates of a point, given in pixels."""
        position_x, position_y = position
        origin_x, origin_y = self.__origin
        unit_size_x, unit_size_y = self.__unit_size

        delta_x = position_x - origin_x
        coordinate_x = delta_x / unit_size_x

        delta_y = origin_y - position_y
        coordinate_y = delta_y / unit_size_y

        return coordinate_x, coordinate_y

    def create_point(self, coordinates):
        """Creates a point in this CoordinateSystem."""
        x, y = self.get_absolute_position(coordinates)
        tkinter = self.create_line((x - 3, y), (x + 3, y), (x, y), (x, y - 3), (x, y + 4), fill='red')
        return (x, y), tkinter

    def create_distance(self, coord_a, coord_b):
        """Creates a distance in this CoordinateSystem."""
        tkinter_objects = []

        pos_a = self.get_absolute_position(coord_a)
        pos_b = self.get_absolute_position(coord_b)

        tkinter = self.create_line(pos_a, pos_b)
        tkinter_objects.append(tkinter)

        x, y = pos_a
        tkinter = self.create_line((x - 3, y), (x + 3, y), (x, y), (x, y - 3), (x, y + 4), fill='red')
        tkinter_objects.append(tkinter)

        x, y = pos_b
        tkinter = self.create_line((x - 3, y), (x + 3, y), (x, y), (x, y - 3), (x, y + 4), fill='red')
        tkinter_objects.append(tkinter)

        return pos_a, pos_b, tkinter_objects

    def create_vector_line(self, coord_sup, coord_dir):
        """Creates a line in this CoordinateSystem."""
        pos_sup_vec = self.get_absolute_position(coord_sup)
        pos_dir_vec = self.get_absolute_position(coord_dir)
        coord_sup_x, coord_sup_y = coord_sup
        coord_dir_x, coord_dir_y = coord_dir
        units_x, units_y = self.__coordinate_system.get_units()
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

        tkinter_object = self.create_line(pos_a, pos_b)

        return pos_sup_vec, pos_dir_vec, tkinter_object

    def create_function_graph(self, function_term):
        """Creates a function graph in this CoordinateSystem."""
        parsed_function = self.__calculator.calculate_expression(function_term)

        canvas_size_x, canvas_size_y = self.__canvas_size
        overhang = canvas_size_y / 2

        units_x, units_y = self.__coordinate_system.get_units()
        neg_units_x, pos_units_x = units_x
        scale_x, scale_y = self.__coordinate_system.get_scale()
        full_graph = []
        current_graph_section = []

        def calculate_y_value(x_value, graph_section, unit_margin=1):
            try:
                y_value = self.__calculator.calculate_function_value(parsed_function, {'x': x_value})
                position_x_value, position_y_value = self.get_absolute_position((x_value, y_value))
                if graph_section:
                    if position_y_value < -overhang:
                        graph_section.append((position_x_value, -overhang))
                        full_graph.append(graph_section)
                        graph_section = []
                    elif position_y_value > canvas_size_y + overhang:
                        graph_section.append((position_x_value, canvas_size_y + overhang))
                        full_graph.append(graph_section)
                        graph_section = []
                    else:
                        graph_section.append((position_x_value, position_y_value))

                else:
                    if position_y_value < -overhang:
                        next_x = x_value + unit_margin
                        next_y = self.__calculator.calculate_function_value(parsed_function, {'x': x_value})
                        next_pos_x, next_pos_y = self.get_absolute_position((next_x, next_y))
                        if not next_pos_y < -overhang:
                            graph_section.append((position_x_value, -overhang))
                    elif position_y_value > canvas_size_y + overhang:
                        next_x = x_value + unit_margin
                        next_y = self.__calculator.calculate_function_value(parsed_function, {'x': x_value})
                        next_pos_x, next_pos_y = self.get_absolute_position((next_x, next_y))
                        if not next_pos_y > canvas_size_y + overhang:
                            graph_section.append((position_x_value, canvas_size_y + overhang))
                    else:
                        graph_section.append((position_x_value, position_y_value))

            except ZeroDivisionError:
                if graph_section:
                    full_graph.append(graph_section)
                    graph_section = []

            except (ValueError, OverflowError, InvalidOperation):
                if graph_section:
                    full_graph.append(graph_section)
                    graph_section = []

            return graph_section

        if scale_x <= 1:
            for x in range(int(neg_units_x), int(pos_units_x+1)):
                for fraction in range(0, 5):
                    x += fraction / 4
                    dec_x = Decimal(x)
                    current_graph_section = calculate_y_value(dec_x, current_graph_section)

        else:
            for unit in range(int(neg_units_x) - 2, int(pos_units_x) + 1):
                dec_unit = Decimal(unit)
                for fraction in range(0, int(scale_x) * 4):
                    margin = Decimal(fraction) / (int(scale_x) * 4)
                    dec_x = dec_unit + margin
                    current_graph_section = calculate_y_value(dec_x, current_graph_section, margin)

        if current_graph_section:
            full_graph.append(current_graph_section)

        tkinter_objects = []
        for section in full_graph:
            if len(section) > 1:
                section = [section[i] for i in range(0, len(section), 4)]
                tkinter_objects.append(self.create_line(section, fill='black'))

        return tkinter_objects

    def del_tkinter_object(self, tkinter_object):
        """Deletes a tkinter object from the canvas."""
        self.delete(tkinter_object)
