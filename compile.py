from validate import validate_spec
from auxiliary import clean_json
import re
import sys
from itertools import chain
                       
def flatten_list(a_type):
    if a_type.endswith("[]"):
        return flatten_list(a_type[:-2])
    else:
        return a_type
        
class Metadata(object): pass
class Enum(object): pass
class Package(object): pass
class Object(object): pass
class Field(object): pass
class Function(object): pass
class Input(object): pass

def compile_metadata(data):
    metadata = Metadata()
    metadata.name = data["name"]
    metadata.author = data.get("author", "Anonymous")
    metadata.contact = data.get("contact", "")
    metadata.version = data.get("version", 1.0)
    metadata.description = data.get("description", "")
    metadata.comment = data.get("comment", "")
    return metadata
    
def compile_enum(name, data):
    enum = Enum()
    enum.name = name
    enum.values = data
    return enum
    
def compile_field(name, data):
    field = Field()
    field.name = name
    field.type = data["type"]
    field.path = data["path"]
    field.description = data.get("description", "")
    field.comment = data.get("comment", "")
    return field
    
def compile_object(name, data):
    obj = Object()
    obj.name = name
    obj.description = data.get("description", "")
    obj.comment = data.get("comment", "")
    obj.format = data.get("format", "text")
    obj.fields = [compile_field(*data) for data in data["fields"].iteritems()]
    obj.dependencies = set([flatten_list(field.type)
                                for field in obj.fields 
                                    if flatten_list(obj.name) != flatten_list(field.type)])
    return obj
    
def compile_input(name, data):
    input = Input()
    input.name = name
    input.type = data["type"]
    input.path = data["path"]
    input.description = data.get("description", "")
    input.comment = data.get("comment", "")
    input.indexed = data.get("indexed", True)
    input.hidden = data.get("hidden", False)
    input.default = data.get("default", None)
    return input
    
def compile_function(name, data):
    function = Function()
    function.name = name
    function.url = data["url"]
    url_input_names = map(str, re.findall("<(.*?)>", function.url))
    function.verb = data["verb"]
    function.format = data["format"]
    function.output = data["output"]
    function.description = data.get("description", "")
    function.comment = data.get("comment", "")
    function.post = data.get("post", "")
    function.authentication = data.get("authentication", None)
    if "inputs" in data:
        inputs = [compile_input(*data) for data in data["inputs"].iteritems()]
    else:
        inputs = []
    # Ensure the url arguments are in the proper order - None indicates missing argument!
    function.url_inputs = [next((i for i in inputs if i.path == input), None) for input in url_input_names]
    function.payload_inputs = [input for input in inputs if input.path not in url_input_names]
    function.dependencies = set([flatten_list(input.type) for input in inputs] + [flatten_list(function.output)])
    return function

def compile_spec(spec):
    package = Package()
    package.metadata = compile_metadata(spec["metadata"])
    package.enums = [compile_enum(*data) for data in spec["enums"].iteritems()]
    package.objects = [compile_object(*data) for data in spec["objects"].iteritems()]
    package.functions = [compile_function(*data) for data in spec["functions"].iteritems()]
    package.formats_required = set(function.format for function in package.functions)
    #package.dependencies = chain(*[function.dependencies for function in package.functions],
    #                             *[obj.dependencies for obj in package.objects])
    return package
    
if __name__ == "__main__":
    import json
    input = clean_json(json.load(open(sys.argv[1],'r')))
    new_package = compile_spec(input)

