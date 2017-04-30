import os, sys, codecs
import glob

def list_dir(pattern):
    return glob.glob(pattern)   

def read_file(path):
    if not os.path.exists(path):
        write_file(path, '')

    with open(path, encoding='utf-8-sig') as f:
        content = f.read()
    
    return content

def write_file(path, data):
    file = open(path, 'w')
    file.write(data)
    file.close()

def csv_to_arrays(data):
    content = data.splitlines()

    for i in range(len(content)):
        content[i] = content[i].split(',')

    return content

def csv_to_dicts(data):
    array = csv_to_arrays(data)
    if len(array) == 0:
        return {}
    
    keys = array[0]
    
    content = [{} for i in range(len(array) - 1)]
    for i in range(len(array) - 1):
        for j in range(len(keys)):
            if j >= len(array[i + 1]):
                break
            
            content[i][keys[j]] = array[i + 1][j]
    
    return content

def dicts_to_csv(dicts):
    if len(dicts) == 0:
        return ''

    field_keys = []
    for key in dicts[0]:
        field_keys.append(key)

    field_keys.sort()

    processed = [[]]
    for key in field_keys:
        processed[0].append(key)

    processed[0].append('')

    for fields in dicts:
        out = []
        for key in field_keys:
            out.append(str(fields[key]))
        
        out.append('')
        
        processed.append(out)
    
    return '\n'.join([','.join(i) for i in processed])

MAX_SEMICIRCLES = 2**31

def semicircles_to_degrees(semicircles):
    return semicircles * (180.0 / MAX_SEMICIRCLES)

def clamp(num, l, r):
    if num < l:
        return l

    if num > r:
        return r
    
    return num

def solve_matrix_2d(m, v):
    #  idet = 1 / (a * d - b * c)
    #  ia = d * idet
    #  ib = -b * idet
    #  ic = -c * idet
    #  id = a * idet
    #  return Vector(ia * e + ib * f, ic * e + id * f)
    return m.inverse().mul_vec(v)

class Vector:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    def add(self, v):
        return Vector(self.x + v.x, self.y + v.y)
    
    def sub(self, v):
        return Vector(self.x - v.x, self.y - v.y)

    def mul(self, c):
        return Vector(self.x * c, self.y * c)
    
    def mul2(self, x, y):
        return Vector(self.x * x, self.y * y)
    
    def __str__(self):
        return str(self.x) + ', ' + str(self.y)
    
    def to_tuple(self):
        return (self.x, self.y)

class Matrix:
    def __init__(self, a, b, c=None, d=None):
        if c == None and d == None:
            self.a = a.x
            self.b = b.x
            self.c = a.y
            self.d = b.y
        
        else:
            self.a = a
            self.b = b
            self.c = c
            self.d = d
    
    def mul(self, c):
        return Matrix(self.a * c, self.b * c, self.c * c, self.d * c)
    
    def mul_vec(self, v):
        return Vector(v.x * self.a + v.y * self.b, v.x * self.c + v.y * self.d)
    
    def inverse(self):
        return Matrix(self.d, -self.b, -self.c, self.a).mul(1 / (self.a * self.d - self.b * self.c))
    
    def mul_mat(self, m):
        return Matrix(self.mul_vec(Vector(m.a, m.c)), self.mul_vec(Vector(m.b, m.d)))

if __name__ == '__main__':
    pass
