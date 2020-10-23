# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

import pathlib
from marshmallow import fields, ValidationError

from tcutils.fs import PosixPermissions


class PathField(fields.Field):
    """Field that serializes Path to string and deserializes to pathlib.Path.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return pathlib.Path(value)
        except Exception as e:
            raise ValidationError(f'{e}')


class PosixPermissionsField(fields.Field):
    """Field that serializes PosixPermissions to string and deserializes
    to PosixPermissions.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return PosixPermissions.from_octal(value)
        except Exception as e:
            raise ValidationError(f'{e}')
