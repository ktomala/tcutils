# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

# Cannot be used with Python3.6
#from __future__ import annotations

import yaml
import logging
import typing

from marshmallow import Schema
from marshmallow.exceptions import ValidationError

from tcutils.types import UniversalPath
from tcutils.paths import check_path
from tcutils.funcutils import class_prefixed_methods
from tcutils.yamlinclude import IncludeLoader

log = logging.getLogger(__file__)


class BaseConfigSchema(Schema):
    """Placeholder base configuration schema.

    You can use it as a base for your own schema by inheriting this class.
    """
    pass


class ConfigurationAttribute:
    """Configuration attribute for easy access."""

    def __init__(self, value: typing.Any):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __getattr__(self, attr_name) -> typing.Any:
        attr_suffix = None
        if attr_name.find('.') > -1:
            attr_name, attr_suffix = attr_name.split('.', 1)
        if attr_name not in dir(self):
            if attr_name not in object.__getattribute__(self, 'value'):
                raise AttributeError(f'No such attribute: {attr_name}')
            attr_value = getattr(self, 'value').get(attr_name)
            if type(attr_value) is dict:
                attr_value = ConfigurationAttribute(attr_value)
        else:
            attr_value = super().__getattribute__(attr_name)
        if attr_suffix:
            attr_value = getattr(attr_value, attr_suffix)
        return attr_value


class Configuration:
    """Configuration class."""

    def __init__(
        self,
        config_dict: typing.Dict[str, typing.Any],
        schema: BaseConfigSchema = BaseConfigSchema
    ):
        self.config = config_dict
        self.schema = schema
        self._parse()

    def __str__(self) -> str:
        return f'Configuration({self.config})'

    def __getitem__(self, k: str) -> typing.Any:
        return self.config.get(k)

    def __getattr__(self, attr_name: str) -> typing.Any:
        attr_suffix = None
        if attr_name.find('.') > -1:
            attr_name, attr_suffix = attr_name.split('.', 1)
        if attr_name not in dir(self):
            if attr_name not in object.__getattribute__(self, 'config'):
                raise AttributeError(f'No such attribute: {attr_name}')
            attr_value = getattr(self, 'config').get(attr_name)
            if type(attr_value) is dict:
                attr_value = ConfigurationAttribute(attr_value)
        else:
            attr_value = super().__getattribute__(attr_name)
        if attr_suffix:
            attr_value = getattr(attr_value, attr_suffix)
        return attr_value

    @classmethod
    def load(
        cls: typing.Type[typing.Any],
        config_path: UniversalPath,
        schema_class: typing.Optional[BaseConfigSchema] = None,
        *schema_args: typing.Iterable[typing.Any],
        **schema_kwargs: typing.Mapping[typing.Any, typing.Any],
    ) -> typing.Type[typing.Any]:
        """Load configuration file."""
        p = check_path(config_path)
        with p.open('r') as fp:
            try:
                config_dict = yaml.load(fp, IncludeLoader)
            except FileNotFoundError as e:
                log.error(f'Configuration !include error: {e}')
                raise e
        if schema_class is None:
            schema_class = BaseConfigSchema
        schema = schema_class(*schema_args, **schema_kwargs)
        try:
            result = schema.load(config_dict)
        except ValidationError as e:
            log.error(f'Configuration file error: "{e.args}"')
            raise e
        if schema_class:
            return cls(result, schema=schema_class)
        else:
            return cls(result)

    def _parse(self):
        """Parse configuration and trigger events if necessary."""
        parsing_methods = class_prefixed_methods(self.__class__, '_parse_')
        for parsing_method in parsing_methods:
            method = getattr(self, parsing_method)
            method()
