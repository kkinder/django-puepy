"""JSON+Datetime/Timespan serialization.

This module wraps the built-in Python `json` library but provides additional logic by supporting datetimes and
timespans using special notation.

Example Usage::

    >>> import dtjson
    >>> import datetime
    >>> serialized = dtjson.dumps(['foo', {'bar': ('baz', None, 1.0, 2), 'spam': datetime.datetime.now()}])
    >>> print(serialized)
    '["foo", {"bar": ["baz", null, 1.0, 2], "spam": {"__type__": "datetime", "isoformat": "2024-05-25T14:23:36.769090"}}]'
    >>> unserialized = dtjson.loads(serialized)
    >>> print(unserialized)
    ['foo', {'bar': ['baz', None, 1.0, 2], 'spam': datetime.datetime(2024, 5, 25, 14, 23, 36, 769090)}]

Timespans are also similarly support. The interface for using dtjson is nearly identical to the json module, and can be
generally used as a replacement.
"""
import json
import datetime


def dump(obj, fp, *args, **kwargs):
    """Serialize ``obj`` as a JSON formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object). This uses the dtjson
    simplification for datetime/timespan objects.

    Additional arguments and keyword arguments are passed through to the underlying json.dump function.

    """
    json.dump(_simplify(obj), fp, *args, **kwargs)


def dumps(obj, *args, **kwargs):
    """
    Serialize ``obj`` to a JSON formatted ``str``. This uses the dtjson
    simplification for datetime/timespan objects.

    Additional arguments and keyword arguments are passed through to the underlying json.dumps function.
    """
    return json.dumps(_simplify(obj), *args, **kwargs)


def load(fp, *args, **kwargs):
    """
    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing a JSON document) to a Python object. This
    uses the dtjson simplification for datetime/timespan objects.

    Additional arguments and keyword arguments are passed through to the underlying json.load function.
    """
    return _complicate(json.load(fp, *args, **kwargs))


def loads(s, *args, **kwargs):
    """Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance containing a JSON document) to a Python
    object. This uses the dtjson simplification for datetime/timespan objects.

    Additional arguments and keyword arguments are passed through to the underlying json.loads function.
    """
    return _complicate(json.loads(s, *args, **kwargs))


def _simplify(data):
    """ """
    if isinstance(data, datetime.datetime):
        return {
            "__type__": "datetime",
            "isoformat": data.isoformat(),
        }
    elif isinstance(data, datetime.timedelta):
        return {
            "__type__": "timedelta",
            "seconds": data.total_seconds(),
        }
    elif isinstance(data, dict):
        return {key: _simplify(value) for key, value in data.items()}
    elif isinstance(data, (list, tuple, set)):
        return [_simplify(item) for item in data]
    else:
        return data


def _complicate(data):
    """ """
    if isinstance(data, dict):
        if data.get("__type__") == "datetime" and set(data.keys()) == {
            "__type__",
            "isoformat",
        }:
            return datetime.datetime.fromisoformat(data["isoformat"])
        elif data.get("__type__") == "timedelta" and set(data.keys()) == {
            "__type__",
            "seconds",
        }:
            return datetime.timedelta(seconds=data["seconds"])
        else:
            return {key: _complicate(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [_complicate(item) for item in data]
    else:
        return data
