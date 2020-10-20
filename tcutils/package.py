# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

from pkg_resources import get_distribution, require
from email import message_from_string
from webob.multidict import MultiDict


class PackageDef:
    """Grouping of package functions.
    """

    def __init__(self, package_name: str):
        self.package_name = package_name

    @property
    def metadata(self) -> MultiDict:
        """Return package metadata.

        NOTE: Remember to run setup.py develop for this method to work.
        """
        pkgInfo = get_distribution(self.package_name).get_metadata('PKG-INFO')
        msg = message_from_string(pkgInfo)
        metadata = MultiDict(msg)
        return metadata

    @property
    def version(self) -> str:
        """Return package version."""
        __version__ = require(self.package_name)[0].version
        return __version__
