# -*- coding: utf-8 -*-

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
    def test_configuration_item_access(self, dummy_configuration, item, result):
        item_attr = getattr(dummy_configuration, item)
        assert item_attr == result
