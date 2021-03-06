#!/usr/bin/env python

__author__ = 'Adam R. Smith'
__license__ = 'Apache 2.0'

import collections

class DotDict(dict):
    """
    Subclass of dict that will recursively look up attributes with dot notation.
    This is primarily for working with JSON-style data in a cleaner way like javascript.
    Note that this will instantiate a number of child DotNotationDicts when you first access attributes;
    do not use in performance-critical parts of your code.
    """

    def __getattr__(self, key):
        """ Make attempts to lookup by nonexistent attributes also attempt key lookups. """
        try:
            val = self.__getitem__(key)
            if isinstance(val, dict) and not isinstance(val, DotDict):
                self[key] = val = DotDict(val)
        except KeyError:
            raise AttributeError(key)

        return val

    def copy(self):
        return DotDict(dict.copy(self))

    @classmethod
    def fromkeys(cls, seq, value=None):
        return DotDict(dict.fromkeys(seq, value))


# dict_merge from: http://appdelegateinc.com/blog/2011/01/12/merge-deeply-nested-dicts-in-python/

def quacks_like_dict(object):
    """Check if object is dict-like"""
    return isinstance(object, collections.Mapping)

def dict_merge(a, b):
    """Merge two deep dicts non-destructively

    Uses a stack to avoid maximum recursion depth exceptions

    >>> a = {'a': 1, 'b': {1: 1, 2: 2}, 'd': 6}
    >>> b = {'c': 3, 'b': {2: 7}, 'd': {'z': [1, 2, 3]}}
    >>> c = merge(a, b)
    >>> from pprint import pprint; pprint(c)
    {'a': 1, 'b': {1: 1, 2: 7}, 'c': 3, 'd': {'z': [1, 2, 3]}}
    """
    assert quacks_like_dict(a), quacks_like_dict(b)
    dst = a.copy()

    stack = [(dst, b)]
    while stack:
        current_dst, current_src = stack.pop()
        for key in current_src:
            if key not in current_dst:
                current_dst[key] = current_src[key]
            else:
                if quacks_like_dict(current_src[key]) and quacks_like_dict(current_dst[key]) :
                    stack.append((current_dst[key], current_src[key]))
                else:
                    current_dst[key] = current_src[key]
    return dst

if __name__ == '__main__':
    dd = DotDict({'a':{'b':{'c':1, 'd':2}}})
    print dd.a.b.c, dd.a.b.d
    print dd.a.b
    #print dd.foo

    print dict.fromkeys(('a','b','c'), 'foo')
    print DotDict.fromkeys(('a','b','c'), 'foo').a