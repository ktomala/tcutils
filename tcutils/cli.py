# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2019-2020 TropiCoders Karol Tomala
#

import click

import types
from tcutils.types import ClickGroupOrCommand


class NotRequiredIf(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if = kwargs.pop('not_required_if')
        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs['help'] = (kwargs.get('help', '') +
            ' NOTE: This argument is mutually exclusive with %s' %
            self.not_required_if
        ).strip()
        super(NotRequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        we_are_present = self.name in opts
        other_present = self.not_required_if in opts

        if other_present:
            if we_are_present:
                raise click.UsageError(
                    "Illegal usage: `%s` is mutually exclusive with `%s`" % (
                        self.name, self.not_required_if))
            else:
                self.prompt = None

        return super(NotRequiredIf, self).handle_parse_result(
            ctx, opts, args)


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
    parent_add_group = getattr(parent, 'add_command')
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


def cli_register_command_group(manager, cli_parent):
    manager.scan()
    for adapter_name in manager:
        adapter = manager.get(adapter_name)
        commands = adapter.cli_commands()
        cli_group_kwargs = adapter.cli_group_kwargs
        if not cli_group_kwargs:
            cli_group_kwargs = {}
        cli_group = click.Group(
            name=adapter.cli_group,
            **cli_group_kwargs
        )
        for command in commands:
            cli_group.add_command(command)
        cli_parent.add_command(cli_group)
