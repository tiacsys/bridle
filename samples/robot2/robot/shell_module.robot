# SPDX-License-Identifier: Apache-2.0

*** Settings ***
Documentation               This robot example runs some commands on the connected board
...                            (e.g.nucleo_f303re, nucleo_f401re, mimxrt1060_evkb). It uses
...                            the space separated plain text format.
Library                     twister_harness.robot_framework.ZephyrLibrary
Suite Setup                 Get a Device
Suite Teardown              Close Device

*** Variables ***
${CMD_KERNEL_VERSION}       kernel version
${RSP_ZEPHYR_VERSION}       Zephyr version 3.5.99
${CMD_DEVICE_LIST}          device list
${RSP_I2C_0005400}          i2c@40005400 (READY)
${CMD_SCAN_I2C}             i2c scan i2c@40005400
${RSP_SCAN_I2C}             devices found on i2c@40005400

*** Test Cases ***
Should Read Version
    [Documentation]         Test that the Zephyr version is correct.
    ...     ${RSP_ZEPHYR_VERSION}
    [Tags]                  SWRQT-VERSION_RQT  SWRQT-OTHER_RQT  SYSRQT-VERSION_SYSTEM_RQT

    Run Device
    Run Command             ${CMD_KERNEL_VERSION}

Check I2C Interface
    [Documentation]         Test that the I2C bus is configured.
    ...     ${RSP_I2C_0005400}
    [Tags]                  SWRQT-I2C_RQT  SYSRQT-I2C_SYSTEM_RQT

    Run Command             ${CMD_DEVICE_LIST}
    Run Command             ${CMD_SCAN_I2C}
