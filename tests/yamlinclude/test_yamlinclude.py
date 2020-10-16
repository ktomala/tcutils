# -*- coding: utf-8 -*-

import pytest
import yaml
import pathlib

from ..context import tcutils

BASE_YAML_PATH = 'data/base.yaml'

FULL_YAML_DICT = {
    'base': {
        'somevar': 'test',
        'somelist': ['one', 'two'],
        'included': {
            'other': {
                'foo': 'bar'
            }
        }
    }
}


class TestYamlInclude:

    @pytest.fixture
    def base_yaml_stream(self):
        yaml_path = pathlib.Path(__file__).parent.absolute() / BASE_YAML_PATH
        return yaml_path.open('r')

    def test_yaml_include(self, base_yaml_stream):
        contents = yaml.load(base_yaml_stream,
            tcutils.yamlinclude.IncludeLoader)
        assert contents == FULL_YAML_DICT
