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
    

class Stock(object):
	"""
	A structured representation of stock information, including ticker symbol, latest sale price, and price change since yesterday.
	"""
	def __init__(self, last_trade_date, last_trade_time, exchange, percent_price_change, last_sale_price, id, ticker, price_change):
		"""
		Creates a new Stock.
        
        :param self: This object
        :type self: Stock
        :param last_trade_date: The entire date of the last trade.
        :type last_trade_date: str
        :param last_trade_time: The time of the last trade.
        :type last_trade_time: str
        :param exchange: The name of the exchange (e.g. NASDAQ)
        :type exchange: str
        :param percent_price_change: The percent price change since yesterday.
        :type percent_price_change: float
        :param last_sale_price: The latest sale price for this stock.
        :type last_sale_price: float
        :param id: The unique ID number for this ticker symbol
        :type id: int
        :param ticker: The Ticker Symbol (e.g. AAPL)
        :type ticker: str
        :param price_change: The price change since yesterday.
        :type price_change: float
        :returns: Stock
		"""
        self.last_trade_date = last_trade_date
        self.last_trade_time = last_trade_time
        self.exchange = exchange
        self.percent_price_change = percent_price_change
        self.last_sale_price = last_sale_price
        self.id = id
        self.ticker = ticker
        self.price_change = price_change
        
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a Stock from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Stock
		"""
		return Stock(json_data['lt'],
                       json_data['ltt'],
                       json_data['e'],
                       json_data['cp'],
                       json_data['l'],
                       json_data['id'],
                       json_data['t'],
                       json_data['c'])

    

def _get_stock_information_request(ticker):
    """
    Used to build the request string used by :func:`get_stock_information`.
    
    
    :param ticker: A comma separated list of ticker symbols (e.g. "AAPL, MSFT, CSCO").
    :type ticker: str
    :returns: str
    """
    key = "http://www.google.com/finance/info".format()
    key += "?" + "".join(["client=", client , "&", "q=", ticker ])
    return key

def _get_stock_information_string(ticker):
    """
    Like :func:`get_stock_information` except returns the raw data instead.
    
    
    :param ticker: A comma separated list of ticker symbols (e.g. "AAPL, MSFT, CSCO").
    :type ticker: str
    :returns: str
    """
    if _CONNECTED:
        key = "http://www.google.com/finance/info".format()
        result = requests.get(key, params = { "client" : client,"q" : ticker) }).text
    else:
        key = _get_stock_information_request(ticker)
        result = lookup(key)
    return result

def get_stock_information(ticker):
    """
    Retrieves current stock information.
    
    
    :param ticker: A comma separated list of ticker symbols (e.g. "AAPL, MSFT, CSCO").
    :type ticker: str
    :returns: list of Stock
    """
    result = _get_stock_information_string(ticker)
    
    return map(list of Stock._from_json, _from_json(result))
    
