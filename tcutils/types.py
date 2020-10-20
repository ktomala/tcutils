# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

import typing
import pathlib
import click

UniversalPath = typing.Union[str, pathlib.Path]
UniversalPathCollection = typing.Iterable[UniversalPath]
CharsList = typing.Union[str, typing.List[str]]
KeywordArgsType = typing.Optional[typing.Dict[str, typing.Any]]
ClickGroupOrCommand = typing.Union[click.Group, click.Command]
AdapterNameOrClass = typing.Union[str, typing.Type['BaseAdapter']]
AdapterManagerNamespaces = typing.Union[str, typing.List[str]]
