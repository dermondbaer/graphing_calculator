# Paul Birke
# 31.05.2016
# value table

from tkinter import *
from math_calculator import *

class Valuetable(object):
    def __init__(self, gui, master_frame, rows, columns, initial_start, initial_delta):
        self.__master = master_frame
        self.__gui = gui

        self.__columns = columns
        self.__rows = rows
        self.__delta = StringVar()
        self.__delta.set(str(initial_delta))
        self.__start = StringVar()
        self.__start.set(str(initial_start))
        # table delta info label
        self.__lbl_value_table_delta_info = Label(master=self.__master, text="delta:", bg=self.__gui.bg)
        self.__lbl_value_table_delta_info.grid(row=1, column=0, sticky="NES", padx=self.__gui.pad_general,
                                               pady=self.__gui.pad_general)
        # table start info label
        self.__lbl_value_table_start_info = Label(master=self.__master, text="start:", bg=self.__gui.bg)
        self.__lbl_value_table_start_info.grid(row=0, column=0, sticky="NES", padx=self.__gui.pad_general,
                                               pady=self.__gui.pad_general)
        # register validate_command callback function
        # table delta entry
        self.__entry_value_table_delta = Spinbox(master=self.__master, bg=self.__gui.bg, from_=0, to=1000000,
                                                 width=10, justify=RIGHT, cursor="XTERM", insertontime=0,
                                                 validate="all", invcmd="bell", textvariable=self.__delta, command=self.recalculate)
        vcmd_delta = (self.__master.register(self.on_validate), '%P', 0, 1000000, "delta")
        self.__entry_value_table_delta['validatecommand'] = vcmd_delta
        self.__entry_value_table_delta.delete(0, END)
        self.__entry_value_table_delta.insert(0, initial_delta)
        self.__entry_value_table_delta.grid(row=1, column=1, sticky="NESW", padx=self.__gui.pad_general,
                                                pady=self.__gui.pad_general)
        # table start entry
        self.__entry_value_table_start = Spinbox(master=self.__master, bg=self.__gui.bg, from_=-1000000000000000,
                                                 to=1000000000000000, width=20, justify=RIGHT, cursor="XTERM",
                                                 insertontime=0, validate="all", invcmd="bell", textvariable=self.__start, command=self.recalculate)
        vcmd_start = (self.__master.register(self.on_validate), '%P', -1000000000000000, 1000000000000000, "start")
        self.__entry_value_table_start['validatecommand'] = vcmd_start
        self.__entry_value_table_start.delete(0, END)
        self.__entry_value_table_start.insert(0, initial_start)
        self.__entry_value_table_start.grid(row=0, column=1, sticky="NESW", padx=self.__gui.pad_general,
                                                pady=self.__gui.pad_general)
        # table
        self.__value_table_frame = Frame(master=self.__master, bg=self.__gui.bg, relief=SUNKEN, borderwidth=1)
        self.__value_table_frame.grid(row=2, column=0, padx=self.__gui.pad_general, pady=self.__gui.pad_general, sticky="NESW",
                                columnspan=2)
        self.__column_list = ["x"]
        self.configure_size(rows, columns, ["" for i in range(columns)])
        self.recalculate()


    def configure_size(self, rows, columns, header_list):
        self.__rows = rows
        self.__columns = columns
        self.__value_table_frame.destroy()
        self.__value_table_frame = Frame(master=self.__master, bg=self.__gui.bg, relief=SUNKEN, borderwidth=1)
        self.__value_table_frame.grid(row=2, column=0, padx=self.__gui.pad_general, pady=self.__gui.pad_general, sticky="NESW",
                                columnspan=2)
        header_list[0] = "x"
        # table header
        self.__value_table_header = [Label(master=self.__value_table_frame, text=header_list[i], bg=self.__gui.bg) for i in range(columns)]
        for column in range(len(self.__value_table_header)):
            self.__value_table_header[column].grid(row=0, column=column, sticky="NESW", padx=self.__gui.pad_general,
                                                           pady=self.__gui.pad_general)
        #self.__value_table_header[0].configure(text="x")

        # table entry frame
        self.__value_table_entry_frame = Frame(master=self.__value_table_frame, bg=self.__gui.bg)
        self.__value_table_entry_frame.grid(row=2, column=0, padx=0, pady=0, sticky="NESW",
                                columnspan=columns)
        # table entries
        self.__value_table_entry = [[Label(master=self.__value_table_entry_frame, text="", bg="white") for i in range(columns)] for i in range(rows)]
        for row in range(len(self.__value_table_entry)):
            for column in range(len(self.__value_table_entry[row])):
                self.__value_table_entry[row][column].grid(row=row, column=column, sticky="NESW", padx=1,
                                                           pady=1)
        for row in range(len(self.__value_table_entry)):
            self.__value_table_entry_frame.grid_rowconfigure(index=row, minsize=20)
        for column in range(len(self.__value_table_entry[0])):
            self.__value_table_entry_frame.grid_columnconfigure(index=column, minsize=60)
        self.__value_table_frame.grid()

    def redraw(self, column_list):
        column_list.insert(0, "x")
        for index, item in enumerate(column_list):
            column_list[index] = "f" + str(item)
        self.__column_list = column_list
        self.configure_size(self.__rows, len(column_list), column_list)
        self.recalculate()

    def recalculate(self):
        for index, row in enumerate(self.__column_list):
            for i in range(self.__rows):
                if self.__column_list[index] == "x":
                    self.__value_table_entry[i][index].configure(text=str(int(self.__start.get())+i*int(self.__delta.get())))
                else:
                    self.__value_table_entry[i][index].configure(text="")

    @staticmethod
    def on_validate(p, min, max, item):
        """
        :param p: string containing the user input
        :type p: basestring
        :return: boolean representing whether the user input is representing a float or not
        :rtype: bool
        """
        p = p.lstrip('0')
        if p == "":
            p = "0"
        try:
            tmp = float(p)
        except ValueError:
            return False
        else:
            if tmp < float(min) or tmp > float(max):
                return False
            else:
                return True

    def set_table_delta(self, delta):
        self.__entry_value_table_delta.delete(0, END)
        self.__entry_value_table_delta.insert(0, delta)

    def set_table_start(self, start):
        self.__entry_value_table_start.delete(0, END)
        self.__entry_value_table_start.insert(0, start)
