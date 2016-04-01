# Pascal Mehnert
# 07.03.2016
#
# V 0.1


class Line(object):
    def __init__(self, coord_sup, coord_dir, pos_sup, pos_dir, tkinter):
        self.__coordinates_support_vector = coord_sup
        self.__coordinates_direction_vector = coord_dir
        self.__position_support_vector = pos_sup
        self.__position_direction_vector = pos_dir
        self.__tkinter_object = tkinter

    def get_coordinates_support_vector(self):
        return self.__coordinates_support_vector

    def get_coordinates_direction_vector(self):
        return self.__coordinates_direction_vector

    def get__position_support_vector(self):
        return self.__position_support_vector

    def get_position_direction_vector(self):
        return self.__position_direction_vector

    def get_tkinter_object(self):
        return self.__tkinter_object
