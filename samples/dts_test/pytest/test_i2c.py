# Copyright (c) 2021-2023 TiaC Systems
# Copyright (c) 2023 Nordic Semiconductor ASA
# SPDX-License-Identifier: Apache-2.0

import os
# from pathlib import Path
import glob
import time

import logging

from devicetree import dtlib

from twister_harness import Shell

logger = logging.getLogger(__name__)

# set dts path
def dts_path():
    dts_file = "".join([os.getcwd(), "/",
                       glob.glob('twister-out/**/zephyr.dts',
                                 recursive=True)[0]])
    logger.info(f'dts = {dts_file}')

    return dts_file


def get_dts_node_with_status(dts_file, node, items):
    keys = ""

    logger.info(f'open dts to find the {node}')
    dt = dtlib.DT(dts_file, [])

    dt_nodes = dt.get_node(node)
    for key, value in dt_nodes.nodes.items():
        logger.info(f'found {key}')
        if items in key:
            logger.info(f'found {key}')
            logger.info(f'found {value}')
            props = value.props["status"]
            if "okay" in str(props):
                logger.info(f'Found status at \"{key}\" -> check this on device')
                if keys:
                    keys += ";"
                keys += key

                props = value.props["pinctrl-0"]
                logger.info(f'***found {props} at pinctrl-0')
                if props:
                    logger.info(f'Found \"pinctrl-0\" at \"{key}\".')
                else:
                    assert(f'Test failed,\n \"pinctrl-0\" is not found.')

                props = value.props["clock-frequency"]
                logger.info(f'***found {props} at clock-frequency')

                props = value.props["interrupts"]
                logger.info(f'***found {props} at interrupts')
            else:
                logger.info(f'Node {key} not added since it is disabled.')

    length = len(keys)
    logger.info(f'length = {length}')
    assert len(keys) != 0, f'Test failed,\n expected node \"{node}\" not found.'
    logger.info('response is valid')
    return keys


def get_dts_node(dts_file, node, items):
    keys = ""

    logger.info(f'open dts to find the {node}')
    dt = dtlib.DT(dts_file, [])

    dt_nodes = dt.get_node(node)
    for key, value in dt_nodes.nodes.items():
        logger.info(f'found {key}')
        if items in key:
            logger.info(f'found {key}')
            logger.info(f'found {value}')
            props = value.props["gpios"]
            if props:
                logger.info(f'Found \"gpios\" at \"{key}\".')
            else:
                assert(f'Test failed,\n \"gpios\" is not found.')
            if keys:
               keys += ";"
            keys += key


    length = len(keys)
    logger.info(f'length = {length}')
    assert len(keys) != 0, f'Test failed,\n expected node \"{node}\" not found.'
    logger.info('response is valid')
    return keys


def test_sample_dts_i2c(shell: Shell):

    dts_file = dts_path()
    logger.info(f'dts = {dts_file}')
    # check i2c interface
    i2c = get_dts_node_with_status(dts_file, "/soc", "i2c@")
    logger.info(f'found {i2c}')
    for i2c_bus in i2c.split(";"):
        logger.info(f'send "I2C scan" command for bus {i2c_bus}')
        lines = shell.exec_command(f'i2c scan {i2c_bus}')
        assert any([f'devices found on {i2c_bus}' in line for line in lines]), \
            'expected response not found'
        logger.info('response is valid')

    # check leds
    leds = get_dts_node(dts_file, "/leds", "led-1")
    logger.info(f'found {leds}')
    for led in leds.split(";"):
        logger.info(f'send "LED on" command to {led} 0')
        lines = shell.exec_command(f'led on leds 0')
        assert any(['leds: turning on LED 0' in line for line in lines]), \
            'expected response not found'
        time.sleep(1)
        logger.info(f'send "LED off" command to {led} 0')
        lines = shell.exec_command(f'led off leds 0')
        assert any([f'leds: turning off LED 0' in line for line in lines]), \
            'expected response not found'
        logger.info('response is valid')


'''

def test_sample_dts_i2c(shell: Shell):
    i2c = get_dts_node("i2c@")
    logger.info(f'found {i2c}')
    logger.info('send "device list" command')
    lines = shell.exec_command('device list')
    assert any(["i2c@" in line for line in lines]), \
        'expected response not found'
    for i2c_bus in i2c.split(";"):
        logger.info(f'send "I2C scan" command for bus {i2c_bus}')
        lines = shell.exec_command(f'i2c scan {i2c_bus}')
        assert any([f'devices found on {i2c_bus}' in line for line in lines]), \
            'expected response not found'
        logger.info('response is valid')
        '''
