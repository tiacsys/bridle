.. _bridle_release_notes_370:

|BRIDLE| 3.7.0 Release Notes
############################

This project demonstrate the integration of |TIAC| support in open
source projects, like the Zephyr RTOS, with libraries and source code
for applications. It is not yet intended or supported by |TIAC| for
product development.

Highlights
**********

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
     - v3.7-branch
     - v3.7.0-rc1
   * - | `tiac-ubxlib`_
       | (`u-blox-ubxlib`_)
     - | *geographiclib*
     - | tiacsys/main
       | (main)
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
     - | tiacsys/v3.7-branch
       | (v3.7-branch)
     - v3.7.0

.. note – component list fetched from 'west list -a -f "{name:24} {groups:40}"'

Supported boards
****************

* Arduino/Genuino Zero
* PicoBoy Mini-Handheld
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

* Allow users to still specify any old board name, and let Bridel together with
  the Zephyr build system (board validation) to select the new board name.
* Rename board ``tiac_magpie`` to ``magpie_f777ni`` and mark the old name as
  deprecated.
* Adapt **new identifier from Hardware Model v2** for *snippets*, *tests*
  and *samples*.
* Add more shields:

  * *Grove Sensor Shields*:

    * **Grove Temperature, Humidity and Barometer Sensor V1.0 (BME280)** by Seeed Studio
    * **Grove Temperature and Barometer Sensor V1.0 (BMP280)** by Seeed Studio
    * **Grove High Precision Enviromental Sensor V1.0 (DPS310)** by Seeed Studio

  * *Raspberry Pi Pico LCD Shields*:

    * **Pico LCD 1.44** shield by PiMoroni (*PIM543*, "Pico Display Pack")
    * **Pico LCD 2** shield by PiMoroni (*PIM580*, "Pico Display Pack 2.0")

    * **Pico LCD 1.54** shield by Spotpear

    * **Pico LCD 0.96** shield by Waveshare
    * **Pico LCD 1.3** shield by Waveshare
    * **Pico LCD 1.44** shield by Waveshare
    * **Pico LCD 1.8** shield by Waveshare
    * **Pico ResTouch LCD 2.8** shield by Waveshare

  * *Raspberry Pi Pico Breadboard Shields*:

    * *EP-0164* **Pico Breadboard Kit** shield by 52Pi (GeeekPi)
    * *EP-0172* **Pico Breadboard Kit Plus** shield by 52Pi (GeeekPi)

  * *SC16IS75x Breakout Boards as Shields*:

    * *BOB-09981* **I2C/SPI-to-UART Breakout - SC16IS750** shield by SparkFun
    * *CJMCU-750* **I2C/SPI-to-UART Breakout - SC16IS750** shield by CJMCU
      (Changjiang Intelligent Technology Co., Ltd.)
    * *GT-SC16IS750* **I2C/SPI-to-UART Breakout - SC16IS750** shield by Q-Baihe
      (Wuhan Lilly Electronics Co., Ltd.)
    * *CJMCU-752* **I2C/SPI-to-UART Breakout - SC16IS752** shield by CJMCU
      (Changjiang Intelligent Technology Co., Ltd.)

  * *NXP SC18IS604-EVB as Shield*:

    * *SC18IS604-EVB* **SPI-to-I2C Evaluation Kit - SC18IS604** shield by NXP

  * *TiaC SC18IS604 Arduino as Shield*:

    * *TCS-604-ARD* **SPI-to-I2C for Arduino - SC18IS604** shield by TiaC

* Provide **WS2812** digital RGB LED **matrix** as standard **Zephyr display**
  on following boards or shields:

  * *Waveshare RP2040-Matrix*
  * *Waveshare Pico RGB LED Shield*

The following sections provide detailed lists of changes by component.

* PROJECT UPDATE to `Zephyr Project`_ v3.7

Build Infrastructure
====================

Take over the new build principles from Zephyr:

* Update of the minimum requirements for Python to version 3.10.
* Update of the minimum requirements for CMake to version 3.20.5.
* Use the new upstream *MIPI DBI driver class* for all *ST7735R* based displays.
* Use the new upstream *MIPI DBI driver class* for all *ST7789V* based displays.
* Convert all Bridle *boards* and *SoCs* to the **new Hardware Model v2**.
* Hook up ``board.cmake`` in Bridle's board extension folder.
* Hook up ``Kconfig.defconfig`` in Bridle's board extension folder.
* With the new ``Kconfig.defconfig`` hookup in the Bridle board extension
  folder, all static configurations can be removed and Kconfig can work more
  sensitively, e.g. only influence the log level in the USB subsystem if the
  USB stack is really activated.
* Add the *Ambiq Micro* HAL to support the new *Apollo 4* SoC in Zephyr upstream
  with Bridle's common test suite ``bridle/tests/bridle/common``.
* Add the *Intel* HAL and the *ACPI Component Architecture* library to support
  Bridle's common test suite ``bridle/tests/bridle/common`` also for most of the
  :zephyr:ref:`Intel boards found in Zephyr upstream <boards-intel>`.
* Adoption of patch and compliance checks from Zephyr upstream for the **new
  Hardware Model v2** with slight adjustments for Bridle:

  * ``BRIDLE_BASE`` as an additional magic string ``<bridle-base>``
  * Bridle with additional external module handling (``MODULE_EXT_ROOT``)
  * use Bridle's ``checkpatch.pl`` and ``.checkpatch.conf``
  * use Bridle's ``spelling.txt`` and ``typedefsfile``
  * use Bridle's ``.gitlint``
  * use Bridle's ``.yamllint``

* Add more Zephyr upstream projects to West submanifest as needed by Zephyr
  upstream test suites:

  * HAL modules for: Analog Devices (formerly Maxim)
  * HAL modules for: Arm Ethos-U NPUs
  * HAL modules for: Würth Elektronik

* Use the Twister CLI argument ``--alt-config-root`` to reuse Zephyr upstream
  test suites for building all drivers together with Bridle's own snippets.

Documentation
=============

1. Export ``ZEPHYR_BASE`` as environment variable to make the Sphinx extension
   ``autodoc`` for the ``pytest-twister-harness`` happy.
2. Update all output messages in documentation to be in sync with the upcoming
   Bridle version v3.7.0, based on Zephyr v3.7 (samples and tests).

Issue Related Items
*******************

These GitHub issues were addressed since project bootstrapping:

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
