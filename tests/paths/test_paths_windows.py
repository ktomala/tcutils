# -*- coding: utf-8 -*-

import pytest
import pathlib
import sys

from ..context import tcutils


current_user_name = tcutils.user.current_user_name()

WINDOWS_PATHS = [
    ("Users/someuser", "Users\\someuser"),
    ("C:\\Users\\someuser", "C:\\Users\\someuser"),
    ("$WINDIR", "C:\\Windows"),
    ("$HOMEPATH", "C:\\Users\\" + current_user_name),
    ("%HOMEPATH%", "C:\\Users\\" + current_user_name),
    ("$HOMEPATH/AppData/Local/../Roaming/Python",
        "C:\\Users\\" + current_user_name + "\\AppData\\Roaming\\Python"),
]

WINDOWS_PATHS_EXIST = [
    ("%HOMEPATH%", True),
    ("C:\\NotExistingDirectoryOne", False),
]

WINDOWS_PATHS_JOINED = [
    ("\\Users", "\\Windows", "C:\\Windows"),
    ("\\Users", "%HOMEPATH%", "C:\\Users\\Users\\" + current_user_name),
    ("Windows", "%HOMEPATH%", "Windows\\Users\\" + current_user_name),
    ("%HOMEPATH%", "\\Windows", "C:\\Windows"),
    ("%WINDIR%\\System32", "..\\System", "C:\\Windows\\System"),
]


@pytest.mark.skipif(sys.platform != "win32", reason="does not run on posix")
class TestWindowsPaths:

    @pytest.fixture
    def default_expandvars(self):
        return pathlib.ntpath.expandvars

    @pytest.fixture
    def path_type(self):
        return pathlib.WindowsPath

    @pytest.mark.parametrize(
        "path, result", WINDOWS_PATHS
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
        "path, result", WINDOWS_PATHS
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

    @pytest.mark.parametrize(
        "path_one, path_two, result", WINDOWS_PATHS_JOINED
    )
    @pytest.mark.parametrize(
        "use_default_expansion", [True, False]
    )
    def test_join_paths(self, path_one, path_two, result, path_type,
        use_default_expansion, default_expandvars
    ):
        joined_path = tcutils.paths.join_paths(path_one, path_two,
            use_default_expansion=use_default_expansion,
            default_expandvars=default_expandvars)

        assert joined_path == path_type(result)


    @pytest.mark.parametrize(
        "use_default_expansion", [True, False]
    )
    def test_current_dir(self, use_default_expansion, default_expandvars):
        current_dir_path = tcutils.paths.get_current_dir(
            use_default_expansion=use_default_expansion,
            default_expandvars=default_expandvars)
        assert pathlib.Path.cwd() == current_dir_path

    # @pytest.mark.parametrize(
    #     "use_default_expansion", [True, False]
    # )
    # def test_create_dirs(self):
    #         use_default_expansion=use_default_expansion,
    #         default_expandvars=default_expandvars)
    #     pass
