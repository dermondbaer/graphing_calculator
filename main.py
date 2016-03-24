# Paul Birke, Pascal Mehnert
# 11.03.2016
# 
# V 0.1


from Gui import *

class Application(object):
    def __init__(self, title):
        self.__title = title
        self.__gui = Gui(self, title)
  
    def start(self):
        self.__gui.start(self.__title)

    def stop(self):
        raise SystemExit

  # config
title = "Not so graphing calculator"

# main
app = Application(title)
app.start()
