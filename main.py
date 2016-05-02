# Paul Birke, Pascal Mehnert
# 11.03.2016
#

from gui import *


class Application(object):
    def __init__(self, title):
        self.__title = title
        self.__gui = Gui(self, title)
  
    def start(self):
        self.__gui.start()

    @staticmethod
    def stop():
        raise SystemExit

# config
title_ = "Not so graphing calculator"

# main
app = Application(title_)
app.start()
