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
* Seeed Studio XIAO SAMD21 (Seeeduino XIAO)
* Seeeduino Lotus Cortex-M0+
* TiaC Magpie STM32F777NIHx

Change log
**********

The following sections provide detailed lists of changes by component.

* Add new boards:

  * :ref:`arduino_zero`, improved copy from Zephyr
  * :ref:`seeed_xiao_samd21`, improved copy from Zephyr
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
    * :ref:`seeeduino_xiao`
    * :ref:`seeed_xiao_samd21`

  * :ref:`grove_button_shield`
  * :ref:`grove_led_shield`

* Add :ref:`tests-shields`

  * :doc:`/tests/shields/grove/dts_bindings/README`
  * :doc:`/tests/shields/grove_btn/dts_bindings/README`
  * :doc:`/tests/shields/grove_led/dts_bindings/README`
  * :doc:`/tests/shields/x_grove_testbed/dts_bindings/README`

* Add new DTS bindings:

  * :dtcompatible:`adafruit,stemma-connector`
  * :dtcompatible:`adafruit,stemmaqt-connector`
  * :dtcompatible:`dfrobot,gravity-connector`
  * :dtcompatible:`digilent,pmod-header`
  * :dtcompatible:`generic-pin-header`
  * :dtcompatible:`nxp,pca9554`
  * :dtcompatible:`nxp,pca9555`
  * :dtcompatible:`raspberrypi,pico-header-r3`
  * :dtcompatible:`seeed,grove-laced-if`
  * :dtcompatible:`seeed,grove-connector`
  * :dtcompatible:`sparkfun,qwiic-connector`
  * :dtcompatible:`st,mems-dil24-socket`

* Add new drivers:

  * PCA9554 I2C-based GPIO chip (:kconfig:option:`CONFIG_GPIO_PCA9554`)
  * PCA9555 I2C-based GPIO chip (:kconfig:option:`CONFIG_GPIO_PCA9555`)

* Add new samples:

  * :ref:`button-sample`, improved copy from Zephyr with feature toggle
    for either "polling thread" or "interrupt callback"

* PROJECT UPDATE to `Zephyr Project`_ v3.3

Build Infrastructure
====================

Take over the new build principles from Zephyr:

* Use the new RST role :code:`dtcompatible` that is provided
  as Sphinx extension by Zephyr:

  * Replace all (now obsolete) Inter-Sphinx references such as
    :code:`:ref:`devicetree:dtbinding_vendor_thing`` to the new
    RST role :code:`:dtcompatible:`vendor,thing``.

* Remove the useless sub-folder ``services``, services should be placed
  below ``subsys``.

* Use original glue code for external 3rd party Zephyr modules that will
  be maintained inside the Bridle repository.

Documentation
=============

1. Update all output messages in documentation to be in sync with the upcoming
   Bridle version v3.3.1, based on Zephyr v3.3 (samples and tests).
2. Following latest Zephyr Coding Guidelines and update terms, see
   :ref:`zephyr:coding_guideline_inclusive_language`.

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

* :github:`99` - [FER] Need a fancy blinky example for novice developer
* :github:`96` - [HW] Grove Interconnect Shields for Seeeduino XIAO
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
