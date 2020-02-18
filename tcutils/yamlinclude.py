# -*- coding: utf-8 -*-

import yaml
import os.path
import pathlib


class IncludeLoader(yaml.SafeLoader):

    """Yaml Loader that allows for !include directive within Yaml file.
    """

    def __init__(self, stream):
        """Input Yaml stream."""
        self._root = os.path.split(stream.name)[0]
        super(IncludeLoader, self).__init__(stream)

    def include(self, node):
        """Take Yaml node and extract filename, then load Yaml file of that
        name."""
        filename = os.path.join(self._root, self.construct_scalar(node))
        filepath = pathlib.Path(filename)
        with filepath.open('r') as file_handle:
            return yaml.load(file_handle, IncludeLoader)


# Make sure we load IncludeLoader on module import
IncludeLoader.add_constructor('!include', IncludeLoader.include)
