import requests
import json

def _recursively_convert_unicode_to_str(input):
    if isinstance(input, dict):
        return {_recursively_convert_unicode_to_str(key): _recursively_convert_unicode_to_str(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [_recursively_convert_unicode_to_str(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def _from_json(data):
    return _recursively_convert_unicode_to_str(json.loads(data))
        
_CACHE = {}
_CACHE_COUNTER = {}
_CONNECTED = False
def connect():
    """
    Connect to the online data source in order to get up-to-date information.
    :returns: void
    """
    _CONNECTED = True
def disconnect(filename="cache.json"):
    """
    Connect to the local cache, so no internet connection is required.
    :returns: void
    """
    _CACHE = _recursively_convert_unicode_to_str(json.load(open(filename, r)))
    for key in CACHE.keys():
        _CACHE_COUNTER[key] = 0
        _CACHE_PATTERN[key] = _CACHE[key][0]
        _CACHE_DATA[key] = _CACHE[key][1:]
    _CONNECTED = False
def lookup(key):
    """
    Internal method that looks up a key in the local cache.
    :param key: Get the value based on the key from the cache.
    :type key: string
    :returns: void
    """
    if _CACHE_COUNTER[key] >= len(_CACHE[key][1:]):
        if _CACHE[key][0] == "empty":
            return ""
        elif _CACHE[key][0] == "repeat" and _CACHE[key][1:]:
            return _CACHE[key][-1]
        elif _CACHE[key][0] == "repeat":
            return ""
        else:
            _CACHE_COUNTER[key] = 0
    else:
        _CACHE_COUNTER[key] += 1
    if _CACHE[key]:
        return _CACHE[key][1+_CACHE_COUNTER]
    else:
        return ""
    
def _save_cache(filename="cache.json"):
    json.dump(_CACHE, filename)
    

class Coordinate(object):
	"""
	The longitudinal, latitudinal, and depth where the earthquake occurred.
	"""
	def __init__(self, longitude, latitude, depth):
		"""
		Creates a new Coordinate.
        
        :param self: This object
        :type self: Coordinate
        :param longitude: The longitude (West-North) component.
        :type longitude: float
        :param latitude: The latitude (South-North) component.
        :type latitude: float
        :param depth: The depth (closer or farther from the surface) component.
        :type depth: float
        :returns: Coordinate
		"""
        self.longitude = longitude
        self.latitude = latitude
        self.depth = depth
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Coordinate from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Coordinate
		"""
		return Coordinate(json_data[0],
                       json_data[1],
                       json_data[2])

class Earthquake(object):
	"""
	Information about a specific earthquake.
	"""
	def __init__(self, location, magnitude, location_description, id, time):
		"""
		Creates a new Earthquake.
        
        :param self: This object
        :type self: Earthquake
        :param location: The location of the earthquake.
        :type location: Coordinate
        :param magnitude: The magnitude of the earthquake on the Richter Scale.
        :type magnitude: float
        :param location_description: A human-readable description of the location.
        :type location_description: str
        :param id: A uniquely identifying id for this earthquake.
        :type id: str
        :param time: The epoch time (http://en.wikipedia.org/wiki/Unix_time) when this earthquake occurred.
        :type time: int
        :returns: Earthquake
		"""
        self.location = location
        self.magnitude = magnitude
        self.location_description = location_description
        self.id = id
        self.time = time
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Earthquake from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Earthquake
		"""
		return Earthquake(Coordinate._from_json(json_data['geometry']['coordinates']),
                       json_data['properties']['mag'],
                       json_data['properties']['place'],
                       json_data['id'],
                       json_data['properties']['time'])

    

def _get_earthquakes_request(threshold,time):
    """
    Used to build the request string used by :func:`get_earthquakes`.
    
    
    :param threshold: A string indicating what kind of earthquakes to report. Must be either "significant" (only significant earthquakes), "all" (all earthquakes, regardless of significance), "4.5", "2.5", or "1.0". Note that for the last three, all earthquakes at and above that level will be reported.
    :type threshold: str
    
    :param time: A string indicating the time range of earthquakes to report. Must be either "hour" (only earthquakes in the past hour), "day" (only earthquakes that happened today), "week" (only earthquakes that happened in the past 7 days), or "month" (only earthquakes that happened in the past 30 days).
    :type time: str
    :returns: str
    """
    key = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{}_{}.geojson".format(threshold,time)
    key += "?" + "".join([])
    return key

def _get_earthquakes_string(threshold,time):
    """
    Like :func:`get_earthquakes` except returns the raw data instead.
    
    
    :param threshold: A string indicating what kind of earthquakes to report. Must be either "significant" (only significant earthquakes), "all" (all earthquakes, regardless of significance), "4.5", "2.5", or "1.0". Note that for the last three, all earthquakes at and above that level will be reported.
    :type threshold: str
    
    :param time: A string indicating the time range of earthquakes to report. Must be either "hour" (only earthquakes in the past hour), "day" (only earthquakes that happened today), "week" (only earthquakes that happened in the past 7 days), or "month" (only earthquakes that happened in the past 30 days).
    :type time: str
    :returns: str
    """
    if _CONNECTED:
        key = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{}_{}.geojson".format(threshold,time)
        result = requests.get(key, params = { ) }).text
    else:
        key = _get_earthquakes_request(threshold,time)
        result = lookup(key)
    return result

def get_earthquakes(threshold,time):
    """
    Retrieves information about earthquakes around the world.
    
    
    :param threshold: A string indicating what kind of earthquakes to report. Must be either "significant" (only significant earthquakes), "all" (all earthquakes, regardless of significance), "4.5", "2.5", or "1.0". Note that for the last three, all earthquakes at and above that level will be reported.
    :type threshold: str
    
    :param time: A string indicating the time range of earthquakes to report. Must be either "hour" (only earthquakes in the past hour), "day" (only earthquakes that happened today), "week" (only earthquakes that happened in the past 7 days), or "month" (only earthquakes that happened in the past 30 days).
    :type time: str
    :returns: list of Earthquake
    """
    result = _get_earthquakes_string(threshold,time)
    
    return map(list of Earthquake._from_json, _from_json(result)['features'])
    
