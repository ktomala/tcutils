import pathlib
import os


def normalize_path(path):
    return os.path.expanduser(os.path.expandvars(path))


def get_current_dir():
    return os.path.dirname(os.path.abspath(
        normalize_path(__file__)))


def create_dirs(dirs_to_create, parent_dir=None, create_parent=False):
    parent_dir = normalize_path(parent_dir) if parent_dir \
        else get_current_dir()

    parent_path = pathlib.Path(parent_dir)
    if not parent_path.exists():
        if create_parent:
            parent_path.mkdir(parents=True, exist_ok=True)
        else:
            raise IOError(f'Path "{parent_path}" does not exist')

    for target_dir in dirs_to_create:
        target_path = parent_path.joinpath(pathlib.Path(target_dir)).resolve()
        if not target_path.exists():
            target_path.mkdir(parents=True, exist_ok=True)


def check_path(path):
    p = pathlib.Path(normalize_path(path)).resolve()
    if not p.exists():
        raise IOError(f'Path "{p}" does not exist')
    return p


def get_path(path):
    p = pathlib.Path(normalize_path(path)).resolve()
    return p


def join_paths(*paths):
    joined_path = pathlib.Path(normalize_path(paths[0])).resolve()
    for path in paths[1:]:
        path_part = pathlib.Path(normalize_path(path))
        joined_path = joined_path.joinpath(path_part).resolve()
    return joined_path
