# SPDX-FileCopyrightText: 2021-2026 TiaC Systems
# SPDX-FileCopyrightText: 2021 Nordic Semiconductor ASA
# SPDX-License-Identifier: Apache-2.0

from sphinx.application import Sphinx

from . import tsn_include

__version__ = '0.0.1'


def setup(app: Sphinx):
    tsn_include.setup(app)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
