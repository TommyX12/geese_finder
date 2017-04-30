from backend import *
import tkinter
from PIL import ImageTk, Image
from tkinter import PhotoImage
import math

ZOOM_MAX = 10.0

class GUI:
    current = None
    mouse_x = 0.0
    mouse_y = 0.0
    img_raw = None
    img = None
    path = None
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
        'nest': {'color': '#4488ff', 'r': 7},
        'ref':  {'color': '#ffffff', 'r': 3},
    }

    def __init__(self, backendObject):
        GUI.current = self
        
        self.width         = 1440
        self.height        = 1080
        
        self.backend       = backendObject
        self.image_objects = self.backend.get_image_objects()
        self.index         = 0
        
        self.zoom          = {'photo': 1.0, 'map': 1.0}
        self.zoom_center   = {'photo': Vector(0.5, 0.5), 'map': Vector(0.5, 0.5)}
        
        self.mode          = 'photo'
        self.goose_pos     = None
        self.goose_type    = ''
        
        self.root          = tkinter.Tk();
        self.canvas        = tkinter.Canvas(self.root, width = self.width, height = self.height)
        self.canvas.configure(scrollregion=(0,0,1000,1000))
        self.canvas.pack()
        self.text = None
        self.root.configure(background='grey')
        
        self.root.bind('<Key>', GUI.on_key_down)
        self.root.bind('<Motion>', GUI.on_mouse_moved)
        self.root.protocol("WM_DELETE_WINDOW", GUI.on_closing)
        
        GUI.img_raw_map = Image.open(self.backend.get_map().path)
    
    def image_to_screen(self, x, y):
        return Vector(x, y).sub(self.zoom_center[self.mode]).mul(self.zoom[self.mode]).add(self.zoom_center[self.mode])
    
    def screen_to_image(self, x, y):
        return Vector(x, y).sub(self.zoom_center[self.mode]).mul(1.0/self.zoom[self.mode]).add(self.zoom_center[self.mode])
    
    def on_closing():
        GUI.current.backend.save()
        GUI.current.root.destroy()
    
    def on_key_down(event):
        char = event.char
        
        if GUI.current.mode == 'photo':
            if char == 'z':
                GUI.current.change_zoom(GUI.mouse_x, GUI.mouse_y, -1.0)
            
            elif char == 'x':
                GUI.current.change_zoom(GUI.mouse_x, GUI.mouse_y, 1.0)
            
            elif char == 'f':
                GUI.current.switch_mode('map')

            elif char == 'a':
                GUI.current.change_image(-1)
                
            elif char == 'd':
                GUI.current.change_image(1)
                
            elif char == 'A':
                GUI.current.change_image(-5)
                
            elif char == 'D':
                GUI.current.change_image(5)
                
            elif char == 'q':
                GUI.current.pop_goose()
                
            elif char >= '0' and char <= '9':
                GUI.current.mark_goose(GUI.mouse_x, GUI.mouse_y, char)
            
            elif char == '`':
                GUI.current.mark_goose(GUI.mouse_x, GUI.mouse_y, 'nest')
            
            elif char == 'r':
                GUI.current.mark_goose(GUI.mouse_x, GUI.mouse_y, 'ref')
        
        elif GUI.current.mode == 'map':
            if char == 'z':
                GUI.current.change_zoom(GUI.mouse_x, GUI.mouse_y, -1.0)
            
            elif char == 'x':
                GUI.current.change_zoom(GUI.mouse_x, GUI.mouse_y, 1.0)
            
            elif char == 'c':
                GUI.current.confirm_goose(GUI.mouse_x, GUI.mouse_y)
                
            elif char == 'f':
                GUI.current.switch_mode('photo')
                GUI.current.goose_pos = None
    
    def change_zoom(self, x, y, delta):
        if delta > 0:
            self.zoom_center[self.mode] = self.screen_to_image(x, y)
            
        self.zoom[self.mode] += delta
        self.zoom[self.mode] = clamp(self.zoom[self.mode], 1.0, ZOOM_MAX)

        self.redraw()
    
    def switch_mode(self, mode):
        self.mode = mode
        self.redraw()
        
    def change_image(self, incr):
        index = self.index + incr
        index = clamp(index, 0, len(self.image_objects) - 1)
        if index != self.index:
            self.index = index
            self.redraw()
            self.backend.save()
    
    def mark_goose(self, x, y, type):
        u = self.screen_to_image(x, y)
        self.goose_pos  = u
        self.goose_type = type
        self.switch_mode('map')
    
    def confirm_goose(self, x, y):
        if self.goose_pos != None:
            u = self.screen_to_image(x, y)
            gps = self.backend.map_to_gps(u)
            self.get_current_image(True).add_goose(self.goose_pos.x, self.goose_pos.y, gps.x, gps.y, self.goose_type)
            self.goose_pos = None
            self.switch_mode('photo')
    
    def pop_goose(self):
        self.get_current_image().pop_goose()
        self.redraw()
    
    def on_mouse_moved(event):
        GUI.mouse_x = event.x / GUI.current.width
        GUI.mouse_y = event.y / GUI.current.height
    
    def load_image_file(self, path, dpi_scale):
        if path == self.backend.get_map().path:
            GUI.img_raw = GUI.img_raw_map

        elif path != GUI.path:
            GUI.img_raw = Image.open(path)
        
        GUI.path = path
        
        c = 1.0/dpi_scale
        d = Vector(self.width, self.height)
        u = self.screen_to_image(0, 0)
        w = u.add(Vector(c, c))
        u = u.mul2(GUI.img_raw.width, GUI.img_raw.height)
        w = w.mul2(GUI.img_raw.width, GUI.img_raw.height)
        GUI.img = ImageTk.PhotoImage(GUI.img_raw.crop((int(u.x), int(u.y), int(w.x), int(w.y))).resize((int(d.x), int(d.y))))
        #  GUI.img = PhotoImage(file=path)
    
    def get_current_image(self, force_non_map=False):
        if self.mode == 'map' and not force_non_map:
            return self.backend.get_map()
        
        return self.image_objects[self.index]
    
    def get_text(self):
        cur = self.get_current_image()
        count = str(len(cur.geese))
        nests = 0
        refs = 0
        for goose in cur.geese:
            if goose.type == 'nest':
                nests += 1
                
            elif goose.type == 'ref':
                refs += 1
            
        texts = [
            str(self.index + 1) + '/' + str(len(self.image_objects)),
            cur.path,
            'count: ' + str(len(cur.geese)),
            'nests: ' + str(nests),
            'refs: ' + str(refs),
            self.mode,
        ]
        return ' | '.join([str(i) for i in texts])
    
    def redraw(self, text_only=False):
        if not text_only:
            self.canvas.delete("all")
            path = self.get_current_image().path
            self.load_image_file(path, self.zoom[self.mode])
            self.canvas.create_image(0, 0, anchor='nw', image=GUI.img)
            if self.mode == 'photo':
                for goose in self.get_current_image().get_geese():
                    self.draw_goose(goose.x, goose.y, goose.type)
                    
            elif self.mode == 'map':
                for image_object in self.image_objects:
                    for goose in image_object.get_geese():
                        self.draw_goose(goose.lat, goose.lon, goose.type, True)
        
        if self.text != None:
            self.canvas.delete(self.text)

        self.canvas.create_rectangle(0, 0, self.width, 25, fill='black')
        self.text = self.canvas.create_text(0, 0, fill='white', font='Arial 14', text=self.get_text(), anchor='nw')
    
    def draw_goose(self, x, y, type, use_gps=False):
        if use_gps:
            coord = self.backend.gps_to_map(Vector(x, y))
            x = coord.x
            y = coord.y
        
        u = self.image_to_screen(x, y)
        x = u.x
        y = u.y
        x *= self.width
        y *= self.height
        r = GUI.type_style[type]['r']
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill = GUI.type_style[type]['color'], outline = '#ff0000')
    
    def run(self):
        self.redraw()
        self.root.mainloop()
