# Copyright (c) 2021-2023 TiaC Systems
# Copyright (c) 2023 Nordic Semiconductor ASA
# SPDX-License-Identifier: Apache-2.0

import logging

from twister_harness import Shell

logger = logging.getLogger(__name__)


def test_shell_print_help(shell: Shell):
    logger.info('send "help" command')
    lines = shell.exec_command('help')
    assert 'Available commands:' in lines, 'expected response not found'
    logger.info('response is valid')


def test_shell_print_kernel_version(shell: Shell):
    logger.info('send "kernel version" command')
    lines = shell.exec_command('kernel version')
    assert any(['Zephyr version' in line for line in lines]), 'expected response not found'
    logger.info('response is valid')


def test_shell_print_bridle_version(shell: Shell):
    logger.info('send "Bridle version" command')
    lines = shell.exec_command('bridle version long')
    assert any(['Bridle version' in line for line in lines]), 'expected response not found'
    logger.info('response is valid')


def test_shell_print_bridle_info(shell: Shell):
    logger.info('send "Bridle information" command')
    lines = shell.exec_command('bridle info')
    assert any(['Zephyr:' in line for line in lines]), 'expected response not found'
    assert any(['Bridle:' in line for line in lines]), 'expected response not found'
    logger.info('response is valid')
