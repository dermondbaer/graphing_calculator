#   Pascal Mehnert
#   29.01.2016
#
#   V 0.1

from geometry_tool.gui import Gui

gui = Gui()

'''
print(gui.get_figures())
p = gui.create_point((1,1))
time.sleep(5)
gui.del_point(p)
print(gui.get_figures())
'''

gui.get_master().mainloop()
