.. _bridle_release_notes_410:

|BRIDLE| 4.1.0 Release Notes (Working draft)
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
     - **Group** : *Imports*
     - Branch
     - Tag
   * - `tiac-bridle`_
     -
     - v4.1-branch
     - v4.1.0
   * - | `tiac-ubxlib`_
       | (`u-blox-ubxlib`_)
     - | *geographiclib*
     - | 62c0021cbf079b43cdd9a219e9b10b49ea616e19
       | (master)
     -
   * - | `tiac-zephyr`_
       | (`zephyr-core`_)
     - | *acpica*
       | *liblc3*
       | *loramac-node*
       | *lvgl*
       | *mcuboot*
       | *open-amp*
       | *openthread*
       | *picolibc*
       | **hal** : *cmsis*
       | **hal** : *hal_adi*
       | **hal** : *hal_altera*
       | **hal** : *hal_ambiq*
       | **hal** : *hal_atmel*
       | **hal** : *hal_espressif*
       | **hal** : *hal_ethos_u*
       | **hal** : *hal_gigadevice*
       | **hal** : *hal_infineon*
       | **hal** : *hal_intel*
       | **hal** : *hal_microchip*
       | **hal** : *hal_nordic*
       | **hal** : *hal_nuvoton*
       | **hal** : *hal_nxp*
       | **hal** : *hal_openisa*
       | **hal** : *hal_quicklogic*
       | **hal** : *hal_renesas*
       | **hal** : *hal_rpi_pico*
       | **hal** : *hal_silabs*
       | **hal** : *hal_st*
       | **hal** : *hal_stm32*
       | **hal** : *hal_tdk*
       | **hal** : *hal_telink*
       | **hal** : *hal_ti*
       | **hal** : *hal_wurthelektronik*
       | **hal** : *hal_xtensa*
       | **hal** : *libmetal*
       | **fs** : *fatfs*
       | **fs** : *littlefs*
       | **tee** : *trusted-firmware-a*
       | **tee** : *trusted-firmware-m*
       | **crypto** : *mbedtls*
       | **crypto** : *tinycrypt*
       | **debug** : *mipi-sys-t*
       | **debug** : *segger*
       | **tools** : *edtt*
       | **tools** : *net-tools*
       | **optional** : *canopennode*
       | **optional** : *chre*
       | **optional** : *psa-arch-tests*
       | **optional** : *tf-m-tests*
     - | tiacsys/v4.1.0
       | (v4.1-branch)
     - v4.1.0

.. note – component list fetched from 'west list -a -f "{name:24} {groups:40}"'

Supported boards
****************

:brd:`NOT YET, tbd.`

* Arduino/Genuino Zero
* PicoBoy Mini-Handheld
* PicoBoy Color (PBC) Mini-Handheld
* Cytron Maker Nano RP2040
* Cytron Maker Pi RP2040
* NXP MIMXRT1010-EVK
* NXP MIMXRT1060-EVK
* NXP MIMXRT1170-EVK/EVKB (CM7)
* Nordic nRF52840 DK
* Nordic nRF9160 DK
* Raspberry Pi Pico and Pico W
* Seeeduino Cortex-M0+
* Seeeduino Lotus Cortex-M0+
* ST Nucleo F2xxxx
* ST Nucleo F3xxxx / L4xxxx
* ST Nucleo F4xxxx
* ST Nucleo F6xxxx
* ST Nucleo F7xxxx
* TiaC Magpie F777NI (former TiaC Magpie STM32F777NIHx)
* Waveshare RP2040 (series of mini and pico sized boards)
* XIAO SAMD21 (former Seeed Studio XIAO SAMD21), also known as Seeeduino XIAO

Supported shields
*****************

:brd:`NOT YET, tbd.`

* Seeed Studio Grove Interconnect Shields
* Grove Button Shields
* Grove LED Shields
* Grove Sensor Shields
* Raspberry Pi Pico Clock Shields
* Raspberry Pi Pico LCD Shields
* Raspberry Pi Pico LED Shields
* Raspberry Pi Pico TEST Shields
* Waveshare LCD Modules
* Waveshare Pico 10-DOF IMU Sensor
* Waveshare Pico Environment Sensor
* SC16IS75x Breakout Boards
* NXP SC18IS604-EVB
* TiaC SC18IS604 Arduino

Supported snippets
******************

:brd:`NOT YET, tbd.`

* USB Console Snippet (usb-console)
* PWM Servomotor Preset Snippet (pwm-servo)
* Delete Default Devicetree Aliases Snippet (del-default-aliases)
* BME280 Sensor Sample Tweaks (samples-sensor-bme280-tweaks)
* CAN timing adjustments (can-timing-adj)
* Watchdog timing adjustments (wdt-timing-adj)
* Build all Display drivers test adjustments (tstdrv-bldall-display-adj)
* Build all GPIO drivers test adjustments (tstdrv-bldall-gpio-adj)
* Build all I2C drivers test adjustments (tstdrv-bldall-i2c-adj)
* Build all MFD drivers test adjustments (tstdrv-bldall-mfd-adj)
* Build all RTC drivers test adjustments (tstdrv-bldall-rtc-adj)
* Build all Sensor drivers test adjustments (tstdrv-bldall-sensor-adj)
* Build all UART drivers test adjustments (tstdrv-bldall-uart-adj)

Change log
**********

:brd:`NOT YET, tbd.`

* Remove our own Maxim DS3231 RTC and temperature sensor driver, use the new
  Zephyr upstream driver instead.
* Support new revision C of NXP MIMXRT1060-EVK.
* Use new unified DTS property names.

The following sections provide detailed lists of changes by component.

:brd:`NOT YET, tbd.`

* tbd.
* tbd.
* tbd.

* PROJECT UPDATE to `Zephyr Project`_ v4.1.0

Build Infrastructure
====================

:brd:`NOT YET, tbd.`

* tbd.
* tbd.
* Remove ``xtools`` toolchain variant references. The ``xtools`` toolchain
  variant has been deprecated since Zephyr v3.3.0 and now removed.
* Enable support for the TDK HAL in the West manifest. This HAL is needed by
  Zephyr upstream test suite to build all sensor drivers.

Documentation
=============

:brd:`NOT YET, tbd.`

1. tbd.
2. tbd.
3. Porting to new doxyrunner. The Sphinx extension ``doxyrunner`` now supports
   multiple Doxygen projects. Adapt it for the original upstream Zephyr API
   and our own Bridle downstream API documentation.
4. Update all output messages in documentation to be in sync with the upcoming
   Bridle version v4.1.0, based on Zephyr v4.1 (samples and tests).

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

* :github:`296` - [HW] The PicoBoy Color as additional board variant
* :github:`277` - [HW] Grove Dual and LED Button Module as Shield
* :github:`275` - [BUG] Lost Bridle's document version selector
* :github:`274` - [FCR] Bump to Zephyr v4.0
* :github:`272` - [BUG] build all Bridle samples test runs into ``devicetree error``
* :github:`271` - [BUG] build all GPIO drivers test runs into ``devicetree error``
* :github:`270` - [BUG] Can't build the documentation sets for Bridle and Zephyr anymore
* :github:`261` - [HW] TiaC SC18IS604 Arduino as Shield
* :github:`258` - [HW] NXP SC18IS604-EVB as Shield
* :github:`257` - [HW] SC16IS75x Breakout Boards as Shields
* :github:`254` - [FCR] Bump to Zephyr v3.7
* :github:`252` - [FCR] Upgrade to Zephyr SDK 0.16.8
* :github:`247` - [HW] NXP SC18IS604 SPI to I2C bridge
* :github:`246` - [HW] NXP SC16IS75x series I2C/SPI to UART/GPIO bridge
* :github:`244` - [HW] Spotpear Raspberry Pi Pico LCD Modules as Shields
* :github:`242` - [HW] 52Pi (GeeekPi) Pico Breadboard Kit -/Plus (EP-0164/0172)
* :github:`239` - [HW] PiMoroni Raspberry Pi Pico LCD Modules as Shields
* :github:`234` - [BUG] boards and shields with LCD do not support the new MIPI-DBI mode
* :github:`233` - [HW] Waveshare Raspberry Pi Pico LCD Modules as Shields
* :github:`231` - [BUG] build Zephyr docset fails
* :github:`229` - [BUG] magpie_f777ni: wdt_basic_api/drivers.watchdog.stm32wwdg FAILED
* :github:`227` - [BUG] Unable to build any application referencing bridle version information
* :github:`222` - [BUG] unsatisfied dependencies by static Kconfig elements
* :github:`217` - [FCR] Convert board ``arduino_zero`` to board extension
* :github:`216` - [FCR] Convert all SOCs to new HWMv2
* :github:`215` - [BUG] ubxlib: missing header ``u_timeout.h``
* :github:`214` - [FER] Convert all boards to new HWMv2
* :github:`205` - [FCR] Bump to Zephyr v3.6
* :github:`202` - [FER] Make the u-blox library GNSS example fit for demonstration
* :github:`200` - [FCR] Support for MCUXpresso IDE (Arm GNU Toolchain)
* :github:`198` - [FCR] Support for STM32CubeCLT (GNU tools for STM32)
* :github:`195` - [FCR] Upgrade to Arm GNU toolchain 13.2.rel1
* :github:`192` - [FCR] Upgrade to Zephyr SDK 0.16.5
* :github:`187` - [BUG] ubx_gnss sample fails to build
* :github:`185` - [HW] Waveshare Pico 10-DOF IMU Sensor
* :github:`183` - [HW] Waveshare Pico RGB LED
* :github:`177` - [HW] Waveshare Pico Environment Sensor
* :github:`176` - [HW] Waveshare Pico Clock Green
* :github:`170` - [FCR] Upgrade to Zephyr SDK 0.16.4
* :github:`169` - [HW] The PicoBoy
* :github:`168` - [HW] Waveshare Pico ResTouch LCD 3.5
* :github:`167` - [HW] Waveshare LCD Modules as Shields
* :github:`166` - [HW] Cytron Maker RP2040
* :github:`163` - [FER] USB console support for NXP MIMXRT1010-EVK and MIMXRT1060-EVK
* :github:`162` - [HW] Raspberry Pi Pico TEST Shields
* :github:`161` - [HW] Raspberry Pi Pico LCD Shields
* :github:`160` - [HW] Waveshare RP2040-Geek
* :github:`159` - [BUG] check_compliance.py needs support for Bridle's downstream modules folder
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
