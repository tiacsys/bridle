.. _bridle_release_notes_331:

|BRIDLE| 3.3.1 Release Notes (Working draft)
############################################

This project demonstrate the integration of |TIAC| support in open
source projects, like the Zephyr RTOS, with libraries and source code
for applications. It is not yet intended or supported by |TIAC| for
product development.

Highlights
**********

* Added proper build infrastructure.

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
     - v3.3-branch
     - v3.3.1
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
       | mcumgr
       | mipi-sys-t
       | net-tools
       | open-amp
       | openthread
       | picolibc
       | segger
       | tinycrypt
     - | tiacsys/v3.3-branch
       | (v3.3-branch)
     - v3.3.0

Supported boards
****************

* Arduino/Genuino Zero
* Seeeduino Lotus Cortex-M0+
* TiaC Magpie STM32F777NIHx

Change log
**********

The following sections provide detailed lists of changes by component.

* Add new boards:

  * :ref:`arduino_zero`, improved copy from Zephyr
  * :ref:`seeeduino_lotus`, new for Zephyr too

* Add new shields:

  * :ref:`grove_shield`, with integration tested for:

    * :ref:`arduino_zero`
    * :ref:`mimxrt1010_evk`
    * :ref:`mimxrt1060_evk`
    * :ref:`nucleo_f303re_board`
    * :ref:`nucleo_f401re_board`
    * :ref:`nucleo_f767zi_board`
    * :ref:`rpi_pico`
    * :ref:`seeeduino_lotus`

  * :ref:`grove_button_shield`
  * :ref:`grove_led_shield`

* Add :ref:`tests-shields`

  * :doc:`/tests/shields/grove/dts_bindings/README`
  * :doc:`/tests/shields/grove_btn/dts_bindings/README`
  * :doc:`/tests/shields/grove_led/dts_bindings/README`
  * :doc:`/tests/shields/x_grove_testbed/dts_bindings/README`

* Add new DTS bindings:

  * :ref:`devicetree:dtbinding_adafruit_stemma_connector`
  * :ref:`devicetree:dtbinding_adafruit_stemmaqt_connector`
  * :ref:`devicetree:dtbinding_dfrobot_gravity_connector`
  * :ref:`devicetree:dtbinding_digilent_pmod_header`
  * :ref:`devicetree:dtbinding_generic_pin_header`
  * :ref:`devicetree:dtbinding_raspberrypi_pico_header_r3`
  * :ref:`devicetree:dtbinding_seeed_grove_laced_if`
  * :ref:`devicetree:dtbinding_seeed_grove_connector`
  * :ref:`devicetree:dtbinding_sparkfun_qwiic_connector`
  * :ref:`devicetree:dtbinding_st_mems_dil24_socket`

* PROJECT UPDATE to `Zephyr Project`_ v3.3

Build Infrastructure
====================

**NOT YET, tbd.**

Take over the new build principles from Zephyr:

* tbd.

  * tbd.
  * tbd.

Documentation
=============

**NOT YET, tbd.**

1. Update all output messages in documentation to be in sync with the upcoming
   Bridle version v3.3.1, based on Zephyr v3.3 (samples and tests).

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

* :github:`90` - [HW] Grove Interconnect Shields for Arduino/Genuino Zero
* :github:`87` - [HW] Seeeduino Lotus Cortex-M0+ board support
* :github:`83` - [FCR] Support Grove System Shields
* :github:`80` - [FCR] Support ST HAL
* :github:`79` - [FCR] Support NXP HAL
* :github:`78` - [FCR] Support Raspberry Pi Pico HAL
* :github:`77` - [FCR] Support Atmel HAL
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
