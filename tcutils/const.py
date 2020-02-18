# -*- coding: utf-8 -*-

import string

VALID_FILENAME_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)
DEFAULT_REPLACEMENT_CHAR = '_'
