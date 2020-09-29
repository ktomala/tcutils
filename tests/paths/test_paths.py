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

WINDOWS_PATHS = [
    ("Users/someuser", "Users\\someuser", pathlib.WindowsPath),
    ("C:\\Users\\someuser", "C:\\Users\\someuser", pathlib.WindowsPath),
    ("$WINDIR", "C:\\Windows", pathlib.WindowsPath),
    ("$HOMEPATH", "C:\\Users\\" + current_user_name, pathlib.WindowsPath),
    ("%HOMEPATH%", "C:\\Users\\" + current_user_name, pathlib.WindowsPath),
    ("$HOMEPATH/AppData/Local/../Roaming/Python",
    "C:\\Users\\" + current_user_name + "\\AppData\\Roaming\\Python",
    pathlib.WindowsPath),
]

WINDOWS_PATHS_EXIST = [
    ("%HOMEPATH%", True),
    ("C:\\NotExistingDirectoryOne", False),
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
        use_default_expansion
    ):
        normalized_path = tcutils.paths.normalize_path(path,
            use_default_expansion, default_expandvars)
        assert normalized_path == path_type(result)


@pytest.mark.skipif(sys.platform != "win32", reason="does not run on posix")
class TestWindowsPaths:

    @pytest.fixture
    def default_expandvars(self):
        return pathlib.ntpath.expandvars

    @pytest.mark.parametrize(
        "path, result, path_type", WINDOWS_PATHS
    )
    @pytest.mark.parametrize(
        "use_default_expansion", [True, False]
    )
    def test_normalize_path(self, path, result, path_type,
        use_default_expansion, default_expandvars
    ):
        normalized_path = tcutils.paths.normalize_path(
            path, use_default_expansion,
            default_expandvars)
        assert normalized_path == path_type(result)

    @pytest.mark.parametrize(
        "path, result, path_type", WINDOWS_PATHS
    )
    @pytest.mark.parametrize(
        "use_default_expansion", [True, False]
    )
    def test_get_path(self, path, result, path_type,
        use_default_expansion, default_expandvars
    ):
        normalized_path = tcutils.paths.get_path(
            path, use_default_expansion=use_default_expansion,
            default_expandvars=default_expandvars)
        assert normalized_path == path_type(result)

    @pytest.mark.parametrize(
        "path, path_exists", WINDOWS_PATHS_EXIST
    )
    @pytest.mark.parametrize(
        "use_default_expansion", [True, False]
    )
    def test_check_path(self, path, path_exists,
        use_default_expansion, default_expandvars
    ):
        try:
            result = tcutils.paths.check_path(path,
            use_default_expansion=use_default_expansion,
            default_expandvars=default_expandvars)
        except IOError as e:
            if not path_exists:
                return True
            else:
                raise e
