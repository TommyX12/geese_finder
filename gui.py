from backend import *
import tkinter

class GUI:
    def __init__(self, backendObject):
        self.backend = backendObject
        pass
    
    def run(self):
        root = tkinter.Tk();
        root.geometry('1024x640')
        pass
        
