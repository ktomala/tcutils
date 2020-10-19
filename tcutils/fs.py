# -*- coding: utf-8 -*-

import logging
import os
import unicodedata
import pathlib
import typing
import tempfile
import urllib.request
import urllib.response
from dataclasses import dataclass
from tcutils.const import VALID_FILENAME_CHARS, DEFAULT_REPLACEMENT_CHAR, \
    DEFAULT_URI_SCHEME
from tcutils.types import CharsList, UniversalPath, KeywordArgsType
from tcutils.paths import normalize_path

log = logging.getLogger(__file__)


@dataclass
class PosixPermissionTriad:
    read: bool
    write: bool
    execute: bool

    @classmethod
    def from_octal(cls, octet: typing.Union[int, str]):
        if type(octet) == str:
            octet = int(octet, 8)
        return cls(
            read = octet & 4,
            write = octet & 2,
            execute = octet & 1
        )

    def to_octal(self) -> int:
        octet = 0x0
        if self.read:
            octet += 0x4
        if self.write:
            octet += 0x2
        if self.execute:
            octet += 0x1
        return octet


@dataclass
class PosixPermissions:
    owner: PosixPermissionTriad
    group: PosixPermissionTriad
    world: PosixPermissionTriad
    sticky: bool = False

    @classmethod
    def from_octal(cls, perm_octet: typing.Union[str, int]):
        sticky = False
        if type(perm_octet) == int:
            perm_octet = str(perm_octet)
        if len(perm_octet) > 4 or len(perm_octet) < 3:
            raise ValueError('Permissions must be in POSIX octal format.')
        elif len(perm_octet) == 4:
            sticky = int(perm_octet[0], 8) & 1
            perm_octet = perm_octet[1:]
        return cls(
            owner = PosixPermissionTriad.from_octal(perm_octet[0]),
            group = PosixPermissionTriad.from_octal(perm_octet[1]),
            world = PosixPermissionTriad.from_octal(perm_octet[2]),
            sticky = sticky
        )

    @classmethod
    def from_stat(cls, stat_mode: int):
        perm_octet = oct(stat_mode)[-4:]
        return cls.from_octal(perm_octet)

    def to_octal_str(self):
        octet_list = [
            1 if self.sticky else 0,
            self.owner.to_octal(),
            self.group.to_octal(),
            self.world.to_octal(),
        ]
        return ''.join([str(octet) for octet in octet_list])

    def to_octal(self):
        return int(self.to_octal_str(), 8)

    def apply(self, path: UniversalPath):
        """Apply permissions to path."""
        if type(path) == str:
            path = pathlib.Path(path)
        path.chmod(self.to_octal())

    def __str__(self):
        return self.to_octal_str()

    def __repr__(self):
        return f"{self.__class__.__name}<'{self.to_octal_str()}'>"


def clean_filename(
    filename: str,
    whitelist: CharsList = VALID_FILENAME_CHARS,
    replace: CharsList = ' ',
    replacement: str = DEFAULT_REPLACEMENT_CHAR
) -> str:
    """Cleans filename according to `whitelist` characters and `replace`
    characters which will be substituted by `replacement` character.
    """
    # Replace spaces (or characters defined by replace)
    for r in replace:
        filename = filename.replace(r, replacement)

    # Keep only valid ASCII chars
    cleaned_filename = unicodedata.normalize(
        'NFKD', filename).encode('ASCII', 'ignore').decode()

    # Keep only whitelisted chars
    return ''.join(c for c in cleaned_filename if c in whitelist)


def temp_dir() -> tempfile.TemporaryDirectory:
    """Return temporary directory."""
    return tempfile.TemporaryDirectory()


def temp_file() -> tempfile.NamedTemporaryFile:
    """Return temporary file."""
    return tempfile.NamedTemporaryFile()


def open_uri(
    uri: str,
    default_uri_scheme: str=DEFAULT_URI_SCHEME,
    *args, **kwargs
) -> urllib.response.addinfourl:
    """Open URI and return stream handle."""
    parsed_uri = urllib.request.urlparse(uri)
    if parsed_uri.scheme == '':
        parsed_uri = parsed_uri._replace(scheme=default_uri_scheme)
    return urllib.request.urlopen(parsed_uri.geturl(), *args, **kwargs)
