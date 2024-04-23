.. _picoboy_board:

The PicoBoy
###########

The PicoBoy is a powerful mini handheld measuring just 3×5 ㎝. It is suitable
for learning programming, developing your own games or simply playing with it.
All you need is a PC, the PicoBoy and a USB-C cable. As the PicoBoy based on
the `RP2040 SoC`_ by Raspberry Pi Ltd. and is compatible with the
:ref:`zephyr:rpi_pico` programming model and process, there are countless other
tutorials, examples and libraries on the internet to make programming easier.

Board Overview
**************

Hardware
========

.. include:: hardware.rsti

Positions
=========

.. include:: positions.rsti

Pinouts
=======

The peripherals of the `RP2040 SoC`_ can be routed to various pins on
the board. The configuration of these routes can be modified through
:ref:`DTS <zephyr:devicetree>`. Please refer to the datasheet to see
the possible routings for each peripheral. The default assignments
for the PicoBoy on-board wiring is defined below. There are no edge
connectors, headers or solder pads with additional signals routed to
outside of the board.

.. include:: pinouts.rsti

Supported Features
******************

Similar to the :ref:`zephyr:rpi_pico` the PicoBoy board configuration
supports the following hardware features:

.. list-table::
   :header-rows: 1

   * - Peripheral
     - Kconfig option
     - Devicetree compatible
     - Zephyr API
   * - PINCTRL
     - :kconfig:option:`CONFIG_PINCTRL`
     - :dtcompatible:`raspberrypi,pico-pinctrl`
     - :ref:`zephyr:pinctrl_api`
   * - GPIO
     - :kconfig:option:`CONFIG_GPIO`
     - :dtcompatible:`raspberrypi,pico-gpio`
     - :ref:`zephyr:gpio_api`
   * - USB Device
     - :kconfig:option:`CONFIG_USB_DEVICE_STACK`
     - :dtcompatible:`raspberrypi,pico-usbd`
     - :ref:`zephyr:usb_api`
   * - I2C
     - :kconfig:option:`CONFIG_I2C`
     - | :dtcompatible:`raspberrypi,pico-i2c` (!)
       | :dtcompatible:`gpio-i2c`
     - :ref:`zephyr:i2c_api`
   * - SPI
     - :kconfig:option:`CONFIG_SPI`
     - :dtcompatible:`raspberrypi,pico-spi`
     - :ref:`zephyr:spi_api`
   * - PWM
     - :kconfig:option:`CONFIG_PWM`
     - :dtcompatible:`raspberrypi,pico-pwm`
     - :ref:`zephyr:pwm_api`
   * - ADC
     - :kconfig:option:`CONFIG_ADC`
     - :dtcompatible:`raspberrypi,pico-adc`
     - :ref:`zephyr:adc_api`
   * - Temperature (Sensor)
     - :kconfig:option:`CONFIG_SENSOR`
     - :dtcompatible:`raspberrypi,pico-temp` (!!)
     - :ref:`zephyr:sensor_api`
   * - Timer (Counter)
     - :kconfig:option:`CONFIG_COUNTER`
     - :dtcompatible:`raspberrypi,pico-timer`
     - :ref:`zephyr:counter_api`
   * - Watchdog Timer (WDT)
     - :kconfig:option:`CONFIG_WATCHDOG`
     - :dtcompatible:`raspberrypi,pico-watchdog`
     - :ref:`zephyr:watchdog_api`
   * - Flash
     - :kconfig:option:`CONFIG_FLASH`
     - :dtcompatible:`raspberrypi,pico-flash-controller`
     - :ref:`zephyr:flash_api` and
       :ref:`zephyr:flash_map_api`
   * - PIO
     - :kconfig:option:`CONFIG_PIO_RPI_PICO`
     - :dtcompatible:`raspberrypi,pico-pio`
     - N/A
   * - SPI (PIO)
     - :kconfig:option:`CONFIG_SPI`
     - :dtcompatible:`raspberrypi,pico-spi-pio`
     - :ref:`zephyr:spi_api`
   * - DMA
     - :kconfig:option:`CONFIG_DMA`
     - :dtcompatible:`raspberrypi,pico-dma`
     - :ref:`zephyr:dma_api`
   * - CLOCK
     - :kconfig:option:`CONFIG_CLOCK_CONTROL`
     - | :dtcompatible:`raspberrypi,pico-clock-controller`
       | :dtcompatible:`raspberrypi,pico-clock`
     - :ref:`zephyr:clock_control_api`
   * - RESET
     - :kconfig:option:`CONFIG_RESET`
     - :dtcompatible:`raspberrypi,pico-reset`
     - :ref:`zephyr:reset_api`
   * - VREG
     - :kconfig:option:`CONFIG_REGULATOR`
     - :dtcompatible:`raspberrypi,core-supply-regulator`
     - :ref:`zephyr:regulator_api`
   * - NVIC
     - N/A
     - :dtcompatible:`arm,v6m-nvic`
     - Nested Vector :ref:`zephyr:interrupts_v2` Controller
   * - HWINFO
     - :kconfig:option:`CONFIG_HWINFO`
     - N/A
     - :ref:`zephyr:hwinfo_api`

(!) Designware I2C driver has issues:
    The :emphasis:`Raspberry Pi Pico I2C driver` is using the
    :emphasis:`Designware I2C driver` automatically. According to our
    observation, this driver has some :strong:`shortcomings in interrupt
    handling` and :brd:`leads to a dead-lock of the entire runtime system`.
    Also known is the lack of support for 0 byte transfers, which prevents
    a proper I2C device scan. Thus, the :strong:`PicoBoy board` will be
    configured to :strong:`use the simple GPIO-I2C bit-bang driver` as
    long as this driver is not applicable as expected.

    See also: https://github.com/zephyrproject-rtos/zephyr/pull/60427

(!!) Die-Temperature Sensor driver has issues:
     It seems the RP2040 Die-Temperature sensor driver has also race conditions
     and :brd:`leads to a dead-lock of the entire runtime system`. Thus, all
     :strong:`PicoBoy board` will be configured to :strong:`disable this
     sensor` node in DTS explicitly. As a workaround the ADC channel 4 can be
     used, but that result have to convert manually to the corresponding chip
     temperature following the formula that can be found in the
     `RP2040 Datasheet`_, section with title :emphasis:`"Temperature Sensor"`.

Other hardware features are not currently supported by Zephyr. The default
configuration can be found in the following Kconfig file:

- :bridle_file:`boards/jsed/picoboy/picoboy_defconfig`

Board Configurations
====================

The PicoBoy board can be configured only for the following single use cases.

.. rubric:: :command:`west build -b picoboy`

Use the native USB device port with CDC-ACM as Zephyr console and for the shell.

Connections and IOs
===================

The `PicoBoy <PicoBoy Details_>`_ website has detailed information about board
connections. Download the different datasheets there or as linked above on the
positions for more details.

System Clock
============

The `RP2040 <RP2040 SoC_>`_ MCU is configured to use the 12㎒ external crystal
with the on-chip PLL generating the 125㎒ system clock. The internal AHB and
APB units are set up in the same way as the upstream `Raspberry Pi Pico C/C++
SDK`_ libraries.

GPIO (PWM) Ports
================

The `RP2040 <RP2040 SoC_>`_ MCU has 1 GPIO cell which covers all I/O pads and
8 PWM function unit each with 2 channels beside a dedicated Timer unit. On
the |PicoBoy|, only 4 PWM channels are available on the three user LEDs and
the passive magnetic speaker.

ADC/TS Ports
============

The `RP2040 <RP2040 SoC_>`_ MCU has 1 ADC with 4 channels and an additional
fifth channel for the on-chip temperature sensor (TS). The ADC channels 0-3
are no available for any on-board function and may be completely unusable,
but they ar all configured.

Also it is completely unclear if the external voltage reference ADC_VREF
is connected to any voltage level, e.g. to the 3.3V power supply.

SPI Port
========

The `RP2040 <RP2040 SoC_>`_ MCU has 2 SPIs. The serial bus SPI0 is connect
to the on-board OLED display over GP19 (MOSI), GP16 (MISO), GP18 (SCK), and
GP17 (CSn), but only MOSI and SCK is really used for the OLED. The display
chip-select signal will driven as simple GPIO by GP10 and the display itself
does not provide any data out signal (MISO). SPI1 is not available in any
default setup.

I2C Port
========

The `RP2040 <RP2040 SoC_>`_ MCU has 2 I2Cs. The serial bus I2C0 is connect
to the on-board acceleration sensor over GP20 (I2C0_SDA), GP21 (I2C0_SCL).
I2C1 is not available in any default setup.

Serial Port
===========

The `RP2040 <RP2040 SoC_>`_ MCU has 2 UARTs. Neither UART0 nor UART1 are
available in any of the default setups. Then ever a Zephyr serial console
will be needed, the USB port have to be used.

USB Device Port
===============

The `RP2040 <RP2040 SoC_>`_ MCU has a (native) USB device port that can be
used to communicate with a host PC. See the :ref:`zephyr:usb-samples` sample
applications for more, such as the :zephyr:code-sample:`zephyr:usb-cdc-acm`
sample which sets up a virtual serial port that echos characters back to the
host PC. The |PicoBoy| provides the Zephyr console per default on the USB port
as :ref:`zephyr:usb_device_cdc_acm`::

   USB device idVendor=2e8a, idProduct=000a, bcdDevice= 3.06
   USB device strings: Mfr=1, Product=2, SerialNumber=3
   Product: PicoBoy (CDC ACM)
   Manufacturer: JSED (Raspberry Pi)
   SerialNumber: BD774B2618DAAA7D

Programmable I/O (PIO)
**********************

The `RP2040 SoC`_ comes with two PIO periherals. These are two simple
co-processors that are designed for I/O operations. The PIOs run a custom
instruction set, generated from a custom assembly language. PIO programs
are assembled using :program:`pioasm`, a tool provided by Raspberry Pi.
Further informations can be found in the `Raspberry Pi Pico C/C++ SDK`_
document, section with title :emphasis:`"Using PIOASM, the PIO Assembler"`.

Zephyr does not (currently) assemble PIO programs. Rather, they should be
manually assembled and embedded in source code. An example of how this is done
can be found at :zephyr_file:`drivers/serial/uart_rpi_pico_pio.c` or
:zephyr_file:`drivers/spi/spi_rpi_pico_pio.c`.

Programming and Debugging
*************************

Flashing
========

The |PicoBoy| can only be flashed with a UF2 file. There is no SWD connector.

Using UF2
---------

By default, building an app for the |PicoBoy| board will generate a
:file:`build/zephyr/zephyr.uf2` file. If the board is powered on with the
:kbd:`BOOTSEL` button pressed, it will appear on the host as a mass
storage device::

   USB device idVendor=2e8a, idProduct=0003, bcdDevice= 1.00
   USB device strings: Mfr=1, Product=2, SerialNumber=3
   Product: RP2 Boot
   Manufacturer: Raspberry Pi
   SerialNumber: E0C9125B0D9B

The UF2 file should be drag-and-dropped or copied on command line to the
device, which will then flash the |PicoBoy| board.

Each `RP2040 SoC`_ ships the `UF2 compatible <UF2 bootloader_>`_ bootloader
pico-bootrom_, a native support in silicon. The full source for the RP2040
bootrom at pico-bootrom_ includes versions 1, 2 and 3 of the bootrom, which
correspond to the B0, B1 and B2 silicon revisions, respectively.

Note that every time you build a program for the RP2040, the Pico SDK selects
an appropriate second stage bootloader based on what kind of external QSPI
Flash type the board configuration you are building for was giving. There
are |several versions of boot2|_ for different flash chips, and each one is
exactly 256 bytes of code which is put right at the start of the eventual
program binary. On Zephyr the :code:`boot2` versions are part of the
`Raspberry Pi Pico HAL`_ module. Possible selections:

:|CONFIG_RP2_FLASH_AT25SF128A|: :file:`boot2_at25sf128a.S`
:|CONFIG_RP2_FLASH_GENERIC_03H|: :file:`boot2_generic_03h.S`
:|CONFIG_RP2_FLASH_IS25LP080|: :file:`boot2_is25lp080.S`
:|CONFIG_RP2_FLASH_W25Q080|: :file:`boot2_w25q080.S`
:|CONFIG_RP2_FLASH_W25X10CL|: :file:`boot2_w25x10cl.S`

The |PicoBoy| board set this option to |CONFIG_RP2_FLASH_W25Q080|. Further
informations can be found in the `RP2040 Datasheet`_, sections with title
:emphasis:`"Bootrom"` and :emphasis:`"Processor Controlled Boot Sequence"`
or Brian Starkey's Blog article `Pico serial bootloader`_

Debugging
=========

The |PicoBoy| does not provide any SWD connector, thus debugging software
is not possible.

More Samples
************

LED Blinky and Fade
===================

.. rubric:: Red User LED Blinky by GPIO

See also Zephyr sample: :zephyr:code-sample:`zephyr:blinky`.

.. zephyr-app-commands::
   :app: zephyr/samples/basic/blinky
   :board: picoboy
   :build-dir: picoboy
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: Red User LED Blinky by PWM

See also Zephyr sample: :zephyr:code-sample:`zephyr:pwm-blinky`.

.. zephyr-app-commands::
   :app: zephyr/samples/basic/blinky_pwm
   :board: picoboy
   :build-dir: picoboy
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: Red User LED Fade by PWM

See also Zephyr sample: :zephyr:code-sample:`zephyr:fade-led`.

.. zephyr-app-commands::
   :app: zephyr/samples/basic/fade_led
   :board: picoboy
   :build-dir: picoboy
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: Red User LED On/Off by GPIO Button (Joystick ENTER)

See also Zephyr sample: :zephyr:code-sample:`zephyr:button`.

.. zephyr-app-commands::
   :app: zephyr/samples/basic/button
   :board: picoboy
   :build-dir: picoboy
   :west-args: -p
   :goals: flash
   :compact:

Hello Shell on the USB-CDC/ACM Console
======================================

.. rubric:: Hello Shell

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :board: picoboy
   :build-dir: picoboy
   :west-args: -p
   :goals: flash
   :compact:

.. include:: helloshell.rsti

Input dump on the USB-CDC/ACM Console
=====================================

Print the input events related to the five on-board joystick keys using
the :ref:`Input subsystem API <zephyr:input>`. That are:

| :hwftlbl-joy:`UP` : :devicetree:`zephyr,code = <INPUT_KEY_UP>;`
| :hwftlbl-joy:`DOWN` : :devicetree:`zephyr,code = <INPUT_KEY_DOWN>;`
| :hwftlbl-joy:`LEFT` : :devicetree:`zephyr,code = <INPUT_KEY_LEFT>;`
| :hwftlbl-joy:`RIGHT` : :devicetree:`zephyr,code = <INPUT_KEY_RIGHT>;`
| :hwftlbl-joy:`ENTER` : :devicetree:`zephyr,code = <INPUT_KEY_ENTER>;`

See also Zephyr sample: :zephyr:code-sample:`zephyr:input-dump`.

.. rubric:: Joystick Test

.. zephyr-app-commands::
   :app: zephyr/samples/subsys/input/input_dump
   :board: picoboy
   :build-dir: picoboy
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: Simple logging output on target

.. parsed-literal::
   :class: highlight-console notranslate

   \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
   W: BUS RESET
   W: BUS RESET
   \*\*\* Booting Zephyr OS … … … (delayed boot 4000ms) \*\*\*
   Input sample started
   I: input event: dev=gpio_keys        SYN type= 1 code=103 value=1
   I: input event: dev=gpio_keys        SYN type= 1 code=103 value=0
   I: input event: dev=gpio_keys        SYN type= 1 code=108 value=1
   I: input event: dev=gpio_keys        SYN type= 1 code=108 value=0
   I: input event: dev=gpio_keys        SYN type= 1 code=105 value=1
   I: input event: dev=gpio_keys        SYN type= 1 code=105 value=0
   I: input event: dev=gpio_keys        SYN type= 1 code=106 value=1
   I: input event: dev=gpio_keys        SYN type= 1 code=106 value=0
   I: input event: dev=gpio_keys        SYN type= 1 code= 28 value=1
   I: input event: dev=gpio_keys        SYN type= 1 code= 28 value=0

Sounds from the speaker on the USB-CDC/ACM Console
==================================================

.. rubric:: Speaker Test

.. image:: img/speaker.jpg
   :align: right
   :alt: PicoBoy Speaker Test

The sample is prepared for the on-board :hwftlbl-spk:`PWM_SPEAKER` connected
to the PWM channel at :rpi-pico-pio:`GP15` / :rpi-pico-pwm:`PWM15` (PWM7CHB).

The PWM period is 880 ㎐, twice the concert pitch frequency of 440 ㎐.

.. literalinclude:: ../core_speaker.dtsi
   :caption: core_speaker.dtsi
   :language: DTS
   :encoding: ISO-8859-1
   :emphasize-lines: 3,11,18
   :linenos:
   :start-at: / {

Invoke :program:`west build` and :program:`west flash`:

.. zephyr-app-commands::
   :app: bridle/samples/buzzer
   :board: picoboy
   :build-dir: picoboy
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: Simple test execution on target

#. play a beep
#. play a folk song
#. play a chrismas song

.. parsed-literal::
   :class: highlight-console notranslate

   :bgn:`uart:~$` **buzzer beep**
   :bgn:`uart:~$` **buzzer play folksong**
   :bgn:`uart:~$` **buzzer play xmastime**

Display Test and Demonstration
==============================

The following samples work with the chosen display. That is:

| :hwftlbl-scr:`OLED` : :devicetree:`chosen { zephyr,display = &oled_panel; };`
| :hwftlbl-scr:`SH1106` : :devicetree:`oled_panel: &sh1106_128x64 {};`

.. rubric:: Devicetree compatible

- :dtcompatible:`zephyr,lvgl-keypad-input` with devicetree relation
  :devicetree:`lvgl_keypad: lvgl-keypad { input = <&gpio_keys>; };`

  | :hwftlbl-joy:`UP` :
    :devicetree:`input-codes = <INPUT_KEY_UP>;` :
    :devicetree:`lvgl-codes = <LV_KEY_UP>;`
  | :hwftlbl-joy:`DOWN` :
    :devicetree:`input-codes = <INPUT_KEY_DOWN>;` :
    :devicetree:`lvgl-codes = <LV_KEY_DOWN>;`
  | :hwftlbl-joy:`LEFT` :
    :devicetree:`input-codes = <INPUT_KEY_LEFT>;` :
    :devicetree:`lvgl-codes = <LV_KEY_LEFT>;`
  | :hwftlbl-joy:`RIGHT` :
    :devicetree:`input-codes = <INPUT_KEY_RIGHT>;` :
    :devicetree:`lvgl-codes = <LV_KEY_RIGHT>;`
  | :hwftlbl-joy:`ENTER` :
    :devicetree:`input-codes = <INPUT_KEY_ENTER>;` :
    :devicetree:`lvgl-codes = <LV_KEY_ENTER>;`

.. rubric:: LCD Orientation and Bit Order Test

.. image:: img/display.gif
   :align: right
   :alt: PicoBoy Display Test

Draw some basic rectangles onto the display using the :ref:`Display driver API
<zephyr:display_api>`. See also Zephyr sample:
:zephyr:code-sample:`zephyr:display`.

.. zephyr-app-commands::
   :app: zephyr/samples/drivers/display
   :board: picoboy
   :build-dir: picoboy
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: LVGL Basic Sample

Displays “Hello World!” in the center of the screen and a counter at the bottom
which increments every second using the LVGL module on top of the :ref:`Display
driver API <zephyr:display_api>`. See also Zephyr sample:
:zephyr:code-sample:`zephyr:lvgl`.

.. zephyr-app-commands::
   :app: zephyr/samples/subsys/display/lvgl
   :board: picoboy
   :build-dir: picoboy
   :west-args: -p
   :goals: flash
   :compact:

This sample comes with a Shell command line access to the LVGL backend
on the console, here configured for a USB console:

.. rubric:: Simple test execution on target

.. parsed-literal::
   :class: highlight-console notranslate

   :bgn:`uart:~$` **lvgl**
   lvgl - LVGL shell commands
   Subcommands:
     stats   :Show LVGL statistics
     monkey  :LVGL monkey testing

   :bgn:`uart:~$` **lvgl stats**
   stats - Show LVGL statistics
   Subcommands:
     memory  :Show LVGL memory statistics
              Usage: lvgl stats memory [-c]
              -c  dump chunk information

   :bgn:`uart:~$` **lvgl stats memory**
   Heap at 0x20001270 contains 2047 units in 11 buckets

     bucket#    min units        total      largest      largest
                threshold       chunks      (units)      (bytes)
     -----------------------------------------------------------
           0            1            1            1            4
           1            2            1            2           12
          10         1024            1         1824        14588

   14604 free bytes, 1544 allocated bytes, overhead = 232 bytes (1.4%)

References
**********

.. target-notes::
