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
    whitelist: CharsList=VALID_FILENAME_CHARS,
    replace: CharsList=' ',
    replacement: str=DEFAULT_REPLACEMENT_CHAR
) -> str:
    """Cleans filename according to `whitelist` characters and `replace`
    characters which will be substituted by `replacement` character.
    """
    # Replace spaces (or characters defined by replace)
    for r in replace:
        filename = filename.replace(r, '_')

    # Keep only valid ASCII chars
    cleaned_filename = unicodedata.normalize(
        'NFKD', filename).encode('ASCII', 'ignore').decode()

    # Keep only whitelisted chars
    return ''.join(c for c in cleaned_filename if c in whitelist)


def check_file_exists_or_increment(
    filepath: UniversalPath,
    **normalize_kwargs: KeywordArgsType
) -> pathlib.Path:
    """Return file path with incremented suffix, if `filepath` already exists.
    Will search for first available number suffix, if previous ones are already
    existing, e.g. `FILENAME_1.EXTENSION`.
    """
    number = 1
    temp_path = normalize_path(filepath)
    if temp_path.exists():
        filepath_root, filepath_ext = temp_path.splitext()
        # FIXME: This is inefficient, should list all files and choose
        #        correct number
        while 1:
            new_filepath_root = filepath_root + '_' + str(number)
            new_filepath = pathlib.Path(new_filepath_root + filepath_ext)
            if new_filepath.exists():
                number += 1
                continue
            else:
                filepath = new_filepath
                break
    return filepath
