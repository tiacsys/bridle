# Copyright (c) 2022 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

import sys
from functools import wraps
from pathlib import Path

from west import log


def _get_zephyr(topdir, manifest) -> str | None:
    ident = 'zephyr'
    projects = None

    try:
        projects = manifest.get_projects([ident], allow_paths=False)
    except ValueError:
        try:
            folder = Path(topdir) / ident
            projects = manifest.get_projects([folder])
        except ValueError:
            pass

    if projects:
        return projects[0]
    else:
        raise ValueError('Zephyr project not found.')


def _get_west_cmd_path(project) -> Path | None:
    abspath = None
    cmdpath = None

    try:
        abspath = Path(project.abspath)
        cmdpath = Path(project.userdata['west-commands-path'])
    except (AttributeError, KeyError):
        pass

    if abspath.exists() and str(cmdpath):
        return (abspath / cmdpath).resolve()
    else:
        raise ValueError(f'West command path in project "{project}" not found.')


def zephyr_sys_path(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if 'sys_path_with_zephyr' not in function.__globals__:
            try:
                zephyr = _get_zephyr(self.topdir, self.manifest)
            except ValueError:
                log.err(
                    'Cannot find Zephyr project metadata.', 'Check your west workspace or manifest.'
                )
                return

            try:
                west_cmd_path = _get_west_cmd_path(zephyr)
            except ValueError:
                log.err(
                    'Cannot find West command path for Zephyr.',
                    'Check your west workspace or manifest entries.',
                )
                return

            sys.path.append(str(west_cmd_path))
            function.__globals__['sys_path_with_zephyr'] = sys.path

        retval = function(self, *args, **kwargs)
        return retval

    return wrapper


def zcmake_run_cmake(function):
    @zephyr_sys_path
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if 'run_cmake' not in function.__globals__:
            from zcmake import run_cmake

            function.__globals__['run_cmake'] = run_cmake

        retval = function(self, *args, **kwargs)
        return retval

    return wrapper
