#   Pascal Mehnert
#   05.02.2016
#
#   V 0.1

from tkinter import *


class UserInput(object):
    def __init__(self, gui, master):
        self.__gui = gui
        self.__master = master

        self.__frame = Frame(self.__master, padx=10)
        self.__frame.pack(side=TOP)

        self.__input_frames = []

    def get_gui(self):
        return self.__gui

    def get_master(self):
        return self.__master

    def get_frame(self):
        return self.__frame

    def get_input_frames(self):
        return self.__input_frames

    def create_point_input(self, row, column):
        frame = Frame(self.__frame)
        frame.grid(row=row, column=column, pady=5, padx=5, sticky=N)

        Label(frame, text='Punkt erstellen', font=('Arial', 11)).grid(row=0, column=0, columnspan=2, pady=2, sticky=W)

        Label(frame, text='X-Wert:').grid(row=1)
        Label(frame, text='Y-Wert:').grid(row=2)

        point_input_x = Entry(frame, width=10)
        point_input_x.grid(row=1, column=1, padx=2, pady=2)

        point_input_y = Entry(frame, width=10)
        point_input_y.grid(row=2, column=1, padx=2, pady=2)

        def create_point():
            x = float(point_input_x.get())
            y = float(point_input_y.get())
            self.__gui.create_point((x, y))

        point_button = Button(frame, text='Erstellen', command=create_point)
        point_button.grid(row=3, column=1, pady=2, padx=2, sticky=E)

        self.__input_frames.append(frame)
        return frame

    def create_distance_input(self, row, column):
        frame = Frame(self.__frame)
        frame.grid(row=row, column=column, pady=5, padx=5, sticky=N)

        label = Label(frame, text='Strecke erstellen', font=('Arial', 11))
        label.grid(row=0, column=0, columnspan=2, pady=2, sticky=W)

        Label(frame, text='Punkt A').grid(row=1, columnspan=2, sticky=W)
        Label(frame, text='X-Wert: ').grid(row=2)
        Label(frame, text='Y-Wert: ').grid(row=3)

        point_a_input_x = Entry(frame, width=10)
        point_a_input_x.grid(row=2, column=1, padx=2, pady=2)

        point_a_input_y = Entry(frame, width=10)
        point_a_input_y.grid(row=3, column=1, padx=2, pady=2)

        Label(frame, text='Punkt B').grid(row=4, columnspan=2, sticky=W)
        Label(frame, text='X-Wert: ').grid(row=5)
        Label(frame, text='Y-Wert: ').grid(row=6)

        point_b_input_x = Entry(frame, width=10)
        point_b_input_x.grid(row=5, column=1, padx=2, pady=2)

        point_b_input_y = Entry(frame, width=10)
        point_b_input_y.grid(row=6, column=1, padx=2, pady=2)

        def create_distance():
            x = float(point_a_input_x.get())
            y = float(point_a_input_y.get())
            point_a = (x, y)

            x = float(point_b_input_x.get())
            y = float(point_b_input_y.get())
            point_b = (x, y)

            self.__gui.create_distance(point_a, point_b)

        distance_button = Button(frame, text='Erstellen', command=create_distance)
        distance_button.grid(row=7, column=1, pady=2, padx=2, sticky=E)

        self.__input_frames.append(frame)
        return frame

    def create_line_input(self, row, column):
        frame = Frame(self.__frame)
        frame.grid(row=row, column=column, pady=5, padx=5, sticky=N)

        label = Label(frame, text='Gerade erstellen', font=('Arial', 11))
        label.grid(row=0, column=0, columnspan=2, pady=2, sticky=W)

        Label(frame, text='Stützvektor').grid(row=1, columnspan=2, sticky=W)
        Label(frame, text='X-Wert: ').grid(row=2)
        Label(frame, text='Y-Wert: ').grid(row=3)

        support_vector_input_x = Entry(frame, width=10)
        support_vector_input_x.grid(row=2, column=1, padx=2, pady=2)

        support_vector_input_y = Entry(frame, width=10)
        support_vector_input_y.grid(row=3, column=1, padx=2, pady=2)

        Label(frame, text='Richtungsvektor').grid(row=4, columnspan=2, sticky=W)
        Label(frame, text='X-Wert: ').grid(row=5)
        Label(frame, text='Y-Wert: ').grid(row=6)

        direction_vector_input_x = Entry(frame, width=10)
        direction_vector_input_x.grid(row=5, column=1, padx=2, pady=2)

        direction_vector_input_y = Entry(frame, width=10)
        direction_vector_input_y.grid(row=6, column=1, padx=2, pady=2)

        def create_line():
            x = float(support_vector_input_x.get())
            y = float(support_vector_input_y.get())
            support_vector = (x, y)

            x = float(direction_vector_input_x.get())
            y = float(direction_vector_input_y.get())
            direction_vector = (x, y)

            self.__gui.create_line(support_vector, direction_vector)

        line_button = Button(frame, text='Erstellen', command=create_line)
        line_button.grid(row=7, column=1, pady=2, padx=2, sticky=E)

        self.__input_frames.append(frame)
        return frame

    def create_function_input(self, row, column):
        frame = Frame(self.__frame)
        frame.grid(row=row, column=column, pady=5, padx=5, sticky=N)

        label = Label(frame, text='Graph erstellen', font=('Arial', 11))
        label.grid(row=0, column=0, columnspan=2, pady=2, sticky=W)

        # Label(frame, text='Funktionsgleichung').grid(row=1, columnspan=2, sticky=W)
        Label(frame, text='f(x)=*').grid(row=2)
        label = Label(frame, text='* Syntax Schreibweise', font=('Arial', 8))
        label.grid(row=3, column=0, columnspan=2, sticky=E)

        function_term_input = Entry(frame, width=15)
        function_term_input.grid(row=2, column=1, padx=2, pady=2)

        def create_function():
            term = function_term_input.get()

            self.__gui.create_function_graph(term)

        function_button = Button(frame, text='Erstellen', command=create_function)
        function_button.grid(row=4, column=1, pady=2, padx=2, sticky=E)

        self.__input_frames.append(frame)
        return frame

    def del_input_frame(self, frame):
        self.__input_frames.remove(frame)
        frame.grid_forget()
        frame.destroy()
