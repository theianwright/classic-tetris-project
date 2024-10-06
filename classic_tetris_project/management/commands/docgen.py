import inspect
from io import TextIOWrapper
import os
from typing import Type

from django.core.management.base import BaseCommand

from classic_tetris_project.commands.command import (
    Command as BotCommand,
    COMMAND_CLASSES,
)
from classic_tetris_project.commands.countdown import Countdown
from classic_tetris_project.util import DocSection
from classic_tetris_project.util.docs import parse_docstring

SECTION_MAP = [
    (DocSection.USER, "User commands"),
    (DocSection.ACCOUNT, "Account linking commands"),
    (DocSection.QUEUE, "Queueing commands"),
    (DocSection.UTIL, "Utility commands"),
    (DocSection.OTHER, "Other commands"),
]
PRELUDE = """# Commands

Note: this file is autogenerated using `python manage.py docgen`. Please do not edit it directly!

The following is a detailed outline of each command the bot supports. Ideas for more commands are always welcome - you may open a [GitHub issue](https://github.com/professor-l/classic-tetris-project/issues/new) to suggest them as well as to report bugs in the existing ones.

Commands are listed with `<required parameters>` and `[optional parameters]`, which occasionally have a `[default=value]`.

"""
DOC_PATH = "docs/COMMANDS.md"

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(DOC_PATH, "w") as f:
            f.write(PRELUDE)
            first_section = True
            for section, section_title in SECTION_MAP:
                if first_section:
                    first_section = False
                else:
                    f.write("\n\n")
                f.write(f"## {section_title}\n\n")
                cmds = [c for c in COMMAND_CLASSES if c.section == section]
                cmds.sort(key=lambda c: c.aliases[0])
                for i, cmd in enumerate(cmds):
                    self.write_cmd(cmd, f)
                    if i < len(cmds)-1:
                        f.write("\n\n---\n\n")

    def write_cmd(self, cmd: Type[BotCommand], f: TextIOWrapper):
        # TODO: maybe the prefix isn't always `!`?
        f.write(f"#### `!{cmd.usage}`")
        f.write("\n")
        f.write(f"[Source]({Command.get_source_url(cmd)})")
        f.write("<br/>\n")
        platform_string = ", ".join(p.display_name() for p in
                                    cmd.supported_platforms)
        f.write(f"**Platforms**: {platform_string}")
        # don't alias countdown command
        alias_string = ", ".join(f"`!{a}`" for a in cmd.aliases[1:])
        if alias_string and cmd != Countdown:
            f.write("<br/>\n")
            f.write(f"**Aliases**: {alias_string}")
        for note in cmd.notes:
            f.write("<br/>\n")
            f.write(f"**{note}**")
        f.write("\n\n")
        assert cmd.__doc__
        f.write(parse_docstring(cmd.__doc__))

    # gets a github-understood relative url to the function
    @staticmethod
    def get_source_url(cmd: Type[BotCommand]):
        source_file = inspect.getsourcefile(cmd)
        assert source_file is not None
        source_path = os.path.relpath(source_file, os.getcwd())
        line_num = inspect.getsourcelines(cmd)[1]
        return f"../{source_path}#L{line_num}"
