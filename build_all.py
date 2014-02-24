from build_python import build_python
from build_java import build_java
from build_racket import build_racket
from compile import compile_spec
from build import build_dir
from auxiliary import clean_json
from validate import validate_spec
import json

def build_all(filename, output=None):
    input = clean_json(json.load(open(filename,'r')))
    validation_warnings, validation_errors = validate_spec(input)
    build_data = ""
    build_errors = []
    if not errors:
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