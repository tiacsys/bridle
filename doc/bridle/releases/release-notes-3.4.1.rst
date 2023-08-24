.. _bridle_release_notes_341:

|BRIDLE| 3.4.1 Release Notes (Working draft)
############################################

This project demonstrate the integration of |TIAC| support in open
source projects, like the Zephyr RTOS, with libraries and source code
for applications. It is not yet intended or supported by |TIAC| for
product development.

Highlights
**********

* |BRIDLE| as CMake package for freestanding projects.
* West manifest harmonized with upstream.

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
       | hal_gigadevice
       | hal_infineon
       | hal_microchip
       | hal_nordic
       | hal_nuvoton
       | hal_nxp
       | hal_openisa
       | hal_quicklogic
       | hal_renesas
       | hal_rpi_pico
       | hal_silabs
       | hal_st
       | hal_stm32
       | hal_telink
       | hal_ti
       | hal_xtensa
       | libmetal
       | liblc3
       | littlefs
       | loramac-node
       | lvgl
       | mbedtls
       | mcuboot
       | mipi-sys-t
       | net-tools
       | open-amp
       | openthread
       | picolibc
       | psa-arch-tests
       | segger
       | tf-m-tests
       | tinycrypt
       | trusted-firmware-a
       | trusted-firmware-m
     - | tiacsys/v3.4-branch
       | (v3.4-branch)
     - v3.4.1

Supported boards
****************

* Arduino/Genuino Zero
* Seeed Studio XIAO SAMD21 (Seeeduino XIAO)
* Seeeduino Lotus Cortex-M0+
* TiaC Magpie STM32F777NIHx

Supported shields
*****************

* Seeed Studio Grove Interconnect Shields
* Grove Button Shields
* Grove LED Shields

Change log
**********

* |BRIDLE| can now properly find in freestanding CMake projects with
  :code:`find_package(Bridle …)`. The CMake package configuration now
  falls back to Zephyr immediately and let it include again by Zephyr
  build configuration.
* All tests and samples use now this mechanic to find |BRIDLE|.
* The Seeed Studio Grove Interconnect Shields now supports the Seeeduino
  Lotus Cortex-M0+ board too, although the board already provides its own
  Grove connectors beside the Arduino header.

The following sections provide detailed lists of changes by component.

* PROJECT UPDATE to `Zephyr Project`_ v3.4

Build Infrastructure
====================

Take over the new build principles from Zephyr:

* Use West submanifest for upstream Zephyr and add multiple more projects:

  * HAL modules for: Renesas, Nuvoton, QuickLogic, Microchip, OpenISA,
    Telink, Texas Instruments, Infineon, SiLabs, GigaDevice
  * secure MCU boot module
  * Arm PSA tests module
  * TF-M tests module
  * TF-M module
  * TF-A module

Documentation
=============

1. Update all output messages in documentation to be in sync with the upcoming
   Bridle version v3.4.1, based on Zephyr v3.4 (samples and tests).

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

* :github:`116` - [BUG] Grove Shields DTS Binding test suites fail for seeeduino_lotus@usbcons
* :github:`115` - [BUG] Bridle Common (core) Testing fails since v3.4
* :github:`113` - [FER] Use sub-manifests for 3rd party projects
* :github:`112` - [FCR] Support Renesas HAL
* :github:`106` - [FER] Snippets
* :github:`105` - [FCR] Bump to Zephyr v3.4
* :github:`104` - [BUG] Bridle CMake Package not usable in Freestanding mode
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
