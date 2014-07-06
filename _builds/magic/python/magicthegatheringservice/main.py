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
    

class Print(object):
	"""
	The print expansion this belongs to.
	"""
	def __init__(self, set, id):
		"""
		Creates a new Print.
        
        :param self: This object
        :type self: Print
        :param set: The ID code of this set.
        :type set: str
        :param id: The unique id number of this set.
        :type id: int
        :returns: Print
		"""
        self.set = set
        self.id = id
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Print from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Print
		"""
		return Print(json_data['set'],
                       json_data['id'])

class CardResult(object):
	"""
	The result of a card search, only having the ID and card name. You can look up the card by its ID for more complete information.
	"""
	def __init__(self, id, name):
		"""
		Creates a new CardResult.
        
        :param self: This object
        :type self: CardResult
        :param id: The unique id number of this card
        :type id: int
        :param name: The name of this card.
        :type name: str
        :returns: CardResult
		"""
        self.id = id
        self.name = name
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a CardResult from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: CardResult
		"""
		return CardResult(json_data['id'],
                       json_data['name'])

class Card(object):
	"""
	A Magic the Gathering Card
	"""
	def __init__(self, flavors, rating, votes, set, all_sets, name, power, watermark, artist, number, rarity, texts, converted_mana_cost, mana_cost, id, types, toughness):
		"""
		Creates a new Card.
        
        :param self: This object
        :type self: Card
        :param flavors: Any flavor texts on this card.
        :type flavors: list of str
        :param rating: The card's voted upon rating.
        :type rating: str
        :param votes: The number of times this card has been voted on.
        :type votes: str
        :param set: The expansion set that this card belongs to.
        :type set: str
        :param all_sets: All the expansion sets that this belongs to.
        :type all_sets: list of Print
        :param name: The name of this card.
        :type name: str
        :param power: The power (http://mtg.wikia.com/wiki/Power) of this card
        :type power: str
        :param watermark: The watermark of this card
        :type watermark: str
        :param artist: The name of the artist for the card's artwork.
        :type artist: str
        :param number: The Card Number.
        :type number: str
        :param rarity: How rare this card is, typically either "uncommon", "common", or "rare".
        :type rarity: str
        :param texts: Any text blocks on the card.
        :type texts: list of str
        :param converted_mana_cost: The converted mana cost.
        :type converted_mana_cost: str
        :param mana_cost: The Mana cost of this card.
        :type mana_cost: list of str
        :param id: A unique id that identifies this card.
        :type id: str
        :param types: Card's types, usually at least one of "artifact", "creature", "enchantment", "instant", "land", "planeswalker", "sorcery", or "tribal". Cards can also have a supertype and/or subtype. 
        :type types: list of str
        :param toughness: The toughness (http://mtg.wikia.com/wiki/Toughness) of this card
        :type toughness: str
        :returns: Card
		"""
        self.flavors = flavors
        self.rating = rating
        self.votes = votes
        self.set = set
        self.all_sets = all_sets
        self.name = name
        self.power = power
        self.watermark = watermark
        self.artist = artist
        self.number = number
        self.rarity = rarity
        self.texts = texts
        self.converted_mana_cost = converted_mana_cost
        self.mana_cost = mana_cost
        self.id = id
        self.types = types
        self.toughness = toughness
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Card from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Card
		"""
		return Card(map(String._from_json, json_data['flavor']),
                       json_data['rating'],
                       json_data['votes'],
                       json_data['set'],
                       map(Print._from_json, json_data['prints']),
                       json_data['name'],
                       json_data['power'],
                       json_data['watermark'],
                       json_data['artist'],
                       json_data['number'],
                       json_data['rarity'],
                       map(String._from_json, json_data['text']),
                       json_data['cmc'],
                       map(String._from_json, json_data['mana']),
                       json_data['id'],
                       map(String._from_json, json_data['type']),
                       json_data['power'])

    

def _search_cards_request(keyword):
    """
    Used to build the request string used by :func:`search_cards`.
    
    
    :param keyword: The keyword to match against card's names
    :type keyword: str
    :returns: str
    """
    key = "http://api.mtgapi.com/v1/card/name/{}".format(keyword)
    key += "?" + "".join([])
    return key

def _search_cards_string(keyword):
    """
    Like :func:`search_cards` except returns the raw data instead.
    
    
    :param keyword: The keyword to match against card's names
    :type keyword: str
    :returns: str
    """
    if _CONNECTED:
        key = "http://api.mtgapi.com/v1/card/name/{}".format(keyword)
        result = requests.get(key, params = { ) }).text
    else:
        key = _search_cards_request(keyword)
        result = lookup(key)
    return result

def search_cards(keyword):
    """
    Searches the database for cards with the keyword in the card's name.
    
    
    :param keyword: The keyword to match against card's names
    :type keyword: str
    :returns: list of CardResult
    """
    result = _search_cards_string(keyword)
    
    return map(list of CardResult._from_json, _from_json(result))
    

def _get_card_request(id):
    """
    Used to build the request string used by :func:`get_card`.
    
    
    :param id: The unique id number of the card.
    :type id: int
    :returns: str
    """
    key = "http://api.mtgapi.com/v1/card/id/{}".format(id)
    key += "?" + "".join([])
    return key

def _get_card_string(id):
    """
    Like :func:`get_card` except returns the raw data instead.
    
    
    :param id: The unique id number of the card.
    :type id: int
    :returns: str
    """
    if _CONNECTED:
        key = "http://api.mtgapi.com/v1/card/id/{}".format(id)
        result = requests.get(key, params = { ) }).text
    else:
        key = _get_card_request(id)
        result = lookup(key)
    return result

def get_card(id):
    """
    Retrieves a card by looking up its ID.
    
    
    :param id: The unique id number of the card.
    :type id: int
    :returns: Card
    """
    result = _get_card_string(id)
    
    return Card._from_json(_from_json(result)[0])
    
