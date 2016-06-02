# Paul Birke
# 31.05.2016
# value table

from tkinter import *
from math_calculator import *

class Valuetable(object):
    def __init__(self, gui, master_frame, rows, initial_start, initial_delta):
        self.__master = master_frame
        self.__master.grid_columnconfigure(index=3, weight=1)
        self.__master.grid_rowconfigure(index=2, weight=1)
        self.__gui = gui

        self.__columns = 1
        self.__column_list = []
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
        # table rows info label
        self.__lbl_value_table_rows_info = Label(master=self.__master, text="rows:", bg=self.__gui.bg)
        self.__lbl_value_table_rows_info.grid(row=0, column=2, sticky="NES", padx=self.__gui.pad_general,
                                               pady=self.__gui.pad_general)
        # # table columns info label
        # self.__lbl_value_table_columns_info = Label(master=self.__master, text="columns:", bg=self.__gui.bg)
        # self.__lbl_value_table_columns_info.grid(row=1, column=2, sticky="NES", padx=self.__gui.pad_general,
        #                                        pady=self.__gui.pad_general)
        # register validate_command callback function
        # table delta entry
        self.__entry_value_table_delta = Spinbox(master=self.__master, bg=self.__gui.bg, from_=0, to=1000000,
                                                 width=10, justify=RIGHT, cursor="XTERM", insertontime=0,
                                                 validate="all", invcmd="bell", textvariable=self.__delta, command=self.recalculate)
        vcmd_delta = (self.__master.register(self.on_validate), 0, 1000000, '%P')
        self.__entry_value_table_delta['validatecommand'] = vcmd_delta
        self.__entry_value_table_delta.delete(0, END)
        self.__entry_value_table_delta.insert(0, initial_delta)
        self.__entry_value_table_delta.grid(row=1, column=1, sticky="NESW", padx=self.__gui.pad_general,
                                                pady=self.__gui.pad_general)
        # table start entry
        self.__entry_value_table_start = Spinbox(master=self.__master, bg=self.__gui.bg, from_=-1000000000000000,
                                                 to=1000000000000000, width=20, justify=RIGHT, cursor="XTERM",
                                                 insertontime=0, validate="all", invcmd="bell", textvariable=self.__start, command=self.recalculate)
        vcmd_start = (self.__master.register(self.on_validate), -1000000000000000, 1000000000000000, '%P')
        self.__entry_value_table_start['validatecommand'] = vcmd_start
        self.__entry_value_table_start.delete(0, END)
        self.__entry_value_table_start.insert(0, initial_start)
        self.__entry_value_table_start.grid(row=0, column=1, sticky="NESW", padx=self.__gui.pad_general,
                                                pady=self.__gui.pad_general)
        # # table rows entry
        self.__entry_value_table_rows = Spinbox(master=self.__master, bg=self.__gui.bg, from_=1, to=50, width=20,
                                                   justify=RIGHT, cursor="XTERM", insertontime=0, validate="all",
                                                   invcmd="bell", command=self.redraw)
        vcmd_rows = (self.__master.register(self.on_validate), 0, 50, '%P')
        self.__entry_value_table_rows['validatecommand'] = vcmd_rows
        self.__entry_value_table_rows.delete(0, END)
        self.__entry_value_table_rows.insert(0, rows)
        self.__entry_value_table_rows.grid(row=0, column=3, sticky="NESW", padx=self.__gui.pad_general,
                                                pady=self.__gui.pad_general)
        # # table columns entry
        # self.__entry_value_table_columns = Spinbox(master=self.__master, bg=self.__gui.bg, from_=0, to=50, width=20,
        #                                            justify=RIGHT, cursor="XTERM", insertontime=0, validate="all",
        #                                            invcmd="bell", textvariable=self.__columns, command=self.redraw)
        # vcmd_columns = (self.__master.register(self.on_validate), '%P', 0, 50, "columns")
        # self.__entry_value_table_columns['validatecommand'] = vcmd_columns
        # self.__entry_value_table_columns.delete(0, END)
        # self.__entry_value_table_columns.insert(0, columns)
        # self.__entry_value_table_columns.grid(row=1, column=3, sticky="NESW", padx=self.__gui.pad_general,
        #                                         pady=self.__gui.pad_general)
        # table
        self.__value_table_frame = Frame(master=self.__master, bg=self.__gui.bg, relief=SUNKEN, borderwidth=1)
        self.__value_table_frame.grid(row=2, column=0, padx=self.__gui.pad_general, pady=self.__gui.pad_general, sticky="NESW",
                                columnspan=4)
        self.redraw()

    def redraw(self):
        # create a local copy of self.__column_list that we can edit
        column_list = []
        for index, item in enumerate(self.__column_list):
            column_list.append("f" + str(item))
        column_list.insert(0, "x")
        self.__columns = len(column_list)
        # update row count
        self.__rows = int(self.__entry_value_table_rows.get())
        # force new layout to be applied by rebuilding the frame
        self.__value_table_frame.destroy()
        self.__value_table_frame = Frame(master=self.__master, bg=self.__gui.bg, relief=SUNKEN, borderwidth=1)
        self.__value_table_frame.grid(row=2, column=0, padx=self.__gui.pad_general, pady=self.__gui.pad_general, sticky="NESW",
                                columnspan=4)
        # table header
        self.__value_table_header = [Label(master=self.__value_table_frame, text=column_list[i], bg=self.__gui.bg) for i in range(self.__columns)]
        for column in range(len(self.__value_table_header)):
            self.__value_table_header[column].grid(row=0, column=column, sticky="NESW", padx=self.__gui.pad_general,
                                                           pady=self.__gui.pad_general)

        # table entry frame
        self.__value_table_entry_frame = Frame(master=self.__value_table_frame, bg=self.__gui.bg)
        self.__value_table_entry_frame.grid(row=2, column=0, padx=0, pady=0, sticky="NESW",
                                columnspan=self.__columns)
        # table entries
        self.__value_table_entry = [[Label(master=self.__value_table_entry_frame, text="", bg="white") for i in range(self.__columns)] for i in range(self.__rows)]
        for row in range(len(self.__value_table_entry)):
            for column in range(len(self.__value_table_entry[row])):
                self.__value_table_entry[row][column].grid(row=row, column=column, sticky="NESW", padx=1,
                                                           pady=1)
        for row in range(len(self.__value_table_entry)):
            self.__value_table_entry_frame.grid_rowconfigure(index=row, minsize=20)
        for column in range(len(self.__value_table_entry[0])):
            self.__value_table_entry_frame.grid_columnconfigure(index=column, minsize=60)
        self.__value_table_frame.grid()
        self.recalculate()

    def recalculate(self):
        for index in range(self.__rows):
            self.__value_table_entry[index][0].configure(text=str(int(self.__start.get())+index*int(self.__delta.get())))
        for index in range(1, self.__columns):
            for i in range(self.__rows):
                self.__value_table_entry[i][index].configure(text="")

    def set_columns(self, column_list):
        self.__column_list = column_list

    @staticmethod
    def on_validate(min, max, p=1):
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
            tmp = int(p)
        except ValueError:
            return False
        else:
            if tmp < int(min) or tmp > int(max):
                return False
            else:
                return True

    def set_table_delta(self, delta):
        self.__entry_value_table_delta.delete(0, END)
        self.__entry_value_table_delta.insert(0, delta)

    def set_table_start(self, start):
        self.__entry_value_table_start.delete(0, END)
        self.__entry_value_table_start.insert(0, start)
