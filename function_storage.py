# Paul Birke
# 31.05.2016
# function storage

from tkinter import *

class Function_storage(object):
    def __init__(self, gui, master_frame, value_table):
        self.__master = master_frame
        self.__gui = gui
        self.__value_table = value_table
        self.__function_count = 10

        # actual function storage
        self.__function = ["" for i in range(self.__function_count)]
        self.__function[0] = "9 x * 3 - 6"

        # function storage master frame
        self.__function_storage_frame = Frame(master=self.__master, bg=self.__gui.bg)
        self.__function_storage_frame.grid(row=0, column=0, sticky="NESW", padx=self.__gui.pad_general,
                                               pady=self.__gui.pad_general)
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
        # # function storage name label
        # self.__lbl_function_storage = [Label(master=self.__function_storage_frame, text="f"+str(i)+":", bg=self.__gui.bg) for i in range(self.__function_count)]
        # for i in range(self.__function_count):
        #     self.__lbl_function_storage[i].grid(row=i+1, column=1, sticky="NSW", padx=self.__gui.pad_general,
        #                                        pady=self.__gui.pad_general)

        # # value table selection
        # self.__selection_frame = Frame(master=self.__master, bg=self.__gui.bg, relief=GROOVE, borderwidth=2)
        # self.__selection_frame.grid(row=1, column=0, sticky="NESW", padx=self.__gui.pad_general,
        #                                        pady=self.__gui.pad_general)
        # # value table selection info label
        # self.__lbl_selection = Label(master=self.__selection_frame, text="Show functions:", bg=self.__gui.bg)
        # self.__lbl_selection.grid(row=0, column=0, sticky="NSW", padx=self.__gui.pad_general,
        #                                        pady=self.__gui.pad_general, columnspan=2)
        #
        # # value table selection
        # self.__entry_selection = [Label(master=self.__selection_frame, text="f"+str(i)+":", bg=self.__gui.bg) for i in range(self.__function_count)]
        # for i in range(self.__function_count):
        #     self.__entry_selection[i].grid(row=i+1, column=0, sticky="NSW", padx=self.__gui.pad_general,
        #                                        pady=self.__gui.pad_general)
    # def tkinter_var(self, i):
    #     self.__selection[i] = BooleanVar()
    #     self.__selection[i].set(0)
    #     return self.__selection[i]

    def reformat_table(self):
        functions = []
        for index, item in enumerate(self.__selection):
            if item.get() == True:
                functions.append(index)
        self.__gui.value_table.redraw(functions)

    def get_function(self, index):
        return self.__function[index]

    def set_function(self, index, function=""):
        self.__function[index] = function
        for i in range(self.__function_count):
            self.__lbl_function_storage[i].configure(text=function)
