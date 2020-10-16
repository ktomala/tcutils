# -*- coding: utf-8 -*-

import pytest
import getpass

from ..context import tcutils


class TestUser:

    def test_current_user_name(self):
        current_user = tcutils.user.current_user_name()
        assert current_user == getpass.getuser()
