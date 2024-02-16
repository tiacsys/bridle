# Copyright (c) 2021-2023 TiaC Systems
# Copyright (c) 2023 Nordic Semiconductor ASA
# SPDX-License-Identifier: Apache-2.0

# import logging
import time
from robot.api import logger

from twister_harness import Shell
from pytest_robotframework import keyword
# logger = logging.getLogger(__name__)


@keyword
def test_shell_test_leds(shell: Shell):
    logger.info('send "device list" command to find the leds')
    lines = shell.exec_command('device list')
    assert any(['led' in line for line in lines]), \
        'expected response not found'
    for line in lines:
        if "led" in line:
            led = line.split(" ")
            logger.info(f'send "LED on" command to {led[1]} 0')
            lines = shell.exec_command(f'led on {led[1]} 0')
            assert any([f'{led[1]}: turning on LED' in line for line in lines]), \
                'expected response not found'
            time.sleep(1)
            logger.info(f'send "LED off" command to {led[1]} 0')
            lines = shell.exec_command(f'led off {led[1]} 0')
            assert any([f'{led[1]}: turning off LED' in line for line in lines]), \
                'expected response not found'
    logger.info('response is valid')
