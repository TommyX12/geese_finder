from gui import *
from backend import *

backendObject = Backend()
guiObject = GUI(backendObject)

guiObject.run()
