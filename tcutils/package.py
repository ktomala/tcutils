# -*- coding: utf-8 -*-

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
