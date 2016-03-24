# Pascal Mehnert
# 09.03.2016
# Grafische Oberfläche für den GTR
# V 0.1

from tkinter import *
from Parser import *

class Gui(object):
    def __init__(self, main, title):
        # attributes
        self.__main = main
        self.__parse_str = ""

        # GUI setup
        # grid_keypad_ipadx; grid_keypad_ipady
        self.__grid_keypad_ipadx = 25; self.__grid_keypad_ipady = 20
        self.__pad_general = 5

        # root window
        self.__tk = Tk()
        self.__tk.withdraw()
        self.__tk.wm_resizable(0,0)
        self.__tk.title(title)
        # menu
        self.__menu = Menu(master=self.__tk)
        self.__menu.add_command(label="Quit", command=self.stop)
        self.__tk.config(menu=self.__menu)
        # output
        self.__output = Frame(master=self.__tk, bg="green")
        self.__output.grid(row=0, column=0, padx=self.__pad_general, pady=self.__pad_general, columnspan=2)
        self.__lbl_parse_expr = Label(master=self.__output, text="<expression>", relief=GROOVE)
        self.__lbl_parse_expr.grid(row=0, column=0, columnspan=2, sticky="NESW")
        # keypad
        self.__keypad = Frame(master=self.__tk, bg="blue")
        self.__keypad.grid(row=2, column=0, padx=self.__pad_general, pady=self.__pad_general)
        self.__btn_9 = Button(master=self.__keypad, text="9", command=self.press)\
            .grid(row=0, column=2, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady)
        self.__btn_8 = Button(master=self.__keypad, text="8", command=self.press)\
            .grid(row=0, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady)
        self.__btn_7 = Button(master=self.__keypad, text="7", command=self.press)\
            .grid(row=0, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady)
        self.__btn_6 = Button(master=self.__keypad, text="6", command=self.press)\
            .grid(row=1, column=2, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady)
        self.__btn_5 = Button(master=self.__keypad, text="5", command=self.press)\
            .grid(row=1, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady)
        self.__btn_4 = Button(master=self.__keypad, text="4", command=self.press)\
            .grid(row=1, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady)
        self.__btn_3 = Button(master=self.__keypad, text="3", command=self.press)\
            .grid(row=2, column=2, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady)
        self.__btn_2 = Button(master=self.__keypad, text="2", command=self.press)\
            .grid(row=2, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady)
        self.__btn_1 = Button(master=self.__keypad, text="1", command=self.press)\
            .grid(row=2, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady)
        self.__btn_0 = Button(master=self.__keypad, text="0", command=self.press)\
            .grid(row=3, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady)
        self.__btn_preminus = Button(master=self.__keypad, text="-", command=self.press)\
            .grid(row=3, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_dec_pt = Button(master=self.__keypad, text=".", command=self.press)\
            .grid(row=3, column=2, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        # base math buttons
        self.__basemathbtn = Frame(master=self.__tk, bg="red")
        self.__basemathbtn.grid(row=2, column=1, padx=self.__pad_general, pady=self.__pad_general)
        self.__btn_divide = Button(self.__basemathbtn, text="/", command=self.press)\
            .grid(row=0, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_multiply = Button(self.__basemathbtn, text="*", command=self.press)\
            .grid(row=1, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_subtract = Button(self.__basemathbtn, text="-", command=self.press)\
            .grid(row=2, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_add = Button(self.__basemathbtn, text="+", command=self.press)\
            .grid(row=3, column=0, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        self.__btn_equals = Button(master=self.__basemathbtn, text="=", command=self.press)\
            .grid(row=2, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW", rowspan=2)
        self.__btn_exp = Button(master=self.__basemathbtn, text="^", command=self.press)\
            .grid(row=1, column=1, ipadx=self.__grid_keypad_ipadx, ipady=self.__grid_keypad_ipady, sticky="NESW")
        # additional math buttons
        # first row
        self.__mathbtn = Frame(master=self.__tk)
        self.__mathbtn.grid(row=1, column=0, columnspan=2, padx=self.__pad_general, pady=self.__pad_general, sticky="NESW")
        self.__btn_pi = Button(master=self.__mathbtn, text="PI").grid(row=0, column=0, sticky="NESW")
        self.__btn_e = Button(master=self.__mathbtn, text="e").grid(row=0, column=1, sticky="NESW")
        self.__btn_x = Button(master=self.__mathbtn, text="x").grid(row=0, column=2, sticky="NESW")
        self.__btn_sqrt = Button(master=self.__mathbtn, text="sqrt()").grid(row=0, column=3, sticky="NESW")
        self.__btn_root = Button(master=self.__mathbtn, text="root()").grid(row=0, column=4, sticky="NESW")
        self.__btn_log = Button(master=self.__mathbtn, text="log()").grid(row=0, column=5, sticky="NESW")
        # second row
        self.__btn_sin = Button(master=self.__mathbtn, text="sin()").grid(row=1, column=0, sticky="NESW")
        self.__btn_cos = Button(master=self.__mathbtn, text="cos()").grid(row=1, column=1, sticky="NESW")
        self.__btn_tan = Button(master=self.__mathbtn, text="tan()").grid(row=1, column=2, sticky="NESW")
        self.__btn_max = Button(master=self.__mathbtn, text="max()").grid(row=1, column=3, sticky="NESW")
        # fill up space
        for i in range(self.__mathbtn.grid_size()[0]):
            self.__mathbtn.grid_columnconfigure(index=i, minsize=50, weight=1)
        for i in range(self.__mathbtn.grid_size()[1]):
            self.__mathbtn.grid_rowconfigure(index=i, minsize=50, weight=1)

        # parser setup
        self.__parser = Parser("supported.xml")

    def start(self, title):
        self.__tk.deiconify()
        self.__tk.mainloop()

    def stop(self):
        self.__main.stop()

    def press(self):
        pass

