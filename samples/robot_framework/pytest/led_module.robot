# SPDX-License-Identifier: Apache-2.0

*** Settings ***
Library                       test_leds    ${type}   ${pathname}   ${serial}   ${baud}   ${timeout}
Suite Setup                   Connect Device
Suite Teardown                Disconnect Device


*** Test Cases ***
Should Set Led On
    Led On                    leds   0
