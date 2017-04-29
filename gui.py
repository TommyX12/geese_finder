from backend import *
import tkinter
from PIL import ImageTk, Image
from tkinter import PhotoImage
import math

class GUI:
    current = None
    mouse_x = 0.0
    mouse_y = 0.0
    img = None
    type_style = {
        '1':    {'color': '#ff0000', 'r': 5},
        '2':    {'color': '#00ff00', 'r': 5},
        '3':    {'color': '#0000ff', 'r': 5},
        '4':    {'color': '#ffff00', 'r': 5},
        '5':    {'color': '#00ffff', 'r': 5},
        '6':    {'color': '#ff00ff', 'r': 5},
        '7':    {'color': '#ff8800', 'r': 5},
        '8':    {'color': '#88ff00', 'r': 5},
        '9':    {'color': '#8800ff', 'r': 5},
        '0':    {'color': '#0088ff', 'r': 5},
        'nest': {'color': '#4488ff', 'r': 10},
    }

    def __init__(self, backendObject):
        GUI.current = self
        
        self.width = 1024
        self.height = 640
        
        self.backend = backendObject
        self.image_objects = self.backend.get_image_objects()
        self.index = 0
        
        self.root = tkinter.Tk();
        self.canvas = tkinter.Canvas(self.root, width = self.width, height = self.height)
        self.canvas.pack()
        self.root.configure(background='grey')
        
        self.root.bind('<Key>', GUI.on_key_down)
        self.root.bind('<Motion>', GUI.on_mouse_moved)
        self.root.protocol("WM_DELETE_WINDOW", GUI.on_closing)
    
    def on_closing():
        GUI.current.backend.save()
        GUI.current.root.destroy()
    
    def on_key_down(event):
        char = event.char

        if char == 'a':
            GUI.current.prev_image()
            
        elif char == 'd':
            GUI.current.next_image()
            
        elif char == 'q':
            GUI.current.pop_goose()
            
        elif char >= '0' and char <= '9':
            GUI.current.mark_goose(GUI.mouse_x, GUI.mouse_y, char)
        
        elif char == '`':
            GUI.current.mark_goose(GUI.mouse_x, GUI.mouse_y, 'nest')
        
    
    def prev_image(self):
        if self.index > 0:
            self.index -= 1
            self.redraw()
            self.backend.save()
    
    def next_image(self):
        if self.index < len(self.image_objects) - 1:
            self.index += 1
            self.redraw()
            self.backend.save()
    
    def mark_goose(self, x, y, type):
        self.image_objects[self.index].add_goose(x, y, type)
        self.draw_goose(x, y, type)
    
    def pop_goose(self):
        self.image_objects[self.index].pop_goose()
        self.redraw()
    
    def on_mouse_moved(event):
        GUI.mouse_x = event.x / GUI.current.width
        GUI.mouse_y = event.y / GUI.current.height
    
    def load_image_file(path):
        GUI.img = ImageTk.PhotoImage(Image.open(path).resize((GUI.current.width, GUI.current.height)))
    
    def redraw(self):
        self.canvas.delete("all")
        #  path = 'image1.jpg'
        path = self.image_objects[self.index].path
        #  img = PhotoImage(file=path)
        GUI.load_image_file(path)
        self.canvas.create_image(0, 0, anchor='nw', image=GUI.img)
        for goose in self.image_objects[self.index].geese:
            self.draw_goose(goose.x, goose.y, goose.type)
            
        #  self.canvas.create_rectangle(65, 35, 135, 65, fill="yellow")
        
        #  img = PhotoImage(width=self.width, height=self.height)
        #  self.canvas.create_image(self.width/2, self.height/2, image=img, state="normal")

        #  for x in range(4 * self.width):
            #  y = int(self.height/2 + self.height/4 * math.sin(x/80.0))
            #  img.put("#ffffff", (x//4,y))
    
    def draw_goose(self, x, y, type=''):
        x *= self.width
        y *= self.height
        r = GUI.type_style[type]['r']
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill = GUI.type_style[type]['color'], outline = '#ff0000')
    
    def run(self):
        #Add hotkeys for labelling, undoing, next and previous
        #Re-render after all commands
        self.redraw()
        self.root.mainloop()
        
