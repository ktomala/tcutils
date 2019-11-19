import sys
import yaml
import logging

from marshmallow import Schema
from marshmallow.exceptions import ValidationError

from tcutils.paths import check_path
from tcutils.funcutils import class_prefixed_methods
from tcutils.yamlinclude import IncludeLoader

log = logging.getLogger(__file__)


class BaseConfigSchema(Schema):
    pass


class ConfigurationAttribute:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __getattr__(self, attr_name):
        if attr_name not in dir(self):
            if attr_name not in object.__getattribute__(self, 'value'):
                raise AttributeError(f'No such attribute: {attr_name}')
            attr_value = getattr(self, 'value').get(attr_name)
            if type(attr_value) is dict:
                return ConfigurationAttribute(attr_value)
            else:
                return attr_value
        return super().__getattribute__(attr_name)


class Configuration:

    def __init__(self, config_dict, schema=BaseConfigSchema):
        self.config = config_dict
        self.schema = schema
        self._parse()

    def __str__(self):
        return f'Configuration({self.config})'

    def __getitem__(self, k):
        return self.config.get(k)

    def __getattr__(self, attr_name):
        if attr_name not in dir(self):
            if attr_name not in object.__getattribute__(self, 'config'):
                raise AttributeError(f'No such attribute: {attr_name}')
            attr_value = getattr(self, 'config').get(attr_name)
            if type(attr_value) is dict:
                return ConfigurationAttribute(attr_value)
            else:
                return attr_value
        return super().__getattribute__(attr_name)

    @classmethod
    def load(cls, config_path, schema_class=None):
        """Load configuration file."""
        p = check_path(config_path)
        with open(p, 'r') as fp:
            try:
                config_dict = yaml.load(fp, IncludeLoader)
            except FileNotFoundError as e:
                log.error(f'Configuration !include error: {e}')
                sys.exit(1)
        if schema_class is None:
            schema_class = cls.schema
        schema = schema_class()
        try:
            result = schema.load(config_dict)
        except ValidationError as e:
            log.error(f'Configuration file error: "{e.args}"')
            sys.exit(1)
        return cls(result)

    def _parse(self):
        """Parse configuration and trigger events if necessary."""
        parsing_methods = class_prefixed_methods(self.__class__, '_parse_')
        for parsing_method in parsing_methods:
            method = getattr(self, parsing_method)
            method()
