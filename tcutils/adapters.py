# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

import abc
import typing
import sys
from dataclasses import dataclass

from tcutils.const import DEFAULT_ADAPTER_METHOD
from tcutils.types import AdapterNameOrClass
from tcutils.funcutils import module_classes


@dataclass
class BaseAdapter(abc.ABC):
    name: str

    @abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError


@dataclass
class BaseAdapterManager(abc.ABC):
    """AdapterManager abstract base class.
    """
    manager_name: str
    namespaces: typing.Union[str, typing.List[str]]
    adapter_class: typing.Type[BaseAdapter]
    adapter_dict: typing.Dict[str, typing.Type[BaseAdapter]] = {}

    @staticmethod
    def _get_adapter_name(adapter_name_or_class: AdapterNameOrClass):
        """Return adapter name from either name or adapter class itself.
        """
        if issubclass(adapter_name_or_class, BaseAdapter):
            adapter_name = adapter_name_or_class.name
        else:
            adapter_name = adapter_name_or_class
        return adapter_name

    def get(self,
        adapter_name_or_class: AdapterNameOrClass
    ):
        """Return adapter."""
        adapter_name = self._get_adapter_name(adapter_name_or_class)
        if adapter_name not in self.adapter_dict:
            raise ValueError(f'Adapter "{adapter_name}" is not registered.')
        return self.adapter_dict.get(adapter_name)

    def execute(self,
        adapter_name_or_class: AdapterNameOrClass,
        method: typing.Optional[str] = None,
        *args,
        **kwargs
    ):
        """Execute adapter method (default: BaseAdapter.execute()).
        """
        adapter_name = self._get_adapter_name(adapter_name_or_class)
        adapter_object = self.get(adapter_name)

        if method:
            if not hasattr(adapter_object, method):
                raise ValueError(
                    f'`{adapter_object}.{method}` does not exist.`)
            adapter_method = getattr(adapter_object, method)
        else:
            adapter_method = getattr(adapter_object, DEFAULT_ADAPTER_METHOD)

        if not callable(adapter_method):
            raise ValueError(
                f'`{adapter_object}.{method}` is not callable.')

        return adapter_method(*args, **kwargs)

    def register(self,
        adapter_class: typing.Type[BaseAdapter],
        allow_multiple: bool=False,
        allow_substitute: bool=False
    ):
        """Register `adapter_class` in manager.
        """
        adapter_name = adapter_class.name
        if allow_multiple and adapter_name in self.adapter_dict:
            if type(self.adapter_dict[adapter_name]) is not list:
                self.adapter_dict[adapter_name] = [
                    self.adapter_dict[adapter_name]]
            self.adapter_dict[adapter_name].append(adapter_class)
        else:
            if not allow_substitute and adapter_name in self.adapter_dict:
                raise RuntimeError(
                    f'Adapter {adapter_class} already registered')
            self.adapter_dict[adapter_name] = adapter_class

    def remove(self,
        adapter_name_or_class: AdapterNameOrClass
    ):
        """Remove registered adapter.
        """
        adapter_name = self._get_adapter_name(adapter_name_or_class)
        if adapter_name in self.adapter_dict:
            del(self.adapter_dict[adapter_name])

    def scan(self,
        namespaces: typing.Optional[
            typing.Union[str, typing.List[str]]
        ] = None,
        adapter_classes: typing.Optional[typing.Union[
            typing.Type[BaseAdapter], typing.List[typing.Type[BaseAdapter]]
        ]] = None,
        skip_unknown_namespaces: bool = True,
        recursive_search: bool = True,
        *args, **kwargs
    ):
        """Scan namespaces in search of `adapter_classes` to register.
        """
        if not adapter_classes:
            adapter_classes = [self.adapter_class]
        if type(adapter_clasess) is not list:
            adapter_classes = [adapter_classes]

        if not namespaces:
            namespaces = [self.namespaces]
        if type(namespaces) is not list:
            namespaces = [namespaces]

        loaded_namespaces = sys.modules.keys()
        modules_to_search = []
        for namespace in namespaces:
            if namespace not in loaded_namespaces:
                if recursive_search:
                    modules_to_search.extend([
                        module_name for module_name in loaded_namespaces
                        if module_name.startswith(namespace)
                    ])
                else:
                    if not skip_unknown_namespaces:
                        raise ValueError(
                            f'Unknown namespace `{namespace}` to scan')
            else:
                modules_to_search.append(namespace)

        found_adapters = []
        for module_name in modules_to_search:
            for adapter_class in adapter_classes:
                module = sys.modules.get(module_name)
                found_adapters.extend(module_classes(module, adapter_class))

        for found_adapter in found_adapters:
            self.register(found_adapter, *args, **kwargs)
