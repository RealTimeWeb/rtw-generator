from build_python import build_python
from build_java import build_java
from build_racket import build_racket
from compile import compile_spec
from build import build_dir
from auxiliary import clean_json, to_dict
from validate import validate_spec
import json
import sys

def build_all(filename, output=None):
    with open(filename, "rb") as file:
        file_data = file.read()
    input = clean_json(json.loads(file_data.decode('utf-8')))
    validation_warnings, validation_errors = validate_spec(input)
    build_data = ""
    build_errors = []
    if not validation_errors:
        new_package = compile_spec(input)
        files = {}
        files.update(build_python(to_dict(new_package)))
        files.update(build_java(to_dict(new_package)))
        files.update(build_racket(to_dict(new_package)))
        if output is None:
            build_data, build_errors = build_zip(files)
        else:
            build_data, build_errors = build_dir(files, output)
    return validation_warnings, validation_errors, build_data, build_errors

if __name__ == "__main__":
    warnings, validation_errors, build_data, build_errors = build_all(sys.argv[1], sys.argv[2])
    print "Compile Warnings: ", "-"*10
    for warning in warnings:
        print "\t",warning
    print "Compile Errors: ", "-"*10
    for error in validation_errors:
        print "\t",error
    print "Build Errors: ", "-"*10
    for error in build_errors:
        print "\t",error
