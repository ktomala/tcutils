# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

import pytest
import getpass

from ..context import tcutils


class TestUser:

    def test_current_user_name(self):
        current_user = tcutils.user.current_user_name()
        assert current_user == getpass.getuser()
