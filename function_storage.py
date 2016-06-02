# Paul Birke
# 31.05.2016
# function storage

from tkinter import *

class Function_storage(object):
    def __init__(self, gui, master_frame, function_count):
        self.__master = master_frame
        self.__gui = gui
        self.__function_count = function_count

        # actual function storage
        self.__function = ["" for i in range(self.__function_count)]
        # self.__function[0] = "2 x"

        # function storage master frame
        self.__function_storage_frame = Frame(master=self.__master, bg=self.__gui.bg)
        self.__function_storage_frame.grid(row=0, column=0, sticky="NESW", padx=self.__gui.pad_general,
                                               pady=self.__gui.pad_general)
        self.__function_storage_frame.grid_columnconfigure(index=2, minsize=120)

        # function storage info label
        self.__lbl_function_storage_info = Label(master=self.__function_storage_frame, text="Saved functions:", bg=self.__gui.bg)
        self.__lbl_function_storage_info.grid(row=0, column=0, sticky="NSW", padx=self.__gui.pad_general,
                                               pady=self.__gui.pad_general, columnspan=2)
        # function storage selection
        self.__selection = [BooleanVar() for i in range(self.__function_count)]
        self.__entry_selection = [Checkbutton(master=self.__function_storage_frame, text="f"+str(i)+":", bg=self.__gui.bg, activebackground=self.__gui.bg, command=self.reformat_table, variable=self.__selection[i]) for i in range(self.__function_count)]
        for i in range(self.__function_count):
            self.__entry_selection[i].grid(row=i+1, column=0, sticky="NSW", padx=self.__gui.pad_general,
                                               pady=self.__gui.pad_general)

        # function storage labels
        self.__lbl_function_storage = [Label(master=self.__function_storage_frame, text=self.__function[i], bg=self.__gui.bg) for i in range(self.__function_count)]
        for i in range(self.__function_count):
            self.__lbl_function_storage[i].grid(row=i+1, column=1, sticky="NSW", padx=self.__gui.pad_general,
                                               pady=self.__gui.pad_general)

    def reformat_table(self):
        # list comprehension to filter out all columns that are deselected
        functions = [i for i, col in enumerate(self.__selection) if col.get() == True and self.__function[i] != ""]
        # update selection (necessary if empty functions have been selected)
        for i in range(self.__function_count):
            if self.__function[i] == "":
                self.__entry_selection[i].deselect()
        # get the value table to update
        self.__gui.value_table.set_columns(functions)
        self.__gui.value_table.redraw()

    def get_function(self, index):
        return self.__function[index]

    def set_function(self, index, function=""):
        self.__function[index] = function
        # for i in range(self.__function_count):
        #     self.__lbl_function_storage[i].configure(text=function)
        self.__lbl_function_storage[index].configure(text=function)
        self.__gui.value_table.recalculate()

    def reset(self):
        self.__function = ["" for i in range(self.__function_count)]
        for i in range(self.__function_count):
            self.__lbl_function_storage[i].configure(text="")
            self.__entry_selection[i].deselect()
        self.__gui.value_table.set_columns([])
        self.__gui.value_table.redraw()
