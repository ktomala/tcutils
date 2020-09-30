# -*- coding: utf-8 -*-

import logging
import os
import unicodedata
import pathlib
from tcutils.const import VALID_FILENAME_CHARS, DEFAULT_REPLACEMENT_CHAR
from tcutils.types import CharsList, UniversalPath, KeywordArgsType
from tcutils.paths import normalize_path

log = logging.getLogger(__file__)


def clean_filename(
    filename: str,
    whitelist: CharsList = VALID_FILENAME_CHARS,
    replace: CharsList = ' ',
    replacement: str = DEFAULT_REPLACEMENT_CHAR
) -> str:
    """Cleans filename according to `whitelist` characters and `replace`
    characters which will be substituted by `replacement` character.
    """
    # Replace spaces (or characters defined by replace)
    for r in replace:
        filename = filename.replace(r, replacement)

    # Keep only valid ASCII chars
    cleaned_filename = unicodedata.normalize(
        'NFKD', filename).encode('ASCII', 'ignore').decode()

    # Keep only whitelisted chars
    return ''.join(c for c in cleaned_filename if c in whitelist)
