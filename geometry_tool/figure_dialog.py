# Pascal Mehnert
# 03.06.2016
# Dialogs used to input figure information.
# V 0.1

from tkinter import *
import math_calculator


class FigureDialog(object):
    @staticmethod
    def validate_entry(entry_dialog):
        try:
            return math_calculator.Calculator.parse_expression(entry_dialog.get())
        except (ValueError, IndexError, AttributeError, KeyError):
            return False


class PointDialog(FigureDialog):
    def __init__(self):
        self.__coordinates = []
        master = Tk()
        master.resizable(0, 0)
        master.title('Create Point')
        master.lift()
        master.attributes('-topmost', True)
        master.focus_force()
        dialog = Frame(master)
        dialog.grid(pady=5)
        dialog.focus_set()

        def set_false():
            self.__coordinates = []

        def on_closing():
            set_false()
            master.destroy()

        def get_coordinates():
            x = y = False
            parser_tree_x = self.validate_entry(input_x)
            parser_tree_y = self.validate_entry(input_y)

            if parser_tree_x and parser_tree_y:
                x = y = True

            if parser_tree_x.is_empty() or parser_tree_y.is_empty():
                x = y = False

            if not parser_tree_x:
                input_x.delete(0, END)
                x = False

            if not parser_tree_y:
                input_y.delete(0, END)
                y = False

            if x and y:
                coordinate_x = math_calculator.Calculator.calculate_function_value(parser_tree_x, {})
                coordinate_y = math_calculator.Calculator.calculate_function_value(parser_tree_y, {})
                self.__coordinates = coordinate_x, coordinate_y

                master.destroy()

        master.protocol('WM_DELETE_WINDOW', on_closing)

        label_font = 'arial 12'

        Label(dialog, text='P (', font=label_font).grid(row=1, column=0)
        Label(dialog, text=' | ', font=label_font, anchor=N).grid(row=1, column=2)
        Label(dialog, text=')', font=label_font).grid(row=1, column=4)

        input_x = Entry(dialog, width=8, justify=CENTER)
        input_x.bind('<Return>', lambda event: get_coordinates())
        input_x.grid(row=1, column=1)
        input_x.focus()
        input_x.selection_range(0, END)

        input_y = Entry(dialog, width=8, justify=CENTER)
        input_y.bind('<Return>', lambda event: get_coordinates())
        input_y.grid(row=1, column=3)

        button = Button(dialog, text='Create', command=get_coordinates, relief='groove', bg='orange')
        button.bind('<Return>', lambda event: get_coordinates())
        button.grid(columnspan=5, pady=5)

        master.wait_window(master)

    def get_coordinates(self):
        return self.__coordinates


class DistanceInput(FigureDialog):
    def __init__(self):
        self.__coordinates_p = []
        self.__coordinates_q = []
        master = Tk()
        master.resizable(0, 0)
        master.title('Create Point')
        master.lift()
        master.attributes('-topmost', True)
        master.focus_force()
        dialog = Frame(master)
        dialog.grid(pady=5)
        dialog.focus_set()

        def set_false():
            self.__coordinates_p = []
            self.__coordinates_q = []

        def on_closing():
            set_false()
            master.destroy()

        def get_coordinates():
            p_x = p_y = q_x = q_y = False
            parser_tree_p_x = self.validate_entry(input_p_x)
            parser_tree_p_y = self.validate_entry(input_p_y)
            parser_tree_q_x = self.validate_entry(input_q_x)
            parser_tree_q_y = self.validate_entry(input_q_y)

            if parser_tree_p_x and parser_tree_p_y:
                p_x = p_y = True
            if parser_tree_q_x and parser_tree_q_y:
                q_x = q_y = True

            if p_x and p_y and q_x and q_y:
                if parser_tree_p_x.is_empty() or parser_tree_p_y.is_empty():
                    p_x = p_y = False
                if parser_tree_q_x.is_empty() or parser_tree_q_y.is_empty():
                    q_x = q_y = False

            if not parser_tree_p_x:
                input_p_x.delete(0, END)
                p_x = False
            if not parser_tree_p_y:
                input_p_y.delete(0, END)
                p_y = False
            if not parser_tree_q_x:
                input_q_x.delete(0, END)
                q_x = False
            if not parser_tree_q_y:
                input_q_y.delete(0, END)
                q_y = False

            if p_x and p_y and q_x and q_y:
                coordinate_x = math_calculator.Calculator.calculate_function_value(parser_tree_p_x, {})
                coordinate_y = math_calculator.Calculator.calculate_function_value(parser_tree_p_y, {})
                self.__coordinates_p = coordinate_x, coordinate_y

                coordinate_x = math_calculator.Calculator.calculate_function_value(parser_tree_q_x, {})
                coordinate_y = math_calculator.Calculator.calculate_function_value(parser_tree_q_y, {})
                self.__coordinates_q = coordinate_x, coordinate_y

                master.destroy()

        master.protocol('WM_DELETE_WINDOW', on_closing)

        label_font = 'arial 12'

        Label(dialog, text='A (', font=label_font).grid(row=1, column=0, pady=2)
        Label(dialog, text=' | ', font=label_font).grid(row=1, column=2, pady=2)
        Label(dialog, text=')', font=label_font).grid(row=1, column=4, pady=2)

        input_p_x = Entry(dialog, width=8, justify=CENTER)
        input_p_x.bind('<Return>', lambda event: get_coordinates())
        input_p_x.grid(row=1, column=1, pady=2)
        input_p_x.focus()
        input_p_x.selection_range(0, END)

        input_p_y = Entry(dialog, width=8, justify=CENTER)
        input_p_y.bind('<Return>', lambda event: get_coordinates())
        input_p_y.grid(row=1, column=3, pady=2)

        Label(dialog, text='B (', font=label_font).grid(row=2, column=0, pady=2)
        Label(dialog, text=' | ', font=label_font).grid(row=2, column=2, pady=2)
        Label(dialog, text=')', font=label_font).grid(row=2, column=4, pady=2)

        input_q_x = Entry(dialog, width=8, justify=CENTER)
        input_q_x.bind('<Return>', lambda event: get_coordinates())
        input_q_x.grid(row=2, column=1, pady=2)
        input_q_x.focus()
        input_q_x.selection_range(0, END)

        input_q_y = Entry(dialog, width=8, justify=CENTER)
        input_q_y.bind('<Return>', lambda event: get_coordinates())
        input_q_y.grid(row=2, column=3, pady=2)

        button = Button(dialog, text='Create', command=get_coordinates, relief='groove', bg='orange')
        button.bind('<Return>', lambda event: get_coordinates())
        button.grid(columnspan=5, pady=5)

        master.wait_window(master)

    def get_coordinates(self):
        return self.__coordinates_p, self.__coordinates_q


class LineInput(FigureDialog):
    def __init__(self):
        self.__vector_pos = []
        self.__vector_dir = []
        master = Tk()
        master.resizable(0, 0)
        master.title('Create Point')
        master.lift()
        master.attributes('-topmost', True)
        master.focus_force()
        dialog = Frame(master)
        dialog.grid(pady=5)
        dialog.focus_set()

        def set_false():
            self.__vector_pos = []
            self.__vector_dir = []

        def on_closing():
            set_false()
            master.destroy()

        def get_coordinates():
            pos_x = pos_y = dir_x = dir_y = False
            parser_tree_pos_x = self.validate_entry(input_pos_x)
            parser_tree_pos_y = self.validate_entry(input_pos_y)
            parser_tree_dir_x = self.validate_entry(input_dir_x)
            parser_tree_dir_y = self.validate_entry(input_dir_y)

            if parser_tree_pos_x and parser_tree_pos_y:
                pos_x = pos_y = True
            if parser_tree_dir_x and parser_tree_dir_y:
                dir_x = dir_y = True

            if pos_x and pos_y and dir_x and dir_y:
                if parser_tree_pos_x.is_empty() or parser_tree_pos_y.is_empty():
                    pos_x = pos_y = False
                if parser_tree_dir_x.is_empty() or parser_tree_dir_y.is_empty():
                    dir_x = dir_y = False

            if not parser_tree_pos_x:
                input_pos_x.delete(0, END)
                pos_x = False
            if not parser_tree_pos_y:
                input_pos_y.delete(0, END)
                pos_y = False
            if not parser_tree_dir_x:
                input_dir_x.delete(0, END)
                dir_x = False
            if not parser_tree_dir_y:
                input_dir_y.delete(0, END)
                dir_y = False

            if pos_x and pos_y and dir_x and dir_y:
                coordinate_x = math_calculator.Calculator.calculate_function_value(parser_tree_pos_x, {})
                coordinate_y = math_calculator.Calculator.calculate_function_value(parser_tree_pos_y, {})
                self.__vector_pos = coordinate_x, coordinate_y

                coordinate_x = math_calculator.Calculator.calculate_function_value(parser_tree_dir_x, {})
                coordinate_y = math_calculator.Calculator.calculate_function_value(parser_tree_dir_y, {})
                self.__vector_dir = coordinate_x, coordinate_y

                master.destroy()

        master.protocol('WM_DELETE_WINDOW', on_closing)

        label_font = 'arial 12'

        Label(dialog, text='OP (', font=label_font).grid(row=0, column=0, rowspan=2)
        Label(dialog, text=')', font=label_font).grid(row=0, column=2, rowspan=2)

        input_pos_x = Entry(dialog, width=6, justify=CENTER)
        input_pos_x.bind('<Return>', lambda event: get_coordinates())
        input_pos_x.grid(row=0, column=1)
        input_pos_x.focus()
        input_pos_x.selection_range(0, END)

        input_pos_y = Entry(dialog, width=6, justify=CENTER)
        input_pos_y.bind('<Return>', lambda event: get_coordinates())
        input_pos_y.grid(row=1, column=1)

        Label(dialog).grid(row=0, column=3, padx=5)

        Label(dialog, text='PQ (', font=label_font).grid(row=0, column=4, rowspan=2)
        Label(dialog, text=')', font=label_font).grid(row=0, column=6, rowspan=2)

        input_dir_x = Entry(dialog, width=6, justify=CENTER)
        input_dir_x.bind('<Return>', lambda event: get_coordinates())
        input_dir_x.grid(row=0, column=5)
        input_dir_x.focus()
        input_dir_x.selection_range(0, END)

        input_dir_y = Entry(dialog, width=6, justify=CENTER)
        input_dir_y.bind('<Return>', lambda event: get_coordinates())
        input_dir_y.grid(row=1, column=5, pady=2)

        button = Button(dialog, text='Create', command=get_coordinates, relief='groove', bg='orange')
        button.bind('<Return>', lambda event: get_coordinates())
        button.grid(columnspan=8, pady=5)

        master.wait_window(master)

    def get_coordinates(self):
        return self.__vector_pos, self.__vector_dir
