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

def avg_fields_dict(dicts, i, j):
    data_avg = {}
    for key in dicts[i]:
        field = {}
        
        total = 0.0
        not_float = False
        for k in range(i, j):
            raw = dicts[k][key]['value']
            if len(raw) > 0 and raw[0] == '"':
                raw = raw[1:-1]
            
            try:
                total += float(raw)
                
            except ValueError:
                not_float = True
                break
        
        if not_float:
            continue
            
        field['value'] = total / (j - i)
        
        field['units'] = dicts[i][key]['units']
        data_avg[key] = field
        
    return data_avg
        

print('reading file...')
dicts = csv_to_dicts(read_file('out.csv'))

print('extracting parameters...')
for i in range(len(dicts)):
    dict = dicts[i]
    fields = {}
    j = 1
    num_unknown = 1
    while True:
        field_name = 'Field ' + str(j)
        value_name = 'Value ' + str(j)
        units_name = 'Units ' + str(j)
        if field_name in dict and value_name in dict and units_name in dict:
            fn = dict[field_name]
            if fn == 'unknown':
                fn = fn + str(num_unknown)
                num_unknown += 1
                
            fields[fn] = {
                'value': dict[value_name],
                'units': dict[units_name],
            }
            dict.pop(field_name)
            dict.pop(value_name)
            dict.pop(units_name)
            
        else:
            break
        
        j += 1
    
    dict['fields'] = fields

gps_data = []

print('filtering gps metadata...')
for dict in dicts:
    if dict['Message'] == 'gps_metadata' and dict['Type'] == 'Data':
        gps_data.append(dict['fields'])

gps_data_avg = []

print('averaging values...')
cur_timestamp = 0
cur_count = 0
id = 1
for i in range(len(gps_data)):
    fields = gps_data[i]
    timestamp = int(fields['timestamp']['value'][1:-1])
    if timestamp == cur_timestamp:
        cur_count += 1
        if cur_count == 10:
            avg1 = avg_fields_dict(gps_data, i - 9, i - 4)
            avg1['id'] = {
                    #  'value': avg1['timestamp']['value'] * 2,
                    'value': id,
                    'units': '',
            }
            id += 1
            avg2 = avg_fields_dict(gps_data, i - 4, i + 1)
            avg2['id'] = {
                    #  'value': avg2['timestamp']['value'] * 2 + 1,
                    'value': id,
                    'units': '',
            }
            id += 1
            gps_data_avg.append(avg1)
            gps_data_avg.append(avg2)
            
            cur_count = 0
            
    else:
        cur_timestamp = timestamp
        cur_count = 1

print('writing file...')
field_keys = []
for key in gps_data_avg[0]:
    field_keys.append(key)

field_keys.sort()

processed = [[]]
for key in field_keys:
    processed[0].append(key + "_value")
    processed[0].append(key + "_units")

processed[0].append('')

for fields in gps_data_avg:
    out = []
    for key in field_keys:
        out.append(str(fields[key]['value']))
        out.append(str(fields[key]['units']))
    
    out.append('')
    
    processed.append(out)
    
GPS_DATA_FILENAME = 'gps_data.csv'

file = open(GPS_DATA_FILENAME, 'w')
file.write('\n'.join([','.join(i) for i in processed]))
file.close()

print('done.')
