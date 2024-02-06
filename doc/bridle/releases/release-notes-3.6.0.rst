.. _bridle_release_notes_360:

|BRIDLE| 3.6.0 Release Notes (Working draft)
############################################

This project demonstrate the integration of |TIAC| support in open
source projects, like the Zephyr RTOS, with libraries and source code
for applications. It is not yet intended or supported by |TIAC| for
product development.

Highlights
**********

* :brd:`NOT YET, tbd.`

* Add the u-blox library (**ubxlib**) and provide a simple GNSS example.
* Add *Raspberry Pi Pico* **LCD** *Shields*.
* Add *Raspberry Pi Pico* **LED** *Shields*.
* Add *Raspberry Pi Pico* **TEST** *Shields*.
* Add *DTS bindings* for  **pwm-buzzers** and **pwm-servos**.
* Support the *Cytron Maker RP2040* family.
* Support *The PicoBoy* mini-handheld.
* Use board extensions.

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
     - main
     -
   * - | `tiac-ubxlib`_
       | (`u-blox-ubxlib`_)
     - | geographiclib
     - | tiacsys/main
       | (main)
     -
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
     - | tiacsys/main
       | (main)
     -

Supported boards
****************

:brd:`NOT YET, tbd.`

* Arduino/Genuino Zero
* PicoBoy Mini-Handheld
* Cytron Maker Nano RP2040
* Cytron Maker Pi RP2040
* NXP MIMXRT1010-EVK
* NXP MIMXRT1060-EVK
* Raspberry Pi Pico and Pico W
* Seeed Studio XIAO SAMD21 (Seeeduino XIAO)
* Seeeduino Cortex-M0+
* Seeeduino Lotus Cortex-M0+
* ST Nucleo F2xxxx
* ST Nucleo F3xxxx / L4xxxx
* ST Nucleo F6xxxx
* TiaC Magpie STM32F777NIHx
* Waveshare RP2040 (series of mini and pico sized boards)

Supported shields
*****************

:brd:`NOT YET, tbd.`

* Seeed Studio Grove Interconnect Shields
* Grove Button Shields
* Grove LED Shields
* Raspberry Pi Pico LCD Shields
* Raspberry Pi Pico LED Shields
* Raspberry Pi Pico TEST Shields
* Waveshare LCD Modules
* Waveshare Pico 10-DOF IMU Sensor
* Waveshare Pico Environment Sensor

Supported snippets
******************

:brd:`NOT YET, tbd.`

* USB Console Snippet (usb-console)
* PWM Servomotor Preset Snippet (pwm-servo)
* CAN timing adjustments (can-timing-adj)

Change log
**********

:brd:`NOT YET, tbd.`

* When ``getopt()`` is active (``CONFIG_SHELL_GETOPT=y``), the Zephyr shell
  is not parsing command handler to print help message. It must be done
  explicitly inside the command implementation.
* Update GPIO to use ``DT_HAS_<compat>_ENABLED`` Kconfig symbol to expose the
  driver and enable it by default based on devicetree.
* Use *Board extensions* to extended Zephyr upstream board configurations.
  In some situations, certain hardware description or choices can not be added
  in the upstream Zephyr repository, but they can be in a downstream project,
  where custom bindings or driver classes can also be created. This feature may
  also be useful in development phases, when the board skeleton lives upstream,
  but other features are developed in a downstream module. Thus the extensions
  spinned around in different shields or snippets were centraliced as board
  extensions, e.g. the special *Raspberry Pi Pico R3 edge connector binding*.
* Remove special board extensions for Nucleo F303RE/F401RE, NXP MIMXRT1010-EVK,
  and RPi Pico from the *Grove Interconnect Shield*.
* Convert all RP2040 based boards to the new *Clock Controller* support.
* Adds the new DTS binding *pwm-buzzers*, which can be used in the same way as
  the Zephyr upstream binding *pwm-leds*; but here for simple buzzers, each
  used by a dedicated PWM channel to output simple digital sounds. A simple
  buzzer sample is now also part of Bridle. This can be used for simple music
  playback via PWM.
* Adds the new DTS binding *pwm-servos* to combine several PWM channels in one
  node and make different numbers of servomotors known via alias entries. As
  long as there is no stable servo motor or motion API in Zephyr or Bridle,
  this binding will remain in flux and will not be finished.
* Add the new *PWM Servomotor Preset Snippet (pwm-servo)* for quite board
  specific preperations of the standard Zephyr Servomotor sample. Add support
  for the following boards:

  * Cytron Maker Pi RP2040

* Add more boards to the *USB Console Snippet (usb-console)*:

  * Cytron Maker Nano RP2040
  * Cytron Maker Pi RP2040
  * NXP MIMXRT1010-EVK
  * NXP MIMXRT1060-EVK
  * Raspberry Pi Pico (W)
  * Waveshare RP2040-Geek

* Add more shields:

  * *Raspberry Pi Pico TEST Shields*:

    * **Pico ALL GPIO TEST** shield by Spotpear

  * *Raspberry Pi Pico LED Shields*:

    * **Pico RGB LED** shield by Waveshare

  * *Raspberry Pi Pico LCD Shields*:

    * **Pico LCD 1.14** shield by Waveshare
    * **Pico LCD 2** shield by Waveshare
    * **Pico ResTouch LCD 3.5** shield by Waveshare

      *Currently not functional because of missing MIPI DBI device type C,
      SPI with 16-bit support, on Zephyr upstream!*

  * *Waveshare LCD Modules*:

    * **2.4inch LCD Module** as shield by Waveshare

  * Sensor shields:

    * **Pico 10-DOF IMU Sensor** shield by Waveshare
    * **Pico Environment Sensor** shield by Waveshare

* New Zephyr module: support u-blox portable C API **ubxlib** with GNSS sample.

The following sections provide detailed lists of changes by component.

* PROJECT UPDATE to `Zephyr Project`_ v3.6

Build Infrastructure
====================

Take over the new build principles from Zephyr:

:brd:`NOT YET, tbd.`

* Use the new upstream *MIPI DBI API* for all *ILI9xxx* based displays.
* tbd.
* tbd.
* tbd.

Documentation
=============

:brd:`NOT YET, tbd.`

1. All scattered links to external resources and internal references to
   sections in the various docsets (e.g. Bridle or Zephyr) were moved to
   a central location in the files `links.txt` and `shortcuts.txt` and
   thus centralized.
2. Update all output messages in documentation to be in sync with the upcoming
   Bridle version v3.6.0, based on Zephyr v3.6 (samples and tests).

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

* :github:`192` - [FCR] Upgrade to Zephyr SDK 0.16.5
* :github:`187` - [BUG] ubx_gnss sample fails to build
* :github:`185` - [HW] Waveshare Pico 10-DOF IMU Sensor
* :github:`183` - [HW] Waveshare Pico RGB LED
* :github:`177` - [HW] Waveshare Pico Environment Sensor
* :github:`170` - [FCR] Upgrade to Zephyr SDK 0.16.4
* :github:`169` - [HW] The PicoBoy
* :github:`168` - [HW] Waveshare Pico ResTouch LCD 3.5
* :github:`167` - [HW] Waveshare LCD Modules as Shields
* :github:`166` - [HW] Cytron Maker RP2040
* :github:`163` - [FER] USB console support for NXP MIMXRT1010-EVK and MIMXRT1060-EVK
* :github:`162` - [HW] Raspberry Pi Pico TEST Shields
* :github:`161` - [HW] Raspberry Pi Pico LCD Shields
* :github:`160` - [HW] Waveshare RP2040-Geek
* :github:`156` - [FCR] Add the u-blox library (ubxlib) as Zephyr module
* :github:`155` - [FCR] Use board extensions to fix upstream declarations
* :github:`152` - [FER] Support filtering by board vendor
* :github:`151` - [FER] Harmonize Grove PWM mapping over all SAMD21 based Arduino boards
* :github:`148` - [HW] Seeeduino Cortex-M0+ board support
* :github:`137` - [FCR] Bump to Zephyr v3.5
* :github:`139` - [FER] Bump to Doxygen v1.9.8
* :github:`136` - [FCR] Bump to Zephyr SDK 0.16.3
* :github:`128` - [FER] Provide USB console by snippets instead of specific board revision
* :github:`127` - [FER] Provide CAN timing tweak for TiaC Magpie by snippets instead of a shield
* :github:`125` - [BUG] Nightly QA integration test fails (convert to ``stm32-bxcan``)
* :github:`122` - [HW] Waveshare RP2040
* :github:`120` - [BUG] Nightly QA integration test fails
* :github:`118` - [BUG] QA Integration Test fails
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
