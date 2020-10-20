# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

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
    (False, False, False, 0o0),
    (False, False, True, 0o1),
    (False, True, False, 0o2),
    (True, False, False, 0o4),
    (False, True, True, 0o3),
    (True, False, True, 0o5),
    (True, True, False, 0o6),
    (True, True, True, 0o7),
]
POSIX_PERM_TRIAD_TEST_STR = [
    ('0', 0o0),
    ('1', 0o1),
    ('2', 0o2),
    ('4', 0o4),
    ('3', 0o3),
    ('5', 0o5),
    ('6', 0o6),
    ('7', 0o7),
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
POSIX_PERM_TEST_STAT = [
    (33152, '0600'),
    (33700, '1644'),
    (32876, '0154'),
]
POSIX_PERM_TEST_OCTET = [
    '0600',
    '0640',
    '0644',
    '0750',
    '1755',
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
        "stat_mode, octet", POSIX_PERM_TEST_STAT
    )
    def test_posix_perm_stat(self, stat_mode, octet):
        perm = tcutils.fs.PosixPermissions.from_stat(stat_mode)
        assert octet == perm.to_octal_str()

    @pytest.mark.parametrize(
        "octet", POSIX_PERM_TEST_OCTET
    )
    def test_posix_perm_apply_file(self, octet):
        temp_file = tcutils.fs.temp_file()
        temp_file_path = pathlib.Path(temp_file.name)
        perm = tcutils.fs.PosixPermissions.from_octal(octet)
        perm.apply(temp_file_path)
        temp_file_perms = oct(temp_file_path.stat().st_mode)[-4:]
        assert temp_file_perms == perm.to_octal_str()

    @pytest.mark.parametrize(
        "filename, whitelist, replace, replacement, result", FS_CLEAN_FILENAMES
    )
    def test_clean_filename(self, filename, whitelist, replace, replacement,
        result
    ):
        cleaned_filename = tcutils.fs.clean_filename(
            filename, whitelist, replace, replacement)
        assert cleaned_filename == result
