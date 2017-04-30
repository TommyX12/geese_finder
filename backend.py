import math
from util import *


"""

TODOs:
- display image name and other stats on bottom of screen
- extensive testing
- research on features of each type of goose

done:
- allow zooming of image at point
- count number of geese of each type
- improve geese type identification

later:
- allow indicator of previously marked geese somehow
- mark gps when marking on picture
- interpolate using reference points
- click on map geese to jump to the picture with corresponding marking
- print random shit

"""

class Goose:
    def type_is_goose(type):
        return type >= '0' and type <= '9'

    def __init__(self, x, y, lat, lon, type):
        self.x    = x
        self.y    = y
        self.lat  = lat
        self.lon  = lon
        self.type = type
    
    def get_data(self, image_object):
        #  corrected = correct_point(self.x, self.y, image_object.latitude, image_object.longitude, image_object.heading)
        return {
            'x':          self.x,
            'y':          self.y,
            'latitude':   self.lat,
            'longitude':  self.lon,
            'type':       self.type,
            'image-id':   image_object.id,
            #  'cam-yaw':       image_object.yaw,
            #  'cam-pitch':     image_object.pitch,
            #  'cam-roll':      image_object.roll,
            #  'cam-altitude':  image_object.altitude,
            'image-name': image_object.path,
            #  'image-time': image_object.time,
            #  'cam-latitude':  image_object.latitude,
            #  'cam-longitude': image_object.longitude,
            #  'cam-heading':   image_object.heading,
            #  'corrected-x':   corrected[0],
            #  'corrected-y':   corrected[1],
        }
    
    def from_data(data):
        return Goose(
            float(data['x']),
            float(data['y']),
            float(data['latitude']),
            float(data['longitude']),
            str(data['type']),
        )

class ImageObject:
    def __init__(self,
            backend   = None,
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
        self.backend   = backend
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
    
    def add_goose(self, x, y, lat, lon, type):
        self.geese.append(Goose(x, y, lat, lon, type))
    
    def pop_goose(self):
        if len(self.geese) > 0:
            return self.geese.pop()

        return None
    
    def get_geese(self):
        return self.geese

#  GPS_DATA_FILENAME = 'gps_data.csv'
MAP_FILENAME = 'geo_info/map.png'
CORNERS_FILENAME = 'geo_info/corners.csv'
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
    # global _count
    # _count += 1
    # return _count

    # return int(path[path.rindex('img') + 3:path.rindex('.')])

    result = 0
    exp = 1
    i = len(path) - 1
    while i >= 0 and not path[i].isdigit():
        i -= 1

    if i < 0:
        return 0

    while i >= 0 and path[i].isdigit():
        result += int(path[i]) * exp
        i -= 1
        exp *= 10

    return result
    

class Backend:
    def __init__(self):
        self.image_objects_list = []
        self.image_objects_dict = {}
        print('back end initialized.')
    
    def load(self):
        #  gps_data    = csv_to_dicts(read_file(GPS_DATA_FILENAME))
        geese_raw   = csv_to_dicts(read_file(GEESE_RAW_FILENAME))
        corners     = csv_to_dicts(read_file(CORNERS_FILENAME))
        image_paths = list_dir('images/*.jpg')
        
        geese_id = {}
        for goose_raw in geese_raw:
            id = int(goose_raw['image-id'])
            if id not in geese_id:
                geese_id[id] = []
                
            geese_id[id].append(Goose.from_data(goose_raw))
        
        ids = []
        for path in image_paths:
            id = image_path_to_id(path)
            #  gps_data_entry = gps_data[id - 1]
            image_object = ImageObject(
                self,
                id,
                geese_id[id] if id in geese_id else [],
                path      = path,
                yaw       = 0,
                pitch     = 0,
                roll      = 0,
                altitude  = 0,
                #  longitude = semicircles_to_degrees(float(gps_data_entry['position_long_value'])),
                #  latitude  = semicircles_to_degrees(float(gps_data_entry['position_lat_value'])),
                #  heading   = float(gps_data_entry['heading_value']),
                #  time      = gps_data_entry['readable_time_value'],
            )
            
            ids.append(id)
            self.image_objects_dict[id] = image_object
        
        ids.sort()
        
        for id in ids:
            self.image_objects_list.append(self.image_objects_dict[id])
        
        self.map = ImageObject(
            path = MAP_FILENAME,
        )
        
        u1 = Vector(corners[0]['x'], corners[0]['y'])
        u2 = Vector(corners[1]['x'], corners[1]['y'])
        u3 = Vector(corners[2]['x'], corners[2]['y'])
        v1 = Vector(corners[0]['lat'], corners[0]['lon'])
        v2 = Vector(corners[1]['lat'], corners[1]['lon'])
        v3 = Vector(corners[2]['lat'], corners[2]['lon'])
        self.corners_u = u1
        self.corners_v = v1
        
        a1 = u2.sub(u1)
        a2 = u3.sub(u1)
        b1 = v2.sub(v1)
        b2 = v3.sub(v1)
        
        self.corners_mu = Matrix(b1, b2).mul_mat(Matrix(a1, a2).inverse())
        self.corners_mv = Matrix(a1, a2).mul_mat(Matrix(b1, b2).inverse())
        
        # u = map, v = gps, mu = from map, mv = from gps
            
        print('back end loaded.')
    
    def get_image_objects(self):
        return self.image_objects_list
    
    def get_image_object_by_id(self, id):
        return self.image_objects_dict[id]
    
    def get_map(self):
        return self.map
    
    def gps_to_map(self, gps):
        #  tl = self.corners['top_left']
        #  tr = self.corners['top_right']
        #  bl = self.corners['bottom_left']
        #  br = self.corners['bottom_right']
        #  dx = tr.sub(tl)
        #  dy = bl.sub(tl)
        #  return solve_matrix_2d(dx.x, dy.x, dx.y, dy.y, gps.x - tl.x, gps.y - tl.y)
        return self.corners_mv.mul_vec(gps.sub(self.corners_v)).add(self.corners_u)
    
    def map_to_gps(self, map):
        #  tl = self.corners['top_left']
        #  tr = self.corners['top_right']
        #  bl = self.corners['bottom_left']
        #  br = self.corners['bottom_right']
        #  return tl.add(tr.sub(tl).mul(map.x)).add(bl.sub(tl).mul(map.y))
        return self.corners_mu.mul_vec(map.sub(self.corners_u)).add(self.corners_v)
    
    def save(self):
        dicts = []
        dicts_nests = []
        total_geese = 0
        types = {}
        for image_object in self.image_objects_list:
            dicts += [goose.get_data(image_object) for goose in image_object.get_geese()]
        
        for goose in dicts:
            type = goose['type']
            if type == 'nest':
                dicts_nests.append(goose)
            
            total_geese += 1
            if type not in types:
                types[type] = 0
                
            types[type] += 1
        
        counts = [
            {
                'name': 'total-geese',
                'value': total_geese,
            },
            {
                'name': 'total-types',
                'value': len(types),
            },
        ]
        
        for type in types:
            counts.append(
                {
                    'name': 'count-' + type,
                    'value': types[type],
                }
            )
        
        write_file(GEESE_RAW_FILENAME, dicts_to_csv(dicts))
        write_file(NESTS_RAW_FILENAME, dicts_to_csv(dicts_nests))
        write_file(COUNTS_FILENAME, dicts_to_csv(counts))

if __name__ == '__main__':
    backend = Backend()
    backend.load()
    # image_object = backend.get_image_object_by_id(1)
    # image_object.add_goose(0.5, 0.5, 'bad goose')
    u1 = backend.gps_to_map(Vector(48.507887717796294,-71.63648124734259))
    u2 = backend.gps_to_map(Vector(48.508937414837504,-71.6501081183125))
    u3 = backend.gps_to_map(Vector(48.51413814770878,-71.64029885586213))
    v1 = Vector(48.50789, -71.63646)
    v2 = Vector(48.50901, -71.65012)
    v3 = Vector(48.5143, -71.6402)
    
    a1 = u2.sub(u1)
    a2 = u3.sub(u1)
    b1 = v2.sub(v1)
    b2 = v3.sub(v1)
    
    c1 = solve_matrix_2d(Matrix(a1, a2), Vector(1, 0))
    c2 = solve_matrix_2d(Matrix(a1, a2), Vector(0, 1))
    i1 = b1.mul(c1.x).add(b2.mul(c2.x))
    i2 = b1.mul(c1.y).add(b2.mul(c2.y))
    
    def transform(u):
        u = u.sub(u1)
        return Vector(i1.x * u.x + i2.x * u.y, i1.y * u.x + i2.y * u.x).add(v1)
    
    #  print(transform(Vector(0, 0)))
    #  print(transform(Vector(1, 0)))
    #  print(transform(Vector(0, 1)))
    #  print(transform(Vector(1, 1)))

    backend.save()
