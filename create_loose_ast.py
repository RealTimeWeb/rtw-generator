from collections import namedtuple

class Package(object): pass
class Class(object): pass
class Field(object): pass
class Method(object): pass
class Argument(object): pass

def _recursively_convert_unicode_to_str(input):
    if isinstance(input, dict):
        return {_recursively_convert_unicode_to_str(key): _recursively_convert_unicode_to_str(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [_recursively_convert_unicode_to_str(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def kebab_case(string):
    return string.replace(" ", "-").replace("_", "-").lower()
    
def snake_case(string):
    return string.replace(" ", "_").lower()
    
def camel_case_caps(string):
    return ''.join(x for x in string.title() if not x.isspace())
    
def camel_case(string):
    s = camel_case_caps(string)
    return s[0].lower() + s[1:] if s else ""
def flat_case(string):
    return string.replace(" ", "").replace("_", "").lower()

def create_loose_ast(spec):
    p = Package()
    
    # Metadata
    p.core_types = ("float", "integer", "string", "list", "boolean")
    p.name = spec["metadata"]["name"]
    p.description = spec["metadata"]["description"]
    p.classes = []
    p.methods = []
    p.author = spec.get("author", "")
    p.author_email = spec.get("author_email", "")
    
    # Domain objects
    for domain in spec["domain"]:
        c = Class()
        c.name = domain["name"]
        c.description = domain.get("description", "")
        c.comment = domain.get("comment", "")
        c.fields = []
        c.dependencies = set()
        for field in domain["fields"]:
            f = Field()
            f.name = field["name"]
            f.type = field["type"]
            f.description = field.get("description", "")
            f.comment = field.get("comment", "")
            f.in_mask = field["in"]
            c.fields.append(f)
            if f.type.startswith("list("):
                dependency = f.type[5:-1]
            else:
                dependency = f.type
            if dependency not in p.core_types and dependency != c.name:
                c.dependencies.add(dependency)
        p.classes.append(c)
    
    p.method_dependencies = set()
    # Service methods
    for service in spec["services"]:
        m = Method()
        m.name = service["name"]
        m.url = service["url"]
        m.type = service["type"]
        m.description = service.get("description", "")
        m.comment = service.get("comment", "")
        m.dependencies = set()
        m.output = service["output"]
        if m.output.startswith("list("):
            dependency = m.output[5:-1]
        else:
            dependency = m.output
        if dependency not in p.core_types:
            m.dependencies.add(dependency)
            p.method_dependencies.add(dependency)
        m.inputs = []
        m.inputs_map = {}
        for input in service["inputs"]:
            a = Argument()
            a.name = input["name"]
            a.clean = input["clean"] if "clean" in input else a.name
            m.inputs_map[a.name] = a.clean
            a.type = input["type"]
            if a.type.startswith("list("):
                dependency = a.type[5:-1]
            else:
                dependency = a.type
            if dependency not in p.core_types:
                m.dependencies.add(dependency)
                p.method_dependencies.add(dependency)
            a.param = input["param"]
            a.indexable = input.get("indexable", False)
            a.default = input.get("default", None)
            a.hidden = input.get("hidden", False)
            a.description = input.get("description", "")
            a.comment = input.get("comment", "")
            m.inputs.append(a)
        p.methods.append(m)
    return p