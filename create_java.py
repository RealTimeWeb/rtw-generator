import json
import sys
from urlparse import urlparse
from urllib import quote_plus, urlencode
from textwrap import wrap
from collections import OrderedDict
import re

from create_loose_ast import camel_case_caps, camel_case, flat_case, create_loose_ast

GOOGLE_GSON_IMPORTS = """
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
"""

    
def indent(string, indentation=0):
    return ("\t" * indentation) + string.replace("\n", "\n"+("\t" * indentation))

def _if(condition, yes, no=""):
    if type(yes) == str:
        if no:
            return "if ({}) {{\n".format(condition) + indent(yes, 1) + "\n} else {\n" + indent(no, 1) + "\n}"
        else:
            return "if ({}) {{\n".format(condition) + indent(yes, 1) + "\n}"
    elif no:
        return "if ({}) {{\n".format(condition) + indent("\n".join(yes), 1) + "\n} else {\n" + indent("\n".join(no), 1) + "\n}"
    else:
        return "if ({}) {{\n".format(condition) + indent("\n".join(yes), 1) + "\n}"
        
def static_code_block(code, indentation=0):
    return indent(code)
    
def package_generator(organization, library):
    return lambda folder : "package "+(".".join([organization, library, folder])) + ";\n\n"

def _import(package):
    if type(package) == str:
        return "import {};".format(package)
    else:
        return "import {};".format(".".join(package))

def _imports(packages):
    return "\n".join(["import {};".format(package) for package in packages]) + "\n"

def assignment(left, right):
    return "{} = {};".format(left, right)
    
def this_assignment_from_param(keyword):
    return "this.{} = {};".format(keyword, keyword)
    
def attribute(name, source="this"):
    return "{}.{}".format(source, name)

def _return(value):
    return "return {};".format(value)
    
def statement(string, indentation = 0):
    return ("\t" * indentation) + "{};\n".format(string)

def invocation(name, args, scope=None):
    arguments = ", ".join(args)
    if scope is not None:
        return "{}.{}({})".format(scope, name, arguments)
    else:
        return "{}({})".format(name, arguments)
    
def method(name, return_type, args, body_lines, modifiers = "", decorators=None, throws=None, description="", arg_modifiers=""):
    arguments = ", ".join(["{}{} {}".format(arg_modifiers, type, arg_name) for type, arg_name, arg_desc in args])
    body = indent("\n".join(body_lines), 1)
    modifiers = modifiers+" " if modifiers else ""
    decorators = "".join(["@{}\n".format(decorator) for decorator in decorators]) if decorators else ""
    if throws:
        throws = "throws {} ".format(", ".join(throws))
    else:
        throws = ""
    comments = "/**\n * {}\n{}\n".format(description, "\n".join([" * @param {} {}".format(arg_name, arg_desc) for type, arg_name, arg_desc in args]))
    if return_type == "void":
        comments += " */"
    else:
        comments += " * @return {}\n */".format(return_type)
    return "{}\n{}{}{} {}({}) {}{{\n{}\n}}\n".format(comments, decorators, modifiers, return_type, name, arguments, throws, body)
    
def _class(modifiers, name, implements, extends, body, class_type = "class", description=""):
    body = "\n".join(body)
    implements = " implements {}".format(", ".join(implements)) if implements else ""
    extends = " extends {}".format(", ".join(extends)) if extends else ""
    modifiers = modifiers+" " if modifiers else ""
    comments = "/**\n * {}\n */".format(description)
    # insert into the format
    return "{}\n{}{} {}{}{} {{\n{}\n}}\n".format(comments, modifiers, class_type, name, implements, extends, indent(body, 1))
    
def new_line():
    return "\n"
    
def file(*lines):
    return "\n".join(lines)
    
def quote(string):
    return '"{}"'.format(string.replace('"', '\"'))
                       
def infix_operator(operator, left, right):
    return "{} {} {}".format(left, operator, right)
    
def anonymous_class(name, args, extends, implements, body):
    body = "\n".join(body)
    implements = " implements {}".format(", ".join(implements)) if implements else ""
    extends = " extends {}".format(", ".join(extends)) if extends else ""
    if type(args) != str:
        args = ", ".join(args)
    # insert into the format
    return "new {}({}){}{} {{\n{}\n}}\n".format(name, args, implements, extends, indent(body, 1))
    
def instance(name, args):
    if type(args) != str:
        args = ", ".join(args)
    return "new {}({})".format(name, args)
    
def attribute_definition(modifiers, type, name, comment=""):
    modifiers = modifiers+" " if modifiers else ""
    comment = "    //{}".format(comment) if comment else ""
    return "{}{} {};{}".format(modifiers, type, name, comment)
    
def method_prototype(modifiers, return_type, method_name, args, description=""):
    arguments = ", ".join(["{} {}".format(type, name) for type, name, arg_desc in args])
    modifiers = modifiers+" " if modifiers else ""
    comments = "/**\n * {}\n{}\n".format(description, "\n".join([" * @param {} {}".format(arg_name, arg_desc) for type, arg_name, arg_desc in args]))
    if return_type == "void":
        comments += " */"
    else:
        comments += " * @return {}\n */".format(return_type)
    return "{}\n{}{} {}({});".format(comments, modifiers, return_type, method_name, arguments)
    
def _try(attempt, failures):
    attempt = "\n".join(attempt)
    result = "try {\n" + indent(attempt, 1)
    for failure in failures:
        exception = failure[0]
        failure = "\n".join(failure[1])
        result += "\n}} catch ({}) {{\n".format(exception) + indent(failure, 1)
    return result + "}\n"
    
def static_file(location, package_data=""):
    store_template = open(location, 'rb')
    data = store_template.read()
    store_template.close()
    return package_data + data
    
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
                    
def convert_to_java_type(source_type):
    is_list = source_type.startswith("list(")
    if is_list:
        source_type = source_type[5:-1] #chomp out the "list(" and ")"
    target_type = java_type_names.get(source_type, source_type)
    if is_list: # if it's a list, apply it to each element
        return "ArrayList<{}>".format(target_type)
    else: # otherwise just return it normally
        return target_type

def generate_getter(name, type, description):
    return method("get"+camel_case_caps(name), convert_to_java_type(type), [], [
                    _return(attribute(camel_case(name)))
                ], "public", description=description)
def generate_setter(name, type, description):
    return method("set"+camel_case_caps(name), "void", [
                    (convert_to_java_type(type), camel_case(name), description)
                ], [
                    this_assignment_from_param(camel_case(name))
                ], "public")
    
def block(label, input, code):
    code = "\n".join(code)
    return "{} ({}) {{\n".format(label, input) + indent(code, 1) + "\n}\n"
        
def make_gson_conversion(in_mask, target_type):
    is_list = target_type.startswith("list(")
    in_mask = 'json.get("' + in_mask.replace("->", '").getAsJsonObject().get("') + '")'
    if is_list:
        return invocation("fromJson",[
                        invocation("getAsJsonArray", [], in_mask),
                        attribute("class", convert_to_java_type(target_type))
                    ], "gson")
    else:
        conversion_method = gson_conversions.get(target_type, None)
        if conversion_method is None:
            return instance(target_type, [invocation("getAsJsonObject", [], in_mask), "gson"])
        else:
            return invocation(conversion_method, [], in_mask)
            
def convert_to_string(source):
    return invocation("valueOf", [source], "String")
            
def mangle_parameter(string):
    return "a"+camel_case_caps(string)

def singleton_constructor(json_service_class_name):
    return method("getInstance", json_service_class_name, [], [
                _if("instance == null",[
                    block("synchronized", attribute("class", json_service_class_name), [
                        _if("instance == null", [
                            assignment("instance", instance(json_service_class_name, []))
                            ])
                        ])
                    ]),
                _return("instance")
            ], "public static", description="Retrieves the singleton instance.")
    
def generate_service_method_arguments(a_method):
    return [(convert_to_java_type(argument.type), argument.clean, argument.description)
                for argument in a_method.inputs 
                    if not argument.hidden ]
            
    
def generate_service_method(a_method):
    # Hidden : won't appear in the generated method's arguments
    # Indexable : used to generate cache hash
    # Default : the value that will be passed to the query by default
    #           - if hidden, then passed in the dict, else pass it in via arguments
    # Param : if false, then it's a query-string arg or post arg, not a url argument
    # Name for building query arguments, clean is for the generated method's arguments
    query_url = quote(re.sub("<.*?>","%s",a_method.url))
    query_url_parameters = map(str, re.findall("<(.*?)>", a_method.url))
    query_url = assignment("String url", "String.format("+query_url+", {})")
    
    method_arguments = []
    method_arguments_names = []
    url_arguments = OrderedDict()
    indexable_parameters = []
    non_indexable_parameters = []
    for argument in a_method.inputs:
        if not argument.hidden:
            method_arguments.append((convert_to_java_type(argument.type), camel_case(argument.clean), argument.description))
        if argument.param:
            url_arguments[argument.name] = convert_to_string(camel_case(argument.clean))
        else:
            if argument.hidden:
                value = quote(argument.default)
            else:
                value = camel_case(argument.clean)
            if argument.indexable:
                indexable_parameters.append( invocation("put", [quote(argument.name), convert_to_string(value)], "parameters")+";")
            else:
                non_indexable_parameters.append( invocation("put", [quote(argument.name), convert_to_string(value)], "parameters")+";")

    url_arguments = [url_arguments[name] for name in query_url_parameters]
    query_url = query_url.format(", ".join(url_arguments))
    return query_url, method_arguments, indexable_parameters, non_indexable_parameters
    
def create_domain_class(a_class, packager, package_name):
    class_name = camel_case_caps(a_class.name)
    class_file = packager("domain")
    class_file += GOOGLE_GSON_IMPORTS + new_line()
    
    attributes = []
    methods = []
    fields = []
    regular_constructor_args = []
    for a_field in a_class.fields:
        property_suffix = camel_case_caps(a_field.name)
        java_field_name = camel_case(a_field.name)
        attributes.append(attribute_definition("private", convert_to_java_type(a_field.type), java_field_name, comment=a_field.comment))
        fields.append(java_field_name)
        methods.append(generate_getter(a_field.name, a_field.type, a_field.description))
        methods.append(generate_setter(a_field.name, a_field.type, a_field.description))
        regular_constructor_args.append((convert_to_java_type(a_field.type), java_field_name, a_field.description))
    comment = ["//"+a_class.comment] if a_class.comment else []
    class_file += _class("public", class_name, [], [], comment + [new_line()] + attributes + [new_line()] + methods + [new_line()] + [
        method("toString", "String", [], [
            _return(quote(class_name + "[") + ' + {} + "]"'.format(' + ", " + '.join(fields)))
        ], "public", description=a_class.description),
        method(class_name, "", [
            ("JsonObject", "json", "The raw json data that will be parsed."),
            ("Gson", "gson", "The Gson parser. See <a href='https://code.google.com/p/google-gson/'>https://code.google.com/p/google-gson/</a> for more information.")
        ], [
            #TODO: Potential optimization of caching repeated lookups
            assignment(attribute(camel_case(arg.name)), 
                       make_gson_conversion(arg.in_mask, arg.type)) 
                for arg in a_class.fields
        ], "public", description="Internal constructor to create a {} from a Json representation.".format(class_name)),
        method(class_name, "", regular_constructor_args, [
            assignment(attribute(camel_case(arg.name)), 
                       camel_case(arg.name)) 
                for arg in a_class.fields
        ], "public", description="Regular constructor to create a {}.".format(class_name))
    ], description = a_class.description)
    return "{}/domain/{}.java".format(package_name, class_name), class_file
    
return_format_class_names = {"json" : "Json", "structured": "Structured", "regular": ""}
def create_listener_class(a_method, return_format, packager, package_name):
    if return_format == "json":
        listener_args = [("String", "data", "The method that should be overridden to handle the data if the method was successful.")]
    elif return_format == "structured":
        if a_method.output.startswith("list("):
            listener_args = [("ArrayList<Object>", "data", "The method that should be overridden to handle the data if the method was successful.")]
        else:
            listener_args = [("HashMap<String, Object>", "data", "The method that should be overridden to handle the data if the method was successful.")]
    elif return_format == "regular":
        listener_args = [(convert_to_java_type(a_method.output), "data", "The method that should be overridden to handle the data if the method was successful.")]
    # General variables
    method_proper_name = camel_case_caps(a_method.name)
    method_name = camel_case(a_method.name)
    listener_class_name = "{}{}Listener".format(return_format_class_names[return_format], method_proper_name)
    # Listener file for the method
    listener_file = packager(return_format)
    listener_file += _import("java.util.ArrayList") + new_line()
    listener_file += _import("java.util.HashMap") + new_line()
    for dependency in a_method.dependencies:
        listener_file += _import("{}.{}.{}".format(packager.base, "domain", camel_case_caps(dependency))) + new_line()
    listener_file += _class("public", listener_class_name, [], [], [
            method_prototype("public abstract", "void", method_name+"Completed", listener_args),
            method_prototype("public abstract", "void", method_name+"Failed", [("Exception", "error", "The method that should be overridden to handle an exception that occurred while getting the SearchResponse.")])
        ], "interface", description="A listener for the {0} method. On success, passes the data into the {0}Completed method. On failure, passes the exception to the {0}Failed method.".format(method_name))
    return "{}/{}/{}.java".format(package_name,
                                 return_format, 
                                 listener_class_name), listener_file
    
def create_java(spec, local=False):
    """
    Welcome to Hell. This is such an ugly God function. I broke it up into a couple of smaller ones, but honestly there's only so much one can do in this scenario. Honestly, it should have been done with Jinja, but this was only my first attempt, and I didn't expect anyone else to ever look into the source.
    
    Run.
    """
    package_name = "{0}/java/src/realtimeweb/{0}".format(flat_case(spec.name))
    packager = package_generator("realtimeweb", flat_case(spec.name))
    packager.base = "realtimeweb.{}".format(flat_case(spec.name))
    project_name = camel_case_caps(spec.name)
    files = {}
        
    # Client store
    if local:
        temp_loc = 'templates/java'
    else:
        temp_loc = '/Users/acbart/Sites/realtimeweb/flask_application/controllers/templates/java'
    files["{}/json/ClientStore.java".format(package_name)] = static_file(temp_loc+'/json/ClientStore.java', packager("json"))
    
    files["{}/build.xml".format(package_name)] = static_file(temp_loc+'/build.xml') % {"ModuleName": project_name}
    
    # Util stuff
    files["{}/util/PropertyString.java".format(package_name)] = static_file(temp_loc+'/util/PropertyString.java', packager("util"))
    files["{}/cache.json".format(package_name)] = "{}"
    files["{}/util/Util.java".format(package_name)] = static_file(temp_loc+'/util/Util.java', packager("util"))
    for libname in ['commons-codec-1.6', 'commons-logging-1.1.1', 'fluent-hc-4.2.5', 'gson-2.2.4', 'httpclient-4.2.5', 'httpclient-cache-4.2.5', 'httpcore-4.2.4', 'httpmime-4.2.5']:
        files["{0}/java/libs/{1}.jar".format(camel_case_caps(spec.name), libname)] = static_file(temp_loc+'/libs/{}.jar'.format(libname))
    files["{0}/java/.classpath".format(camel_case_caps(spec.name))] = static_file(temp_loc+'/.classpath')
    
    # Abstract service
    abstract_name = "Abstract"+ project_name
    abstract_file = packager("main")
    abstract_file += _class("public", abstract_name, [], [], [
            method_prototype("public", "void", "connect", []),
            method_prototype("public", "void", "disconnect", [])
        ], "interface")
    files["{}/main/{}.java".format(package_name, abstract_name)] = abstract_file
    
        
    # Domain objects
    for a_class in spec.classes:
        name, body = create_domain_class(a_class, packager, package_name)
        files[name] = body
    
    # Service listeners
    for return_format in ("json", "structured", "regular"):
        for a_method in spec.methods:
            name, body = create_listener_class(a_method, return_format, packager, package_name)
            files[name] = body
                                         
    abstract_service_class_name = "Abstract"+project_name
    
    # Json Service class
    json_service_class_name = "Json" + project_name
    json_service_file = packager("json")
    json_service_file += _imports(["{}.main.Abstract".format(packager.base)+project_name, "java.util.HashMap", "{}.util.Util".format(packager.base)]) + new_line()
    service_methods = []
    for a_method in spec.methods:
        query_url, args, indexable_parameters, non_indexable_parameters = generate_service_method(a_method)
        service_methods.append(method(camel_case(a_method.name), "String", args, [
                                    query_url
                                ] + [
                                    "HashMap<String, String> parameters = new HashMap<String, String>();"
                                ] + indexable_parameters + [
                                    _if(attribute("local"), [
                                        _return(invocation("getData", [invocation("hashRequest",["url", "parameters"],"Util")], "clientStore"))
                                    ])
                                ] + non_indexable_parameters + [
                                    """String jsonResponse = "";
try {
    jsonResponse = Util.get(url, parameters);
    if (jsonResponse.startsWith("<")) {
        throw new Exception(jsonResponse);
    }
    return jsonResponse;
} catch (Exception e) {
    throw new Exception(e.toString());
}"""
                                ], modifiers="public", decorators=None, throws=["Exception"], description = a_method.description))
        listener = "Json{}Listener".format(camel_case_caps(a_method.name))
        service_methods.append(method(camel_case(a_method.name), "void", args + [(listener, "callback", "The listener that will be given the data (or error).")], [
                                    """
Thread thread = new Thread() {{
    @Override
    public void run() {{
        try {{
            callback.{}Completed({}.getInstance().{}({}));
        }} catch (Exception e) {{
            callback.{}Failed(e);
        }}
    }}
}};
thread.start();
""".format(camel_case(a_method.name), json_service_class_name, camel_case(a_method.name), ", ".join(zip(*args)[1]), camel_case(a_method.name))
                                ], modifiers = "public", decorators=None, description = a_method.description, arg_modifiers="final "))
    json_service_file += _class("public", json_service_class_name, [
                                abstract_service_class_name
                            ], [], [
                                attribute_definition("private static", json_service_class_name, "instance"),
                                attribute_definition("protected",  "boolean", "local"),
                                attribute_definition("private",  "ClientStore", "clientStore"),
                                method(json_service_class_name, "", [], [
                                        invocation("disconnect", []) +";",
                                        assignment("this.clientStore", instance("ClientStore", []))
                                    ], "protected", description="**For internal use only!** Protected Constructor guards against instantiation."),
                                singleton_constructor(json_service_class_name),
                                method("connect", "void", [], [
                                        assignment(attribute("local"), "false")
                                    ], "public", ["Override"], description="Establishes a connection to the online service. Requires an internet connection."),
                                method("disconnect", "void", [], [
                                        assignment(attribute("local"), "true")
                                    ], "public", ["Override"], description="Establishes that Business Search data should be retrieved locally. This does not require an internet connection.<br><br>If data is being retrieved locally, you must be sure that your parameters match locally stored data. Otherwise, you will get nothing in return."),
                                generate_getter("client Store", "ClientStore", "**For internal use only!** The ClientStore is the internal cache where offline data is stored."),
                                ] + service_methods, description="Used to get data as a raw string."
                            )
    files["{}/json/{}.java".format(package_name,
                                   json_service_class_name)] = json_service_file
                                  
    # Structured Service class
    structured_service_class_name = "Structured" + project_name
    structured_service_file = packager("structured")
    structured_service_file += _imports(["{}.main.Abstract".format(packager.base)+project_name, "{}.util.Util".format(packager.base), "java.util.HashMap", "java.util.LinkedHashMap", "com.google.gson.Gson", "{}.json.Json".format(packager.base)+project_name]+ ["{}.json.Json{}Listener".format(packager.base, camel_case_caps(a_method.name)) for a_method in spec.methods]) + new_line()
    service_methods = []
    for a_method in spec.methods:
        query_url, args, indexable_parameters, non_indexable_parameters = generate_service_method(a_method)
        service_methods.append(method(camel_case(a_method.name), "HashMap<String, Object>", args, [
                                    _return(invocation("fromJson", [
                                        invocation(camel_case(a_method.name),[", ".join(zip(*args)[1])], "jsonInstance"),
                                        ("ArrayList" if a_method.output.startswith("list(") else "LinkedHashMap")+".class"
                                    ], "gson"))
                                ], modifiers="public", decorators=None, throws=["Exception"], description = a_method.description))
        listener = "Structured{}Listener".format(camel_case_caps(a_method.name))
        json_listener = "Json{}Listener".format(camel_case_caps(a_method.name))
        service_methods.append(method(camel_case(a_method.name), "void", args + [("final {}".format(listener), "callback", "The listener that will be given the data (or error)")], [
                                    """
jsonInstance.{0}({1}, new {2}() {{
    @Override
    public void {0}Failed(Exception exception) {{
        callback.{0}Failed(exception);
    }}
    
    @Override
    public void {0}Completed(String data) {{
        callback.{0}Completed(gson.fromJson(data, {3}.class));
    }}
}});
""".format(camel_case(a_method.name), ", ".join(zip(*args)[1]), json_listener, "ArrayList" if a_method.output.startswith("list(") else "LinkedHashMap")
                                ], modifiers = "public", decorators=None, description = a_method.description))
    
    structured_service_file += _class("public", structured_service_class_name, [
                                abstract_service_class_name
                            ], [], [
                                attribute_definition("private static", structured_service_class_name, "instance"),
                                attribute_definition("private", json_service_class_name, "jsonInstance"),
                                attribute_definition("private",  "Gson", "gson"),
                                method(structured_service_class_name, "", [], [
                                        assignment(attribute("jsonInstance"),
                                                   invocation("getInstance", [], json_service_class_name)),
                                        assignment("this.gson", instance("Gson", []))
                                    ], "protected", description="**For internal use only!** Protected Constructor guards against instantiation."),
                                singleton_constructor(structured_service_class_name),
                                method("connect", "void", [], [
                                        invocation("connect", [], "jsonInstance") + ";"
                                    ], "public", ["Override"], description="Establishes a connection to the online service. Requires an internet connection."),
                                method("disconnect", "void", [], [
                                        invocation("disconnect", [], "jsonInstance") + ";"
                                    ], "public", ["Override"], description="Establishes that Business Search data should be retrieved locally. This does not require an internet connection.<br><br>If data is being retrieved locally, you must be sure that your parameters match locally stored data. Otherwise, you will get nothing in return.")
                                ] + service_methods, description="Used to get data as built-in Java objects (HashMap, ArrayList, etc.)."
                            )
    files["{}/structured/{}.java".format(package_name,
                                   structured_service_class_name)] = structured_service_file
                                 
    # Regular Service class
    regular_service_class_name = project_name
    regular_service_file = packager("regular")
    regular_service_file += _imports(["{}.main.Abstract".format(packager.base)+project_name, "{}.json.Json".format(packager.base)+project_name, "{}.util.Util".format(packager.base), "java.util.ArrayList", "java.util.HashMap", "java.util.Map", "com.google.gson.Gson", "com.google.gson.GsonBuilder", "com.google.gson.JsonArray", "com.google.gson.JsonObject", "com.google.gson.JsonParser"] + ["{}.domain.{}".format(packager.base, camel_case_caps(dependency)) for dependency in spec.method_dependencies]+ ["{}.json.Json{}Listener".format(packager.base, camel_case_caps(a_method.name)) for a_method in spec.methods]) + new_line()
    
    service_methods = []
    for a_method in spec.methods:
        query_url, args, indexable_parameters, non_indexable_parameters = generate_service_method(a_method)
        if a_method.output.startswith("list("): 
            response_transform = ["JsonArray allChildren = parser.parse(response).getAsJsonArray();",
                                  "{0} result = new {0}();".format(convert_to_java_type(a_method.output)),
                                  "for (int i = 0; i < allChildren.size(); i += 1) {",
                                  "\tresult.add(new {}(allChildren.get(i).getAsJsonObject(), gson));".format(convert_to_java_type(a_method.output)[10:-1]),
                                  "}",
                                  _return("result")]
        else:
            response_transform = ["JsonObject top = parser.parse(response).getAsJsonObject();",
                                   _return(instance(convert_to_java_type(a_method.output), ["top", "gson"]))]
        service_methods.append(method(camel_case(a_method.name), convert_to_java_type(a_method.output), args, [
                                    assignment("String response", invocation(camel_case(a_method.name), [",".join(zip(*args)[1])], "jsonInstance")),
                                    "JsonParser parser = new JsonParser();"
                                ]+response_transform, modifiers="public", decorators=None, throws=["Exception"], description = a_method.description))
        listener = "{}Listener".format(camel_case_caps(a_method.name))
        service_methods.append(method(camel_case(a_method.name), "void", args + [("final {}".format(listener), "callback", "The listener that will receive the data (or error).")], [
                                    ("""
jsonInstance.{0}({1}, new {2}() {{
    @Override
    public void {0}Failed(Exception exception) {{
        callback.{0}Failed(exception);
    }}
    
    @Override
    public void {0}Completed(String response) {{
        JsonParser parser = new JsonParser();
""" + ("""      JsonArray allChildren = parser.parse(response).getAsJsonArray();
        {3} result = new {3}();
        for (int i = 0; i < allChildren.size(); i += 1) {{
            result.add(new {4}(allChildren.get(i).getAsJsonObject(), gson));
        }}"""
        if a_method.output.startswith("list(") else 
        """JsonObject top = parser.parse(response).getAsJsonObject();
        {3} result = new {3}(top, gson)"""
    ) +
"""
        callback.{0}Completed(result);
    }}
}});
""").format(camel_case(a_method.name), ", ".join(zip(*args)[1]), "Json"+listener, convert_to_java_type(a_method.output), convert_to_java_type(a_method.output)[10:-1])
                                ], modifiers = "public", decorators=None, description = a_method.description))

    regular_service_file += _class("public", regular_service_class_name, [
                                abstract_service_class_name
                            ], [], [
                                attribute_definition("private static", regular_service_class_name, "instance"),
                                attribute_definition("private", json_service_class_name, "jsonInstance"),
                                attribute_definition("private",  "Gson", "gson"),
                                method(regular_service_class_name, "", [], [
                                        assignment(attribute("jsonInstance"),
                                                   invocation("getInstance", [], json_service_class_name)),
                                        assignment("this.gson", instance("Gson", []))
                                    ], "protected", description="**For internal use only!** Protected Constructor guards against instantiation."),
                                singleton_constructor(regular_service_class_name),
                                method("connect", "void", [], [
                                        invocation("connect", [], "jsonInstance")+";"
                                    ], "public", ["Override"], description="Establishes a connection to the online service. Requires an internet connection."),
                                method("disconnect", "void", [], [
                                        invocation("disconnect", [], "jsonInstance")+";"
                                    ], "public", ["Override"], description="Establishes that Business Search data should be retrieved locally. This does not require an internet connection.<br><br>If data is being retrieved locally, you must be sure that your parameters match locally stored data. Otherwise, you will get nothing in return.")
                                ] + service_methods, description="Used to get data as classes."
                            )
    files["{}/regular/{}.java".format(package_name,
                                   regular_service_class_name)] = regular_service_file
    
    return files
    
if __name__ == "__main__":
    import os
    from create_loose_ast import _recursively_convert_unicode_to_str
    for file, body in create_java(create_loose_ast(_recursively_convert_unicode_to_str(json.load(open(sys.argv[1],'r'))))).iteritems():
        #if not os.path.exists(os.path.dirname(file)):
            #os.makedirs(os.path.dirname(file))
        #f = open(file, 'w+')
        #f.write(body)
        #f.close()
        if os.path.basename(file) not in ("ClientStore.java","PropertyString.java", "Util.java") and "domain" not in file and "Listener" not in file:
            print file
            print "~~~" * 10
            print body
            print "~~~" * 10
            