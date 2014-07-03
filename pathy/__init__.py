import collections


def deep_update(d, u, depth=-1):
    """
    Recursively merge or update dict-like objects.
    >>> deep_update({'k1': {'k2': 2}}, {'k1': {'k2': {'k3': 3}}, 'k4': 4})
    {'k1': {'k2': {'k3': 3}}, 'k4': 4}
    """

    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping) and not depth == 0:
            r = deep_update(d.get(k, {}), v, depth=max(depth - 1, -1))
            d[k] = r
        elif isinstance(d, collections.Mapping):
            d[k] = u[k]
        else:
            d = {k: u[k]}
    return d


def flatten_dict(_dict, lkey=''):
    """Flattens a nested dict

    >>> flatten_dict({'a': {'b': {'c': 5}}, 'd': None})
    {'a.b.c': 5, 'a.d': None}

    :param _dict: the dict to flatten
    :type _dict: dict
    :returns: a flattened dict
    :rtype: dict
    """
    ret = {}
    for rkey, val in _dict.items():
        key = lkey + rkey
        if isinstance(val, dict):
            ret.update(flatten_dict(val, key + '.'))
        else:
            ret[key] = val
    return ret


def deepen_dict(_dict, split_key='.'):
    """Deepens a flat dict by splitting its key

    >>> deepen_dict({"a.b.c": 1, "a.b.d": 2})
    {'a': {'b': {'c': 1, 'd': 2}}}

    :param _dict: the flat dict to transform
    :type _dict: dict
    :param split_key: separator of dict path, defaults to `.`
    :type split_key: str
    :returns: a deepened dict
    :rtype: dict
    """
    deep = {}
    for k, v in _dict.iteritems():
        deep_update(deep, reduce(lambda x, y: {y: x},
                                 reversed(k.split(split_key) + [v])))
    return deep


def get_from_path(path, _dict):
    """Get the corresponding sub-dict or value from a dict by a
    dot separated path

        For example, _dict = {'a': {'b': {'c': 1}}} called with
        path 'a.b.c' will return the value 1. With path 'a.b' will
        return the sub dict {'c': 1}

    >>> get_from_path('a.b.c', {'a': {'b': {'c'}}})
    1
    >>> get_from_path('a.b', {'a': {'b': {'c'}}})
    {'c': 1}

    :param path: a valid dot separated path
    :type path: str
    :returns: sub dict or value
    """
    return reduce(lambda d, key: d[key], path.split('.'), _dict)


def path_in_dict(path, _dict):
    """Check whether a path is valid in a dict

    :param path: dot separated path to check
    """
    res = True
    try:
        get_from_path(path, _dict)
    except KeyError:
        res = False
    return res


def update_path_in_dict(path, value, _dict):
    keys = path.split('.')
    _len = len(keys)
    current = _dict
    for i in xrange(0, _len):
        key = keys[i]
        if i is _len - 1:
            # override existing value
            # create non-existing value
            current[key] = value
        else:
            if key in current:
                _next = current[key]
                if isinstance(_next, dict):
                    current = _next
                else:
                    _next = {}
                    current = _next
            else:
                current[key] = {}
                current = current[key]


def update_dict(dict_to_update, update):
    """Merge an update dict in a non-overridden way"""
    for item in flatten_dict(update).iteritems():
        path, value = item
        update_path_in_dict(path, value, dict_to_update)


# TODO extract dict path traversal part
def delete_path_in_dict(path, _dict):
    """Delete an element in the dict by its complete path

    Note that this function does nothing if the path does not exists

    :param path: the complete path to the element to delete
        eg. `top.sub.element`
    :param _dict: the dictionary to operate on
    """
    keys = path.split('.')
    _len = len(keys)
    current = _dict
    for i in xrange(0, _len):
        key = keys[i]
        if i is _len - 1:
            # override existing value
            # create non-existing value
            if key in current:
                current.pop(key)
        else:
            if key in current:
                _next = current[key]
                if isinstance(_next, dict):
                    current = _next
                else:
                    _next = {}
                    current = _next
            else:
                return


# TODO benchmark needed
def clean_dict(_dict, fields_to_clean=(None, [], {})):
    """Remove `empty` keys in the dict

    :param _dict: the dict to clean
    :param fields_to_clean: `empty` values, defaults to
        `None`, `[]` and `{}`
    """
    def _recursive_clean(doc, access):
        for k, v in doc.items():
            if isinstance(v, dict):
                if len(v) == 0:
                    del(access[k])
                else:
                    _recursive_clean(v, doc[k])
            elif v in fields_to_clean:
                del(access[k])
    _recursive_clean(_dict, _dict)