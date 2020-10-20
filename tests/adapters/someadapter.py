# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

import typing
from dataclasses import dataclass, field

from ..context import tcutils


@dataclass
class SomeAdapter(tcutils.adapters.BaseAdapter):
    name: str = "SomeAdapter"

    def execute(self, *args, **kwargs):
        return f'{self.name} executing'


@dataclass
class SomeAdapterManager(tcutils.adapters.BaseAdapterManager):
    name: str = "SomeAdapterManager"
    namespaces: tcutils.types.AdapterManagerNamespaces = field(
        default_factory=lambda: ['tcutils.tests.adapters.test_adapters'])
    adapter_class: typing.Type[tcutils.adapters.BaseAdapter] = SomeAdapter
