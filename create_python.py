import json
import sys
from urlparse import urlparse
from urllib import quote_plus, urlencode
from textwrap import wrap
from collections import OrderedDict

from create_loose_ast import camel_case_caps, snake_case, create_loose_ast
from create_loose_ast import _recursively_convert_unicode_to_str

# quickstart-sphinx (or copy files)
# Add . and ./<modulename/ to sys.path in conf.py
# modify index.rst to list the classes and functions

FIX_JSON = """
def _recursively_convert_unicode_to_str(input):
    if isinstance(input, dict):
        return {_recursively_convert_unicode_to_str(key): _recursively_convert_unicode_to_str(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [_recursively_convert_unicode_to_str(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
"""

TAB = " " * 4

def indent(string, indentation=0):
    return (TAB * indentation) + string.replace("\n", "\n"+(TAB * indentation))

def _if(condition, yes, no):
    if type(yes) == str:
        return "if {}:\n".format(condition) + indent(yes, 1) + "\nelse:\n" + indent(no, 1)
    else:
        return "if {}:\n".format(condition) + indent("\n".join(yes), 1) + "\nelse:\n" + indent("\n".join(no), 1)
        
def static_code_block(code, indentation=0):
    return indent(code)

def _import(package, *items):
    if items:
        items = ", ".join(items)
        return "from {} import {}".format(package, items)
    else:
        return "import {}".format(package)

def assignment(left, right):
    return "{} = {}".format(left, right)
    
def self_assignment_from_param(keyword):
    return "self.{} = {}".format(keyword, keyword)

def _return(value):
    return "return {}".format(value)

def invocation(name, args, scope=None):
    arguments = ", ".join(args)
    if scope is not None:
        return "{}.{}({})".format(scope, name, arguments)
    else:
        return "{}({})".format(name, arguments)
    
def method(name, args, body_lines, indentation=0, description="", returns="void"):
    tabs = TAB * indentation
    arguments = ", ".join([arg_name for arg_name, arg_type, arg_desc in args])
    body = indent("\n".join(body_lines), 1)
    arg_descriptions = "\n".join([":param {0}: {2}\n:type {0}: {1}".format(arg_name, arg_type, arg_desc) for arg_name, arg_type, arg_desc in args] + [":returns: {}".format(returns)])
    description = '"""\n{}\n\n{}\n"""'.format(description, arg_descriptions)
    return "{}def {}({}):\n{}\n{}".format(tabs, name, arguments, indent(description, 1), body)
    
def _class(name, functions, static_functions, description=""):
    # add in static functions
    functions = functions + ["@staticmethod\n" + sf for sf in static_functions]
    # concatenate them with new lines, or if it's empty return "pass"
    functions = "\n\n".join(functions) if functions else "pass"
    # insert into the format
    description = '"""\n{}\n"""'.format(description)
    return "class {}(object):\n{}\n{}".format(name, indent(description, 1), indent(functions, 1))
    
def new_line():
    return "\n"
    
def file(*lines):
    return "\n".join(lines)
    
def dictionary(pairs):
    return "{%s}" % (", ".join(["{} : {}".format(k, v) for k, v in pairs.iteritems()]),)
    
def quote(string):
    return '"{}"'.format(string)
    
conversion_mapping = { ("string", "integer") : "",
                       ("string", "float") : "",
                       ("string", "string") : "",
                       ("string", "boolean") : "",
                       ("string", "long") : "",
                       ("long", "string") : "str",
                       ("boolean", "string") : "str",
                       ("integer", "string") : "str",
                       ("float", "string") : "str"}
                       
python_types = {"string": "string",
                "float": "float",
                "integer": "int",
                "void": "void",
                "boolean": "boolean",
                "long": "int"}
    
def make_python_type(source):
    is_list = source.startswith("list(")
    if is_list:
        source = source[5:-1] #chomp out the "list(" and ")"
    converted_type= python_types.get(source, None)
    if converted_type is None: # need to convert to custom class
        converted_type = camel_case_caps(source)
    if is_list: # if it's a list, apply it to each element
        return "listof {}".format(converted_type)
    else: # otherwise just return it normally
        return converted_type
                       
def make_conversion(source, target, source_type):
    is_list = target.startswith("list(")
    if is_list:
        target = target[5:-1] #chomp out the "list(" and ")"
    conversion_function = conversion_mapping.get((source_type, target), None)
    if conversion_function == "": # might require no conversion
        return source
    elif conversion_function is None: # need to convert to custom class
        conversion_function = "{}._from_json".format(target)
    if is_list: # if it's a list, apply it to each element
        return invocation("map", [conversion_function, source])
    else: # otherwise just return it normally
        return invocation(conversion_function, [source])
        
def infix_operator(operator, left, right):
    return "{} {} {}".format(left, operator, right)
    
def convert_json(source, target):
    source= "json_data['" + source.replace("->", "']['") + "']"
    return make_conversion(source, target, "string")

def _tuple(*args):
    if not args:
        return "tuple()"
    elif len(args) == 1:
        return "({},)".format(args[0])
    else:
        return "({})".format(", ".join(args))
        
def triple_quoted(string):
    return '"""\n{}\n"""'.format("\n".join(wrap(string, 70)))
    
def _try(attempt, failure):
    if type(attempt) == str:
        return "try:\n" + indent(attempt, 1) + "\nexcept Exception, e:\n" + indent(failure, 1)
    else:
        return "try:\n" + indent("\n".join(attempt), 1) + "\nexcept Exception, e:\n" + indent("\n".join(failure), 1)

def create_python(spec):
    package_name = snake_case(spec.name)
    base_dir = "{}/python/".format(camel_case_caps(spec.name))
    files = {}
    
    # cache.py
    cache_file = _import("json") + new_line()
    cache_file += static_code_block(FIX_JSON) + new_line()
    cache_file += assignment("CACHE", "{}") + new_line()
    cache_file += method("unload", [], ["CACHE= {}"], description="Internal method that empties the local cache.") + new_line()
    cache_file += method("load", [], [
            assignment("CACHE", 
                invocation("_recursively_convert_unicode_to_str", 
                    [invocation("load", 
                        [invocation("open", ["cache.json", "r"])],
                        "json")]))
        ], description="Internal method that loads the local cache.") + new_line()
    cache_file += method("lookup", [("key", "string", "Get the value based on the key from the cache.")], ['return CACHE.get(key, "")'], description="Internal method that looks up a key in the local cache.") + new_line()
    files['{}_cache.py'.format(base_dir)] = cache_file
    
    # Empty cache.json
    files['{}cache.json'.format(base_dir)] = "{}"
    
    # "json.py", "structured.py", and "regular.py"
    # These have the service methods
    for return_type in ("raw_json", "structured", "regular"):
        service_file = _import("requests") + new_line()
        service_file += _import("json") + new_line()
        service_file += _import("threading") + new_line()
        service_file += _import("_cache", "_recursively_convert_unicode_to_str", "lookup") + new_line()
        for dependency in spec.method_dependencies:
            service_file += _import(snake_case(dependency), camel_case_caps(dependency)) + new_line()
            
        if return_type == "raw_json":
            service_file += _import("_cache") + new_line()
            service_file += assignment("_using_cache", "False") + new_line()
            service_file += method("connect", [], ["global _using_cache", "cache.load()", "_using_cache = True"], description="Connect to the online data source in order to get up-to-date information.")
            service_file += 2 * new_line()
            service_file += method("disconnect", [], ["global _using_cache", "cache.unload()", "_using_cache = False"], description="Connect to the local cache, so no internet connection is required.")
            service_file += 2 * new_line()
        elif return_type == "structured":
            service_file += _import("raw_json") + new_line()
            service_file += method("connect", [], ["raw_json.connect()"], description="Connect to the online data source in order to get up-to-date information.") + new_line()
            service_file += method("disconnect", [], ["raw_json.disconnect()"], description="Connect to the local cache, so no internet connection is required.") + new_line()
        elif return_type == "regular":
            service_file += _import("structured") + new_line()
            service_file += method("connect", [], ["structured.connect()"], description="Connect to the online data source in order to get up-to-date information.") + new_line()
            service_file += method("disconnect", [], ["structured.disconnect()"], description="Connect to the local cache, so no internet connection is required.") + new_line()
        
        for a_method in spec.methods:
            # Hidden : won't appear in the generated method's arguments
            # Indexable : used to generate cache hash
            # Default : the value that will be passed to the query by default
            #           - if hidden, then passed in the dict, else pass it in via arguments
            # Param : if false, then it's a query-string arg or post arg, not a url argument
            # Name for building query arguments, clean is for the generated method's arguments
            query_url = quote(a_method.url.replace("<", "%(").replace(">", ")s"))
            url_arguments = OrderedDict()
            param_arguments = OrderedDict()
            method_arguments = []
            documented_method_arguments = []
            method_arguments_names = []
            hash_arguments = OrderedDict()
            for argument in a_method.inputs:
                if argument.hidden:
                    value = quote(argument.default)
                else:
                    if argument.default is not None:
                        method_arguments.append(assignment(snake_case(argument.clean), quote(argument.default)))
                    else:
                        method_arguments.append(snake_case(argument.clean))
                    documented_method_arguments.append( (snake_case(argument.clean), argument.type, argument.description))
                    method_arguments_names.append(snake_case(argument.clean))
                    value = snake_case(argument.clean)
                if argument.param:
                    url_arguments[quote(argument.name)] = make_conversion(value, "string", argument.type)
                else:
                    param_arguments[quote(argument.name)] = make_conversion(value, "string", argument.type)

                if argument.indexable and not argument.param:
                    hash_arguments[argument.name] = make_conversion(value, "string", argument.type)
            if url_arguments:
                query_url = infix_operator("%", query_url, dictionary(url_arguments))
            query_hash = "(" + query_url + ") + " + ("".join(['"%{' + k + '=" + ' + v + '+ "}"' for k,v in hash_arguments.iteritems()]) if hash_arguments else quote(""))
            params_pass = "data" if a_method.type == "post" else "params"
            if return_type == "raw_json":
                service_file += method(snake_case(a_method.name), documented_method_arguments, [
                        _if("_using_cache", [
                                assignment("result", invocation("lookup", [query_hash], "cache")),
                                _return("result")
                            ], [
                                assignment("result", invocation(a_method.type, [
                                    query_url,
                                    assignment(params_pass, dictionary(param_arguments))
                                    ], "requests")),
                                _return("result.text")
                            ])
                    ], description=a_method.description, returns="string")
                service_file += (new_line() * 2)
                method_arguments= ["callback", "error_callback"] + method_arguments
                documented_method_arguments = [("callback", "function", "Function that consumes the data (string) returned on success."), ("error_callback", "function", "Function that consumes the exception returned on failure.")] +documented_method_arguments
                service_file += method(snake_case(a_method.name+"_async"), documented_method_arguments, [
                        method("server_call", documented_method_arguments, [
                            _try([  
                                    invocation("callback", [invocation(snake_case(a_method.name), method_arguments[2:])])
                                ], [
                                    invocation("error_callback", ["e"])
                                ])
                        ], description="Internal closure to thread this call."),
                        invocation("start", [], invocation("Thread", ["target=server_call", assignment("args", _tuple(*method_arguments_names))] , "threading"))
                    ], description="Asynchronous version of {}".format(snake_case(a_method.name)))
            elif return_type == "structured":
                service_file += method(snake_case(a_method.name), documented_method_arguments, [
                        _return(invocation("_recursively_convert_unicode_to_str",
                            [invocation("loads", 
                                [invocation(snake_case(a_method.name), 
                                           method_arguments, 
                                           "raw_json")], 
                                "json")]))
                    ], description = a_method.description, returns=("list" if a_method.output.startswith("list(") else "dict"))
                service_file += (new_line() * 2)
                method_arguments= ["callback", "error_callback"] + method_arguments
                documented_method_arguments = [("callback", "function", "Function that consumes the data (a {}) returned on success.".format(("list" if a_method.output.startswith("list(") else "dict"))), ("error_callback", "function", "Function that consumes the exception returned on failure.")] + documented_method_arguments
                service_file += method(snake_case(a_method.name+"_async"), documented_method_arguments, [
                        method("server_call", documented_method_arguments, [
                            _try([  
                                    invocation("callback", [invocation(snake_case(a_method.name), method_arguments[2:])])
                                ], [
                                    invocation("error_callback", ["e"])
                                ])
                        ], description="Internal closure to thread this call."),
                        invocation("start", [], invocation("Thread", ["target=server_call", assignment("args", _tuple(*method_arguments_names))] , "threading"))
                    ], description="Asynchronous version of {}".format(snake_case(a_method.name)))
            elif return_type == "regular":
                service_file += method(snake_case(a_method.name), documented_method_arguments, [
                        _return(make_conversion(invocation(snake_case(a_method.name), 
                                                            method_arguments, 
                                                            "structured"),
                                                a_method.output, "string"))
                    ], description=a_method.description, returns=make_python_type(a_method.output))
                service_file += (new_line() * 2)
                method_arguments= ["callback", "error_callback"] + method_arguments
                documented_method_arguments = [("callback", "function", "Function that consumes the data (a {}) returned on success.".format(make_python_type(a_method.output))), ("error_callback", "function", "Function that consumes the exception returned on failure.")] +documented_method_arguments
                service_file += method(snake_case(a_method.name+"_async"), documented_method_arguments, [
                        method("server_call", documented_method_arguments, [
                            _try([  
                                    invocation("callback", [invocation(snake_case(a_method.name), method_arguments[2:])])
                                ], [
                                    invocation("error_callback", ["e"])
                                ])
                        ], description="Internal closure to thread this call."),
                        invocation("start", [], invocation("Thread", ["target=server_call", assignment("args", _tuple(*method_arguments_names))] , "threading"))
                    ], description="Asynchronous version of {}".format(snake_case(a_method.name)))
            service_file += (new_line() * 2)
        files["{}{}.py".format(base_dir, return_type)] = service_file
    
    # These are the domain objects
    for a_class in spec.classes:
        class_file_name = snake_case(a_class.name)
        class_name = camel_case_caps(a_class.name)
        init_function = method("__init__", [("self", class_name, "This object")] + [
                (snake_case(arg.name), make_python_type(arg.type), arg.description) for arg in a_class.fields
            ], [
                self_assignment_from_param(snake_case(arg.name)) for arg in a_class.fields
            ], returns=class_name, description="Creates a new {}".format(class_name))
        from_json_function = method("_from_json", [("json_data", "dict", "The raw json data to parse")], [
                _return(invocation(class_name, 
                                   [(",\n"+(3*TAB)).join([convert_json(arg.in_mask, arg.type) for arg in a_class.fields])]))
            ], returns=class_name, description="Creates a {} from json data.".format(class_name))
        class_file = ""
        for an_import in a_class.dependencies:
            class_file += _import(snake_case(an_import), camel_case_caps(an_import)) + new_line()
        class_file += _class(class_name, [init_function], [from_json_function], description=a_class.description)
        files["{}{}.py".format(base_dir, class_file_name)] = class_file
        
    # __main__
    main_file = ""
    files["{}__init__.py".format(base_dir)] = main_file
    
    return files
    
if __name__ == "__main__":
    import os
    for file, body in create_python(create_loose_ast(_recursively_convert_unicode_to_str(json.load(open(sys.argv[1],'r'))))).iteritems():
        if not os.path.exists(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))
        #f = open(file, 'w+')
        #f.write(body)
        #f.close()
        print file
        print "~~~" * 10
        print body
        print "~~~" * 10