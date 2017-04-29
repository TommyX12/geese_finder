from gui import *
from backend import *

backendObject = Backend()
backendObject.load()

guiObject = GUI(backendObject)
guiObject.run()
