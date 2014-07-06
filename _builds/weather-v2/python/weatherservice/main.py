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
    

class Report(object):
	"""
	A container for the weather, forecasts, and location information.
	"""
	def __init__(self, weather, location, forecasts):
		"""
		Creates a new Report.
        
        :param self: This object
        :type self: Report
        :param weather: The current weather for this location.
        :type weather: Weather
        :param location: More detailed information on this location.
        :type location: Location
        :param forecasts: The forecast for the next 7 days and 7 nights.
        :type forecasts: list of Forecast
        :returns: Report
		"""
        self.weather = weather
        self.location = location
        self.forecasts = forecasts
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Report from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Report
		"""
		return Report(Weather._from_json(json_data['currentobservation']),
                       Location._from_json(json_data['location']),
                       map(Forecast._from_json, json_data))

class Weather(object):
	"""
	A structured representation the current weather.
	"""
	def __init__(self, wind_speed, windchill, dewpoint, image_url, wind_direction, visibility, humidity, pressure, temp, description):
		"""
		Creates a new Weather.
        
        :param self: This object
        :type self: Weather
        :param wind_speed: The current wind speed (in miles-per-hour).
        :type wind_speed: int
        :param windchill: The perceived temperature (in Fahrenheit).
        :type windchill: int
        :param dewpoint: The current dewpoint temperature (in Fahrenheit).
        :type dewpoint: int
        :param image_url: A url pointing to a picture that describes the weather.
        :type image_url: str
        :param wind_direction: The current wind direction (in degrees).
        :type wind_direction: int
        :param visibility: How far you can see (in miles).
        :type visibility: float
        :param humidity: The current relative humidity (as a percentage).
        :type humidity: int
        :param pressure: The barometric pressure (in inches).
        :type pressure: float
        :param temp: The current temperature (in Fahrenheit).
        :type temp: int
        :param description: A human-readable description of the current weather.
        :type description: str
        :returns: Weather
		"""
        self.wind_speed = wind_speed
        self.windchill = windchill
        self.dewpoint = dewpoint
        self.image_url = image_url
        self.wind_direction = wind_direction
        self.visibility = visibility
        self.humidity = humidity
        self.pressure = pressure
        self.temp = temp
        self.description = description
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Weather from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Weather
		"""
		return Weather(json_data['Winds'],
                       json_data['WindChill'],
                       json_data['Dewp'],
                       json_data['Weatherimage'],
                       json_data['Windd'],
                       json_data['Visibility'],
                       json_data['Relh'],
                       json_data['SLP'],
                       json_data['Temp'],
                       json_data['Weather'])

class Location(object):
	"""
	A detailed description of a location
	"""
	def __init__(self, latitude, elavation, name, longitude):
		"""
		Creates a new Location.
        
        :param self: This object
        :type self: Location
        :param latitude: The latitude (up-down) of this location.
        :type latitude: float
        :param elavation: The height above sea-level (in feet).
        :type elavation: int
        :param name: The city and state that this location is in.
        :type name: str
        :param longitude: The longitude (left-right) of this location.
        :type longitude: float
        :returns: Location
		"""
        self.latitude = latitude
        self.elavation = elavation
        self.name = name
        self.longitude = longitude
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Location from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Location
		"""
		return Location(json_data['latitude'],
                       json_data['elevation'],
                       json_data['areaDescription'],
                       json_data['longitude'])

class Forecast(object):
	"""
	A prediction for future weather.
	"""
	def __init__(self, long_description, description, image_url, temperature_label, period_name, probability_of_precipitation, period_time, temperature):
		"""
		Creates a new Forecast.
        
        :param self: This object
        :type self: Forecast
        :param long_description: A more-detailed, human-readable description of the predicted weather for this period.
        :type long_description: str
        :param description: A human-readable description of the predicted weather for this period.
        :type description: str
        :param image_url: A url pointing to a picture that describes the predicted weather for this period.
        :type image_url: str
        :param temperature_label: Either 'High' or 'Low', depending on whether or not the predicted temperature is a daily high or a daily low.
        :type temperature_label: str
        :param period_name: A human-readable name for this time period (e.g. Tonight or Saturday).
        :type period_name: str
        :param probability_of_precipitation: The probability of precipitation for this period (as a percentage).
        :type probability_of_precipitation: int
        :param period_time: A string representing the time that this period starts. Encoded as YYYY-MM-DDTHH:MM:SS, where the T is not a number, but a always present character (e.g. 2013-07-30T18:00:00).
        :type period_time: str
        :param temperature: The predicted temperature for this period (in Fahrenheit).
        :type temperature: int
        :returns: Forecast
		"""
        self.long_description = long_description
        self.description = description
        self.image_url = image_url
        self.temperature_label = temperature_label
        self.period_name = period_name
        self.probability_of_precipitation = probability_of_precipitation
        self.period_time = period_time
        self.temperature = temperature
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Forecast from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Forecast
		"""
		return Forecast(json_data['data']['text'],
                       json_data['data']['weather'],
                       json_data['data']['iconLink'],
                       json_data['time']['tempLabel'],
                       json_data['time']['startPeriodName'],
                       json_data['data']['pop'],
                       json_data['time']['startValidTime'],
                       json_data['data']['temperature'])

    

def _get_report_request(latitude,longitude):
    """
    Used to build the request string used by :func:`get_report`.
    
    
    :param latitude: The latitude (up-down) of the location to get information about.
    :type latitude: float
    
    :param longitude: The longitude (left-right) of the location to get information about.
    :type longitude: float
    :returns: str
    """
    key = "http://forecast.weather.gov/MapClick.php".format()
    key += "?" + "".join(["lat=", latitude , "&", "FcstType=", fcsttype , "&", "lon=", longitude ])
    return key

def _get_report_string(latitude,longitude):
    """
    Like :func:`get_report` except returns the raw data instead.
    
    
    :param latitude: The latitude (up-down) of the location to get information about.
    :type latitude: float
    
    :param longitude: The longitude (left-right) of the location to get information about.
    :type longitude: float
    :returns: str
    """
    if _CONNECTED:
        key = "http://forecast.weather.gov/MapClick.php".format()
        result = requests.get(key, params = { "lat" : latitude,"FcstType" : fcsttype,"lon" : longitude) }).text
    else:
        key = _get_report_request(latitude,longitude)
        result = lookup(key)
    return result

def get_report(latitude,longitude):
    """
    Gets a report on the current weather, forecast, and more detailed information about the location.
    
    
    :param latitude: The latitude (up-down) of the location to get information about.
    :type latitude: float
    
    :param longitude: The longitude (left-right) of the location to get information about.
    :type longitude: float
    :returns: Report
    """
    result = _get_report_string(latitude,longitude)
    
    return Report._from_json(_from_json(result))
    
