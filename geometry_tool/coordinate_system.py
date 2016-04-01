#   Pascal Mehnert
#   29.01.2016
#
#   V 0.1

from tkinter import *
from math import *
import parser


class CoordinateSystem(object):
    def __init__(self, gui, master, size):
        self.__gui = gui
        self.__axis_size = size
        self.__master = master

        size_x, size_y = size
        neg_x, pos_x = size_x
        neg_y, pos_y = size_y

        self.__origin = (abs(neg_x), abs(pos_y))

        canvas_width = pos_x - neg_x
        canvas_height = pos_y - neg_y

        self.__frame = Frame(self.__master, borderwidth=1, background='black')
        self.__frame.pack(side=RIGHT)

        self.__canvas = Canvas(self.__frame, width=canvas_width, height=canvas_height, highlightthickness=0)
        self.__canvas.pack()
        self.__canvas_size = (canvas_width, canvas_height)
        self.__canvas.create_line((abs(neg_x), 0), (abs(neg_x), canvas_height))
        self.__canvas.create_line((0, pos_y), (canvas_width, pos_y))

        self.__canvas.create_line((abs(neg_x) - 10, 10), (abs(neg_x), 0), (abs(neg_x) + 11, 11))
        width = canvas_width
        self.__canvas.create_line((width - 11, pos_y - 10), (width - 1, pos_y), (width - 12, pos_y + 11))

        unit_size_x, unit_size_y = self.__gui.get_scale()

        if unit_size_x < 25:
            multiplicand_x = 0
            temp = unit_size_x
            while temp < 25:
                temp = unit_size_x
                multiplicand_x += 5
                temp *= multiplicand_x
            unit_size_x *= multiplicand_x
        elif unit_size_x >= 100:
            multiplicand_x = 1
            temp = unit_size_x
            while temp >= 100:
                temp = unit_size_x
                multiplicand_x /= 2
                temp *= multiplicand_x
            unit_size_x *= multiplicand_x
        else:
            multiplicand_x = 1

        if unit_size_y < 25:
            multiplicand_y = 0
            temp = unit_size_y
            while temp < 25:
                temp = unit_size_y
                multiplicand_y += 5
                temp *= multiplicand_y
            unit_size_y *= multiplicand_y
        elif unit_size_y >= 100:
            multiplicand_y = 1
            temp = unit_size_y
            while temp >= 100:
                temp = unit_size_y
                multiplicand_y /= 2
                temp *= multiplicand_y
            unit_size_y *= multiplicand_y
        else:
            multiplicand_y = 1

        units = self.__gui.get_size()
        units_x, units_y = units
        neg_units_x, pos_units_x = units_x
        neg_units_y, pos_units_y = units_y

        neg_units_x = abs(int(neg_units_x / multiplicand_x))
        pos_units_x = abs(int(pos_units_x / multiplicand_x))
        neg_units_y = abs(int(neg_units_y / multiplicand_y))
        pos_units_y = abs(int(pos_units_y / multiplicand_y))

        origin_x, origin_y = self.__origin

        for i in range(0, neg_units_x):
            margin = origin_x - (i * unit_size_x)
            self.__canvas.create_line((margin, origin_y + 6), (margin, origin_y - 7))
            if i > 0:
                self.__canvas.create_text((margin, origin_y - 15), text=(-i * multiplicand_x), font="arial 7")
            margin = origin_x - ((i + 0.5) * unit_size_x)
            self.__canvas.create_line((margin, origin_y + 4), (margin, origin_y - 5))

        for i in range(0, pos_units_x):
            margin = origin_x + (i * unit_size_x)
            self.__canvas.create_line((margin, origin_y + 6), (margin, origin_y - 7))
            if i > 0:
                self.__canvas.create_text((margin, origin_y + 15), text=(i * multiplicand_x), font="arial 7")
            margin = origin_x + ((i + 0.5) * unit_size_x)
            self.__canvas.create_line((margin, origin_y + 4), (margin, origin_y - 5))

        for i in range(0, neg_units_y):
            margin = origin_y + (i * unit_size_y)
            self.__canvas.create_line((origin_x + 6, margin), (origin_x - 7, margin))
            if i > 0:
                self.__canvas.create_text((origin_x - 15, margin), text=(-i * multiplicand_y), font="arial 7")
            margin = origin_y + ((i + 0.5) * unit_size_y)
            self.__canvas.create_line((origin_x + 4, margin), (origin_x - 5, margin))

        for i in range(0, pos_units_y):
            margin = origin_y - (i * unit_size_y)
            self.__canvas.create_line((origin_x + 6, margin), (origin_x - 7, margin))
            if i > 0:
                self.__canvas.create_text((origin_x + 15, margin), text=(i * multiplicand_y), font="arial 7")
            margin = origin_y - ((i + 0.5) * unit_size_y)
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
        scale_x, scale_y = self.__gui.get_scale()

        abs_pos_x = origin_x + (x * scale_x)
        abs_pos_y = origin_y - (y * scale_y)

        return abs_pos_x, abs_pos_y

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
        pos_sup = self.get_absolute_position(coord_sup)
        pos_dir = self.get_absolute_position(coord_dir)
        sup_x, sup_y = coord_sup
        dir_x, dir_y = coord_dir
        size_x, size_y = self.__gui.get_size()
        neg_x, pos_x = size_x
        neg_y, pos_y = size_y

        if pos_x >= abs(neg_x):
            max_x = pos_x
        else:
            max_x = abs(neg_x)

        if pos_y >= abs(neg_y):
            max_y = pos_y
        else:
            max_y = abs(neg_y)

        x = y = 0
        t = 10

        while abs(x) < max_x and abs(y) < max_y:
            x = sup_x + t * dir_x
            y = sup_y + t * dir_y
            t += 10
        point_a = (x, y)

        x = y = 0
        t = -10

        while abs(x) < max_x and abs(y) < max_y:
            x = sup_x + t * dir_x
            y = sup_y + t * dir_y
            t -= 10
        point_b = (x, y)

        pos_a = self.get_absolute_position(point_a)
        pos_b = self.get_absolute_position(point_b)

        tkinter_object = self.__canvas.create_line(pos_a, pos_b)

        return pos_sup, pos_dir, tkinter_object

    def create_function_graph(self, function_term):
        function = parser.expr(function_term).compile()

        size_x, size_y = self.__gui.get_size()
        neg_x, pos_x = size_x
        scale_x, scale_y = self.__gui.get_scale()
        graph = [[]]

        if scale_x >= 1:
            for a in range(neg_x, pos_x):
                for b in range(0, scale_x):
                    x = a + (b / scale_x)
                    try:
                        y = eval(function)
                        pos = self.get_absolute_position((x, y))
                        graph[-1].append(pos)
                    except ZeroDivisionError:
                        if graph[-1]:
                            graph.append([])
                    except ValueError:
                        if graph[-1]:
                            graph.append([])
        else:
            for x in range(neg_x, pos_x):
                try:
                    y = eval(function)
                    pos = self.get_absolute_position((x, y))
                    graph[-1].append(pos)
                except ZeroDivisionError:
                    if graph[-1]:
                        graph.append([])
                except ValueError:
                    if graph[-1]:
                        graph.append([])

        tkinter_objects = []
        for a in graph:
            tkinter_objects.append(self.__canvas.create_line(a))

        return tkinter_objects

    def del_tkinter_object(self, tkinter_object):
        self.__canvas.delete(tkinter_object)
