#   Pascal Mehnert
#   03.02.2016
#
#   V 1.0


class Point(object):
    def __init__(self, coordinates, position, tkinter):
        self.__coordinates = coordinates
        self.__position = position
        self.__tkinter_objects = [tkinter]

    def get_coordinates(self):
        return self.__coordinates

    def get_position(self):
        return self.__position

    def get_tkinter_objects(self):
        return self.__tkinter_objects
