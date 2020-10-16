# -*- coding: utf-8 -*-

import typing
import pathlib
import click


UniversalPath = typing.Union[str, pathlib.Path]
UniversalPathCollection = typing.Iterable[UniversalPath]
CharsList = typing.Union[str, typing.List[str]]
KeywordArgsType = typing.Optional[typing.Dict[str, typing.Any]]
ClickGroupOrCommand = typing.Union[click.Group, click.Command]
