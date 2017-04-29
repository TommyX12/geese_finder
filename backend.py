from util import *

class Goose:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
    
    def get_data(self, image_object):
        return {
            'x':             self.x,
            'y':             self.y,
            'type':          self.type,
            'id':            image_object.id,
            #  'cam-yaw':       image_object.yaw,
            #  'cam-pitch':     image_object.pitch,
            #  'cam-roll':      image_object.roll,
            #  'cam-altitude':  image_object.altitude,
            'image-name':    image_object.path,
            'cam-longitude': image_object.longitude,
            'cam-latitude':  image_object.latitude,
        }
    
    def from_data(data):
        return Goose(
            float(data['x']),
            float(data['y']),
            str(data['type']),
        )

class ImageObject:
    def __init__(self,
            id        = 0,
            geese     = [],
            path      = '',
            yaw       = 0,
            pitch     = 0,
            roll      = 0,
            altitude  = 0,
            longitude = 0,
            latitude  = 0,
            ):
        self.id        = id
        self.geese     = geese
        self.path      = path
        self.yaw       = yaw
        self.pitch     = pitch
        self.roll      = roll
        self.altitude  = altitude
        self.longitude = longitude
        self.latitude  = latitude
    
    def add_goose(self, x, y, type):
        self.geese.append(Goose(x, y, type))
    
    def pop_goose(self):
        if len(self.geese) > 0:
            self.geese.pop()
    
    def get_geese(self):
        return self.geese

GPS_DATA_FILENAME = 'gps_data.csv'
GEESE_RAW_FILENAME = 'geese_raw.csv'
NESTS_RAW_FILENAME = 'nests_raw.csv'
COUNTS_FILENAME = 'counts.csv'

_count = 0
def image_path_to_id(path):
    #  global _count
    #  _count += 1
    #  return _count
    
    return int(path[path.rindex('img') + 3:path.rindex('.')])

class Backend:
    def __init__(self):
        self.image_objects_list = []
        self.image_objects_dict = {}
        print('back end initialized.')
    
    def load(self):
        gps_data    = csv_to_dicts(read_file(GPS_DATA_FILENAME))
        geese_raw   = csv_to_dicts(read_file(GEESE_RAW_FILENAME))
        image_paths = list_dir('images/*.jpg')
        
        geese = {}
        for goose_raw in geese_raw:
            id = int(goose_raw['id'])
            if id not in geese:
                geese[id] = []
                
            geese[id].append(Goose.from_data(goose_raw))
        
        ids = []
        for path in image_paths:
            id = image_path_to_id(path)
            image_object = ImageObject(
                id,
                geese[id] if id in geese else [],
                path      = path,
                yaw       = 0,
                pitch     = 0,
                roll      = 0,
                altitude  = 0,
                longitude = gps_data[id - 1]['position_long_value'],
                latitude  = gps_data[id - 1]['position_lat_value'],
            )
            
            ids.append(id)
            self.image_objects_dict[id] = image_object
        
        ids.sort()
        
        for id in ids:
            self.image_objects_list.append(self.image_objects_dict[id])
            
        print('back end loaded.')
    
    def get_image_objects(self):
        return self.image_objects_list
    
    def get_image_object_by_id(self, id):
        return self.image_objects_dict[id]
    
    def save(self):
        dicts = []
        dicts_nests = []
        total_geese = 0
        total_types = {}
        for image_object in self.image_objects_list:
            dicts += [goose.get_data(image_object) for goose in image_object.get_geese()]
        
        for goose in dicts:
            if goose['type'] == 'nest':
                dicts_nests.append(goose)
            
            else:
                total_geese += 1
                total_types[goose['type']] = 1
        
        counts = [{
            'total-geese': total_geese,
            'total-types': len(total_types),
        }]
        
        write_file(GEESE_RAW_FILENAME, dicts_to_csv(dicts))
        write_file(NESTS_RAW_FILENAME, dicts_to_csv(dicts_nests))
        write_file(COUNTS_FILENAME, dicts_to_csv(counts))

if __name__ == '__main__':
    backend = Backend()
    backend.load()
    image_object = backend.get_image_object_by_id(1)
    #  image_object.add_goose(0.5, 0.5, 'bad goose')
    backend.save()
