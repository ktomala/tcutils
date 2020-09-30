# -*- coding: utf-8 -*-

import pytest
import pathlib
import sys

from ..context import tcutils

FS_CLEAN_FILENAMES = [
    ('normal_file.txt', tcutils.const.VALID_FILENAME_CHARS, ' ',
    tcutils.const.DEFAULT_REPLACEMENT_CHAR, 'normal_file.txt'),
    ('spaced file.txt', tcutils.const.VALID_FILENAME_CHARS, ' ',
    tcutils.const.DEFAULT_REPLACEMENT_CHAR, 'spaced_file.txt'),
    ('On€ Unicódę File', tcutils.const.VALID_FILENAME_CHARS, ' ',
    tcutils.const.DEFAULT_REPLACEMENT_CHAR, 'On_Unicode_File'),
    ('abc(12).tar.gz', tcutils.const.VALID_FILENAME_CHARS, ' ',
    tcutils.const.DEFAULT_REPLACEMENT_CHAR, 'abc(12).tar.gz'),
    ('test-file@ bla.!something', tcutils.const.VALID_FILENAME_CHARS, ' @!',
    tcutils.const.DEFAULT_REPLACEMENT_CHAR, 'test-file__bla._something'),
]

class TestFS:

    @pytest.fixture
    def default_expandvars(self):
        return pathlib.ntpath.expandvars if sys.platform == 'win32' else \
            pathlib.posixpath.expandvars

    @pytest.mark.parametrize(
        "filename, whitelist, replace, replacement, result", FS_CLEAN_FILENAMES
    )
    def test_clean_filename(self, filename, whitelist, replace, replacement,
        result
    ):
        cleaned_filename = tcutils.fs.clean_filename(
            filename, whitelist, replace, replacement)
        assert cleaned_filename == result
