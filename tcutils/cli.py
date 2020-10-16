# -*- coding: utf-8 -*-

import click

import types
from tcutils.types import ClickGroupOrCommand


def cli_add_groups(
    parent: ClickGroupOrCommand,
    group_module: types.ModuleType
):
    """Attach Click sub groups to Click parent."""
    groups = [
        group_function
        for group_function in vars(group_module).values()
        if isinstance(group_function, click.Group)
    ]

    parent_add_group = getattr(parent, 'group')
    for group_function in groups:
        parent_add_group(group_function)


def cli_add_commands(
    parent: ClickGroupOrCommand,
    command_module: types.ModuleType
):
    """Attach Click sub commands to Click parent."""
    commands = [
        command_function
        for command_function in vars(command_module).values()
        if isinstance(command_function, click.Command)
    ]

    parent_add_command = getattr(parent, 'add_command')
    for command_function in commands:
        parent_add_command(command_function)
