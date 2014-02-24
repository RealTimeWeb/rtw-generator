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
    

class MyAuthors(object):
	"""
	A list of authors.
	"""
	def __init__(self, test, books, other, years):
		"""
		Creates a new MyAuthors.
        
        :param self: This object
        :type self: MyAuthors
        :param test: amazing
        :type test: str
        :param books: All the authors.
        :type books: list of str
        :param other: amazing
        :type other: Earthquake
        :param years: All the years.
        :type years: list of int
        :returns: MyAuthors
		"""
        self.test = test
        self.books = books
        self.other = other
        self.years = years
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a MyAuthors from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: MyAuthors
		"""
		return MyAuthors(json_data['/bookstore/'],
                       map(String._from_json, json_data['/bookstore/book/author']),
                       Earthquake._from_json(json_data['/bookstore/']),
                       map(Integer._from_json, json_data['/bookstore/book/year']))

class Report(object):
	"""
	Information about earthquakes matching certain criteria, including the area that they occurred.
	"""
	def __init__(self, area, earthquakes, title):
		"""
		Creates a new Report.
        
        :param self: This object
        :type self: Report
        :param area: A region that contains all the earthquakes.
        :type area: BoundingBox
        :param earthquakes: A list of the earthquakes.
        :type earthquakes: list of Earthquake
        :param title: A human-readable title that describes this data.
        :type title: str
        :returns: Report
		"""
        self.area = area
        self.earthquakes = earthquakes
        self.title = title
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Report from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Report
		"""
		return Report(BoundingBox._from_json(json_data['bbox']),
                       map(Earthquake._from_json, json_data['features']),
                       json_data['metadata']['title'])

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
	def __init__(self, maximum_estimated_intensity, distance, alert_level, felt_reports, location_description, url, time, root_mean_square, event_source, gap, magnitude, location, significance, maximum_reported_intensity, id):
		"""
		Creates a new Earthquake.
        
        :param self: This object
        :type self: Earthquake
        :param maximum_estimated_intensity: The maximum estimated instrumental intensity for the event, or null if the data is not available. While typically reported as a roman numeral, intensity is reported here as the decimal equivalent. More information can be found at http://earthquake.usgs.gov/learn/topics/mag_vs_int.php
        :type maximum_estimated_intensity: float
        :param distance: Horizontal distance from the epicenter to the nearest station (in degrees), or null if the data is not available. 1 degree is approximately 111.2 kilometers. In general, the smaller this number, the more reliable is the calculated depth of the earthquake.
        :type distance: float
        :param alert_level: A color string (one of "green", "yellow", "orange", "red") indicating how dangerous the quake was, or null if the data is not available. More information about this kind of alert is available at http://earthquake.usgs.gov/research/pager/
        :type alert_level: str
        :param felt_reports: The total number of "Felt" reports submitted, or null if the data is not available.
        :type felt_reports: int
        :param location_description: A human-readable description of the location.
        :type location_description: str
        :param url: A webpage with more information about the earthquake.
        :type url: str
        :param time: The epoch time (http://en.wikipedia.org/wiki/Unix_time) when this earthquake occurred.
        :type time: int
        :param root_mean_square: The root-mean-square (RMS) travel time residual, in sec, using all weights. This parameter provides a measure of the fit of the observed arrival times to the predicted arrival times for this location. Smaller numbers reflect a better fit of the data. The value is dependent on the accuracy of the velocity model used to compute the earthquake location, the quality weights assigned to the arrival time data, and the procedure used to locate the earthquake.
        :type root_mean_square: float
        :param event_source: Either "AUTOMATIC", "PUBLISHED", or "REVIEWED". Indicates how the earthquake was identified and whether it was reviewed by a human.
        :type event_source: str
        :param gap: The largest azimuthal gap between azimuthally adjacent stations (in degrees), or null if the data is not available. In general, the smaller this number, the more reliable is the calculated horizontal position of the earthquake.
        :type gap: float
        :param magnitude: The magnitude of the earthquake on the Richter Scale.
        :type magnitude: float
        :param location: The location of the earthquake.
        :type location: Coordinate
        :param significance: A number describing how significant the event is. Larger numbers indicate a more significant event. This value is determined on a number of factors, including: magnitude, maximum estimated intensity, felt reports, and estimated impact.
        :type significance: int
        :param maximum_reported_intensity: The maximum reported intensity for this earthquake, or null if the data is not available. While typically reported as a roman numeral, intensity is reported here as a decimal number. More information can be found at http://earthquake.usgs.gov/learn/topics/mag_vs_int.php
        :type maximum_reported_intensity: float
        :param id: A uniquely identifying id for this earthquake.
        :type id: str
        :returns: Earthquake
		"""
        self.maximum_estimated_intensity = maximum_estimated_intensity
        self.distance = distance
        self.alert_level = alert_level
        self.felt_reports = felt_reports
        self.location_description = location_description
        self.url = url
        self.time = time
        self.root_mean_square = root_mean_square
        self.event_source = event_source
        self.gap = gap
        self.magnitude = magnitude
        self.location = location
        self.significance = significance
        self.maximum_reported_intensity = maximum_reported_intensity
        self.id = id
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Earthquake from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Earthquake
		"""
		return Earthquake(json_data['properties']['mmi'],
                       json_data['properties']['dmin'],
                       json_data['properties']['alert'],
                       json_data['properties']['felt'],
                       json_data['properties']['place'],
                       json_data['properties']['url'],
                       json_data['properties']['time'],
                       json_data['properties']['rms'],
                       json_data['properties']['status'],
                       json_data['properties']['gap'],
                       json_data['properties']['mag'],
                       Coordinate._from_json(json_data['geometry']['coordinates']),
                       json_data['properties']['sig'],
                       json_data['properties']['cdi'],
                       json_data['id'])

class BoundingBox(object):
	"""
	The longitudinal, latitudinal, and depth of the region required to display all the earthquakes.
	"""
	def __init__(self, minimum_longitude, minimum_latitude, minimum_depth, maximum_longitude, maximum_latitude, maximum_depth):
		"""
		Creates a new BoundingBox.
        
        :param self: This object
        :type self: BoundingBox
        :param minimum_longitude: The lower longitude (West) component.
        :type minimum_longitude: float
        :param minimum_latitude: The lower latitude (South) component.
        :type minimum_latitude: float
        :param minimum_depth: The lower depth (closer or farther from the surface) component.
        :type minimum_depth: float
        :param maximum_longitude: The higher longitude (East) component.
        :type maximum_longitude: float
        :param maximum_latitude: The higher latitude (North) component.
        :type maximum_latitude: float
        :param maximum_depth: The higher depth (closer or farther from the surface) component.
        :type maximum_depth: float
        :returns: BoundingBox
		"""
        self.minimum_longitude = minimum_longitude
        self.minimum_latitude = minimum_latitude
        self.minimum_depth = minimum_depth
        self.maximum_longitude = maximum_longitude
        self.maximum_latitude = maximum_latitude
        self.maximum_depth = maximum_depth
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a BoundingBox from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: BoundingBox
		"""
		return BoundingBox(json_data[0],
                       json_data[1],
                       json_data[2],
                       json_data[3],
                       json_data[4],
                       json_data[5])

    

def _get_some_books_request():
    """
    Used to build the request string used by :func:`get_some_books`.
    
    :returns: str
    """
    key = "http://www.w3schools.com/dom/books.xml".format()
    key += "?" + "".join([])
    return key

def _get_some_books_string():
    """
    Like :func:`get_some_books` except returns the raw data instead.
    
    :returns: str
    """
    if _CONNECTED:
        key = "http://www.w3schools.com/dom/books.xml".format()
        result = requests.post(key, data = { ) }).text
    else:
        key = _get_some_books_request()
        result = lookup(key)
    return result

def get_some_books():
    """
    Connects without any parameters
    
    :returns: MyAuthors
    """
    result = _get_some_books_string()
    
    return MyAuthors._from_json(_from_json(result)['/book/'])
    

def _get_earthquakes_request(threshold,time):
    """
    Used to build the request string used by :func:`get_earthquakes`.
    
    
    :param threshold: A string indicating what kind of earthquakes to report. Must be either "significant" (only significant earthquakes), "all" (all earthquakes, regardless of significance), "4.5", "2.5", or "1.0". Note that for the last three, all earthquakes at and above that level will be reported.
    :type threshold: int
    
    :param time: A string indicating the time range of earthquakes to report. Must be either "hour" (only earthquakes in the past hour), "day" (only earthquakes that happened today), "week" (only earthquakes that happened in the past 7 days), or "month" (only earthquakes that happened in the past 30 days).
    :type time: str
    :returns: str
    """
    key = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{}_{}.geojson".format(time,threshold)
    key += "?" + "".join(["my_secret=", secret ])
    return key

def _get_earthquakes_string(threshold,time):
    """
    Like :func:`get_earthquakes` except returns the raw data instead.
    
    
    :param threshold: A string indicating what kind of earthquakes to report. Must be either "significant" (only significant earthquakes), "all" (all earthquakes, regardless of significance), "4.5", "2.5", or "1.0". Note that for the last three, all earthquakes at and above that level will be reported.
    :type threshold: int
    
    :param time: A string indicating the time range of earthquakes to report. Must be either "hour" (only earthquakes in the past hour), "day" (only earthquakes that happened today), "week" (only earthquakes that happened in the past 7 days), or "month" (only earthquakes that happened in the past 30 days).
    :type time: str
    :returns: str
    """
    if _CONNECTED:
        key = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{}_{}.geojson".format(time,threshold)
        result = requests.get(key, params = { "my_secret" : secret) }).text
    else:
        key = _get_earthquakes_request(threshold,time)
        result = lookup(key)
    return result

def get_earthquakes(threshold,time):
    """
    Retrieves information about earthquakes around the world.
    
    
    :param threshold: A string indicating what kind of earthquakes to report. Must be either "significant" (only significant earthquakes), "all" (all earthquakes, regardless of significance), "4.5", "2.5", or "1.0". Note that for the last three, all earthquakes at and above that level will be reported.
    :type threshold: int
    
    :param time: A string indicating the time range of earthquakes to report. Must be either "hour" (only earthquakes in the past hour), "day" (only earthquakes that happened today), "week" (only earthquakes that happened in the past 7 days), or "month" (only earthquakes that happened in the past 30 days).
    :type time: str
    :returns: Report
    """
    result = _get_earthquakes_string(threshold,time)
    
    return Report._from_json(_from_json(result)['book']['test'][3]['children']['data'])
    

def _get_first_year_request():
    """
    Used to build the request string used by :func:`get_first_year`.
    
    :returns: str
    """
    key = "http://www.w3schools.com/dom/books.xml".format()
    key += "?" + "".join([])
    return key

def _get_first_year_string():
    """
    Like :func:`get_first_year` except returns the raw data instead.
    
    :returns: str
    """
    if _CONNECTED:
        key = "http://www.w3schools.com/dom/books.xml".format()
        result = requests.get(key, params = { ) }).text
    else:
        key = _get_first_year_request()
        result = lookup(key)
    return result

def get_first_year():
    """
    Gets the first books
    
    :returns: int
    """
    result = _get_first_year_string()
    
    return _from_json(result)['/bookstore/book'][0]['/year']
    
