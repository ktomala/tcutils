# -*- coding: utf-8 -*-

import string
import types


VALID_FILENAME_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)
DEFAULT_REPLACEMENT_CHAR = '_'

CLASS_METHOD_TYPES = [types.FunctionType, classmethod, staticmethod]

DEFAULT_URI_SCHEME = 'file'
