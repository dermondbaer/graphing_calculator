#   Pascal Mehert
#   06.02.2016
#
#   V 0.1

from tkinter import *


class GuiOutput(object):
    def __init__(self, gui, master):
        self.__gui = gui
        self.__master = master

        self.__frame = Frame(master, padx=10, pady=10)
        self.__frame.pack(side=BOTTOM)

        def scroll_function(event):
            self.__object_list_canvas.configure(scrollregion=canvas.bbox("all"), width=250, height=500)

        outer_frame = Frame(self.__frame, relief=GROOVE, bd=1)
        self.__object_list_outer_frame = outer_frame
        self.__object_list_outer_frame.pack()

        canvas = Canvas(self.__object_list_outer_frame)
        self.__object_list_canvas = canvas

        inner_frame = Frame(self.__object_list_canvas)
        self.__object_list_inner_frame = inner_frame

        scrollbar = Scrollbar(self.__object_list_outer_frame, orient='vertical', command=canvas.yview)
        self.__object_list_scrollbar = scrollbar
        self.__object_list_canvas.configure(yscrollcommand=self.__object_list_scrollbar.set)

        self.__object_list_scrollbar.pack(side="right", fill="y")
        self.__object_list_canvas.pack(side="left")
        self.__object_list_canvas.create_window((0, 0), window=self.__object_list_inner_frame, anchor='nw')
        self.__object_list_inner_frame.bind("<Configure>", scroll_function)
        self.__object_list_index = 0
        self.__object_list_points = []
        self.__object_list_distances = []
        self.__object_list_lines = []
        self.__object_list_functions = []

    def get_gui(self):
        return self.__gui

    def get_master(self):
        return self.__master

    def get_frame(self):
        return self.__frame

    def add_point(self, point):
        x, y = point.get_coordinates()

        if round(x) == x:
            x = round(x)
        if round(y) == y:
            y = round(y)

        label_text = "Punkt ({0}, {1})".format(x, y)
        index = self.__object_list_index
        Label(self.__object_list_inner_frame, text=label_text).grid(row=index, column=0,sticky=W)

        self.__object_list_index += 1
        self.__object_list_points.append(point)

    def add_distance(self, distance):
        start_x, start_y = distance.get_coordinates_a()
        end_x, end_y = distance.get_coordinates_b()

        if round(start_x) == start_x:
            start_x = round(start_x)
        if round(start_y) == start_y:
            start_y = round(start_y)
        if round(end_x) == end_x:
            end_x = round(end_x)
        if round(end_y) == end_y:
            end_y = round(end_y)

        label_text = "Strecke ({0}, {1}), ({2}, {3})".format(start_x, start_y, end_x, end_y)
        index = self.__object_list_index
        Label(self.__object_list_inner_frame, text=label_text).grid(row=index, column=0, sticky=W)

        self.__object_list_index += 1
        self.__object_list_distances.append(distance)

    def add_line(self, line):
        pass

    def add_function(self, function):
        term = function.get_function_term()

        label_text = "f(x) = {0}".format(term)
        index = self.__object_list_index
        Label(self.__object_list_inner_frame, text=label_text).grid(row=index, column=0, sticky=W)

        self.__object_list_index += 1
