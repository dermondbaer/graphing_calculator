#   Pascal Mehnert
#   05.02.2016
#
#   V 0.1


class Function(object):
    def __init__(self, function_term, tkinter_objects):
        self.__function_term = function_term
        self.__tkinter_objects = tkinter_objects

    def get_function_term(self):
        return self.__function_term

    def get_tkinter_objects(self):
        return self.__tkinter_objects
