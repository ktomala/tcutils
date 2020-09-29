# -*- coding: utf-8 -*-

import pathlib
import os
import sys
import typing
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


# Directory functions


def get_current_dir(
    **normalize_kwargs: KeywordArgsType,
) -> pathlib.Path:
    """Return current directory Path based on __file__.
    """
    current_dir_path = normalize_path(__file__, **normalize_kwargs)
    return current_dir_path.directory


def create_dirs(
    dirs_to_create: UniversalPathCollection,
    parent_dir: typing.Optional[UniversalPath] = None,
    create_parent: bool = False,
    **normalize_kwargs: KeywordArgsType,
) -> None:
    """Create directories.

    If `parent_dir` is specified it will create directories from the list
    as subfolders of `parent_dir`.

    If `create_parent` is `False`, and
    `parent_dir` path does not exist function will `raise IOError`, otherwise
    `parent_dir` will be created.
    """
    parent_path = normalize_path(parent_dir, **normalize_kwargs) if parent_dir \
        else get_current_dir()

    if not parent_path.exists():
        if create_parent:
            parent_path.mkdir(parents=True, exist_ok=True)
        else:
            raise IOError(f'Path "{parent_path}" does not exist')

    for target_dir in dirs_to_create:
        target_path = parent_path.joinpath(pathlib.Path(target_dir)).resolve()
        if not target_path.exists():
            target_path.mkdir(parents=True, exist_ok=True)
