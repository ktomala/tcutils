# -*- coding: utf-8 -*-

import logging
import os
import unicodedata
import pathlib
import typing
from tcutils.const import VALID_FILENAME_CHARS, DEFAULT_REPLACEMENT_CHAR
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
    def from_octal(cls, perm_octet: str):
        sticky = False
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

    def to_octal(self):
        octet_list = [
            1 if self.sticky else 0,
            self.owner.to_octal(),
            self.group.to_octal(),
            self.world.to_octal(),
        ]
        return ''.join([str(octet) for octet in octet_list])


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
