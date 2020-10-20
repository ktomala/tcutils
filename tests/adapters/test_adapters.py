# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

import pytest

from ..context import tcutils

from .someadapter import SomeAdapter, SomeAdapterManager


class TestAdapters:

    @pytest.fixture
    def some_adapter_manager(self):
        return SomeAdapterManager()

    def test_adapter_manager(self, some_adapter_manager):
        assert some_adapter_manager.name == 'SomeAdapterManager'
        assert some_adapter_manager.namespaces == [
            'tcutils.tests.adapters.test_adapters']
        assert some_adapter_manager.adapter_class == SomeAdapter

    def test_adapter_manager_register_get_remove(self, some_adapter_manager):
        some_adapter_manager.register(SomeAdapter)
        assert SomeAdapter.name in some_adapter_manager.list()
        adapter = some_adapter_manager.get('SomeAdapter')
        assert isinstance(adapter, SomeAdapter)
        some_adapter_manager.remove(SomeAdapter)
        assert SomeAdapter.name not in some_adapter_manager.list()

    def test_adapter_manager_scan(self, some_adapter_manager):
        some_adapter_manager.scan([
            'tcutils.tests.adapters.someadapter',
            'tests.adapters.test_adapters'
        ])
        assert SomeAdapter.name in some_adapter_manager.list()

    def test_adapter_manager_execute(self, some_adapter_manager):
        adapter = SomeAdapter
        some_adapter_manager.register(adapter)
        result = some_adapter_manager.execute(adapter)
        assert result == 'SomeAdapter executing'
