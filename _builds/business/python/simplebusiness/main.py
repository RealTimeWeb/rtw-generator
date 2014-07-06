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
    

class Business(object):
	"""
	Information about a specific earthquake.
	"""
	def __init__(self, rating, description, phone, location, id, name):
		"""
		Creates a new Business.
        
        :param self: This object
        :type self: Business
        :param rating: Rating for this business (value ranges from 1, 1.5, ... 4.5, 5)
        :type rating: float
        :param description: Snippet text associated with this business
        :type description: str
        :param phone: Phone number for this business formatted for display
        :type phone: str
        :param location: Address for this business formatted for display. Includes all address fields, cross streets and city, state_code, etc.
        :type location: str
        :param id: A uniquely identifying id for this business.
        :type id: str
        :param name: Name of this business.
        :type name: str
        :returns: Business
		"""
        self.rating = rating
        self.description = description
        self.phone = phone
        self.location = location
        self.id = id
        self.name = name
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Business from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Business
		"""
		return Business(json_data['rating'],
                       json_data['snippet_text'],
                       json_data['display_phone'],
                       json_data['location']['display_address'],
                       json_data['id'],
                       json_data['name'])

    

def _search_request(term,location):
    """
    Used to build the request string used by :func:`search`.
    
    
    :param term: Search term (e.g. "food", "restaurants").
    :type term: str
    
    :param location: Specifies the combination of "address, neighborhood, city, state or zip, optional country" to be used when searching for businesses.
    :type location: str
    :returns: str
    """
    key = "http://api.yelp.com/v2/search".format()
    key += "?" + "".join(["term=", term , "&", "location=", location ])
    return key

def _search_string(term,location):
    """
    Like :func:`search` except returns the raw data instead.
    
    
    :param term: Search term (e.g. "food", "restaurants").
    :type term: str
    
    :param location: Specifies the combination of "address, neighborhood, city, state or zip, optional country" to be used when searching for businesses.
    :type location: str
    :returns: str
    """
    if _CONNECTED:
        key = "http://api.yelp.com/v2/search".format()
        result = requests.get(key, params = { "term" : term,"location" : location) }).text
    else:
        key = _search_request(term,location)
        result = lookup(key)
    return result

def search(term,location):
    """
    Retrieves information about the businesses that include the given term for the given area
    
    
    :param term: Search term (e.g. "food", "restaurants").
    :type term: str
    
    :param location: Specifies the combination of "address, neighborhood, city, state or zip, optional country" to be used when searching for businesses.
    :type location: str
    :returns: list of Business
    """
    result = _search_string(term,location)
    
    return map(list of Business._from_json, _from_json(result)['businesses'])
    
