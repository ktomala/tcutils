# -*- coding: utf-8 -*-

import logging
import os
import unicodedata
from softtrove.const import VALID_FILENAME_CHARS

log = logging.getLogger(__file__)


def clean_filename(filename, whitelist=VALID_FILENAME_CHARS, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r, '_')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize(
        'NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    return ''.join(c for c in cleaned_filename if c in whitelist)


def check_file_exists_or_increment(filepath):
    number = 1
    if os.path.exists(filepath):
        filepath_root, filepath_ext = os.path.splitext(filepath)
        # FIXME: This is inefficient, should list all files and choose
        #        correct number
        while 1:
            new_filepath_root = filepath_root + '_' + str(number)
            new_filepath = new_filepath_root + filepath_ext
            if os.path.exists(new_filepath):
                number += 1
                continue
            else:
                filepath = new_filepath
                break
    return filepath
