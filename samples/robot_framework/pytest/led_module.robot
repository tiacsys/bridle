# SPDX-License-Identifier: Apache-2.0

*** Settings ***
Library                       test_leds    ${type}   ${pathname}   ${serial}   ${baud}   ${timeout}
# Suite Setup                   test_leds.Connect Device
# Suite Teardown                test_leds.Disconnect Device


*** Test Cases ***
Connect to device for led test
    test_leds.Connect Device

Should Set Led On
    Led On                    leds   0

Disconnect from device
    test_leds.Disconnect Device
