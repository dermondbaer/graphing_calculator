# Paul Birke, Pascal Mehnert
# 11.03.2016
#

from gui import *


class Application(Gui):
    def __init__(self, title):
        Gui.__init__(self, self, title)

    @staticmethod
    def stop_application():
        raise SystemExit

# config
title_ = "Not so graphing calculator"

# main
app = Application(title_)
app.start()
