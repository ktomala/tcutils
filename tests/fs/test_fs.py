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

POSIX_PERM_TRIAD_TEST = [
    (False, False, False, 0x0),
    (False, False, True, 0x1),
    (False, True, False, 0x2),
    (True, False, False, 0x4),
    (False, True, True, 0x3),
    (True, False, True, 0x5),
    (True, True, False, 0x6),
    (True, True, True, 0x7),
]
POSIX_PERM_TRIAD_TEST_STR = [
    ('0', 0x0),
    ('1', 0x1),
    ('2', 0x2),
    ('4', 0x4),
    ('3', 0x3),
    ('5', 0x5),
    ('6', 0x6),
    ('7', 0x7),
]
POSIX_PERM_TEST_STR = [
    ('000', '0000'),
    ('100', '0100'),
    ('010', '0010'),
    ('001', '0001'),
    ('775', '0775'),
    ('644', '0644'),
    ('1775', '1775'),
    ('640', '0640'),
    ('700', '0700'),
    ('1777', '1777'),
]


class TestFS:

    @pytest.fixture
    def default_expandvars(self):
        return pathlib.ntpath.expandvars if sys.platform == 'win32' else \
            pathlib.posixpath.expandvars

    @pytest.mark.parametrize(
        "read, write, execute, octet", POSIX_PERM_TRIAD_TEST
    )
    def test_posix_perm_triad(self, read, write, execute, octet):
        triad = tcutils.fs.PosixPermissionTriad(
            read=read, write=write, execute=execute)
        assert octet == triad.to_octal()

    @pytest.mark.parametrize(
        "input_str, octet", POSIX_PERM_TRIAD_TEST_STR
    )
    def test_posix_perm_triad_from_str(self, input_str, octet):
        triad = tcutils.fs.PosixPermissionTriad.from_octal(input_str)
        assert octet == triad.to_octal()

    @pytest.mark.parametrize(
        "input_str, octet", POSIX_PERM_TEST_STR
    )
    def test_posix_perm(self, input_str, octet):
        perm = tcutils.fs.PosixPermissions.from_octal(input_str)
        assert octet == perm.to_octal_str()

    @pytest.mark.parametrize(
        "input_str, octet", POSIX_PERM_TEST_STR
    )
    def test_posix_perm_to_octal(self, input_str, octet):
        perm = tcutils.fs.PosixPermissions.from_octal(input_str)
        assert int(octet, 8) == perm.to_octal()

    @pytest.mark.parametrize(
        "filename, whitelist, replace, replacement, result", FS_CLEAN_FILENAMES
    )
    def test_clean_filename(self, filename, whitelist, replace, replacement,
        result
    ):
        cleaned_filename = tcutils.fs.clean_filename(
            filename, whitelist, replace, replacement)
        assert cleaned_filename == result
