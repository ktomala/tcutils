# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

try:
    import pwd
except ModuleNotFoundError:
    import getpass
import os


def current_user_name() -> str:
    """Return current user name."""
    try:
        return pwd.getpwuid(os.getuid())[0]
    except NameError:
        return getpass.getuser()
