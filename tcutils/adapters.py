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
import click
from dataclasses import dataclass, field
from functools import update_wrapper
from click.globals import get_current_context

from tcutils.const import DEFAULT_ADAPTER_METHOD
from tcutils.types import AdapterNameOrClass, AdapterManagerNamespaces
from tcutils.funcutils import module_classes


def adapter_command(name=None, cls=None, **attrs):
    """Decorator for adding Click command within Adapter.
    """
    if cls is None:
        cls = click.Command

    def decorator(func):
        func._adapter_command = True
        func._adapter_command_name = name
        func._adapter_command_cls = cls
        func._adapter_command_attrs = attrs
        return func
    return decorator


def adapter_pass_context(f):
    """Decorator for passing click context as second argument for Adapter.
    """

    def new_func(*args, **kwargs):
        if args:
            args = args[:1] + (get_current_context(),) + args[1:]
        return f(*args, **kwargs)

    return update_wrapper(new_func, f)


@dataclass
class BaseAdapter(abc.ABC):
    name: str

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError


@dataclass
class BaseCliAdapter(BaseAdapter):
    cli_group: str

    def _get_command_functions(self):
        items = [item for item in dir(self)]
        methods = list(map(lambda x: getattr(self, x), items))
        return [item for item in methods
            if hasattr(item, '_adapter_command')
            and getattr(item, '_adapter_command')]

    def cli_commands(self):
        commands = []
        for f in self._get_command_functions():
            name = f._adapter_command_name
            attrs = f._adapter_command_attrs
            cls = f._adapter_command_cls
            params = f.__click_params__ if hasattr(f, '__click_params__') else []
            cmd = click.decorators._make_command(f, name, attrs, cls)
            # Not sure why is this needed
            cmd.params = params
            cmd.__doc__ = f.__doc__
            commands.append(cmd)
        return commands


@dataclass
class BaseAdapterManager(abc.ABC):
    """AdapterManager abstract base class.
    """
    name: str
    namespaces: AdapterManagerNamespaces
    adapter_class: typing.Type[BaseAdapter]
    adapter_dict: typing.Dict[str, BaseAdapter] = field(
        default_factory=dict)

    @staticmethod
    def _get_adapter_name(adapter_name_or_class: AdapterNameOrClass):
        """Return adapter name from either name or adapter class itself.
        """
        if type(adapter_name_or_class) is not str:
            if not issubclass(adapter_name_or_class, BaseAdapter):
                raise ValueError(
                    f'"{adapter_name_or_class}" is not BaseAdapter type.')
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

    def list(self, objects=False):
        """Return list of registered adapters.

        If objects=True return Adapter instances
        """
        if objects:
            result = []
            for item in self.adapter_dict.values():
                if type(item) is list:
                    result.extend(item)
                else:
                    result.append(item)
            return result
        else:
            return list(self.adapter_dict.keys())

    def __iter__(self):
        """Iterate over registered adapters.
        """
        for adapter_name in self.adapter_dict:
            yield adapter_name

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
                    f'`{adapter_object}.{method}` does not exist.')
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
        allow_substitute: bool=False,
        *args, **kwargs
    ):
        """Register `adapter_class` in manager.
        """
        adapter_name = adapter_class.name
        if allow_multiple and adapter_name in self.adapter_dict:
            if type(self.adapter_dict[adapter_name]) is not list:
                self.adapter_dict[adapter_name] = [
                    self.adapter_dict[adapter_name]]
            self.adapter_dict[adapter_name].append(
                adapter_class(*args, **kwargs))
        else:
            if not allow_substitute and adapter_name in self.adapter_dict:
                raise RuntimeError(
                    f'Adapter {adapter_class} already registered')
            self.adapter_dict[adapter_name] = adapter_class(*args, **kwargs)

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
        if type(adapter_classes) is not list:
            adapter_classes = [adapter_classes]

        if not namespaces:
            namespaces = self.namespaces
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
                if recursive_search:
                    modules_to_search.extend([
                        module_name for module_name in loaded_namespaces
                        if module_name.startswith(namespace)
                    ])
                else:
                    modules_to_search.append(namespace)

        found_adapters = []
        for module_name in modules_to_search:
            for adapter_class in adapter_classes:
                module = sys.modules.get(module_name)
                found_adapters.extend(module_classes(module, adapter_class))

        for found_adapter in found_adapters:
            # Skip abstract classes
            if found_adapter.__abstractmethods__:
                continue
            self.register(found_adapter, *args, **kwargs)
