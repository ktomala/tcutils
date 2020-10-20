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

WINDOWS_PATHS_CREATE = [
    (("tcutils-tests",), "%TEMP%", False),
    (("tcutils-tests/one", "tcutils-tests/two", "tcutils-tests/three"), "%TEMP%", False),
    (("tcutils-tests-2/one/two", "tcutils-tests/one/three",), "%TEMP%", False),
    (("tcutils-tests/two/one", "tcutils-tests/one/three",),
    "%TEMP%\\tcutils-tests-3", True),
]

WINDOWS_CHECK_FILE_INCREMENT = [
    ("%WINDIR%\\System32\\drivers\\etc\\hosts", "C:\\Windows\\System32\\drivers\\etc\\hosts_1"),
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
        current_dir_path = tcutils.paths.current_dir(
            use_default_expansion=use_default_expansion,
            default_expandvars=default_expandvars)
        assert pathlib.Path.cwd() == current_dir_path


    @pytest.mark.parametrize(
        "dirs_to_create, parent_dir, create_parent", WINDOWS_PATHS_CREATE
    )
    @pytest.mark.parametrize(
        "use_default_expansion", [True, False]
    )
    def test_create_dirs(self, dirs_to_create, parent_dir, create_parent,
        use_default_expansion, default_expandvars
    ):
        created_paths = tcutils.paths.create_dirs(dirs_to_create,
            parent_dir, create_parent,
            use_default_expansion=use_default_expansion,
            default_expandvars=default_expandvars)
        parent_path = tcutils.paths.check_path(parent_dir)
        result_paths = [parent_path / x for x in dirs_to_create]
        if create_parent:
            result_paths.insert(0, parent_path)
        try:
            assert created_paths == result_paths
        finally:
            result_paths.sort()
            # Cleanup
            for result_path in result_paths:
                try:
                    result_path.rmdir()
                except IOError:
                    pass


    @pytest.mark.parametrize(
        "filepath, result", WINDOWS_CHECK_FILE_INCREMENT
    )
    @pytest.mark.parametrize(
        "use_default_expansion", [True, False]
    )
    def test_check_file_exists_or_increment(self, filepath, result,
        use_default_expansion, default_expandvars
    ):
        new_filepath = tcutils.paths.check_file_exists_or_increment(filepath,
            use_default_expansion=use_default_expansion,
            default_expandvars=default_expandvars)
        assert new_filepath == pathlib.WindowsPath(result)

    def test_temp_system_dir_path(self):
        temp_dir = tcutils.paths.temp_system_dir_path()
        assert normalize_path('%TEMP%') == temp_dir
