# Copyright (c) 2021 TiaC Systems
# Copyright (c) 2021 Nordic Semiconductor ASA
# SPDX-License-Identifier: Apache-2.0

from sphinx.application import Sphinx
from . import robot_to_rst

__version__ = '0.0.1'


def setup(app: Sphinx):
    robot_to_rst.setup(app)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
