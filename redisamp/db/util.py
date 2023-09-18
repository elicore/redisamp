# def is_array_response(response: list) -> bool:
#     return isinstance(list, response) \
#         and len(response) > 0 and len(response) % 2 == 0 \
#         and all([
#             not (isinstance(x, list) or (isinstance(x, dict)))
#             for x in response
#             ])

def array_response_to_dict(response: list, skip_conversion_keys: list[str] | None = None) -> dict:
    """
    Converts a list response to a dictionary.

    This function takes a list of key-value pairs and converts it into a dictionary.
    If a value is a list of key-value pairs, it is recursively converted to a dictionary.
    Keys that are in the skip_conversion_keys list are included in the resulting dictionary, 
    but their corresponding values are not recursively converted to dictionaries.

    Parameters:
    response (list): The list of key-value pairs to convert.
    skip_conversion_keys (list[str] | None): A list of keys to skip recursive conversion for (default None).

    Returns:
    dict: The converted dictionary.

    Examples:
    >>> array_response_to_dict(['key1', 'value1', 'key2', ['key3', 'value3']])
    {'key1': 'value1', 'key2': {'key3': 'value3'}}

    >>> array_response_to_dict(['key1', 'value1', 'key2', ['key3', 'value3']], skip_conversion_keys=['key2'])
    {'key1': 'value1', 'key2': ['key3', 'value3']}
    """
    res = {}
    skip_conversion_keys = skip_conversion_keys or []
    for i in range(0, len(response), 2):
        k = response[i]
        v = response[i + 1]
        if k not in skip_conversion_keys \
            and isinstance(v, list) \
            and len(v) > 0 and len(v) % 2 == 0:
            v = array_response_to_dict(v)
        res[k] = v
    return res
