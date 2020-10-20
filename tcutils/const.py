# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

import string
import types


VALID_FILENAME_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)
DEFAULT_REPLACEMENT_CHAR = '_'

CLASS_METHOD_TYPES = [types.FunctionType, classmethod, staticmethod]

DEFAULT_URI_SCHEME = 'file'

DEFAULT_ADAPTER_METHOD = 'execute'
