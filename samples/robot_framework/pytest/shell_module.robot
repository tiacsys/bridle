# SPDX-License-Identifier: Apache-2.0

*** Settings ***
Documentation               This robot example runs some commands on the connected board
...                            (e.g.nucleo_f303re, nucleo_f401re, mimxrt1060_evkb). It uses
...                            the space separated plain text format.
Library                     test_uarts   ${type}   ${pathname}   ${serial}   ${baud}   ${timeout}
Suite Setup                 Connect Device
Suite Teardown              Disconnect Device

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

    Write Line To Uart      ${CMD_KERNEL_VERSION}
    Wait For Line On Uart   ${RSP_ZEPHYR_VERSION}

Check I2C Interface
    [Documentation]         Test that the I2C bus is configured.
    ...     ${RSP_I2C_0005400}
    [Tags]                  SWRQT-I2C_RQT  SYSRQT-I2C_SYSTEM_RQT

    Write Line To Uart      ${CMD_DEVICE_LIST}
    Wait For Line On Uart   ${RSP_I2C_0005400}
    Write Line To Uart      ${CMD_SCAN_I2C}
    Wait For Line On Uart   ${RSP_SCAN_I2C}
