#   Pascal Mehnert
#   29.01.2016
#
#   V 0.1
import parser
from tkinter import *
from math import *

from CoordinateSystem import CoordinateSystem
from GuiOutput import GuiOutput
from UserInput import UserInput
from ValidateInput import validate_axis_size
from Function import Function
from Point import Point
from Distance import Distance
from Line import Line


class Gui(object):
    def __init__(self, resolution_x=1000, resolution_y=1000):
        dialog = GuiDialog()
        size_x, size_y = dialog.get_gui_size()
        del dialog

        neg_x, pos_x = size_x
        neg_y, pos_y = size_y

        if pos_x < neg_x:
            temp = pos_x
            pos_x = neg_x
            neg_x = temp

        if pos_y < neg_y:
            temp = pos_y
            pos_y = neg_y
            neg_y = temp

        if neg_x >= 0:
            neg_x = -1

        if pos_x <= 0:
            pos_x = 1

        if neg_y >= 0:
            neg_y = -1

        if pos_y <= 0:
            pos_y = 1

        scale_x = resolution_x / (abs(neg_x) + abs(pos_x))
        scale_y = resolution_y / (abs(neg_y) + abs(pos_y))

        if scale_x >= 1:
            scale_x = round(scale_x)
        else:
            scale_x = round(scale_x, 10)

        if scale_y >= 1:
            scale_y = round(scale_y)
        else:
            scale_y = round(scale_y, 10)

        absolute_size = ((scale_x * neg_x, scale_x * pos_x), (scale_y * neg_y, scale_y * pos_y))

        self.__scale = (scale_x, scale_y)
        self.__size = (size_x, size_y)
        self.__figures = []
        self.__master = Tk()
        self.__master.wm_title("Koordinatensystem")

        self.__in_out_container = Frame(self.__master)
        self.__in_out_container.pack(side=LEFT)

        self.__user_input = UserInput(self, self.__in_out_container)
        self.__user_input.create_point_input(0, 0)
        self.__user_input.create_function_input(0, 1)
        self.__user_input.create_distance_input(1, 0)
        self.__user_input.create_line_input(1, 1)

        self.__gui_output = GuiOutput(self, self.__in_out_container)
        self.__coordinate_system = CoordinateSystem(self, self.__master, absolute_size)

    def __del__(self):
        self.__master.destroy()

    def get_size(self):
        return self.__size

    def get_scale(self):
        return self.__scale

    def get_figures(self):
        return self.__figures

    def get_coordinate_system(self):
        return self.__coordinate_system

    def get_master(self):
        return self.__master

    def create_point(self, coordinates):
        position, tkinter_object = self.__coordinate_system.create_point(coordinates)
        point = Point(coordinates, position, tkinter_object)
        self.__figures.append(point)
        return point

    def create_distance(self, coord_a, coord_b):
        pos_a, pos_b, tkinter_objects = self.__coordinate_system.create_distance(coord_a, coord_b)
        distance = Distance(coord_a, coord_b, pos_a, pos_b, tkinter_objects)
        self.__figures.append(distance)
        return distance

    def create_line(self, support_vector, direction_vector):
        pos_sup, pos_dir, tkinter = self.__coordinate_system.create_line(support_vector, direction_vector)
        line = Line(support_vector, direction_vector, pos_sup, pos_dir, tkinter)
        self.__figures.append(line)
        return line

    def create_function_graph(self, function_term):
        tkinter_objects = self.__coordinate_system.create_function_graph(function_term)
        function = Function(function_term, tkinter_objects)
        self.__figures.append(function)
        return function

    def del_point(self, point):
        self.__figures.remove(point)
        self.__coordinate_system.del_tkinter_object(point.get_tkinter_object())

    def del_distance(self, distance):
        self.__figures.remove(distance)
        for a in distance.get_tkinter_objects():
            self.__coordinate_system.del_tkinter_object(a)

    def del_line(self, line):
        self.__figures.remove(line)
        self.__coordinate_system.del_tkinter_object(line.get_tkinter_object())

    def del_function_graph(self, function):
        self.__figures.remove(function)
        for a in function.get_tkinter_objects():
            self.__coordinate_system.del_tkinter_object(a)


class GuiDialog(object):
    def __init__(self):
        master = Tk()
        dialog = Frame(master).grid(pady=2)

        Label(dialog, text='X: [ -').grid(row=1, column=0)
        Label(dialog, text=';  ').grid(row=1, column=2)
        Label(dialog, text=']').grid(row=1, column=4)

        input_neg_x = Entry(dialog, width=10)
        input_neg_x.grid(row=1, column=1)
        input_pos_x = Entry(dialog, width=10)
        input_pos_x.grid(row=1, column=3)

        Label(dialog, text='Y: [ -').grid(row=2, column=0, pady=2)
        Label(dialog, text=';  ').grid(row=2, column=2, pady=2)
        Label(dialog, text=']').grid(row=2, column=4, pady=2)

        input_neg_y = Entry(dialog, width=10)
        input_neg_y.grid(row=2, column=1, pady=2)
        input_pos_y = Entry(dialog, width=10)
        input_pos_y.grid(row=2, column=3, pady=2)

        def get_size():
            is_float = re.compile(r'^-?\d+(\.\d+)?$')

            neg = validate_axis_size(is_float, input_neg_x)
            pos = validate_axis_size(is_float, input_pos_x)
            if neg and pos:
                x = True
            if not neg:
                input_neg_x.delete(0, END)
                x = False
            if not pos:
                input_pos_x.delete(0, END)

            neg = validate_axis_size(is_float, input_neg_y)
            pos = validate_axis_size(is_float, input_pos_y)
            if neg and pos:
                y = True
            if not neg:
                input_neg_y.delete(0, END)
                y = False
            if not pos:
                input_pos_y.delete(0, END)
                y = False

            if x and y:
                neg_x = -abs(round(float(input_neg_x.get())))
                pos_x = abs(round(float(input_pos_x.get())))
                self.__size_x = (neg_x, pos_x)

                neg_y = -abs(round(float(input_neg_y.get())))
                pos_y = abs(round(float(input_pos_y.get())))
                self.__size_y = (neg_y, pos_y)
                master.destroy()

        Button(dialog, text='Erstellen', command=get_size).grid(columnspan=5, pady=5)

        master.wait_window(dialog)

    def get_gui_size(self):
        return self.__size_x, self.__size_y
