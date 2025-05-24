# Copyright (c) 2022 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

import argparse
from pathlib import Path

from west import log
from west.commands import WestCommand
from zephyr_trampoline import zcmake_run_cmake

EXPORT_DESCRIPTION = '''\
This command registers the current Bridle installation as a CMake
config package in the CMake user package registry.

In Windows, the CMake user package registry is found in:
HKEY_CURRENT_USER\\Software\\Kitware\\CMake\\Packages\\

In Linux and MacOS, the CMake user package registry is found in:
~/.cmake/packages/'''


class BridleExport(WestCommand):
    def __init__(self):
        super().__init__(
            'bridle-export',
            # Keep this in sync with the string in west-commands.yml.
            'export Bridle installation as a CMake config package',
            EXPORT_DESCRIPTION,
            accepts_unknown_args=False,
        )

    def do_add_parser(self, parser_adder):
        parser = parser_adder.add_parser(
            self.name,
            help=self.help,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=self.description,
        )
        return parser

    def do_run(self, args, unknown_args):
        # The 'share' subdirectory of the top level bridle repository.
        share = Path(__file__).parents[2] / 'share'

        self.run_cmake_export(share / 'bridle-package' / 'cmake')

    @zcmake_run_cmake
    def run_cmake_export(self, path):
        # Run a package installation script.
        #
        # Filtering out lines that start with -- ignores the normal
        # CMake status messages and instead only prints the important
        # information.

        # pylint: disable=undefined-variable
        lines = run_cmake(  # noqa F821
            ['-P', str(path / 'bridle_export.cmake')],
            capture_output=True,
        )
        msg = [line for line in lines if not line.startswith('-- ')]
        log.inf('\n'.join(msg))
