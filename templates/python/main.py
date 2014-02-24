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
    
{% for object in objects %}
class {{ object.name | camel_case_caps }}(object):
	"""
	{{ object.description }}
	"""
	def __init__(self{% for field in object.fields %}, {{ field.name | snake_case }}{% endfor %}):
		"""
		Creates a new {{ object.name | camel_case_caps }}.
        
        :param self: This object
        :type self: {{ object.name | camel_case_caps }}
        {% for field in object.fields -%}
        :param {{ field.name | snake_case }}: {{ field.description }}
        :type {{ field.name | snake_case }}: {{ field.type | to_python_type}}
        {% endfor -%}
        :returns: {{ object.name | camel_case_caps }}
		"""
        {% for field in object.fields -%}
        self.{{ field.name | snake_case }} = {{ field.name | snake_case }}
        {% endfor %}
	
	@staticmethod
	def _from_json(json_data):
		"""
		Creates a {{ object.name | camel_case_caps }} from json data.
        
        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: {{ object.name | camel_case_caps }}
		"""
		return {{ object.name | camel_case_caps }}({% for field in object.fields %}{% if field.type | is_builtin %}{{ field.path | parse_json_path}}{% elif field.type | is_list %}map({{ field.type | strip_list | camel_case_caps }}._from_json, {{ field.path | parse_json_path}}){% else %}{{ field.type | camel_case_caps }}._from_json({{ field.path | parse_json_path}}){% endif %}{% if not loop.last %},
                       {% endif %}{% endfor %})
{% endfor %}
    
{% for function in functions %}
def _{{ function.name | snake_case }}_request({% for input in function.visible_inputs %}{{input.name| snake_case }}{% if not loop.last %},{% endif %}{% endfor %}):
    """
    Used to build the request string used by :func:`{{ function.name | snake_case }}`.
    
    {% for input in function.visible_inputs %}
    :param {{input.name | snake_case }}: {{ input.description }}
    :type {{input.name | snake_case }}: {{ input.type | to_python_type }}
    {% endfor -%}
    :returns: str
    """
    key = "{{ function.url | convert_url_parameters }}".format({% for input in function.url_inputs %}{{ input.name | snake_case}}{% if not loop.last %},{% endif%}{% endfor %})
    key += "?" + "".join([{% for input in function.payload_inputs if input.indexed %}"{{ input.path }}=", {{ input.name | snake_case }} {% if not loop.last %}, "&", {% endif %}{%endfor%}])
    return key

def _{{ function.name | snake_case }}_string({% for input in function.visible_inputs %}{{input.name| snake_case }}{% if not loop.last %},{% endif %}{% endfor %}):
    """
    Like :func:`{{ function.name | snake_case }}` except returns the raw data instead.
    
    {% for input in function.visible_inputs %}
    :param {{input.name | snake_case }}: {{ input.description }}
    :type {{input.name | snake_case }}: {{ input.type | to_python_type }}
    {% endfor -%}
    :returns: str
    """
    if _CONNECTED:
        key = "{{ function.url | convert_url_parameters }}".format({% for input in function.url_inputs %}{{ input.name | snake_case}}{% if not loop.last %},{% endif%}{% endfor %})
        result = requests.{{ function.verb }}(key, {{ function.verb | requests_verb }} = { {% for input in function.payload_inputs %}"{{ input.path }}" : {{ input.name | snake_case}}{% if not loop.last %},{% endif%}{% endfor %}) }).text
    else:
        key = _{{ function.name | snake_case }}_request({% for input in function.visible_inputs %}{{input.name| snake_case }}{% if not loop.last %},{% endif %}{% endfor %})
        result = lookup(key)
    return result

def {{ function.name | snake_case }}({% for input in function.visible_inputs %}{{input.name| snake_case }}{% if not loop.last %},{% endif %}{% endfor %}):
    """
    {{ function.description }}
    
    {% for input in function.visible_inputs %}
    :param {{input.name | snake_case }}: {{ input.description }}
    :type {{input.name | snake_case }}: {{ input.type | to_python_type }}
    {% endfor -%}
    :returns: {{ function.output | to_python_type }}
    """
    result = _{{ function.name | snake_case }}_string({% for input in function.visible_inputs %}{{input.name| snake_case }}{% if not loop.last %},{% endif %}{% endfor %})
    {% if function.output | is_builtin %}
    return _from_json(result){{ function.post | parse_json_path("") }}
    {% elif function.output | is_list %}
    return map({{ function.output | to_python_type }}._from_json, _from_json(result){{ function.post | parse_json_path("")}})
    {% else %}
    return {{ function.output | to_python_type }}._from_json(_from_json(result){{ function.post | parse_json_path("") }})
    {% endif %}
{% endfor %}