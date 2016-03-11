# ddr
# 11.03.2016
# Externer Code; Quelle: Stackoverflow; User: http://stackoverflow.com/users/2805357/ddr
# V 1.0


class Node:
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val


class ParserTree:
    def __init__(self):
        self.__root = None
