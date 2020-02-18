# -*- coding: utf-8 -*-

import types
import typing


def class_methods(cls: typing.Any) -> typing.List(str):
    """Return list of methods from the class.
    """
    return [name for name, kind in cls.__dict__.items() \
            if type(kind) == types.FunctionType]


def class_prefixed_methods(cls: typing.Any, prefix: str) -> typing.List(str):
    """Return list of methods in a class that start with prefix.
    """
    methods = class_methods(cls)
    return list(filter(lambda x: x.startswith(prefix), methods))
