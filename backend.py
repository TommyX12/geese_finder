import math
from util import *


"""

TODOs:
- display image name and other stats on bottom of screen
- allow indicator of previously marked geese somehow
- allow zooming of image at point
- test GPS and lens correction

"""

class Goose:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
    
    def get_data(self, image_object):
        corrected = correct_point(self.x, self.y, image_object.latitude, image_object.longitude, image_object.heading)
        return {
            'x':             self.x,
            'y':             self.y,
            'type':          self.type,
            'id':            image_object.id,
            'cam-yaw':       image_object.yaw,
            'cam-pitch':     image_object.pitch,
            'cam-roll':      image_object.roll,
            'cam-altitude':  image_object.altitude,
            'image-name':    image_object.path,
            'image-time':    image_object.time,
            'cam-longitude': image_object.longitude,
            'cam-latitude':  image_object.latitude,
            'cam-heading':   image_object.heading,
            'corrected-x':   corrected[0],
            'corrected-y':   corrected[1],
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
            heading   = 0,
            time      = 0,
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
        self.heading   = heading
        self.time      = time
    
    def add_goose(self, x, y, type):
        self.geese.append(Goose(x, y, type))
    
    def pop_goose(self):
        if len(self.geese) > 0:
            self.geese.pop()
    
    def get_geese(self):
        return self.geese

GPS_DATA_FILENAME = 'gps_data.csv'
GEESE_RAW_FILENAME = 'output/geese_raw.csv'
NESTS_RAW_FILENAME = 'output/nests_raw.csv'
COUNTS_FILENAME = 'output/counts.csv'

# latex = string('\n');

def correct_point(x, y, lat, lon, heading):
    r = math.sqrt((x - 0.5)**2 + (y - 0.5)**2)
    x = (x-0.5)*(1+1.0*(r**2))/0.5 * 83 / 1000000
    y = (y-0.5)*(1+1.0*(r**2))/0.5 * 83 / 1000000
    
    xu = lat - x * math.sin(heading) + y * math.cos(heading)
    yu = lon + y * math.sin(heading) + x * math.cos(heading)
    # latex += string(i)) + string('&')+ string(loc(i, 1)) + string('&') + string(loc(i, 2)) + string('\\')
    return (xu, yu)

                                
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
            gps_data_entry = gps_data[id - 1]
            image_object = ImageObject(
                id,
                geese[id] if id in geese else [],
                path      = path,
                yaw       = 0,
                pitch     = 0,
                roll      = 0,
                altitude  = 0,
                longitude = semicircles_to_degrees(float(gps_data_entry['position_long_value'])),
                latitude  = semicircles_to_degrees(float(gps_data_entry['position_lat_value'])),
                heading   = float(gps_data_entry['heading_value']),
                time      = gps_data_entry['readable_time_value'],
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
    # image_object = backend.get_image_object_by_id(1)
    # image_object.add_goose(0.5, 0.5, 'bad goose')
    backend.save()
