.. _bridle_release_notes_351:

|BRIDLE| 3.5.1 Release Notes
############################

This project demonstrate the integration of |TIAC| support in open
source projects, like the Zephyr RTOS, with libraries and source code
for applications. It is not yet intended or supported by |TIAC| for
product development.

Highlights
**********

* Support for the Waveshare RP2040 Geek board, too.

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
     - v3.5-branch
     - v3.5.1
   * - | `tiac-zephyr`_
       | (`zephyr-core`_)
     - | canopennode
       | chre (optional)
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
       | psa-arch-tests (optional)
       | segger
       | tf-m-tests (optional)
       | tinycrypt
       | trusted-firmware-a
       | trusted-firmware-m
     - | tiacsys/v3.5-branch
       | (v3.5-branch)
     - v3.5.0

Supported boards
****************

* Arduino/Genuino Zero
* Seeed Studio XIAO SAMD21 (Seeeduino XIAO)
* Seeeduino Cortex-M0+
* Seeeduino Lotus Cortex-M0+
* TiaC Magpie STM32F777NIHx
* Waveshare RP2040 (series of mini and pico sized boards)

Supported shields
*****************

* Seeed Studio Grove Interconnect Shields
* Grove Button Shields
* Grove LED Shields

Supported snippets
******************

* USB Console Snippet (usb-console)
* CAN timing adjustments (can-timing-adj)

Change log
**********

* When ``getopt()`` is active (``CONFIG_SHELL_GETOPT=y``), the Zephyr shell
  is not parsing command handler to print help message. It must be done
  explicitly inside the command implementation.
* All tests for *Grove Interconnect, Button, and LED Shields* converted to be
  more generic and guided by a list of well-known integration platforms
  currently supported by Bridle. This leads to a super-matrix of test suites
  and cases, thus all invalid board/shield conditions, not yet well supported
  boards or not finished implementations are now excluded by the new global
  quarantine list in `tests/quarantine.yaml`.
* All SAMD21 targets doesn't yet support the LED shell command against the
  internal LED driver API properly in case of mixed GPIO and PWM LEDs on same
  I/O pin (shared pin function), thus related :kconfig:option:`CONFIG_LED` and
  :kconfig:option:`CONFIG_LED_SHELL` were disable for this boards as default.
* The *Grove Interconnect Shield* demonstration has been expanded to also
  include the *Raspberry Pi Pico W* and *Waveshare RP2040-LCD-0.96* boards
  on the *Grove Shield for Pi Pico V1*.
* In conjunction with the new Twister upstream support for filtering tests
  by board manufacturer or vendor, Bridle now also provides the vendor entry
  for each supported board.

The following sections provide detailed lists of changes by component.

* PROJECT UPDATE to `Zephyr Project`_ v3.5

Build Infrastructure
====================

Take over the new build principles from Zephyr:

* Update Github actions to their latest versions to fix warnings about
  Node.js 16 actions are deprecated.

  * actions/labeler@v5
  * actions/stale@v9
  * actions/cache@v4
  * actions/checkout@v4
  * actions/github-script@v7
  * actions/upload-artifact@v4
  * mikepenz/action-junit-report@v4

Documentation
=============

1. Update all output messages in documentation to be in sync with the upcoming
   Bridle version v3.5.1, based on Zephyr v3.5 (samples and tests).

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

* :github:`160` - [HW] Waveshare RP2040-Geek
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
