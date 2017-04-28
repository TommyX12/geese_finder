from backend import *
import tkinter
from PIL import ImageTk, Image
class GUI:
    def __init__(self, backendObject):
        self.backend = backendObject
        pass
    
    def run(self):
        root = tkinter.Tk();
        canvas = tkinter.Canvas(root, width = 1024, height = 640)
        canvas.pack()
        
        #Load First image automatically
        path = "image1.jpg"
        img = Image.open(path)
        tk_img = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=tk_img)
        #Add hotkeys for labelling, undoing, next and previous
        #Re-render after all commands
        root.mainloop()
        pass
        
