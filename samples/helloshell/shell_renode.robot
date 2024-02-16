# SPDX-License-Identifier: Apache-2.0

*** Settings ***
Resource                      ${RENODEKEYWORDS}
Suite Setup                   Setup
Suite Teardown                Teardown
Test Setup                    Reset Emulation
Test Teardown                 Test Teardown

*** Variables ***
${UART}                       sysbus.usart2

*** Test Cases ***
Should Read Version From Shell
    # Prepare Machine
    Execute Command           include @${CURDIR}/renode/nucleo_f401re.resc

    Create Terminal Tester    sysbus.usart2
    Start Emulation

    Wait For Prompt On Uart   uart:~$
    Write Line To Uart        kernel version
    Wait For Line On Uart     Zephyr version 3.5.99
    Write Line To Uart        device list
    Wait For Line On Uart     i2c@40005400 (READY)
#    Write Line To Uart        i2c scan i2c@40005400
#    Wait For Line On Uart     devices found on i2c@40005400
    Write Line To Uart        kernel threads
    Wait For Line On Uart     sysworkq
