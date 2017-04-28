from util import *

class Goose:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ImageObject:
    def __init__(self):
        self.geese = []
    
    def add_geese(self, x, y):
        self.geese.append(Goose(x, y))
    
    def pop_geese(self):
        self.geese.pop()

class Backend:
    def __init__(self):
        self.imageObjects = []
        print('back end initialized.')
    
    def get_imageObject(self):
        pass
    
