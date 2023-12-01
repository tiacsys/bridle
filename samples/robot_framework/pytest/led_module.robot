# SPDX-License-Identifier: Apache-2.0

*** Settings ***
Documentation               This robot example runs some commands on the connected board
...                         (e.g.nucleo_f303re, nucleo_f401re, mimxrt1060_evkb). It uses
...                         the space separated plain text format.
Library                     test_leds    ${type}   ${pathname}   ${serial}   ${baud}   ${timeout}
Suite Setup                 Connect Device
Suite Teardown              Disconnect Device

*** Variables ***
${CMD_LED_ON}               leds
${LED_0}                    0

*** Test Cases ***
Should Set Led On
    [Documentation]         Test that the led can be switched on.
    [Tags]                  SWRQT-LED_RQT  SYSRQT-LED_SYSTEM_RQT

    Led On                  ${CMD_LED_ON}   ${LED_0}
