import json
import sys
from urlparse import urlparse
from urllib import quote_plus, urlencode
from textwrap import wrap
from collections import OrderedDict
from auxiliary import to_dict, camel_case_caps, camel_case
from auxiliary import snake_case, kebab_case, flat_case
import re
from jinja2 import Environment, FileSystemLoader
templates = 'templates/java/'
env = Environment(loader=FileSystemLoader(templates))
env.filters['camel_case_caps'] = camel_case_caps
env.filters['camel_case'] = camel_case
env.filters['snake_case'] = snake_case
env.filters['kebab_case'] = kebab_case
env.filters['flat_case'] = flat_case

conversion_mapping = { ("string", "integer") : "Integer.parseInt",
                       ("string", "float") : "Double.parseDouble",
                       ("string", "long") : "Long.parseLong",
                       ("string", "string") : "",
                       ("string", "boolean") : "Boolean.parseBoolean",
                       ("integer", "string") : "Integer.toString",
                       ("long", "string") : "Long.toString",
                       ("float", "string") : "Double.toString",
                       ("boolean", "string") : "Boolean.toString"}

java_type_names = { "string" : "String",
                    "integer" : "int",
                    "float" : "double",
                    "boolean" : "boolean",
                    "long": "long"}

gson_conversions = { "string" : "getAsString",
                     "integer" : "getAsInt",
                     "float" : "getAsDouble",
                     "boolean" : "getAsBoolean",
                     "long" : "getAsLong"}
                     
def convert_url_parameters(url):
    return re.sub("<.*?>","%s",url)

def collect_url_parameters(url):
    return map(str, re.findall("<(.*?)>", url))
                    
def convert_to_java_type(source_type):
    is_list = source_type.startswith("list(")
    if is_list:
        source_type = source_type[5:-1] #chomp out the "list(" and ")"
    target_type = java_type_names.get(source_type, camel_case_caps(source_type))
    if is_list: # if it's a list, apply it to each element
        return "ArrayList<{}>".format(target_type)
    else: # otherwise just return it normally
        return target_type

env.filters['to_java_type'] = convert_to_java_type
env.filters['convert_url_parameters'] = convert_url_parameters
env.filters['collect_url_parameters'] = collect_url_parameters

def build_metafiles(model):
    return {'.classpath': env.get_template('.classpath',globals=model).render(),
            '.project': env.get_template('.project',globals=model).render(),
            'build.xml': env.get_template('build.xml', globals=model).render()}
    
def build_main(model):
    name = model['metadata']['name']
    root = 'src/realtimeweb/' + flat_case(name) + '/'
    return {root + camel_case_caps(name) + '.java' :
                env.get_template('main.java', globals=model).render()}
                
def copy_file(filename):
    with open(filename, 'r') as input:
        return input.read()

def build_java(model):
    files = {'libs/StickyWeb.jar' : copy_file(templates+'libs/StickyWeb.jar')}
    files.update(build_metafiles(model))
    files.update(build_main(model))
    return files
    
if __name__ == "__main__":
    import json
    from auxiliary import clean_json
    input = clean_json(json.load(open(sys.argv[1],'r')))
    from validate import validate_spec
    warnings, errors = validate_spec(input)
    for warning in warnings:
        print "Warning!", warning
    if not errors:
        from compile import compile_spec
        new_package = compile_spec(input)
        files = build_java(to_dict(new_package))
        from build import build_dir
        build_dir(files, sys.argv[2])
    else:
        for error in errors:
            print "Error!", error
