# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2021 TropiCoders Karol Tomala
#

from tcutils.types import *


def object_vars(obj: typing.Any) -> typing.List[str]:
    """Get all object variables that do not start with underscore '_'
    and are not callable.
    """
    properties = dir(obj)
    non_callable = [property_name for property_name in properties if not (
        callable(getattr(obj, property_name)) or property_name.startswith('_'))]
    return non_callable
