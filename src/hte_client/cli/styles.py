#   Copyright 2022 Modelyst LLC
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Utilities for printing things to screen for CLI."""
import typer
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme

from hte_client import __version__
from hte_client.utils.log import console

THEME_COLOR = typer.colors.GREEN
theme = Theme({'theme': 'green'})
LOGO = r"""
 _,_ ___ __,     _, _,  _ __, _, _ ___
 |_|  |  |_     / ` |   | |_  |\ |  |
 | |  |  |   ~~ \ , | , | |   | \|  |
 ~ ~  ~  ~~~     ~  ~~~ ~ ~~~ ~  ~  ~

"""

VERSION = f"""VERSION: {__version__}"""


def delimiter(color: str = THEME_COLOR):
    console.rule(style=color)


LOGO_STYLE = Panel.fit(
    Group(Panel(Text(LOGO)), Panel(Text(VERSION, justify='center'))),
    style=THEME_COLOR,
)


# Easy printers
typer_print = lambda color=None: lambda msg: console.print(msg, style=color)
good_typer_print = typer_print('green')
bad_typer_print = typer_print('red')
theme_typer_print = typer_print('theme')
greens = lambda x: typer.style(x, fg=typer.colors.BRIGHT_GREEN)
reds = lambda x: typer.style(x, fg=typer.colors.BRIGHT_RED)
