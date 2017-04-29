import os, sys, codecs
import glob

def list_dir(pattern):
    return glob.glob(pattern)   

def read_file(path):
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
