# Paul Birke
# 26.03.2016
# Graphical User Interface (GUI)

from functools import partial
from tkinter import *
# from math_parser import *
from math_calculator import *
import re


class Gui(object):
    def __init__(self, main, title):
        # attributes
        self.__main = main
        self.__parse_expr = ""         # Not empty because of bug in Parser.py
        self.__expr = []

        # GUI setup
        # padding
        self.__grid_keypad_ipadx = 35
        self.__grid_keypad_ipady = 25
        self.__pad_general = 5
        self.__bg = "grey"
        
        # root window
        self.__tk = Tk()
        self.__tk.withdraw()
        self.__tk.wm_resizable(1, 1)
        self.__tk.title(title)
        self.__tk.configure(bg=self.__bg)
        # menu
        self.__menu = Menu(master=self.__tk)
        self.__menu.add_command(label="Quit", command=self.stop)
        self.__tk.config(menu=self.__menu)
        
        # output
        self.__output = Frame(master=self.__tk, bg=self.__bg, relief=GROOVE)
        self.__output.grid(row=0, column=0, padx=(15, 15), pady=(10, self.__pad_general), columnspan=2, sticky="NESW")
        self.__lbl_parse_expr = Label(master=self.__output, text="", bg=self.__bg)
        self.__lbl_parse_expr_info = Label(master=self.__output, text="Current expression: ", bg=self.__bg)
        self.__lbl_postf_expr = Label(master=self.__output, text="", bg=self.__bg)
        self.__lbl_postf_expr_info = Label(master=self.__output, text="Postfix notation: ", bg=self.__bg)
        self.__lbl_result = Label(master=self.__output, text="", bg=self.__bg)
        self.__lbl_result_info = Label(master=self.__output, text="Result: ", bg=self.__bg)
        self.__lbl_err = Label(master=self.__output, text="", bg=self.__bg)
        self.__lbl_err_info = Label(master=self.__output, text="Errors: ", bg=self.__bg)
        self.__output_expr = Frame(master=self.__output, bg="white", relief=GROOVE)
        self.__output_expr.grid(row=0, column=0, columnspan=2, sticky="NESW")
        
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
        self.__output.grid_rowconfigure(index=0, minsize=200)

        # keypad
        self.__keypad = Frame(master=self.__tk, bg="blue")
        self.__keypad.grid(row=2, column=0, padx=self.__pad_general, pady=self.__pad_general, sticky="NESW")
        self.__btn_9 = Button(master=self.__keypad, text="9", command=partial(self.press, "9")) \
            .grid(row=0, column=2, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_8 = Button(master=self.__keypad, text="8", command=partial(self.press, "8")) \
            .grid(row=0, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_7 = Button(master=self.__keypad, text="7", command=partial(self.press, "7")) \
            .grid(row=0, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_6 = Button(master=self.__keypad, text="6", command=partial(self.press, "6")) \
            .grid(row=1, column=2, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_5 = Button(master=self.__keypad, text="5", command=partial(self.press, "5")) \
            .grid(row=1, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_4 = Button(master=self.__keypad, text="4", command=partial(self.press, "4")) \
            .grid(row=1, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_3 = Button(master=self.__keypad, text="3", command=partial(self.press, "3")) \
            .grid(row=2, column=2, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_2 = Button(master=self.__keypad, text="2", command=partial(self.press, "2")) \
            .grid(row=2, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_1 = Button(master=self.__keypad, text="1", command=partial(self.press, "1")) \
            .grid(row=2, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_0 = Button(master=self.__keypad, text="0", command=partial(self.press, "0")) \
            .grid(row=3, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_preminus = Button(master=self.__keypad, text="(-)", command=partial(self.press, " -")) \
            .grid(row=3, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_dec_pt = Button(master=self.__keypad, text=".", command=partial(self.press, ".")) \
            .grid(row=3, column=2, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        
        # base math buttons
        self.__basemathbtn = Frame(master=self.__tk, bg="red")
        self.__basemathbtn.grid(row=2, column=1, padx=self.__pad_general, pady=self.__pad_general, sticky="NESW")
        self.__btn_divide = Button(self.__basemathbtn, text="/", command=partial(self.press, " / ")) \
            .grid(row=0, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_multiply = Button(self.__basemathbtn, text="*", command=partial(self.press, " * ")) \
            .grid(row=1, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_subtract = Button(self.__basemathbtn, text="-", command=partial(self.press, " - ")) \
            .grid(row=2, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_add = Button(self.__basemathbtn, text="+", command=partial(self.press, " + ")) \
            .grid(row=3, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_equals = Button(master=self.__basemathbtn, text="=", command=self.equals) \
            .grid(row=2, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW",
                  rowspan=2)
        #self.__btn_exp = Button(master=self.__basemathbtn, text="^", command=partial(self.press, " ^ ")) \
        #    .grid(row=1, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_clr = Button(master=self.__basemathbtn, text="C", command=self.clear, bg="orange") \
            .grid(row=0, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_clr_last = Button(master=self.__basemathbtn, text="AC", command=self.clear_last) \
            .grid(row=1, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        
        # additional math buttons
        # first row
        self.__mathbtn = Frame(master=self.__tk)
        self.__mathbtn.grid(row=1, column=0, columnspan=2, padx=self.__pad_general, pady=self.__pad_general,
                            sticky="NESW")
        self.__btn_pi = Button(master=self.__mathbtn, text="PI", command=partial(self.press, "pi")) \
            .grid(row=0, column=0, sticky="NESW")
        self.__btn_e = Button(master=self.__mathbtn, text="e", command=partial(self.press, "e")) \
            .grid(row=0, column=1, sticky="NESW")
        self.__btn_x = Button(master=self.__mathbtn, text="x", command=partial(self.press, "x")) \
            .grid(row=0, column=2, sticky="NESW")
        self.__btn_sqrt = Button(master=self.__mathbtn, text="sqrt()", command=partial(self.press, "sqrt ( ")) \
            .grid(row=0, column=3, sticky="NESW")
        self.__btn_root = Button(master=self.__mathbtn, text="root()", command=partial(self.press, "root ( ")) \
            .grid(row=0, column=4, sticky="NESW")
        self.__btn_log = Button(master=self.__mathbtn, text="log()", command=partial(self.press, "log ( ")) \
            .grid(row=0, column=5, sticky="NESW")
        # second row
        self.__btn_sin = Button(master=self.__mathbtn, text="sin()", command=partial(self.press, "sin ( ")) \
            .grid(row=1, column=0, sticky="NESW")
        self.__btn_cos = Button(master=self.__mathbtn, text="cos()", command=partial(self.press, "cos ( ")) \
            .grid(row=1, column=1, sticky="NESW")
        self.__btn_tan = Button(master=self.__mathbtn, text="tan()", command=partial(self.press, "tan ( ")) \
            .grid(row=1, column=2, sticky="NESW")
        self.__btn_max = Button(master=self.__mathbtn, text="max()", command=partial(self.press, "max ( ")) \
            .grid(row=1, column=3, sticky="NESW")
        self.__btn_opbr = Button(master=self.__mathbtn, text="(", command=partial(self.press, " ( ")) \
            .grid(row=1, column=4, sticky="NESW")
        self.__btn_clbr = Button(master=self.__mathbtn, text=")", command=partial(self.press, " ) ")) \
            .grid(row=1, column=5, sticky="NESW")

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

        # resize proportional
        for i in range(self.__tk.grid_size()[0]):
            self.__tk.grid_columnconfigure(index=i, weight=1)
        for i in range(self.__tk.grid_size()[1]):
            self.__tk.grid_rowconfigure(index=i, weight=1)

        # set minimal size
        self.__tk.update()
        self.__tk.wm_minsize(self.__parsegeometry(self.__tk.winfo_geometry())[0],
                             self.__parsegeometry(self.__tk.winfo_geometry())[1])

        # parser setup
        self.__parser = Parser()

        # calculator setup
        self.__calc = Calculator()

    def __parsegeometry(self, geometry):
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
        self.__tk.destroy()
        self.__main.stop()

    def press(self, value):
        self.__expr.append(value)
        self.__lbl_parse_expr.configure(text=self.convert_list_to_string(self.__expr))

    def clear(self):
        self.__parse_expr = ""
        self.__expr.clear()
        self.__lbl_parse_expr.configure(text="")
        self.__lbl_postf_expr.configure(text="")
        self.__lbl_result.configure(text="")

    def clear_last(self):
        if not len(self.__expr) == 0:
            self.__expr.pop()
            self.__lbl_parse_expr.configure(text=self.convert_list_to_string(self.__expr))

    def is_numeral(self, value):
        if value in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            return True
        else:
            return False

    def equals(self):
        try:
            expr = self.convert_list_to_string(self.__expr)
            tmp = self.__parser.make_expression_postfix(expr)
            self.__lbl_postf_expr.configure(text=tmp)
            result = self.__calc.calculate_expression(expr)
            if result.get_root() is not None:
                self.__lbl_result.configure(text=str(result.get_root().get_value()))
            self.__lbl_err.configure(text="")
        except ValueError:
            self.__lbl_err.configure(text="Syntax isn't correct; check your parenthesis!")
            self.__lbl_postf_expr.configure(text="")

    def render_expression(self):
        pass

    def convert_list_to_string(self, list):
        string = ""
        for item in list:
            string += item
        return string
