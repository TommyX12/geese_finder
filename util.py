import os, sys, codecs


def read_file(path):
    with open(path, encoding='utf-8-sig') as f:
        content = f.read()
    
    return content

def csv_to_arrays(data):
    content = data.splitlines()

    for i in range(len(content)):
        content[i] = content[i].split(',')

    return content

def csv_to_dicts(data):
    array = csv_to_arrays(data)
    keys = array[0]
    
    content = [{} for i in range(len(array) - 1)]
    for i in range(len(array) - 1):
        for j in range(len(keys)):
            if j >= len(array[i + 1]):
                break
            
            content[i][keys[j]] = array[i + 1][j]
    
    return content



