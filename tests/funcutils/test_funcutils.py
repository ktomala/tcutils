# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

import pytest
import types

from ..context import tcutils


class DummyClass:

    somevar = 'one'
    foo = 'bar'

    def __init__(self, other):
        self.something = other

    def one(self):
        pass

    @classmethod
    def cls_method_two(cls, foo):
        pass

    @staticmethod
    def somestatic():
        pass

    def _prefixed_method(self):
        pass

    def _prefixed_other(self):
        pass


CLASS_TYPES_DEFINED = [
    (tcutils.const.CLASS_METHOD_TYPES, ['__init__', 'one', 'cls_method_two',
        'somestatic', '_prefixed_method', '_prefixed_other']),
    ([types.FunctionType], ['__init__', 'one', '_prefixed_method',
        '_prefixed_other']),
    ([classmethod], ['cls_method_two']),
    ([staticmethod], ['somestatic']),
    ([classmethod, staticmethod], ['cls_method_two', 'somestatic']),
]


class TestFuncUtils:

    @pytest.mark.parametrize(
        "method_types, defined", CLASS_TYPES_DEFINED
    )
    def test_class_methods(self, method_types, defined):
        defined = set(defined)
        methods = tcutils.funcutils.class_methods(DummyClass, method_types)
        assert set(methods) == defined

    def test_class_prefixed_methods(self):
        defined = set(['_prefixed_method', '_prefixed_other'])
        methods = tcutils.funcutils.class_prefixed_methods(DummyClass,
            '_prefixed_')
        assert set(methods) == defined
