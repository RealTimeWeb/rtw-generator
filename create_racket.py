import json
import traceback
import sys
from urlparse import urlparse
from urllib import quote_plus
from textwrap import wrap
from collections import OrderedDict

from create_loose_ast import kebab_case, snake_case, create_loose_ast, flat_case, camel_case_caps
from create_loose_ast import _recursively_convert_unicode_to_str

def racket_name(string):
    return string.lower().replace(" ", "-").replace("_", "-")

def indent(string, indentation=0):
    return ("\t" * indentation) + string.replace("\n", "\n"+("\t" * indentation))

def invocation(function, args=""):
    if type(args) == str:
        return "({}{}{})".format(function, " " if args else "", args)
    else:
        return "({}{}{})".format(function, " " if args else "", " ".join(args))
                  
def struct_out(struct):
    return provide(invocation("struct-out", struct))

def _if(condition, yes, no):
    return "(if {}\n{}\n{})".format(condition, indent(yes, 1), indent(no, 1))
    
def provide(method):
    return invocation("provide", [method])
    
def require(library):
    return invocation("require", library)
    
def define_struct(name, fields):
    return invocation("define-struct", [name, "({})".format(" ".join(fields))])
    
def define(name, args, body):
    return "(define {}\n{})".format(invocation(name, args), indent(body, 1))
    
def define_constant(name, value):
    return "(define {} {})".format(name, value)
    
def comment(string):
    return "; "+string
    
def new_line(times=1):
    return "\n" * times
    
def quote(string=""):
    return '"{}"'.format(string)

conversion_mapping = {("string", "float") : "",
                  ("float", "string") : "number->string",
                  ("long", "string") : "number->string",
                  ("integer", "string") : "number->string",
                  ("string", "integer") : "",
                  ("boolean", "string") : "boolean->string",
                  ("string", "boolean") : "",
                  ("string", "long") : "",
                  ("string", "string") : ""}
                  
racket_types = {"string": "string",
                "float": "number",
                "long": "number",
                "integer": "number",
                "void": "void",
                "boolean": "boolean"}
    
def make_racket_type(source, modifier="?"):
    is_list = source.startswith("list(")
    if is_list:
        source = source[5:-1] #chomp out the "list(" and ")"
    converted_type= racket_types.get(source, None)
    if converted_type is None: # need to convert to custom class
        converted_type = kebab_case(source)
    if is_list: # if it's a list, apply it to each element
        return "(listof {}{})".format(converted_type, modifier)
    else: # otherwise just return it normally
        return converted_type+modifier
                  
def make_conversion(source, target, source_type):
    is_list = target.startswith("list(")
    if is_list:
        target = target[5:-1] #chomp out the "list(" and ")"
    conversion_function = conversion_mapping.get((source_type, target), None)
    if conversion_function == "": # might require no conversion
        return source
    elif conversion_function is None: # need to convert to custom class
        conversion_function = "json->{}".format(target)
    if is_list: # if it's a list, apply it to each element
        return invocation("map", [conversion_function, source])
    else: # otherwise just return it normally
        return invocation(conversion_function, [source])
        
def symbol(string):
    return "'" + string
    
def defproc(name, return_type, args, description):
    if type(args) == list:
        arg_string = "\n\t\t\t".join(["[{} {}]".format(arg_name, arg_type) for arg_name, arg_type, arg_description in args])
    list_arguments = "\n\n\t\t".join("\t@item{{@racket[{}] --- {}}}".format(arg_name, arg_description) for arg_name, arg_type, arg_description in args)
    description = "\n\n"+description + "\n@itemlist[\n\n\t\t{}]".format(list_arguments)
    return "@defproc[({} {}) {}]{{{}}}\n\n".format(name, arg_string, return_type, description)
                  
def create_racket(spec):
    # Header Data
    project_name = kebab_case(spec.name)
    result = "#lang racket" + new_line(2)
    documentation = """
#lang scribble/manual
 
@title{{{}}}
@author{{author+email "{}" "{}"}}

@section{{Structs}}
 
""".format(kebab_case(spec.name), spec.author, spec.author_email) + spec.description + new_line(3)

    # Provide structs
    result += comment("Provide the external structs") + new_line(1)
    for a_class in spec.classes:
        result += struct_out(kebab_case(a_class.name)) + new_line(1)
    
        
    # Provide functions
    result += "\n; Provide the external functions\n"
    for a_method in spec.methods:
        result += provide(kebab_case(a_method.name)) + new_line(1)
        result += provide(kebab_case(a_method.name+"/string")) + new_line(1)
        result += provide(kebab_case(a_method.name+"/json")) + new_line(1)
    result += provide("disconnect-{}".format(project_name)) + new_line()
    result += provide("connect-{}".format(project_name)) + new_line()

    # Import internal libraries
    result += new_line() + comment("Load the internal libraries") + new_line()
    result += require("net/url") + new_line()
    result += require("srfi/19") + new_line()
    result += require("srfi/6") + new_line()
    result += require("racket/port") + new_line()
    result += require("json") + new_line()
    result += require("net/uri-codec") + new_line(2)
    result += comment("Define the structs") + new_line()
    # Define structs
    struct_list = set()
    for a_class in spec.classes:
        domain_name = kebab_case(a_class.name)
        domain_args = map(lambda x : kebab_case(x.name), a_class.fields)
        struct_list.add(domain_name)
        result += define_struct(domain_name, domain_args) + new_line(2)
        args = [(kebab_case(a_field.name), make_racket_type(a_field.type), a_field.description) for a_field in a_class.fields]
        documentation += defproc("make-"+domain_name, domain_name, args, a_class.description)
        
    # Define json->struct functions
    for a_class in spec.classes:
        domain_name = kebab_case(a_class.name)
        parser_args = []
        for a_field in a_class.fields:
            in_name = a_field.in_mask
            out_name, out_type = map(kebab_case, [a_field.name, a_field.type])
            in_name_chain = in_name.split("->")
            in_name_chain_string = "jdata"
            for name in in_name_chain:
                in_name_chain_string = "(hash-ref {} '{})".format(in_name_chain_string, name)
            mapper = ""
            if out_type.startswith("list("):
                out_type = out_type[5:-1]
                mapper = "map "
            if out_type in struct_list:
                parser_arg = "({}json->{} {})".format(mapper, out_type, in_name_chain_string)
            elif out_type == "string":
                parser_arg = in_name_chain_string
            elif ("string", out_type) in conversion_mapping:
                #parser_arg = "({}{} {})".format(mapper, conversion_mapping[("string", out_type)], in_name_chain_string)
                parser_arg = in_name_chain_string # Racket/json actually handles all that for us.
            else:
                parser_arg = "(json->{} {})".format(out_type, in_name_chain_string)
            parser_args.append(parser_arg)
        parser_args = "\n\t\t".join(parser_args)
        body = invocation("make-{}".format(domain_name), parser_args)
        result += define("json->{}".format(domain_name), "jdata", body) + new_line(2)
        
    # Handle connections
    result += new_line() + comment("Handle connections") + new_line()
    result += define_constant("CONNECTION", "true") + new_line()
    result += define("disconnect-{}".format(project_name), [], 
                        invocation("set!", ["CONNECTION", "false"])) + new_line()
    result += define("connect-{}".format(project_name), [], 
                        invocation("set!", ["CONNECTION", "true"])) + new_line()
                        
    documentation += "\n\n@section{Functions}\n\n"
    documentation += defproc("disconnect-{}".format(project_name), "void", [], "Establishes that data will be retrieved locally.")
    documentation += defproc("connect-{}".format(project_name), "void", [], "Establishes that the online service will be used.")
                        
    # Build client store
    result += new_line() + comment("Build Client Store") + new_line()
    result += define_constant("CLIENT_STORE", invocation("read-json", invocation("open-input-file", quote("cache.json")))) + new_line(2)
    
    # Define service functions
    result += define("boolean->string", "a-boolean",
                        _if("a-boolean", quote("true"), quote("false")))+new_line()
    result += define("string->boolean", "a-string",
                        invocation("string=?", ["a-string", quote("true")])) +new_line()
    result += define("key-value", "pair", 
                invocation("string-append", [invocation("symbol->string", invocation("car", "pair")),
                                             quote("="), 
                                             invocation("cdr", "pair")])) + new_line()
    result += define("convert-post-args", "data", 
                invocation("string->bytes/utf-8", 
                    invocation("alist->form-urlencoded", "data"))) + new_line()
    result += define("convert-get-args", ["url", "data"], 
                    invocation("string-append", ["url", quote("?"), 
                        invocation("string-join", [invocation("map", 
                                                             ["key-value", "data"]), 
                                                   quote("&")])])) + new_line()
    result += define("hash-request", ["url", "data"],
                    invocation("string-append", ["url", 
                                                 quote("%{"), 
                                                invocation("string-join", [invocation("map", 
                                                                                     ["key-value", "data"]), 
                                                                           quote("}%{")]),
                                                 quote("}")])) + new_line()
    result += define("post->json", ["url", "full-data", "index-data"], 
                        _if("CONNECTION", 
                                invocation("port->string", 
                                    invocation("post-pure-port", [invocation("string->url", "url"), 
                                                                  invocation("convert-post-args", "full-data")])),
                                invocation("hash-ref", ["CLIENT_STORE", 
                                                        invocation("hash-request", ["url", "index-data"]), 
                                                        quote()]))
                    ) + new_line()
    result += define("get->json", ["url", "full-data", "index-data"], 
                        _if("CONNECTION", 
                                invocation("port->string", 
                                    invocation("get-pure-port", invocation("string->url", invocation("convert-get-args", ["url", "full-data"])))),
                                invocation("hash-ref", ["CLIENT_STORE", 
                                                        invocation("hash-request", ["url", "index-data"]),
                                                        quote()]))
                    ) + new_line()
        
    # Define functions
    result += new_line() + comment("Define the services, and their helpers") + new_line()
    for a_method in spec.methods:
        service_name = kebab_case(a_method.name)
        
        indexed_arguments_map = {}
        url_argument_map = OrderedDict()
        param_arguments_map = {}
        visible_arguments = []
        documentation_arguments = []
        for argument in a_method.inputs:
            if argument.default:
                value = quote(argument.default)
            else:
                value = make_conversion(kebab_case(argument.clean), kebab_case(argument.type), "string")
            if argument.indexable:
                indexed_arguments_map[argument.name] = value
            if not argument.hidden:
                visible_arguments.append(kebab_case(argument.clean))
                documentation_arguments.append((kebab_case(argument.clean), make_racket_type(argument.type), argument.description))
            if argument.param:
                url_argument_map[argument.name] = value
            else:
                param_arguments_map[argument.name] = value
        
        # Build URL
        url = a_method.url
        url_components = []
        for pattern, value in url_argument_map.iteritems():
            pre, post = url.split("<{}>".format(pattern), 1)
            url_components += [quote(pre), value]
            url = post
        if url:
            url_components.append(quote(url))
        url = invocation("string-append", url_components)
        
        # Build parameter arguments
        all_arguments = []
        for name, value in param_arguments_map.iteritems():
            all_arguments.append(invocation("cons", [symbol(name), value]))
        
        # Build index arguments
        indexed_arguments = []
        for name, value in indexed_arguments_map.iteritems():
            indexed_arguments.append(invocation("cons", [symbol(name), value]))
        
        
        all_arguments = invocation("list", all_arguments)
        indexed_arguments = invocation("list", indexed_arguments)
        result += define(service_name, visible_arguments, 
                            make_conversion(invocation(service_name+"/json", visible_arguments), kebab_case(a_method.output), "string")
                        ) + new_line(2)
        result += define(service_name+"/json", visible_arguments, 
                            invocation("string->jsexpr", 
                                invocation(service_name+"/string", visible_arguments))
                        ) + new_line(2)
        result += define(service_name+"/string", visible_arguments, 
                            invocation(a_method.type+"->json", 
                                       [url, new_line(), 
                                        indent(all_arguments, 1), new_line(), 
                                        indent(indexed_arguments, 1)])
                        ) + new_line(2)
        documentation += defproc(service_name, make_racket_type(a_method.output), documentation_arguments, a_method.description)
    base_dir = "{}/racket/".format(camel_case_caps(spec.name))
    files = {"{}{}.rkt".format(base_dir, kebab_case(spec.name)): result}
    
    files["{}{}.scrbl".format(base_dir, kebab_case(spec.name))] = documentation
    files["{}cache.json".format(base_dir)] = "{}"
    return files

if __name__ == "__main__":
    import os
    for file, body in create_racket(create_loose_ast(_recursively_convert_unicode_to_str(json.load(open(sys.argv[1],'r'))))).iteritems():
        if not os.path.exists(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))
        #f = open(file, 'w+')
        #f.write(body)
        #f.close()
        print file
        print "~~~" * 10
        print body
        print "~~~" * 10