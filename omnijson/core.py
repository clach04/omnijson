# -*- coding: utf-8 -*-

"""
omijson.core
~~~~~~~~~~~~

This module provides the core omnijson functionality.

"""

import sys

engine = None
_engine = None


options = [
    # [library, deserializer from string function name, serializer to string function name, expected exceptions]

    # can't make this work ['com.xhaus.jyson_from_JysonCodec', 'loads', 'dumps', (ValueError,)],  # https://opensource.xhaus.com/projects/jyson/wiki/JysonEncoding
    # unclear how to materialize jyson exception JSONDecodeError - table uses actual exception not a name
    ['com.xhaus.jyson.JysonCodec', 'xhaus.jyson.JysonCodec.loads', 'xhaus.jyson.JysonCodec.dumps', (ValueError,)],  # https://opensource.xhaus.com/projects/jyson/wiki/JysonEncoding
    ['ujson', 'loads', 'dumps', (ValueError,)],
    ['yajl', 'loads', 'dumps', (TypeError, ValueError)],
    ['jsonlib2', 'read', 'write', (ValueError,)],
    ['jsonlib', 'read', 'write', (ValueError,)],
    ['simplejson', 'loads', 'dumps', (TypeError, ValueError)],
    ['json', 'loads', 'dumps', (TypeError, ValueError)],
    ['simplejson_from_packages', 'loads', 'dumps', (ValueError,)],
]


def _import(engine):
    try:
        if '_from_' in engine:
            engine, package = engine.split('_from_')
            m = __import__(package, globals(), locals(), [engine], 0)
            return getattr(m, engine)

        return __import__(engine)

    except ImportError:
        return False


def loads(s, **kwargs):
    """Loads JSON object."""

    try:
        return _engine[0](s, **kwargs)

    except _engine[2]:
        # except_clause: 'except' [test ['as' NAME]]  # grammar for py3x
        # except_clause: 'except' [test [('as' | ',') test]] # grammar for py2x
        why = sys.exc_info()[1]
        raise JSONError(why)


def dumps(o, **kwargs):
    """Dumps JSON object."""

    try:
        return _engine[1](o, **kwargs)

    except:
        ExceptionClass, why = sys.exc_info()[:2]

        if any([(issubclass(ExceptionClass, e)) for e in _engine[2]]):
            raise JSONError(why)
        else:
            raise why


class JSONError(ValueError):
    """JSON Failed."""


# ------
# Magic!
# ------

def _my_getattr(module_obj, name):
    if '.' not in name:
        return getattr(module_obj, name)

    """so far this is just for Jython in Java with jyson
        >>> getattr(x, 'jyson.JysonCodec.loads')
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        AttributeError: 'javapackage' object has no attribute 'xhaus.jyson.JysonCodec.loads'

    Versus:

        getattr(getattr(getattr(x, 'xhaus'), 'jyson'), 'JysonCodec')
    """
    result = module_obj
    for name_part in name.split('.'):
        result = getattr(result, name_part)
    return result


for e in options:

    __engine = _import(e[0])

    if __engine:
        engine, _engine = e[0], e[1:4]

        for i in (0, 1):
            _engine[i] = _my_getattr(__engine, _engine[i])

        break
