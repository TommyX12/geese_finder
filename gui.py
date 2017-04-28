from backend import *
import tkinter
from PIL import ImageTk, Image
class GUI:
    def __init__(self, backendObject):
        self.backend = backendObject
        pass
    
    def run(self):
        root = tkinter.Tk();
        root.geometry('1024x640')
        
        #Load First image automatically
        path = "image1.jpg"
        img = ImageTk.PhotoImage(Image.open(path))
        #Add hotkeys for labelling, undoing, next and previous
        #Re-render after all commands
        pass
        
