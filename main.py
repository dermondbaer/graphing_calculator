# Paul Birke, Pascal Mehnert
# 11.03.2016
# 
# V 0.1


from Gui import Gui *

class Application(object):
  def __init__(self):
    self.__gui = Gui()
  
  def start(self):
    self.__gui.start()


# main
app = Application()
app.start()
