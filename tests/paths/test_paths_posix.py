# -*- coding: utf-8 -*-

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
