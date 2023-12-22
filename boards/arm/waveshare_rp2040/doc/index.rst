.. _waveshare_rp2040:

Waveshare RP2040
################

The `RP2040 SoC`_ by Raspberry Pi Ltd. is a small sized and low-cost 32-bit
dual ARM Cortex-M0+ microcontroller and predestined for versatile board
designs. The Waveshare RP2040 board series based on this microcontroller
offers a wide range with different scaling factors, in size, features and
interfaces for communication, input and output.

Supported Boards
****************

Hardware
========

.. tabs::

   .. group-tab:: RP2040-One

      .. _waveshare_rp2040_one:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-one/hardware.rsti

   .. group-tab:: RP2040-Zero

      .. _waveshare_rp2040_zero:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-zero/hardware.rsti

   .. group-tab:: RP2040-Matrix

      .. _waveshare_rp2040_matrix:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-matrix/hardware.rsti

   .. group-tab:: RP2040-Tiny

      .. _waveshare_rp2040_tiny:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-tiny/hardware.rsti

   .. group-tab:: RP2040-ETH

      .. _waveshare_rp2040_eth:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-eth/hardware.rsti

   .. group-tab:: RP2040-LCD-0.96

      .. _waveshare_rp2040_lcd_0_96:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-lcd-0.96/hardware.rsti

   .. group-tab:: RP2040-Plus

      .. _waveshare_rp2040_plus:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-plus/hardware.rsti

   .. group-tab:: RP2040-Geek

      .. _waveshare_rp2040_geek:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-geek/hardware.rsti

Positions
=========

.. tabs::

   .. group-tab:: RP2040-One

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-one/positions.rsti

   .. group-tab:: RP2040-Zero

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-zero/positions.rsti

   .. group-tab:: RP2040-Matrix

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-matrix/positions.rsti

   .. group-tab:: RP2040-Tiny

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-tiny/positions.rsti

   .. group-tab:: RP2040-ETH

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-eth/positions.rsti

   .. group-tab:: RP2040-LCD-0.96

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-lcd-0.96/positions.rsti

   .. group-tab:: RP2040-Plus

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-plus/positions.rsti

   .. group-tab:: RP2040-Geek

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-geek/positions.rsti

Pinouts
=======

The peripherals of the `RP2040 SoC`_ can be routed to various pins on
the board. The configuration of these routes can be modified through
:ref:`DTS <zephyr:devicetree>`. Please refer to the datasheet to see
the possible routings for each peripheral. The default assignments
for the various Waveshare RP2040 boards are defined below separately
in a single tab.

.. tabs::

   .. group-tab:: RP2040-One

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-one/pinouts.rsti

   .. group-tab:: RP2040-Zero

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-zero/pinouts.rsti

   .. group-tab:: RP2040-Matrix

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-matrix/pinouts.rsti

   .. group-tab:: RP2040-Tiny

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-tiny/pinouts.rsti

   .. group-tab:: RP2040-ETH

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-eth/pinouts.rsti

   .. group-tab:: RP2040-LCD-0.96

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-lcd-0.96/pinouts.rsti

   .. group-tab:: RP2040-Plus

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-plus/pinouts.rsti

   .. group-tab:: RP2040-Geek

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-geek/pinouts.rsti

Supported Features
******************

Similar to the :ref:`zephyr:rpi_pico` the Waveshare RP2040 board configuration
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
   * - UART
     - :kconfig:option:`CONFIG_SERIAL`
     - :dtcompatible:`raspberrypi,pico-uart`
     - :ref:`zephyr:uart_api`
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
   * - UART (PIO)
     - :kconfig:option:`CONFIG_SERIAL`
     - :dtcompatible:`raspberrypi,pico-uart-pio`
     - :ref:`zephyr:uart_api`
   * - SPI (PIO)
     - :kconfig:option:`CONFIG_SPI`
     - :dtcompatible:`raspberrypi,pico-spi-pio`
     - :ref:`zephyr:spi_api`
   * - DMA
     - :kconfig:option:`CONFIG_DMA`
     - :dtcompatible:`raspberrypi,pico-dma`
     - :ref:`zephyr:dma_api`
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
    a proper I2C device scan. Thus, all :strong:`Waveshare RP2040 boards`
    will be configured to :strong:`use the simple GPIO-I2C bit-bang driver`
    as long as this driver is not applicable as expected.

    See also: https://github.com/zephyrproject-rtos/zephyr/pull/60427

(!!) Die-Temperature Sensor driver has issues:
     It seems the RP2040 Die-Temperature sensor driver has also race conditions
     and :brd:`leads to a dead-lock of the entire runtime system`. Thus, all
     :strong:`Waveshare RP2040 boards` will be configured to :strong:`disable
     this sensor` node in DTS explicitly. As a workaround the ADC channel 4
     can be used, but that result have to convert manually to the corresponding
     chip temperature following the formula that can be found in the
     `RP2040 Datasheet`_, section with title :emphasis:`"Temperature Sensor"`.

Other hardware features are not currently supported by Zephyr. The default
configuration can be found in the different Kconfig files:

- :bridle_file:`boards/arm/waveshare_rp2040/waveshare_rp2040_one_defconfig`
- :bridle_file:`boards/arm/waveshare_rp2040/waveshare_rp2040_zero_defconfig`
- :bridle_file:`boards/arm/waveshare_rp2040/waveshare_rp2040_matrix_defconfig`
- :bridle_file:`boards/arm/waveshare_rp2040/waveshare_rp2040_tiny_defconfig`
- :bridle_file:`boards/arm/waveshare_rp2040/waveshare_rp2040_eth_defconfig`
- :bridle_file:`boards/arm/waveshare_rp2040/waveshare_rp2040_lcd_0_96_defconfig`
- :bridle_file:`boards/arm/waveshare_rp2040/waveshare_rp2040_plus_defconfig`
- :bridle_file:`boards/arm/waveshare_rp2040/waveshare_rp2040_geek_defconfig`

Board Configurations
====================

The Waveshare RP2040 boards can be configured for the following different
use cases. The |RP2040-Plus| board offers an assembly option with 16㎆ Flash,
which is mapped as a hardware revision.

.. tabs::

   .. group-tab:: RP2040-One

      .. rubric:: :command:`west build -b waveshare_rp2040_one`

      Use the serial port UART0 on edge header as
      Zephyr console and for the shell.

      .. rubric:: :command:`west build -b waveshare_rp2040_one -S usb-console`

      Use the native USB device port with CDC-ACM as
      Zephyr console and for the shell.

   .. group-tab:: RP2040-Zero

      .. rubric:: :command:`west build -b waveshare_rp2040_zero`

      Use the serial port UART0 on edge header as
      Zephyr console and for the shell.

      .. rubric:: :command:`west build -b waveshare_rp2040_zero -S usb-console`

      Use the native USB device port with CDC-ACM as
      Zephyr console and for the shell.

   .. group-tab:: RP2040-Matrix

      .. rubric:: :command:`west build -b waveshare_rp2040_matrix`

      Use the serial port UART0 on edge header as
      Zephyr console and for the shell.

      .. rubric:: :command:`west build -b waveshare_rp2040_matrix -S usb-console`

      Use the native USB device port with CDC-ACM as
      Zephyr console and for the shell.

   .. group-tab:: RP2040-Tiny

      .. rubric:: :command:`west build -b waveshare_rp2040_tiny`

      Use the serial port UART0 on edge header as
      Zephyr console and for the shell.

      .. rubric:: :command:`west build -b waveshare_rp2040_tiny -S usb-console`

      Use the native USB device port with CDC-ACM as
      Zephyr console and for the shell.

   .. group-tab:: RP2040-ETH

      .. rubric:: :command:`west build -b waveshare_rp2040_eth`

      Use the serial port UART0 on edge header as
      Zephyr console and for the shell.

      .. rubric:: :command:`west build -b waveshare_rp2040_eth -S usb-console`

      Use the native USB device port with CDC-ACM as
      Zephyr console and for the shell.

   .. group-tab:: RP2040-LCD-0.96

      .. rubric:: :command:`west build -b waveshare_rp2040_lcd_0_96`

      Use the serial port UART0 on edge header as
      Zephyr console and for the shell.

      .. rubric:: :command:`west build -b waveshare_rp2040_lcd_0_96 -S usb-console`

      Use the native USB device port with CDC-ACM as
      Zephyr console and for the shell.

   .. group-tab:: RP2040-Plus

      .. rubric:: :command:`west build -b waveshare_rp2040_plus`

      Use the serial port UART0 on edge header as
      Zephyr console and for the shell.

      .. rubric:: :command:`west build -b waveshare_rp2040_plus -S usb-console`

      Use the native USB device port with CDC-ACM as
      Zephyr console and for the shell.

      .. rubric:: :command:`west build -b waveshare_rp2040_plus@16mb`

      Setup QSPI Flash controller to work with 16㎆ and
      use the serial port UART0 on edge header as Zephyr
      console and for the shell.

      .. rubric:: :command:`west build -b waveshare_rp2040_plus@16mb -S usb-console`

      Setup QSPI Flash controller to work with 16㎆ and
      use the native USB device port with CDC-ACM as
      Zephyr console and for the shell.

   .. group-tab:: RP2040-Geek

      .. rubric:: :command:`west build -b waveshare_rp2040_geek`

      Use the serial port UART1 on edge header as
      Zephyr console and for the shell.

      .. rubric:: :command:`west build -b waveshare_rp2040_geek -S usb-console`

      Use the native USB device port with CDC-ACM as
      Zephyr console and for the shell.

Connections and IOs
===================

The `Waveshare wiki`_ has detailed information about board connections.
Download the different schematics or datasheets as linked above per board
for more details. The pinout diagrams can also be found there.

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
the two boards |RP2040-Plus| and |RP2040-LCD-0.96|, PWM4 channel B is available
on the on-board user or backlight LED. But the PWM operation is not enable by
default. Only if :kconfig:option:`CONFIG_PWM_RPI_PICO` is enabled then the
first user or backlight LED is driven by PWM4CHB instead of by GPIO. All
channels of PWM0 until PWM7 are available on the |Raspberry Pi Pico| or
|Waveshare RP2040 Mini| header and |Waveshare RP2040 Mini PCB Pads|.

The |RP2040-Geek| board has no such LED and no standard header and therefore
does not provide any PWM to the outside on any pad by default.

ADC/TS Ports
============

The `RP2040 <RP2040 SoC_>`_ MCU has 1 ADC with 4 channels and an additional
fifth channel for the on-chip temperature sensor (TS). The ADC channels 0-2
are available on the |Raspberry Pi Pico| or |Waveshare RP2040 Mini| header,
channel 3 only on the |Waveshare RP2040 Mini| header. On the |RP2040-Plus|,
the |RP2040-LCD-0.96| and |RP2040-ETH|, ADC channel 3 will be used for
internal on-board voltage monitoring.

The external voltage reference ADC_VREF can be used optional for the ADC
and is only available on the |Raspberry Pi Pico| header.

The |RP2040-Geek| board provides ADC channel 2 and 3 over GP28 (ADC2) and
GP29 (ADC3) on one of the three edge connectors but these are disabled by
default. Both ADC channels will share the same lines with the I2C0 signals.

SPI Port
========

The `RP2040 <RP2040 SoC_>`_ MCU has 2 SPIs. To the edge connectors SPI0 is
connect to external devices over GP19 (MOSI), GP16 (MISO), GP18 (SCK), and
GP17 (CSn) on the |Raspberry Pi Pico| header or over GP7 (MOSI), GP4 (MISO),
GP6 (SCK), and GP5 (CSn) on the |Waveshare RP2040 Mini| header. A special
case is the |RP2040-ETH| board where SPI0 is routed on the |Raspberry Pi Pico|
header with the same GP4-7 layout as on the |Waveshare RP2040 Mini| header.

The |RP2040-Geek| does not provide any SPI to the outside on any pad. These
are connected internally to the LCD and the TF/microSD card interfaces.

I2C Port
========

The `RP2040 <RP2040 SoC_>`_ MCU has 2 I2Cs. To the edge connectors I2C0 and
I2C1 is connect to external devices over GP4 (I2C0_SDA), GP5 (I2C0_SCL),
GP14 (I2C1_SDA), and GP15 (I2C1_SCL) on the |Raspberry Pi Pico| header or
over GP8 (I2C0_SDA), GP9 (I2C0_SCL), GP14 (I2C1_SDA), and GP15 (I2C1_SCL)
on the |Waveshare RP2040 Mini| header. A special case is the |RP2040-ETH|
board where I2C1 is omitted and I2C0 is routed on the |Raspberry Pi Pico|
header with the same GP8-9 layout as on the |Waveshare RP2040 Mini| header.

The |RP2040-Geek| board provides I2C0 over GP28 (SDA) and GP29 (SCL) on one
of the three edge connectors and it is enabled by default. Both I2C0 signals
will share the same lines with ADC channels 2 and 3.

Serial Port
===========

The `RP2040 <RP2040 SoC_>`_ MCU has 2 UARTs. One of the UARTs (UART0) is
connected to external devices over GP0 (TX) and GP1 (RX) on both the
|Raspberry Pi Pico| and the |Waveshare RP2040 Mini| header in same manner
and is the Zephyr console.

The |RP2040-Geek| board provides UART1 over GP4 (TX) and GP5 (RX) on one
of the three edge connectors and it is enabled by default.

USB Device Port
===============

The `RP2040 <RP2040 SoC_>`_ MCU has a (native) USB device port that can be
used to communicate with a host PC. See the :ref:`zephyr:usb-samples` sample
applications for more, such as the :doc:`zephyr:samples/subsys/usb/cdc_acm/README`
sample which sets up a virtual serial port that echos characters back to the
host PC. As an alternative to the default Zephyr console on serial port the
Bridle :ref:`snippet-usb-console` can be used to enable
:ref:`zephyr:usb_device_cdc_acm` and switch the console to USB::

   USB device idVendor=2e8a, idProduct=000a, bcdDevice= 3.05
   USB device strings: Mfr=1, Product=2, SerialNumber=3
   Product: RP2040-Plus (CDC ACM)
   Manufacturer: Waveshare (Raspberry Pi)
   SerialNumber: B69F8448A6E91514

To integrate specific USB device functions that do not follow a USB standard
class, the following alternate identifier numbers are available for the various
Waveshare RP2040 boards according to the `Raspberry Pi USB product ID list`_:

:0x101F: |RP2040-Zero|
:0x1020: |RP2040-Plus|
:0x1021: |RP2040-LCD-0.96|
:0x1039: RP2040-LCD-1.28
:0x103A: |RP2040-One|
:0x1044: Power Management HAT (B)
:0x1055: |RP2040-ETH|
:0x1056: RP2040-HACK
:0x1057: RP2040-Touch-LCD-1.28

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

Using UF2
---------

If you don't have an SWD adapter, you can flash the Waveshare RP2040 boards
with a UF2 file. By default, building an app for this board will generate a
:file:`build/zephyr/zephyr.uf2` file. If the board is powered on with the
:kbd:`BOOTSEL` button pressed, it will appear on the host as a mass
storage device::

   USB device idVendor=2e8a, idProduct=0003, bcdDevice= 1.00
   USB device strings: Mfr=1, Product=2, SerialNumber=3
   Product: RP2 Boot
   Manufacturer: Raspberry Pi
   SerialNumber: E0C9125B0D9B

The UF2 file should be drag-and-dropped or copied on command line to the
device, which will then flash the Waveshare RP2040 board.

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

All Waveshare RP2040 boards set this option to |CONFIG_RP2_FLASH_W25Q080|.
Further informations can be found in the `RP2040 Datasheet`_, sections with
title :emphasis:`"Bootrom"` and :emphasis:`"Processor Controlled Boot Sequence"`
or Brian Starkey's Blog article `Pico serial bootloader`_

.. |CONFIG_RP2_FLASH_AT25SF128A| replace::
   :kconfig:option:`CONFIG_RP2_FLASH_AT25SF128A`
.. |CONFIG_RP2_FLASH_GENERIC_03H| replace::
   :kconfig:option:`CONFIG_RP2_FLASH_GENERIC_03H`
.. |CONFIG_RP2_FLASH_IS25LP080| replace::
   :kconfig:option:`CONFIG_RP2_FLASH_IS25LP080`
.. |CONFIG_RP2_FLASH_W25Q080| replace::
   :kconfig:option:`CONFIG_RP2_FLASH_W25Q080`
.. |CONFIG_RP2_FLASH_W25X10CL| replace::
   :kconfig:option:`CONFIG_RP2_FLASH_W25X10CL`

Using SEGGER JLink
------------------

You can flash the Waveshare RP2040 boards with a SEGGER JLink debug probe as
described in :ref:`Building, Flashing and Debugging <zephyr:west-flashing>`.

Here is an example of building and flashing the
:doc:`zephyr:samples/basic/blinky/README` application.

.. zephyr-app-commands::
   :zephyr-app: zephyr/samples/basic/blinky
   :board: waveshare_rp2040_plus
   :build-dir: waveshare_rp2040
   :goals: flash
   :flash-args: -r jlink
   :west-args: -p

Using OpenOCD
-------------

To use `PicoProbe`_ or `Raspberry Pi Debug Probe`_, you must configure
:program:`udev`. Create a file in :file:`/etc/udev.rules.d` with any name,
and write the line below.

.. code-block:: bash

   ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="0004", MODE="660", GROUP="plugdev", TAG+="uaccess"
   ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="000c", MODE="660", GROUP="plugdev", TAG+="uaccess"

This example is valid for the case that the user joins to :code:`plugdev`
groups.

The |RP2040-LCD-0.96| and |RP2040-Plus| has an SWD interface that can be used
to program and debug the on board RP2040. This interface can be utilized by
OpenOCD. To use it with the RP2040, OpenOCD version 0.12.0 or later is needed.
If you are using a Debian based system (including RaspberryPi OS, Ubuntu,
and more), using the `pico_setup.sh`_ script is a convenient way to set up
the forked version of OpenOCD. Depending on the interface used (such as JLink),
you might need to checkout to a branch that supports this interface, before
proceeding. Build and install OpenOCD as described in the README.

Here is an example of building and flashing the
:doc:`zephyr:samples/basic/blinky/README` application.

.. zephyr-app-commands::
   :zephyr-app: zephyr/samples/basic/blinky
   :board: waveshare_rp2040_plus
   :build-dir: waveshare_rp2040
   :goals: flash
   :west-args: -p
   :flash-args: -r openocd
   :gen-args: \
              -DOPENOCD=/usr/local/bin/openocd \
              -DOPENOCD_DEFAULT_PATH=/usr/local/share/openocd/scripts \
              -DWAVESHARE_RP2040_DEBUG_ADAPTER=picoprobe

Set the environment variables :strong:`OPENOCD` to
:file:`/usr/local/bin/openocd` and :strong:`OPENOCD_DEFAULT_PATH` to
:file:`/usr/local/share/openocd/scripts`. This should work with the OpenOCD
that was installed with the default configuration. This configuration also
works with an environment that is set up by the `pico_setup.sh`_ script.

:strong:`WAVESHARE_RP2040_DEBUG_ADAPTER` specifies what debug adapter is
used for debugging. If :strong:`WAVESHARE_RP2040_DEBUG_ADAPTER` was not
assigned, :dfn:`cmsis-dap` is used by default. The other supported adapters
are :dfn:`picoprobe`, :dfn:`raspberrypi-swd`, :dfn:`jlink` and
:dfn:`blackmagicprobe`. How to connect :dfn:`picoprobe` and
:dfn:`raspberrypi-swd` is described in `Getting Started Guide with Raspberry
Pi Pico`_. Any other SWD debug adapter maybe also work with this configuration.
The value of :strong:`WAVESHARE_RP2040_DEBUG_ADAPTER` is cached, so it can
be omitted from :program:`west flash` and :program:`west debug` if it was
previously set while running :program:`west build`.
:strong:`WAVESHARE_RP2040_DEBUG_ADAPTER` is used in an argument to OpenOCD as
:code:`"source [find interface/${WAVESHARE_RP2040_DEBUG_ADAPTER}.cfg]"`. Thus,
:strong:`WAVESHARE_RP2040_DEBUG_ADAPTER` needs to be assigned the file name of
the debug adapter.

You can also flash the board with the following command that directly calls
OpenOCD (assuming a SEGGER JLink adapter is used):

.. code-block:: console

   $ openocd -f interface/jlink.cfg    \
             -c 'transport select swd' \
             -f target/rp2040.cfg      \
             -c "adapter speed 2000"   \
             -c 'targets rp2040.core0' \
             -c 'program path/to/zephyr.elf verify reset exit'

Debugging
=========

The SWD interface can also be used to debug the board. To achieve this, you can
either use SEGGER JLink or OpenOCD.

Using SEGGER JLink
------------------

Use a SEGGER JLink debug probe and follow the instruction in
:ref:`Building, Flashing and Debugging <zephyr:west-debugging>`.

Using OpenOCD
-------------

Install OpenOCD as described for flashing the board.

Here is an example for debugging the
:doc:`zephyr:samples/basic/blinky/README` application.

.. zephyr-app-commands::
   :zephyr-app: zephyr/samples/basic/blinky
   :board: waveshare_rp2040_plus
   :build-dir: waveshare_rp2040
   :maybe-skip-config:
   :goals: debug
   :west-args: -p
   :flash-args: -r openocd
   :gen-args: \
              -DOPENOCD=/usr/local/bin/openocd \
              -DOPENOCD_DEFAULT_PATH=/usr/local/share/openocd/scripts \
              -DWAVESHARE_RP2040_DEBUG_ADAPTER=raspberrypi-swd
   :host-os: unix

As with flashing, you can specify the debug adapter by specifying
:strong:`WAVESHARE_RP2040_DEBUG_ADAPTER` at :program:`west build` time.
No needs to specify it at :program:`west debug` time.

You can also debug with OpenOCD and gdb launching from command-line.
Run the following command:

.. code-block:: console

   $ openocd -f interface/jlink.cfg    \
             -c 'transport select swd' \
             -f target/rp2040.cfg      \
             -c "adapter speed 2000"   \
             -c 'targets rp2040.core0'

On another terminal, run:

.. code-block:: console

   $ gdb-multiarch

Inside gdb, run:

.. code-block:: console

   (gdb) tar ext :3333
   (gdb) file path/to/zephyr.elf

You can then start debugging the board.

More Samples
************

LED Blinky and Fade
===================

.. tabs::

   .. group-tab:: RP2040-One

      .. rubric:: WS2812 LED Test Pattern by PIO

      See also Zephyr sample: :doc:`zephyr:samples/drivers/led_ws2812/README`

      .. image:: /boards/arm/waveshare_rp2040/doc/rp2040-one/ws2812b.gif
         :align: right
         :alt: Waveshare RP2040-One WS2812 LED Test Pattern

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/led_ws2812
         :board: waveshare_rp2040_one
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. hint::

         Neither LED Blinky nor LED Fade can be built and executed on
         |RP2040-One|, because this system has only one digital RGB LED.
         A simple GPIO or PWM control is not possible!

   .. group-tab:: RP2040-Zero

      .. rubric:: WS2812 LED Test Pattern by PIO

      See also Zephyr sample: :doc:`zephyr:samples/drivers/led_ws2812/README`

      .. image:: /boards/arm/waveshare_rp2040/doc/rp2040-zero/ws2812b.gif
         :align: right
         :alt: Waveshare RP2040-Zero WS2812 LED Test Pattern

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/led_ws2812
         :board: waveshare_rp2040_zero
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. hint::

         Neither LED Blinky nor LED Fade can be built and executed on
         |RP2040-Zero|, because this system has only one digital RGB LED.
         A simple GPIO or PWM control is not possible!

   .. group-tab:: RP2040-Matrix

      .. rubric:: WS2812 LED Test Pattern by PIO

      See also Zephyr sample: :doc:`zephyr:samples/drivers/led_ws2812/README`

      .. image:: /boards/arm/waveshare_rp2040/doc/rp2040-matrix/ws2812b-5x5.gif
         :align: right
         :alt: Waveshare RP2040-Matrix WS2812 LED Test Pattern

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/led_ws2812
         :board: waveshare_rp2040_matrix
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. hint::

         Neither LED Blinky nor LED Fade can be built and executed on
         |RP2040-Matrix|, because this system has only one digital RGB LED.
         A simple GPIO or PWM control is not possible!

   .. group-tab:: RP2040-Tiny

      .. rubric:: WS2812 LED Test Pattern by PIO

      See also Zephyr sample: :doc:`zephyr:samples/drivers/led_ws2812/README`

      .. image:: /boards/arm/waveshare_rp2040/doc/rp2040-tiny/ws2812b.gif
         :align: right
         :alt: Waveshare RP2040-Tiny WS2812 LED Test Pattern

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/led_ws2812
         :board: waveshare_rp2040_tiny
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. hint::

         Neither LED Blinky nor LED Fade can be built and executed on
         |RP2040-Tiny|, because this system has only one digital RGB LED.
         A simple GPIO or PWM control is not possible!

   .. group-tab:: RP2040-ETH

      .. rubric:: WS2812 LED Test Pattern by PIO

      See also Zephyr sample: :doc:`zephyr:samples/drivers/led_ws2812/README`

      .. image:: /boards/arm/waveshare_rp2040/doc/rp2040-eth/ws2812b.gif
         :align: right
         :alt: Waveshare RP2040-ETH WS2812 LED Test Pattern

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/led_ws2812
         :board: waveshare_rp2040_eth
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. hint::

         Neither LED Blinky nor LED Fade can be built and executed on
         |RP2040-ETH|, because this system has only one digital RGB LED.
         A simple GPIO or PWM control is not possible!

   .. group-tab:: RP2040-LCD-0.96

      .. rubric:: LCD Backlight LED Blinky by GPIO

      See also Zephyr sample: :doc:`zephyr:samples/basic/blinky/README`

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky
         :board: waveshare_rp2040_lcd_0_96
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: LCD Backlight LED Blinky by PWM

      See also Zephyr sample: :doc:`zephyr:samples/basic/blinky_pwm/README`

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky_pwm
         :board: waveshare_rp2040_lcd_0_96
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: LCD Backlight LED Fade by PWM

      See also Zephyr sample: :doc:`zephyr:samples/basic/fade_led/README`

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/fade_led
         :board: waveshare_rp2040_lcd_0_96
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

   .. group-tab:: RP2040-Plus

      .. rubric:: Green User LED Blinky by GPIO

      See also Zephyr sample: :doc:`zephyr:samples/basic/blinky/README`

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky
         :board: waveshare_rp2040_plus
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Green User LED Blinky by PWM

      See also Zephyr sample: :doc:`zephyr:samples/basic/blinky_pwm/README`

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky_pwm
         :board: waveshare_rp2040_plus
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Green User LED Fade by PWM

      See also Zephyr sample: :doc:`zephyr:samples/basic/fade_led/README`

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/fade_led
         :board: waveshare_rp2040_plus
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

   .. group-tab:: RP2040-Geek

      .. hint::

         Neither LED Blinky nor LED Fade can be built and executed on
         |RP2040-Geek|, because this system has no user LED.
         A simple GPIO or PWM control is not possible by default!

         But with the help of the dedicated :ref:`loopback_test_shield` shield,
         all necessary Devicetree changes and board extensions are carried out
         temporarily in order to be able to execute the standard examples. This
         assumes the external wiring as shown below (right).

      .. image:: /boards/arm/waveshare_rp2040/doc/rp2040-geek/loopback_test_shield.jpg
         :align: right
         :alt: Waveshare RP2040-Geek with loopback wiring for tests

      .. rubric:: External LED Blinky by GPIO

      See also Zephyr sample: :doc:`zephyr:samples/basic/blinky/README`

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky
         :board: waveshare_rp2040_geek
         :shield: loopback_test
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: External LED Blinky by PWM

      See also Zephyr sample: :doc:`zephyr:samples/basic/blinky_pwm/README`

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky_pwm
         :board: waveshare_rp2040_geek
         :shield: loopback_test
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: External LED Fade by PWM

      See also Zephyr sample: :doc:`zephyr:samples/basic/fade_led/README`

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/fade_led
         :board: waveshare_rp2040_geek
         :shield: loopback_test
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: External LED Switch ON/OFF by External Button

      See also Zephyr sample: :doc:`zephyr:samples/basic/button/README`

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/button
         :board: waveshare_rp2040_geek
         :shield: loopback_test
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

Hello Shell with USB-CDC/ACM Console
====================================

.. tabs::

   .. group-tab:: RP2040-One

      .. rubric:: Hello Shell

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :board: waveshare_rp2040_one
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-one/helloshell.rsti

   .. group-tab:: RP2040-Zero

      .. rubric:: Hello Shell

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :board: waveshare_rp2040_zero
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-zero/helloshell.rsti

   .. group-tab:: RP2040-Matrix

      .. rubric:: Hello Shell

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :board: waveshare_rp2040_matrix
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-matrix/helloshell.rsti

   .. group-tab:: RP2040-Tiny

      .. rubric:: Hello Shell

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :board: waveshare_rp2040_tiny
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-tiny/helloshell.rsti

   .. group-tab:: RP2040-ETH

      .. rubric:: Hello Shell

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :board: waveshare_rp2040_eth
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-eth/helloshell.rsti

   .. group-tab:: RP2040-LCD-0.96

      .. rubric:: Hello Shell

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :board: waveshare_rp2040_lcd_0_96
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-lcd-0.96/helloshell.rsti

   .. group-tab:: RP2040-Plus

      .. rubric:: Hello Shell on ``16㎆`` revision

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :board: waveshare_rp2040_plus@16mb
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-plus/helloshell.rsti

   .. group-tab:: RP2040-Geek

      .. rubric:: Hello Shell

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :board: waveshare_rp2040_geek
         :shield: loopback_test
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. include:: /boards/arm/waveshare_rp2040/doc/rp2040-geek/helloshell.rsti

Display Test and Demonstration
==============================

This samples and test applications are only applicable on the |RP2040-LCD-0.96|
and |RP2040-Geek| board. They will be built with activated USB-CDC/ACM console.

.. tabs::

   .. group-tab:: RP2040-LCD-0.96

      The following samples work with the chosen display. That is:

      | :hwftlbl-scr:`LCD` : :devicetree:`chosen { zephyr,display = &lcd_panel; };`
      | :hwftlbl-scr:`ST7735S` : :devicetree:`lcd_panel: &st7735s_160x80 {};`

      .. rubric:: LCD Orientation and Bit Order Test

      Using the :ref:`Display driver API <zephyr:display_api>` with chosen
      display. See also Zephyr sample:
      :doc:`zephyr:samples/drivers/display/README`.

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/display
         :board: waveshare_rp2040_lcd_0_96
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. list-table::
         :align: center
         :width: 66%
         :header-rows: 1

         * - .. image:: /boards/arm/waveshare_rp2040/doc/rp2040-lcd-0.96/display.*
                :align: center
                :alt: Waveshare RP2040-LCD-0.96 Display Sample Animation
         * - .. rst-class:: centered

                :brd:`TOP LEFT`, :bgn:`TOP RIGHT`, :bbl:`BOTTOM RIGHT`

      .. rubric:: LVGL Basic Sample

      Using the LVGL module on top of the :ref:`Display driver API
      <zephyr:display_api>` with chosen display. See also Zephyr sample:
      :doc:`zephyr:samples/subsys/display/lvgl/README`.

      .. zephyr-app-commands::
         :app: zephyr/samples/subsys/display/lvgl
         :board: waveshare_rp2040_lcd_0_96
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

   .. group-tab:: RP2040-Geek

      The following samples work with the chosen display. That is:

      | :hwftlbl-scr:`LCD` : :devicetree:`chosen { zephyr,display = &lcd_panel; };`
      | :hwftlbl-scr:`ST7789V` : :devicetree:`lcd_panel: &st7789v_240x135 {};`

      .. rubric:: LCD Orientation and Bit Order Test

      Using the :ref:`Display driver API <zephyr:display_api>` with chosen
      display. See also Zephyr sample:
      :doc:`zephyr:samples/drivers/display/README`.

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/display
         :board: waveshare_rp2040_geek
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. list-table::
         :align: center
         :width: 66%
         :header-rows: 1

         * - .. image:: /boards/arm/waveshare_rp2040/doc/rp2040-geek/display.*
                :align: center
                :alt: Waveshare RP2040-Geek Display Sample Animation
         * - .. rst-class:: centered

                :brd:`TOP LEFT`, :bgn:`TOP RIGHT`, :bbl:`BOTTOM RIGHT`

      .. rubric:: LVGL Basic Sample

      Using the LVGL module on top of the :ref:`Display driver API
      <zephyr:display_api>` with chosen display. See also Zephyr sample:
      :doc:`zephyr:samples/subsys/display/lvgl/README`.

      .. zephyr-app-commands::
         :app: zephyr/samples/subsys/display/lvgl
         :board: waveshare_rp2040_geek
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

References
**********

.. target-notes::

.. _RP2040 SoC:
   https://www.raspberrypi.com/products/rp2040

.. _RP2040 Datasheet:
   https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf

.. _Hardware design with RP2040:
   https://datasheets.raspberrypi.com/rp2040/hardware-design-with-rp2040.pdf

.. _Raspberry Pi Pico C/C++ SDK:
   https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-c-sdk.pdf

.. _Getting Started Guide with Raspberry Pi Pico:
    https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf

.. _Raspberry Pi USB product ID list:
   https://github.com/raspberrypi/usb-pid

.. _pico-bootrom:
   https://github.com/raspberrypi/pico-bootrom

.. |several versions of boot2| replace::
   :strong:`several versions of` :code:`boot2`
.. _several versions of boot2:
   https://github.com/raspberrypi/pico-sdk/tree/master/src/rp2_common/boot_stage2

.. _Raspberry Pi Pico HAL:
   https://github.com/zephyrproject-rtos/hal_rpi_pico

.. _Pico serial bootloader:
    https://blog.usedbytes.com/2021/12/pico-serial-bootloader

.. _UF2 bootloader:
    https://github.com/Microsoft/uf2#user-content-bootloaders

.. _PicoProbe:
   https://github.com/raspberrypi/picoprobe

.. _Raspberry Pi Debug Probe:
   https://www.raspberrypi.com/products/debug-probe

.. _Raspberry Pi Debug Probe Documentation:
   https://raspberrypi.com/documentation/microcontrollers/debug-probe.html

.. _Raspberry Pi 3-pin Debug Connector Specification:
   https://rptl.io/debug-spec

.. _JST 1.0㎜ (SH) Connector:
   https://www.jst.com/products/crimp-style-connectors-wire-to-board-type/sh-connector

.. _(B/S)M03B-SRSS-TB:
   https://www.jst.com/wp-content/uploads/2021/01/eSH-new.pdf

.. _SHR-03V-S(-B):
   https://www.jst.com/wp-content/uploads/2021/01/eSH-new.pdf

.. _(B/S)M04B-SRSS-TB:
   https://www.jst.com/wp-content/uploads/2021/01/eSH-new.pdf

.. _SHR-04V-S(-B):
   https://www.jst.com/wp-content/uploads/2021/01/eSH-new.pdf

.. _pico_setup.sh:
   https://raw.githubusercontent.com/raspberrypi/pico-setup/master/pico_setup.sh

.. _W25Q16JV:
   https://www.winbond.com/hq/product/code-storage-flash-memory/serial-nor-flash/index.html?__locale=en&partNo=W25Q16JV

.. _W25Q16JV Datasheet:
   https://www.winbond.com/hq/support/documentation/levelOne.jsp?__locale=en&DocNo=DA00-W25Q16JV.1

.. _W25Q32JV:
   https://www.winbond.com/hq/product/code-storage-flash-memory/serial-nor-flash/index.html?__locale=en&partNo=W25Q32JV

.. _W25Q32JV Datasheet:
   https://www.winbond.com/hq/support/documentation/levelOne.jsp?__locale=en&DocNo=DA00-W25Q32JV.1

.. _W25Q128JV:
   https://www.winbond.com/hq/product/code-storage-flash-memory/serial-nor-flash/index.html?__locale=en&partNo=W25Q128JV

.. _W25Q128JV Datasheet:
   https://www.winbond.com/hq/support/documentation/levelOne.jsp?__locale=en&DocNo=DA00-W25Q128JV

.. _RT9013-33:
   https://www.richtek.com/Products/Linear%20Regulator/Single%20Output%20Linear%20Regulator/RT9013

.. _RT9013 Datasheet:
   https://www.richtek.com/assets/product_file/RT9013/DS9013-10.pdf

.. _RT9193-33:
   https://www.richtek.com/Products/Linear%20Regulator/Single%20Output%20Linear%20Regulator/RT9193

.. _RT9193 Datasheet:
   https://www.richtek.com/assets/product_file/RT9193/DS9193-18.pdf

.. _ME6217C33:
   http://www.microne.com.cn/en/ProductDetail.aspx?id=8

.. _ME6217 Datasheet:
   http://www.microne.com.cn/UploadFiles/Files2/20190429/20190429164112.pdf

.. _TPS63000:
   https://www.ti.com/product/TPS63000

.. _TPS63000 Datasheet:
   https://www.ti.com/lit/gpn/tps63000

.. _MP28164:
   https://www.monolithicpower.com/mp28164.html

.. _MP28164 Datasheet:
   https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP28164GD-Z/document_id/1764

.. _MP28164 Reliability Report:
   https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Reliability%20Report/lang/en/sku/MP28164GD-Z/document_id/6077

.. _ETA6096:
   http://www.eta-semi.com/product/915.html

.. _ETA6096 Datasheet:
   http://www.eta-semi.com/wp-content/uploads/2022/03/ETA6096_V1.4.pdf

.. _CH9120:
   https://wch-ic.com/products/CH9120.html

.. _CH9120 Datasheet:
   https://wch-ic.com/downloads/CH9120DS1_PDF.html

.. _CH9120 Evaluation Tools:
   https://www.wch.cn/downloads/CH9120EVT_ZIP.html

.. _CH9120 Serial Instruction Set:
   https://files.waveshare.com/upload/e/e1/CH9120_Serial_Commands_Set.pdf
.. https://www.waveshare.com/wiki/RP2040-ETH#Document

.. _WS2812B:
   http://www.world-semi.com/ws2812-family

.. _WS2812B Datasheet V5:
   https://content.instructables.com/F10/WH6U/KQMCJ7I4/F10WH6UKQMCJ7I4.pdf

.. _WS2812B Datasheet V2:
   https://d2j2m4p6r3pg95.cloudfront.net/module_files/led-cube/assets/datasheets/WS2812B.pdf

.. _WS2812B Datasheet V1:
   https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf

.. _Understanding the WS2812:
   https://cpldcpu.wordpress.com/2014/01/14/light_ws2812-library-v2-0-part-i-understanding-the-ws2812

.. _WS2812B with RP2040 PIO & DMA:
   https://mcuoneclipse.com/2023/04/02/rp2040-with-pio-and-dma-to-address-ws2812b-leds

.. _ST7735S:
   https://www.sitronix.com.tw/en/products/aiot-device-ddi

.. _ST7735S Datasheet V1.4 (2014/10):
   https://github.com/michal037/driver-ST7735S/raw/master/documentation/datasheet/st7735s-datasheet-v1.4.pdf

.. _ST7735S Datasheet V1.1 (2011/11):
   http://www.lcdwiki.com/res/MSP0961/ST7735S_V1.1_20111121.pdf
.. https://www.waveshare.com/wiki/RP2040-LCD-0.96#Documents
.. https://files.waveshare.com/upload/e/e2/ST7735S_V1.1_20111121.pdf

.. _ST7789V:
   https://www.sitronix.com.tw/en/products/aiot-device-ddi

.. _ST7789VW Datasheet V1.0 (2017/09):
   http://www.lcdwiki.com/res/MSP1308/ST7789VW_datasheet.pdf
.. https://www.rhydolabz.com/documents/33/ST7789.pdf
.. https://www.waveshare.com/wiki/Pico-LCD-1.14#Document
.. https://files.waveshare.com/upload/a/ad/ST7789VW.pdf
.. https://files.waveshare.com/upload/a/ae/ST7789_Datasheet.pdf

.. _ST7789V Datasheet V1.6 (2017/09):
   https://www.crystalfontz.com/controllers/Sitronix/ST7789V/470

.. _ST7789V Datasheet V1.4 (2014/10):
   https://www.crystalfontz.com/controllers/Sitronix/ST7789V/446

.. _ST7789V Datasheet V1.3 (2014/03):
   https://newhavendisplay.com/content/datasheets/ST7789V.pdf
.. https://orientdisplay.com/wp-content/uploads/2020/11/ST7789V.pdf
.. https://threefivedisplays.com/wp-content/uploads/datasheets/lcd_driver_datasheets/ST7789_V_REV_1_3_DS.pdf

.. _ST7789V Datasheet V0.1 (2013/07):
   https://github.com/Xinyuan-LilyGO/LilyGo-HAL/raw/master/DISPLAY/ST7789V.pdf
.. https://www.crystalfontz.com/controllers/Sitronix/ST7789V/382

.. _0.5K-AX-nPWB:
   http://www.szhdgc.com/a/FPCxilie/0.50mm/2022/0813/203.html

.. _0.5K-AX-nPWB Engineering Drawing:
   http://www.szhdgc.com/uploads/soft/230215/0.5K-AX-nPWB

.. _Waveshare wiki:
   https://www.waveshare.com/wiki

.. _RP2040-One:
   https://www.waveshare.com/wiki/RP2040-One

.. _RP2040-One Schematic:
   https://www.waveshare.com/wiki/RP2040-One#Documents
.. https://files.waveshare.com/upload/9/90/RP2040-One.pdf

.. _RP2040-One STEP 3D-Model:
   https://www.waveshare.com/wiki/RP2040-One#Documents
.. https://files.waveshare.com/upload/c/cc/RP2040-One.zip

.. _RP2040-Zero:
   https://www.waveshare.com/wiki/RP2040-Zero

.. _RP2040-Zero Schematic:
   https://www.waveshare.com/wiki/RP2040-Zero#Documents
.. https://files.waveshare.com/upload/4/4c/RP2040_Zero.pdf

.. _RP2040-Zero STEP 3D-Model:
   https://www.waveshare.com/wiki/RP2040-Zero#Documents
.. https://files.waveshare.com/upload/f/f7/RP2040_Zero_stp.zip

.. _RP2040-Zero WS2812 Test:
   https://files.waveshare.com/upload/5/58/RP2040-Zero.zip
.. https://www.waveshare.com/wiki/RP2040-Zero#Demo_Codes

.. _RP2040-Matrix:
   https://www.waveshare.com/wiki/RP2040-Matrix

.. _RP2040-Matrix Schematic:
   https://www.waveshare.com/wiki/RP2040-Matrix#Document
.. https://files.waveshare.com/upload/4/49/RP2040-Matrix.pdf

.. _RP2040-Tiny:
   https://www.waveshare.com/wiki/RP2040-Tiny

.. _RP2040-Tiny V1.0 Schematic:
   https://www.waveshare.com/wiki/RP2040-Tiny#Document
.. https://files.waveshare.com/upload/7/7a/RP2040-Tiny_Schematic.pdf

.. _RP2040-Tiny V1.1 Schematic:
   https://www.waveshare.com/wiki/RP2040-Tiny#Document
.. https://files.waveshare.com/upload/7/7f/RP2040-Tiny_V1.1_SCH.pdf

.. _RP2040-Tiny V1.1 STEP 3D-Model:
   https://www.waveshare.com/wiki/RP2040-Tiny#3D_Model
.. https://files.waveshare.com/upload/9/94/RP2040-Tiny-Step_V1.1.zip

.. _RP2040-Tiny Adapter V1.1 Schematic:
   https://www.waveshare.com/wiki/RP2040-Tiny#Document
.. https://files.waveshare.com/upload/3/35/RP2040-Tiny-Adapter_V1.1-SCH.pdf

.. _RP2040-Tiny Adapter V1.1 STEP 3D-Model:
   https://www.waveshare.com/wiki/RP2040-Tiny#3D_Model
.. https://files.waveshare.com/upload/1/1e/RP2040-Tiny-Adapter-Step_V1.1.zip

.. _RP2040-ETH:
   https://www.waveshare.com/wiki/RP2040-ETH

.. _RP2040-ETH Schematic:
   https://www.waveshare.com/wiki/RP2040-ETH#Document
.. https://files.waveshare.com/upload/2/20/RP2040-ETH-SchDoc.pdf

.. _RP2040-ETH STEP 3D-Model:
   https://www.waveshare.com/wiki/RP2040-ETH#Document
.. https://files.waveshare.com/upload/1/19/RP2040-ETH.zip

.. _RP2040-ETH WS2812 Test:
   https://www.waveshare.com/wiki/RP2040-ETH#Demo
.. https://files.waveshare.com/upload/3/36/RP2040-ETH-WS2812B.zip

.. _RP2040-ETH COM Test:
   https://www.waveshare.com/wiki/RP2040-ETH#Demo
.. https://files.waveshare.com/upload/8/88/RP2040_ETH_CODE.zip

.. _RP2040-LCD-0.96:
   https://www.waveshare.com/wiki/RP2040-LCD-0.96

.. _RP2040-LCD-0.96 Schematic:
   https://www.waveshare.com/wiki/RP2040-LCD-0.96#Documents
.. https://files.waveshare.com/upload/0/01/RP2040-LCD-0.96.pdf

.. _RP2040-LCD-0.96 LCD/OLED Test:
   https://www.waveshare.com/wiki/RP2040-LCD-0.96#Demo_Codes
.. https://files.waveshare.com/upload/2/28/Pico_code.7z

.. _RP2040-Plus:
   https://www.waveshare.com/wiki/RP2040-Plus

.. _RP2040-Plus Schematic:
   https://www.waveshare.com/wiki/RP2040-Plus#Documents
.. https://files.waveshare.com/upload/d/d1/RP2040_Plus.pdf

.. _RP2040-Geek Schematic:
   https://www.waveshare.com/wiki/RP2040-GEEK#Document
.. https://files.waveshare.com/wiki/RP2040-GEEK/RP2040-GEEK-Schematic.pdf

.. _IEEE-754:
   https://en.wikipedia.org/wiki/IEEE_754

.. |RP2040-One| replace::
   :ref:`RP2040-One <waveshare_rp2040_one>`

.. |RP2040-Zero| replace::
   :ref:`RP2040-Zero <waveshare_rp2040_zero>`

.. |RP2040-Matrix| replace::
   :ref:`RP2040-Matrix <waveshare_rp2040_matrix>`

.. |RP2040-Tiny| replace::
   :ref:`RP2040-Tiny <waveshare_rp2040_tiny>`

.. |RP2040-ETH| replace::
   :ref:`RP2040-ETH <waveshare_rp2040_eth>`

.. |RP2040-LCD-0.96| replace::
   :ref:`RP2040-LCD-0.96 <waveshare_rp2040_lcd_0_96>`

.. |RP2040-Plus| replace::
   :ref:`RP2040-Plus <waveshare_rp2040_plus>`

.. |RP2040-Geek| replace::
   :ref:`RP2040-Geek <waveshare_rp2040_geek>`

.. |Raspberry Pi Pico| replace::
   :dtcompatible:`Raspberry Pi Pico <raspberrypi,pico-header>`

.. |Raspberry Pi Pico R3| replace::
   :dtcompatible:`Raspberry Pi Pico R3 <raspberrypi,pico-header-r3>`

.. |Waveshare RP2040 Mini| replace::
   :dtcompatible:`Waveshare RP2040 Mini <waveshare,rp2040mini-header>`

.. |Waveshare RP2040 Mini PCB Pads| replace::
   :dtcompatible:`Waveshare RP2040 Mini PCB Pads <waveshare,rp2040mini-pcbpads>`

.. |Grove BMP280 Sensor| replace::
   :strong:`Grove Temperature and Barometer Sensor – BMP280`
.. _`Grove BMP280 Sensor`:
   https://www.seeedstudio.com/Grove-Barometer-Sensor-BMP280.html
