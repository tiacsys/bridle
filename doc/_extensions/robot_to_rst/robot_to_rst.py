"""
Copyright (c) 2021 Nordic Semiconductor ASA
SPDX-License-Identifier: Apache-2.0

This extension calls the Zephyr extension 'external_content' to
copy the *.robot from Robot Framework and *.rst files from the
documentation to the destination directory.
Then the robot files are converted to rst files using 'robot2rst'
and a simple 'index.rst' for the *robot.rst files is created in
the folder of the *robot.rst file.

"""

import os
from pathlib import Path
import subprocess
from typing import Dict, Any

from sphinx.application import Sphinx
import zephyr.external_content


def write_index(fname: Path) -> None:
    dir_path = fname.parents[0]
    name = fname.stem
    f = open(os.path.join(dir_path, "index.rst"), "w")
    f.write(".. _" + name + ":\n\n")
    f.write(name + "\n")
    sections = ""
    for n in range(len(name)):
        sections += '='
    f.write(sections + "\n\n")
    f.write(".. toctree::\n   :maxdepth: 2\n   :glob:\n\n")
    f.write("   *robot\n")
    f.close


def generate_robot(app: Sphinx) -> None:
    """convert all robot files to rst files.

    Args:import sys

        app: Sphinx application instance.
    """

    srcdir = Path(app.srcdir).resolve()

    for src in srcdir.glob('**/*.robot'):
        if not src.is_dir():
            robot = str(src).replace(".robot", "_robot.rst")
            subprocess.run(["robot2rst", "-i", src, "-o", robot,
                            "-p", "CZM_LUZERN-", "-t", "SWRQT-",
                            "SYSRQT-", "-r", "validates", "ext_toolname"])
            write_index(src)


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_config_value("external_content_contents", [], "env")
    app.add_config_value("external_content_directives",
                         zephyr.external_content.DEFAULT_DIRECTIVES, "env")
    app.add_config_value("external_content_keep", [], "")

    app.connect("builder-inited", zephyr.external_content.sync_contents)
    app.connect("builder-inited", generate_robot)
