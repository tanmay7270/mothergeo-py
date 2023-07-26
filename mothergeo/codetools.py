#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: mothergeo.codetools
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Helpful utilities from mother.
"""

from collections import namedtuple
from enum import Enum
from itertools import tee
from insensitive_dict import CaseInsensitiveDict
from typing import Iterator


class TryGetResult(namedtuple('TryResult', ['result', 'value'])):
    """
    This is a named tuple that contains a ``bool`` result that indicates success or failure of a "try-get" operation,
    and the value retrieved.
    """


class Enums(object):
    """
    This is a utility class that wants to help you work with :py:class:`Enum` types.
    """
    _names2members = {}  #: An index of enumeration member values indexed first by class, then by member name.

    @staticmethod
    def from_name(enum_cls, name: str) -> Enum:
        """
        Get an enumeration member value from its name.
        
        :param enum_cls: the :py:class:`Enum` ``class``
        :type enum_cls:  ``class``
        :param name: the enumeration member's name
        :type name:  ``str``
        :return: the enumeration member
        :rtype:  :py:class:`Enum`
        """
        # Benign forgiveness:  If we were actually passed a value from the enumeration instead of its name...
        if isinstance(name, enum_cls):
            # ...that's OK.  Just return the enumeration value.
            return name
        # Make sure we're dealing with an Enum type.
        if not issubclass(enum_cls, Enum):
            raise ValueError('enum_class must be of type {typ}'.format(typ=type(Enum)))
        # Now let's get a reference to the index of symbols to their enumeration members.
        symbols2members = None
        # It's possible we haven't see this type before, so we may not have the index on file.
        try:
            symbols2members = Enums._names2members[enum_cls]
        except KeyError:  # This is all right.  It should only happen the first time.
            pass
        # If we haven't already done so...
        if symbols2members is None:
            # ...now's the time to create the index of symbols to the member names.
            symbols2members = CaseInsensitiveDict(dict(enum_cls.__members__.items()))
            # Now save the collection we just created for next time.
            Enums._names2members[enum_cls] = symbols2members
        # Return the enumeration member indexed to the symbol that was passed in.
        return symbols2members[name]


class Dicts(object):
    """
    This is a utility class that wants to help you work with ``dict`` types.
    """
    @staticmethod
    def try_get(obj: dict, key: str, default=None) -> TryGetResult:
        """
        Try to retrieve a value from a :py:class:`dict` that may, or may not be present.
        
        :param obj: the object that defines the value
        :type obj:  ``dict``
        :param key: the key whose value you want
        :type key:  ``str``
        :param default: the value that will be returned if no value is defined for the key
        :return: a named tuple that indicates whether or not the key was defined, and the value
        :rtype:  :py:class:`TryGetResult`
        """
        if obj is None or key not in obj:  # Sanity check.
            return TryGetResult(False, default)
        else:  # If the key is defined...
            # ...just return the value.
            return TryGetResult(True, obj[key])


class Iters(object):
    """
    This is a utility class that wnats to help you work with iterators.
    """
    @staticmethod
    def count(it: Iterator) -> int:
        """
        Get the number of items in an iterator.

        :param it: the iterator
        :type it:  ``iter``
        :return: the number of items in the iterator
        :rtype:  ``int``
        """
        # Use the tee function to make a copy of the iterator (so we don't exhaust the original iterator).
        t = tee(it, 1)[0]
        # So, this is one way to get the count...
        return sum(1 for _ in t)

    @staticmethod
    def get_item_at(it: Iterator, index: int):
        """
        Get the item at a given index from an iterator.

        :param it: the iterator
        :type it:  ``iter``
        :param index: the index of the item you want
        :type index:  ``int``
        :return:  the item at the specified index
        """
        # Use the tee function to make a copy of the iterator (so we don't exhaust the original iterator).
        t = tee(it, 1)[0]
        # Use the copy to create a list and get the item.
        return list(t)[index]


