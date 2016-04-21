#   Pascal Mehnert
#   03.02.2016
#
#   V 1.0


class Distance(object):
    def __init__(self, coord_a, coord_b, pos_a, pos_b, tkinter_objects):
        self.__coordinates_a = coord_a
        self.__coordinates_b = coord_b
        self.__position_a = pos_a
        self.__position_b = pos_b
        self.__tkinter_objects = tkinter_objects

    def get_coordinates_a(self):
        return self.__coordinates_a

    def get_coordinates_b(self):
        return self.__coordinates_b

    def get_position_a(self):
        return self.__position_a

    def get_position_b(self):
        return self.__position_b

    def get_tkinter_objects(self):
        return self.__tkinter_objects
