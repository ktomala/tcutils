# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import types
import typing

from tcutils.const import CLASS_METHOD_TYPES

def class_methods(
    cls: typing.Any,
    method_types: typing.Iterable[typing.Type] = CLASS_METHOD_TYPES
) -> typing.List[str]:
    """Return list of methods from the class.
    """
    return [name for name, kind in cls.__dict__.items() \
            if type(kind) in method_types]


def class_prefixed_methods(cls: typing.Any, prefix: str) -> typing.List[str]:
    """Return list of methods in a class that start with prefix.
    """
    methods = class_methods(cls)
    return list(filter(lambda x: x.startswith(prefix), methods))
