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


current_user_name = tcutils.user.current_user_name()

POSIX_PATHS = [
    ("/home/someuser", "/home/someuser", pathlib.PosixPath),
    ("$HOME", "/home/" + current_user_name, pathlib.PosixPath),
    ("/usr/lib/python/../../bin/python", "/usr/bin/python", pathlib.PosixPath),
]

@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
class TestPosixPaths:

    @pytest.fixture
    def default_expandvars(self):
        return pathlib.posixpath.expandvars

    @pytest.mark.parametrize(
        "path, result, path_type", POSIX_PATHS
    )
    @pytest.mark.parametrize(
        "use_default_expansion", [True, False]
    )
    def test_normalize_path(self, path, result, path_type,
        use_default_expansion, default_expandvars
    ):
        normalized_path = tcutils.paths.normalize_path(path,
            use_default_expansion, default_expandvars)
        assert normalized_path == path_type(result)

    def test_temp_system_dir_path(self):
        temp_dir = tcutils.paths.temp_system_dir_path()
        assert pathlib.Path('/tmp') == temp_dir
