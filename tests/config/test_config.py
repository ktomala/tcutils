# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

import pytest

from ..context import tcutils


DUMMY_CONFIG = {
    'string': 'foo',
    'number': 42,
    'flag': False,
    'nested': {
        'one': 1,
        'two': 2.0,
        'three': 'something',
        'inception': {
            'full': 'stars',
            'nice': 1,
        }
    }
}

CONFIG_ITEMS = [
    ('string', 'foo'),
    ('number', 42),
    ('nested.one', 1),
    ('nested.inception.full', 'stars'),
    ('nested.inception.nice', 1),
]


class TestConfig:

    @pytest.fixture
    def dummy_configuration(self):
        config = tcutils.config.Configuration(DUMMY_CONFIG)
        return config

    def test_dummy_configuration(self, dummy_configuration):
        result = 'Configuration({config_dict})'.format(
            config_dict=str(DUMMY_CONFIG))
        assert str(dummy_configuration) == result

    @pytest.mark.parametrize(
        "item, result", CONFIG_ITEMS
    )
    def test_configuration_attr_access(self, dummy_configuration, item, result):
        item_attr = getattr(dummy_configuration, item)
        assert item_attr == result

    @pytest.mark.parametrize(
        "item, result", CONFIG_ITEMS
    )
    def test_configuration_item_access(self, dummy_configuration, item, result):
        if item.find('.') > -1:
            items = item.split('.')
        else:
            items = [item]
        item_attr = dummy_configuration
        for item_part in items:
            item_attr = item_attr[item_part]
        assert item_attr == result
