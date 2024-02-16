# SPDX-License-Identifier: Apache-2.0

*** Settings ***
Documentation               This robot example runs some commands on the connected board
...                         (e.g.nucleo_f303re, nucleo_f401re, mimxrt1060_evkb). It uses
...                         the space separated plain text format.
Library                     twister_harness.robot_framework.ZephyrLibrary
Suite Setup                 Get a Device
Suite Teardown              Close Device

*** Variables ***
${CMD_LED_ON}               led on leds 0
${LED_0}                    0

*** Test Cases ***
Should Set Led On
    [Documentation]         Test that the led can be switched on.
    [Tags]                  SWRQT-LED_RQT  SYSRQT-LED_SYSTEM_RQT

    Run Device
    Run Command             ${CMD_LED_ON}
