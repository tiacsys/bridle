# Copyright (c) 2021-2023 TiaC Systems
# Copyright (c) 2023 Nordic Semiconductor ASA
# SPDX-License-Identifier: Apache-2.0

import os
from pathlib import Path

import logging

from devicetree import dtlib

from twister_harness import Shell

logger = logging.getLogger(__name__)


def dts_path():
    for path in Path(os.getcwd()).rglob('zephyr.dts'):
        dts_file = str(path)
        logger.info(f'dts = {dts_file}')
        if "twister-out" in dts_file:
            return dts_file





def get_dts_node(node):
    logger.info(f'open dts to find the {node}')
    dts_file = dts_path()
    logger.info(f'dts = {dts_file}')
    dt = dtlib.DT(dts_file, ["i2c"])

    dt_nodes = dt.get_node("/soc")
    for key, value in dt_nodes.nodes.items():
        if node in key:
            logger.info(f'found {key}')
            return key


def test_sample_dts_leds(shell: Shell):
    i2c = get_dts_node("led")
    logger.info(f'found {i2c}')
    logger.info('send "device list" command')
    lines = shell.exec_command('device list')
    assert any([i2c in line for line in lines]), \
        'expected response not found'
    logger.info(f'send "I2C scan" command for bus {i2c}')
    lines = shell.exec_command(f'i2c scan {i2c}')
    assert any([f'devices found on {i2c}' in line for line in lines]), \
        'expected response not found'
    logger.info('response is valid')

    # check leds
    leds = get_dts_node(dts_file, "/leds", "led_2")
    logger.info(f'found {leds}')
    for led in leds.split(";"):
        logger.info(f'send "LED on" command to {led} 0')
        lines = shell.exec_command(f'led on {led} 0')
        assert any([f'{led}: turning on LED' in line for line in lines]), \
            'expected response not found'
        time.sleep(3)
        logger.info(f'send "LED off" command to {led} 0')
        lines = shell.exec_command(f'led off {led} 0')
        assert any([f'{led}: turning off LED' in line for line in lines]), \
            'expected response not found'
        logger.info('response is valid')


import logging
import time

from twister_harness import Shell

logger = logging.getLogger(__name__)


def test_shell_test_leds(shell: Shell):
    logger.info('send "device list" command to find the leds')
    lines = shell.exec_command('device list')
    assert any(['led' in line for line in lines]), \
        'expected response not found'
    for line in lines:
        if "led" in line:
            """ Since the command 'led get_info' fails with error -88
            switch the led on/off
            """
            led = line.split(" ")
            logger.info(f'send "LED on" command to {led[1]} 0')
            lines = shell.exec_command(f'led on {led[1]} 0')
            assert any([f'{led[1]}: turning on LED' in line for line in lines]), \
                'expected response not found'
            time.sleep(3)
            logger.info(f'send "LED off" command to {led[1]} 0')
            lines = shell.exec_command(f'led off {led[1]} 0')
            assert any([f'{led[1]}: turning off LED' in line for line in lines]), \
                'expected response not found'
    logger.info('response is valid')
