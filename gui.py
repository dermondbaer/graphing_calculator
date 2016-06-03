# Paul Birke
# 26.03.2016
# Graphical User Interface (GUI)

from functools import partial
from tkinter import *
from math_calculator import *
from value_table import *
from function_storage import *
from geometry_tool.coordinate_system import *
import re
import copy


class Gui(object):
    def __init__(self, main, title):
        # attributes
        self.__main = main
        self.__parse_expr = ""
        self.__expr = []
        self.__result = ""
        self.__err = ""
        self.__postfix_expr = ""

        # calculator setup
        self.calc = Calculator()

        # GUI setup
        # padding
        self.grid_keypad_ipadx = 35
        self.grid_keypad_ipady = 25
        self.pad_general = 5
        self.bg = "grey"
        self.__function_count = 10
        
        # root window
        self.__tk = Tk()
        self.__tk.withdraw()
        self.__tk.wm_resizable(0, 0)
        self.__tk.title(title)
        self.__tk.configure(bg=self.bg)
        self.__tk.wm_protocol("WM_DELETE_WINDOW", self.stop)


        # menu
        self.__menu = Menu(master=self.__tk)
        self.__menu.add_command(label="Quit", command=self.stop)
        # "view" menu
        self.__menu_view = Menu(master=self.__menu, tearoff=0)
        self.__menu_view.add_checkbutton(label="Show Functions", command=self.expand_functions)
        self.__menu_view.add_checkbutton(label="Show Value Table", command=self.expand_table)
        self.__menu_view.add_checkbutton(label="Show Coordinate System", command=self.display_cs)
        self.__menu.add_cascade(label="View", menu=self.__menu_view)
        # "save expression to..." menu
        self.__menu_save_function = Menu(master=self.__menu, tearoff=0)
        for index in range(self.__function_count):
            self.__menu_save_function.add_command(label="function "+str(index), command=partial(self.save_to, index))
        self.__menu_save_function.add_separator()
        self.__menu_save_function.add_command(label="Reset all functions", command=self.reset_functions)
        self.__menu.add_cascade(label="Save Expression To...", menu=self.__menu_save_function)
        self.__tk.config(menu=self.__menu)

        # main frames
        self.__functions_master = Frame(master=self.__tk, bg=self.bg, relief=GROOVE, borderwidth=2)
        self.__functions_master.grid(row=1, column=3, padx=self.pad_general, pady=self.pad_general, sticky="NESW",
                                       rowspan=2)
        self.__output = Frame(master=self.__tk, bg=self.bg, relief=GROOVE)
        self.__output.grid(row=0, column=1, padx=(15, 15), pady=(10, self.pad_general), columnspan=2, sticky="NEW")

        self.__keypad = Frame(master=self.__tk, bg="blue")
        self.__keypad.grid(row=2, column=1, padx=self.pad_general, pady=self.pad_general, sticky="NESW")

        self.__basemathbtn = Frame(master=self.__tk, bg="red")
        self.__basemathbtn.grid(row=2, column=2, padx=self.pad_general, pady=self.pad_general, sticky="NESW")

        self.__mathbtn = Frame(master=self.__tk)
        self.__mathbtn.grid(row=1, column=1, columnspan=2, padx=self.pad_general, pady=self.pad_general,
                            sticky="NESW")

        self.__value_table_master = Frame(master=self.__tk, bg=self.bg, relief=GROOVE, borderwidth=2)
        self.__value_table_master.grid(row=0, column=3, padx=self.pad_general, pady=self.pad_general, sticky="NESW")

        # child window
        self.__graph_window = Toplevel()
        self.__graph_window.withdraw()
        self.__graph_window.title = title
        self.__graph_window.wm_resizable(0, 0)
        self.__graph_window.wm_protocol("WM_DELETE_WINDOW", partial(self.__menu_view.invoke, 2))
        # menu of the child window
        self.__menu_graph_window = Menu(master=self.__graph_window, tearoff=0)
        # dropdown selection menu
        self.__menu_graph_window_selection = Menu(master=self.__graph_window, tearoff=0)
        self.__graph_window_selection = [BooleanVar() for i in range(self.__function_count)]
        for index in range(self.__function_count):
            self.__menu_graph_window_selection.add_checkbutton(label="function "+str(index),
                                                               command=partial(self.display_func, index),
                                                               variable=self.__graph_window_selection[index])
        self.__menu_graph_window.add_cascade(label="Select Functions...", menu=self.__menu_graph_window_selection)
        # dropdown "add figure" menu
        self.__menu_graph_window_add_figure = Menu(master=self.__graph_window, tearoff=0)
        self.__menu_graph_window_add_figure.add_command(label="Add point...", command=self.graph_add_point)
        self.__menu_graph_window_add_figure.add_command(label="Add line...", command=self.graph_add_line)
        self.__menu_graph_window_add_figure.add_command(label="Add line segment...", command=self.graph_add_distance)
        self.__menu_graph_window_add_figure.add_separator()
        self.__menu_graph_window_add_figure.add_command(label="Clear all figures", command=self.graph_clear_figures)
        self.__menu_graph_window.add_cascade(label="Draw...", menu=self.__menu_graph_window_add_figure)
        # Resize Menu
        self.__menu_graph_window.add_command(label="Resize...", command=self.graph_resize)
        self.__graph_window.configure(menu=self.__menu_graph_window)
        self.graph = CoordinateSystem(self.__graph_window, 600, 600, 10, 10)
        # reference to the drawn figures
        self.__graph_window_function = [None for i in range(self.__function_count)]
        self.__graph_window_figure = []

        # output
        self.__lbl_parse_expr = Label(master=self.__output, text="", bg=self.bg)
        self.__lbl_parse_expr_info = Label(master=self.__output, text="Current expression: ", bg=self.bg)
        self.__lbl_postf_expr = Label(master=self.__output, text="", bg=self.bg)
        self.__lbl_postf_expr_info = Label(master=self.__output, text="Postfix notation: ", bg=self.bg)
        self.__lbl_result = Label(master=self.__output, text="", bg=self.bg)
        self.__lbl_result_info = Label(master=self.__output, text="Result: ", bg=self.bg)
        self.__lbl_err = Label(master=self.__output, text="", bg=self.bg)
        self.__lbl_err_info = Label(master=self.__output, text="Errors: ", bg=self.bg)
        self.__output_expr = Frame(master=self.__output, bg="white", relief=GROOVE)
        self.__output_expr.grid(row=0, column=1, columnspan=2, sticky="NESW")
        
        # layout
        self.__lbl_parse_expr.grid(row=1, column=1, sticky="NES")
        self.__lbl_parse_expr_info.grid(row=1, column=0, sticky="NES")
        self.__lbl_postf_expr.grid(row=2, column=1, sticky="NES")
        self.__lbl_postf_expr_info.grid(row=2, column=0, sticky="NES")
        self.__lbl_result.grid(row=3, column=1, sticky="NES")
        self.__lbl_result_info.grid(row=3, column=0, sticky="NES")
        self.__lbl_err.grid(row=4, column=1, sticky="NESW")
        self.__lbl_err_info.grid(row=4, column=0, sticky="NES")
        
        self.__output.grid_columnconfigure(index=1, minsize=100, weight=1)
        for i in range(self.__output.grid_size()[1]):
            self.__output.grid_rowconfigure(index=i, minsize=40, weight=1)
        self.__output.grid_rowconfigure(index=0, minsize=100)

        # keypad
        self.__btn_9 = Button(master=self.__keypad, text="9", command=partial(self.press, "9")) \
            .grid(row=0, column=2, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_8 = Button(master=self.__keypad, text="8", command=partial(self.press, "8")) \
            .grid(row=0, column=1, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_7 = Button(master=self.__keypad, text="7", command=partial(self.press, "7")) \
            .grid(row=0, column=0, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_6 = Button(master=self.__keypad, text="6", command=partial(self.press, "6")) \
            .grid(row=1, column=2, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_5 = Button(master=self.__keypad, text="5", command=partial(self.press, "5")) \
            .grid(row=1, column=1, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_4 = Button(master=self.__keypad, text="4", command=partial(self.press, "4")) \
            .grid(row=1, column=0, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_3 = Button(master=self.__keypad, text="3", command=partial(self.press, "3")) \
            .grid(row=2, column=2, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_2 = Button(master=self.__keypad, text="2", command=partial(self.press, "2")) \
            .grid(row=2, column=1, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_1 = Button(master=self.__keypad, text="1", command=partial(self.press, "1")) \
            .grid(row=2, column=0, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_0 = Button(master=self.__keypad, text="0", command=partial(self.press, "0")) \
            .grid(row=3, column=0, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_preminus = Button(master=self.__keypad, text="(-)", command=partial(self.press, " -")) \
            .grid(row=3, column=1, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_dec_pt = Button(master=self.__keypad, text=".", command=partial(self.press, ".")) \
            .grid(row=3, column=2, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        
        # base math buttons
        self.__btn_divide = Button(self.__basemathbtn, text="/", command=partial(self.press, " / ")) \
            .grid(row=2, column=1, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_multiply = Button(self.__basemathbtn, text="*", command=partial(self.press, " * ")) \
            .grid(row=1, column=1, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_subtract = Button(self.__basemathbtn, text="-", command=partial(self.press, " - ")) \
            .grid(row=2, column=0, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_add = Button(self.__basemathbtn, text="+", command=partial(self.press, " + ")) \
            .grid(row=1, column=0, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_equals = Button(master=self.__basemathbtn, text="=", command=self.equals) \
            .grid(row=3, column=1, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW",
                  rowspan=1)
        # self.__btn_exp = Button(master=self.__basemathbtn, text="^", command=partial(self.press, " ^ ")) \
        #    .grid(row=1, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_clr = Button(master=self.__basemathbtn, text="C", command=self.clear, bg="orange") \
            .grid(row=0, column=1, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_clr_last = Button(master=self.__basemathbtn, text="AC", command=self.clear_last) \
            .grid(row=0, column=0, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")
        self.__btn_comma = Button(self.__basemathbtn, text=",", command=partial(self.press, " , ")) \
            .grid(row=3, column=0, ipadx=self.grid_keypad_ipadx, ipady=self.grid_keypad_ipady, sticky="NESW")

        # dropdown menu with saved functions
        self.__menu_functions = Menu(master=self.__menu, tearoff=0)
        for i in range(self.__function_count):
            self.__menu_functions.add_command(label="function "+str(i), command=partial(self.recall, i))
        self.__menu.add_cascade(label="Recall Function", menu=self.__menu_functions)

        # dropdown menu with mathematical functions
        self.__menu_math_functions = Menu(master=self.__menu, tearoff=0)
        self.__menu_math_functions.add_command(label="sinh( x )", command=partial(self.press, " sinh ("))
        self.__menu_math_functions.add_command(label="asinh( x )", command=partial(self.press, " asinh ("))
        self.__menu_math_functions.add_command(label="cosh( x )", command=partial(self.press, " cosh ("))
        self.__menu_math_functions.add_command(label="acosh( x )", command=partial(self.press, " acosh ("))
        self.__menu_math_functions.add_command(label="tanh( x )", command=partial(self.press, " tanh ("))
        self.__menu_math_functions.add_command(label="atanh( x )", command=partial(self.press, " atanh ("))
        self.__menu_math_functions.add_separator()
        self.__menu_math_functions.add_command(label="ncr( x )", command=partial(self.press, " ncr ("))
        self.__menu_math_functions.add_command(label="npr( x )", command=partial(self.press, " npr ("))
        self.__menu_math_functions.add_command(label="binompdf( n, p, k )", command=partial(self.press, " binompdf ("))
        self.__menu_math_functions.add_command(label="binomcdf( n, p, k )", command=partial(self.press, " binomcdf ("))
        self.__menu_math_functions.add_separator()
        self.__menu_math_functions.add_command(label="min( a, b )", command=partial(self.press, " min ("))
        self.__menu_math_functions.add_command(label="max( a, b )", command=partial(self.press, " max ("))
        self.__menu_math_functions.add_separator()
        self.__menu_math_functions.add_command(label="nderiv( f(x), x )", command=partial(self.press, " nderiv ("))
        self.__menu_math_functions.add_command(label="fnint( f(x), a, b )", command=partial(self.press, " fnint ("))
        self.__menu.add_cascade(label="Mathematical Functions", menu=self.__menu_math_functions)

        # additional math buttons
        math_btn = [[]]

        # additional math buttons
        # # first row
        # self.__btn_pi = Button(master=self.__mathbtn, text="PI", command=partial(self.press, " pi ")) \
        #     .grid(row=0, column=0, sticky="NESW")
        # self.__btn_e = Button(master=self.__mathbtn, text="e", command=partial(self.press, " e ")) \
        #     .grid(row=0, column=1, sticky="NESW")
        # self.__btn_x = Button(master=self.__mathbtn, text="x", command=partial(self.press, " x ")) \
        #     .grid(row=0, column=2, sticky="NESW")
        # self.__btn_sqrt = Button(master=self.__mathbtn, text="sqrt()", command=partial(self.press, "sqrt ( ")) \
        #     .grid(row=0, column=3, sticky="NESW")
        # self.__btn_root = Button(master=self.__mathbtn, text="root()", command=partial(self.press, "root ( ")) \
        #     .grid(row=0, column=4, sticky="NESW")
        # self.__btn_log = Button(master=self.__mathbtn, text="log()", command=partial(self.press, "log ( ")) \
        #     .grid(row=0, column=5, sticky="NESW")
        # # second row
        # self.__btn_sin = Button(master=self.__mathbtn, text="sin()", command=partial(self.press, "sin ( ")) \
        #     .grid(row=1, column=0, sticky="NESW")
        # self.__btn_cos = Button(master=self.__mathbtn, text="cos()", command=partial(self.press, "cos ( ")) \
        #     .grid(row=1, column=1, sticky="NESW")
        # self.__btn_tan = Button(master=self.__mathbtn, text="tan()", command=partial(self.press, "tan ( ")) \
        #     .grid(row=1, column=2, sticky="NESW")
        # self.__btn_max = Button(master=self.__mathbtn, text="max()", command=partial(self.press, "max ( ")) \
        #     .grid(row=1, column=3, sticky="NESW")
        # self.__btn_opbr = Button(master=self.__mathbtn, text="(", command=partial(self.press, " ( ")) \
        #     .grid(row=1, column=4, sticky="NESW")
        # self.__btn_clbr = Button(master=self.__mathbtn, text=")", command=partial(self.press, " ) ")) \
        #     .grid(row=1, column=5, sticky="NESW")

        # saved functions
        self.functions = Function_storage(self, self.__functions_master, self.__function_count)
        # hide saved functions frame
        self.__functions_master.grid_remove()

        # value table
        self.value_table = Valuetable(self, self.__value_table_master, 10, 0, 1)
        # hide the value table
        self.__value_table_master.grid_remove()

        # fill up space
        for i in range(self.__mathbtn.grid_size()[0]):
            self.__mathbtn.grid_columnconfigure(index=i, minsize=50, weight=1)
        for i in range(self.__mathbtn.grid_size()[1]):
            self.__mathbtn.grid_rowconfigure(index=i, minsize=50, weight=1)
        for i in range(self.__keypad.grid_size()[0]):
            self.__keypad.grid_columnconfigure(index=i, minsize=50, weight=1)
        for i in range(self.__keypad.grid_size()[1]):
            self.__keypad.grid_rowconfigure(index=i, minsize=50, weight=1)
        for i in range(self.__basemathbtn.grid_size()[0]):
            self.__basemathbtn.grid_columnconfigure(index=i, minsize=50, weight=1)
        for i in range(self.__basemathbtn.grid_size()[1]):
            self.__basemathbtn.grid_rowconfigure(index=i, minsize=50, weight=1)

        # set minimal size
        self.__tk.update()
        # debug
        for i in range(2):
            self.__menu_view.invoke(i)
        #self.__tk.wm_minsize(self.__parsegeometry(self.__tk.winfo_geometry())[0],
        #                     self.__parsegeometry(self.__tk.winfo_geometry())[1])

    def expand_table(self):
        self.__menu_view.entryconfigure(index=1, command=self.collapse_table)
        self.__value_table_master.grid()

    def collapse_table(self):
        self.__menu_view.entryconfigure(index=1, command=self.expand_table)
        self.__value_table_master.grid_remove()

    def expand_functions(self):
        self.__menu_view.entryconfigure(index=0, command=self.collapse_functions)
        self.__functions_master.grid()

    def collapse_functions(self):
        self.__menu_view.entryconfigure(index=0, command=self.expand_functions)
        self.__functions_master.grid_remove()

    def display_cs(self):
        self.__menu_view.entryconfigure(index=2, command=self.hide_cs)
        self.__graph_window.deiconify()

    def hide_cs(self):
        self.__menu_view.entryconfigure(index=2, command=self.display_cs)
        self.__graph_window.withdraw()

    def display_func(self, index):
        if  self.functions.get_function(index) != "":
            self.__graph_window_function[index] = self.graph.create_function_graph(self.functions.get_function(index))
            self.__menu_graph_window_selection.entryconfigure(index=index, command=partial(self.hide_func, index))
        else:
            self.__graph_window_selection[index].set(False)

    def hide_func(self, index):
        if self.__graph_window_function[index] != None:
            self.graph.del_figure(self.__graph_window_function[index])
            self.__menu_graph_window_selection.entryconfigure(index=index, command=partial(self.display_func, index))
        else:
            self.__menu_graph_window_selection[index].set(True)

    def graph_add_point(self):
        figure = self.graph.create_point()
        if figure != False:
            self.__graph_window_figure.append(figure)

    def graph_add_line(self):
        figure = self.graph.create_line()
        if figure != False:
            self.__graph_window_figure.append(figure)

    def graph_add_distance(self):
        figure = self.graph.create_distance()
        if figure != False:
            self.__graph_window_figure.append(figure)

    def graph_clear_figures(self):
        for figure in self.__graph_window_figure:
           self.graph.del_figure(figure)
        self.__graph_window_figure = []

    def graph_resize(self):
        self.graph.restart(True)

    def reset_functions(self):
        self.functions.reset()

    def save_to(self, index=0):
        print("save expression \""+self.convert_list_to_string(self.__expr)+"\" to f"+str(index))
        self.functions.set_function(index, self.convert_list_to_string(self.__expr), copy.deepcopy(self.__expr))

    def recall(self, index):
        # function = ["f"+str(index)]
        # for i, item in enumerate(self.functions.get_function_list(index)):
        #     function.append(item)
        # print(function)
        # self.__expr.append(function)
        if self.functions.get_function_list(index) != []:
            self.__expr = self.functions.get_function_list(index)
            self.redraw()

    @staticmethod
    def __parsegeometry(geometry):
        """
        :arg geometry: string with the format "%dx%d%+d%+d" % (width, height, xoffset, yoffset)
        :type geometry: basestring
        :return: tuple containing the width, offset, xoffset, yoffset
        :rtype: tuple
        """
        m = re.match("(\d+)x(\d+)([-+]\d+)([-+]\d+)", geometry)
        if not m:
            raise ValueError("failed to parse geometry string")
        return m.groups()

    def start(self):
        self.__tk.deiconify()
        self.__tk.mainloop()

    def stop(self):
        self.__main.stop_application()

    def press(self, value):
        self.__expr.append(value)
        self.redraw()

    def clear(self):
        self.__parse_expr = ""
        self.__expr.clear()
        self.__postfix_expr = ""
        self.__result = ""
        self.__err = ""
        self.redraw()

    def clear_last(self):
        if not len(self.__expr) == 0:
            self.__expr.pop()
            self.redraw()

    @staticmethod
    def is_numeral(value):
        if value in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            return True
        else:
            return False

    def equals(self):
        try:
            expr = self.convert_list_to_string(self.__expr)
            self.__postfix_expr = self.calc.make_expression_postfix(expr)
            expr = self.convert_list_to_expr(self.__expr)
            result = self.calc.calculate_expression(expr)
            self.__result=str(result.to_string())
            self.__err = ""
            self.redraw()
        except ValueError:
            self.__err = "Syntax isn't correct; check your parenthesis!"
            self.__postfix_expr = ""
            self.redraw()
        except ZeroDivisionError:
            pass

    def render_expression(self):
        pass

    def redraw(self):
        self.__lbl_parse_expr.configure(text=self.convert_list_to_string(self.__expr))
        self.__lbl_result.configure(text=self.__result)
        self.__lbl_postf_expr.configure(text=self.__postfix_expr)
        self.__lbl_err.configure(text=self.__err)

    @staticmethod
    def convert_list_to_string(list_):
        string = ""
        for item in list_:
            if type(item) == str:
                string += item
            elif type(item) == list:
                string += item[0]
        return string

    @staticmethod
    def convert_list_to_expr(list_):
        string= ""
        for item in list_:
            if type(item) == str:
                string += item
            elif type(item) == list:
                for i in range(1, len(item)):
                    string += item[i]
        print(string)
        return string
