# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

import pathlib
import os
import sys
import typing
import tempfile
from tcutils.types import UniversalPath, UniversalPathCollection, \
    KeywordArgsType


if sys.platform == 'win32':
    DEFAULT_EXPANDVARS = pathlib.ntpath.expandvars
else:
    DEFAULT_EXPANDVARS = pathlib.posixpath.expandvars


# Path functions


def normalize_path(
   path: UniversalPath,
   use_default_expansion: bool = False,
   default_expandvars: typing.Callable = DEFAULT_EXPANDVARS
) -> pathlib.Path:
    """Normalize path. If use_default_expansion is True,
    default_expandvars will be used as variable expansion.
    """
    temp_path = pathlib.Path(path)
    if use_default_expansion:
        temp_path = default_expandvars(temp_path)
    else:
        try:
            temp_path = temp_path.expandvars(temp_path)
        except:
            temp_path = default_expandvars(temp_path)
    temp_path = pathlib.Path(temp_path)
    temp_path = temp_path.expanduser()
    return temp_path.resolve()


def get_path(
    path: UniversalPath,
    **normalize_kwargs: KeywordArgsType,
) -> pathlib.Path:
    """Alias for normalize_path.
    """
    return normalize_path(path, **normalize_kwargs)


def check_path(
    path: UniversalPath,
    **normalize_kwargs: KeywordArgsType,
) -> pathlib.Path:
    """Checks path and return normalized Path.
    """
    normalized_path = normalize_path(path, **normalize_kwargs)
    if not normalized_path.exists():
        raise IOError(f'Path "{path}" does not exist')
    return normalized_path


def join_paths(
    *paths: UniversalPathCollection,
    **normalize_kwargs: KeywordArgsType,
) -> pathlib.Path:
    """Joins iterable of paths to one path.
    """
    joined_path = normalize_path(paths[0], **normalize_kwargs)
    for path_part in paths[1:]:
        joined_path = joined_path.joinpath(path_part)
    joined_path = normalize_path(joined_path, **normalize_kwargs)
    return joined_path


def make_relative_path(path: UniversalPath) -> pathlib.Path:
    """Strip leading / from path to make it relative.
    """
    return pathlib.Path(str(path)[1:]) if str(path).startswith('/') else path


# Directory functions


def current_dir(
    **normalize_kwargs: KeywordArgsType,
) -> pathlib.Path:
    """Return current directory Path.
    """
    current_dir_path = normalize_path(pathlib.Path.cwd(), **normalize_kwargs)
    return current_dir_path


def create_dirs(
    dirs_to_create: UniversalPathCollection,
    parent_dir: typing.Optional[UniversalPath] = None,
    create_parent: bool = False,
    **normalize_kwargs: KeywordArgsType,
) -> typing.List[pathlib.Path]:
    """Create directories.

    If `parent_dir` is specified it will create directories from the list
    as subfolders of `parent_dir`.

    If `create_parent` is `False`, and
    `parent_dir` path does not exist function will `raise IOError`, otherwise
    `parent_dir` will be created.
    """
    parent_path = normalize_path(parent_dir, **normalize_kwargs) if parent_dir \
        else current_dir()

    created_paths = []

    if not parent_path.exists():
        if create_parent:
            parent_path.mkdir(parents=True, exist_ok=True)
        else:
            raise IOError(f'Path "{parent_path}" does not exist')
    if create_parent:
        created_paths.append(parent_path)

    for target_dir in dirs_to_create:
        target_path = parent_path.joinpath(pathlib.Path(target_dir)).resolve()
        if not target_path.exists():
            target_path.mkdir(parents=True, exist_ok=True)
        created_paths.append(target_path)

    return created_paths


def temp_system_dir_path():
    """Return temporary system directory path.
    """
    temp_file = tempfile.TemporaryFile()
    return pathlib.Path(tempfile.tempdir)


def list_dir(path: UniversalPath, recursive: bool=False):
    """List directory contents.
    """
    path = check_path(path)
    glob_pattern = '**/*' if recursive else '*'
    return path.glob(glob_pattern)


# File functions


def check_file_exists_or_increment(
    filepath: UniversalPath,
    **normalize_kwargs: KeywordArgsType
) -> pathlib.Path:
    """Return file path with incremented suffix, if `filepath` already exists.
    Will search for first available number suffix, if previous ones are already
    existing, e.g. `FILENAME_1.EXTENSION`.
    """
    number = 1
    temp_path = normalize_path(filepath, **normalize_kwargs)
    if temp_path.exists():
        filepath_ext = temp_path.suffix
        if filepath_ext:
            filepath_root = str(temp_path)[:-len(str(filepath_ext))]
        else:
            filepath_root = str(temp_path)
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
