import json
import traceback
import sys
from urlparse import urlparse
from urllib import quote_plus
from zipfile import ZipFile
from StringIO import StringIO
from flask import make_response, send_file
from create_racket import create_racket
from create_java import create_java
from create_python import create_python
from create_loose_ast import create_loose_ast

def _recursively_convert_unicode_to_str(input):
    if isinstance(input, dict):
        return {_recursively_convert_unicode_to_str(key): _recursively_convert_unicode_to_str(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [_recursively_convert_unicode_to_str(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def parse_spec(input):
    spec = create_loose_ast(_recursively_convert_unicode_to_str(input))
    inMemoryOutputFile = StringIO()
    zipFile = ZipFile(inMemoryOutputFile, 'w') 
    error_log = ""
    for method in [create_racket, create_python, create_java]:        
        try:
            files = method(spec)
            for filename, data in files.iteritems():
                zipFile.writestr(filename, data)
        except Exception, e:
            error_log += traceback.format_exc() + "\n\n"
    if error_log:
        zipFile.writestr("error_log", error_log)
    zipFile.close()
    inMemoryOutputFile.seek(0)
    data = inMemoryOutputFile.read()
    inMemoryOutputFile.close()
    return data

if __name__ == "__main__":
    import os
    spec = create_loose_ast(_recursively_convert_unicode_to_str(json.load(open(sys.argv[1],'r'))))
    for method in [create_racket, create_python, lambda x : create_java(x, True)]:
        try:
            files = method(spec)
            for filename, data in files.iteritems():
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                f = open(filename, 'wb+')
                f.write(data)
                f.close()
        except Exception, e:
            traceback.print_exc()
    
#print parse_spec(open("example-clientlibspec.json", "r").read())