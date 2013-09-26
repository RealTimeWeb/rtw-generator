def clean_json(input):
    if isinstance(input, dict):
        return {clean_json(key): clean_json(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [clean_json(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input