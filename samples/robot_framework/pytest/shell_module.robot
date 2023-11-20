# SPDX-License-Identifier: Apache-2.0

*** Settings ***
Library                       test_uarts   ${type}   ${pathname}   ${serial}   ${baud}   ${timeout}
Suite Setup                   Connect Device
Suite Teardown                Disconnect Device


*** Test Cases ***
Should Read Version
    Write Line To Uart        kernel version
    Wait For Line On Uart     Zephyr version 3.5.99

Check I2C Interface
    Write Line To Uart        device list
    Wait For Line On Uart     i2c@40005400 (READY)
    Write Line To Uart        i2c scan i2c@40005400
    Wait For Line On Uart     devices found on i2c@40005400
