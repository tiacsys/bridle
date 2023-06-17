.. _bridle_release_notes_341:

|BRIDLE| 3.4.1 Release Notes (Working draft)
############################################

This project demonstrate the integration of |TIAC| support in open
source projects, like the Zephyr RTOS, with libraries and source code
for applications. It is not yet intended or supported by |TIAC| for
product development.

Highlights
**********

* :brd:`NOT YET, tbd.`

.. note:: See the changelog and readme files in the component repositories
   for a detailed description of changes.

Repositories
************

For more details, see: :ref:`repos_and_revs`.

.. list-table::
   :header-rows: 1

   * - Component
     - Imports
     - Branch
     - Tag
   * - `tiac-bridle`_
     -
     - v3.4-branch
     - v3.4.1
   * - | `tiac-zephyr`_
       | (`zephyr-core`_)
     - | canopennode
       | chre
       | cmsis
       | edtt
       | fatfs
       | hal_altera
       | hal_atmel
       | hal_espressif
       | hal_nordic
       | hal_nxp
       | hal_rpi_pico
       | hal_st
       | hal_stm32
       | hal_xtensa
       | libmetal
       | liblc3
       | littlefs
       | loramac-node
       | lvgl
       | mbedtls
       | mipi-sys-t
       | net-tools
       | open-amp
       | openthread
       | picolibc
       | segger
       | tinycrypt
     - | tiacsys/v3.4-branch
       | (v3.4-branch)
     - v3.4.1

Supported boards
****************

:brd:`NOT YET, tbd.`

* Arduino/Genuino Zero
* Seeed Studio XIAO SAMD21 (Seeeduino XIAO)
* Seeeduino Lotus Cortex-M0+
* TiaC Magpie STM32F777NIHx

Supported shields
*****************

:brd:`NOT YET, tbd.`

* Seeed Studio Grove Interconnect Shields
* Grove Button Shields
* Grove LED Shields

Change log
**********

:brd:`NOT YET, tbd.`

* tbd.
* tbd.
* tbd.

The following sections provide detailed lists of changes by component.

* PROJECT UPDATE to `Zephyr Project`_ v3.4

Build Infrastructure
====================

Take over the new build principles from Zephyr:

:brd:`NOT YET, tbd.`

* tbd.
* tbd.
* tbd.

Documentation
=============

:brd:`NOT YET, tbd.`

1. Update all output messages in documentation to be in sync with the upcoming
   Bridle version v3.4.1, based on Zephyr v3.4 (samples and tests).

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

* :github:`106` - [FER] Snippets
* :github:`105` - [FCR] Bump to Zephyr v3.4
* :github:`96` - [HW] Grove Interconnect Shields for Seeeduino XIAO
* :github:`90` - [HW] Grove Interconnect Shields for Arduino/Genuino Zero
* :github:`87` - [HW] Seeeduino Lotus Cortex-M0+ board support
* :github:`85` - [BUG] Zephyr counter driver test fails
* :github:`83` - [FCR] Support Grove System Shields
* :github:`80` - [FCR] Support ST HAL
* :github:`79` - [FCR] Support NXP HAL
* :github:`78` - [FCR] Support Raspberry Pi Pico HAL
* :github:`77` - [FCR] Support Atmel HAL
* :github:`76` - [FCR] Bump to Zephyr (bleeding edge) main line
* :github:`73` - [BUG] reduced setup time of clang-format in workflow
* :github:`72` - [FCR] Bump to Zephyr v3.3
* :github:`68` - [BUG] Upgrade to Sphinx 5.x
* :github:`60` - [FCR] Bump to Zephyr v3.2
* :github:`64` - [FCR] Backporting new feature enhancements to v3.0
* :github:`59` - [FCR] Bump to Zephyr v3.1
* :github:`54` - [FCR] Bump to Zephyr v3.0
* :github:`53` - [FCR] Bump to Zephyr v2.7
* :github:`49` - Can't rebuild documentation
* :github:`39` - [FCR] Bump to Zephyr v2.6
* :github:`30` - [FER] Bridle version definition
* :github:`21` - Change all copyright strings
* :github:`7` - Missing CI build and test for all supported boards
* :github:`5` - Improve documentation environment
* :github:`4` - Zephyr does not know F777
* :github:`3` - Missing TiaC Magpie STM32F777NIHx
