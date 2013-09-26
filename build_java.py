import json
import sys
from urlparse import urlparse
from urllib import quote_plus, urlencode
from textwrap import wrap
from collections import OrderedDict
import re

def snake_case(string):
    return string.replace(" ", "_").lower()
    
def camel_case_caps(string):
    return ''.join(x for x in string.title() if not x.isspace())
    
def camel_case(string):
    s = camel_case_caps(string)
    return s[0].lower() + s[1:] if s else ""
def flat_case(string):
    return string.replace(" ", "").replace("_", "").lower()

def build_classes(package):
    

def build(package):
    build_classes(package)
    
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
    else:
        for error in errors:
            print "Error!", error