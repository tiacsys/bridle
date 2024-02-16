# Copyright (c) 2021-2023 TiaC Systems
# Copyright (c) 2023 Nordic Semiconductor ASA
# SPDX-License-Identifier: Apache-2.0

import os
from pathlib import Path
from robot.api import logger

# import logging

from twister_harness import Shell
from pytest_robotframework import keyword

# logger = logging.getLogger(__name__)


@keyword
def test_shell_test_i2c(shell: Shell):
    logger.info('send "device list" command to find the I2C bus')
    lines = shell.exec_command('device list')
    assert any(['i2c@' in line for line in lines]), \
        'expected response not found'
    for i2c_bus in lines:
        if "i2c@" in i2c_bus:
            logger.info(f'send "I2C scan" command for bus {i2c_bus}')
            i2c = i2c_bus.split(" ")
            lines = shell.exec_command(f'i2c scan {i2c[1]}')
            assert any([f'device found on {i2c[1]}' in line for line in lines]), \
                'expected response not found'
    logger.info('response is valid')
