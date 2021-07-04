# Copyright (c) 2020 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

from sphinx.application import Sphinx
from . import interbreathe

__version__ = '0.1.0'


def setup(app: Sphinx):
    interbreathe.setup(app)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
