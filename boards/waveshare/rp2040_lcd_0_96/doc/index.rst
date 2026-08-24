.. _waveshare_rp2040_lcd_0_96:

Waveshare RP2040-LCD-0.96
#########################

The `RP2040 SoC`_ by Raspberry Pi Ltd. is a small sized and low-cost 32-bit
dual ARM Cortex-M0+ microcontroller and predestined for versatile board
designs. The Waveshare RP2040 board series based on this microcontroller
offers a wide range with different scaling factors, in size, features and
interfaces for communication, input and output.

Supported Boards
****************

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
:external+zephyr:ref:`DTS <devicetree>`. Please refer to the datasheet
to see the possible routings for each peripheral. The default assignments
for the various Waveshare RP2040 boards are defined below separately
in a single tab.

.. include:: pinouts.rsti

Supported Features
******************

Similar to the |zephyr:board:rpi_pico| the Waveshare RP2040 board configuration
supports the following hardware features:

.. list-table:: Hardware Features Supported by Zephyr
   :class: longtable
   :align: center
   :header-rows: 1

   * - Peripheral
     - Kconfig option
     - Devicetree compatible
     - Zephyr API
   * - PINCTRL
     - :kconfig:option:`CONFIG_PINCTRL`
     - :dtcompatible:`raspberrypi,pico-pinctrl`
     - :external+zephyr:ref:`pinctrl_api`
   * - GPIO
     - :kconfig:option:`CONFIG_GPIO`
     - :dtcompatible:`raspberrypi,pico-gpio`
     - :external+zephyr:ref:`gpio_api`
   * - UART
     - :kconfig:option:`CONFIG_SERIAL`
     - | :dtcompatible:`raspberrypi,pico-uart`
       | :dtcompatible:`arm,pl011`
     - :external+zephyr:ref:`uart_api`
   * - UDC (USB Device Controller)
     - :kconfig:option:`CONFIG_USB_DEVICE_STACK_NEXT`
     - :dtcompatible:`raspberrypi,pico-usbd`
     - :external+zephyr:ref:`usb_device_next_api`
   * - I2C
     - :kconfig:option:`CONFIG_I2C`
     - :dtcompatible:`raspberrypi,pico-i2c`
     - :external+zephyr:ref:`i2c_api`
   * - SPI
     - :kconfig:option:`CONFIG_SPI`
     - | :dtcompatible:`raspberrypi,pico-spi`
       | :dtcompatible:`arm,pl022`
     - :external+zephyr:ref:`spi_api`
   * - PWM
     - :kconfig:option:`CONFIG_PWM`
     - :dtcompatible:`raspberrypi,pico-pwm`
     - :external+zephyr:ref:`pwm_api`
   * - ADC
     - :kconfig:option:`CONFIG_ADC`
     - :dtcompatible:`raspberrypi,pico-adc`
     - :external+zephyr:ref:`adc_api`
   * - Temperature (Sensor)
     - :kconfig:option:`CONFIG_SENSOR`
     - :dtcompatible:`raspberrypi,pico-temp`
     - :external+zephyr:ref:`sensor`
   * - RTC
     - :kconfig:option:`CONFIG_RTC`
     - :dtcompatible:`raspberrypi,pico-rtc`
     - :external+zephyr:ref:`rtc_api`
   * - Timer (Counter)
     - :kconfig:option:`CONFIG_COUNTER`
     - :dtcompatible:`raspberrypi,pico-timer`
     - :external+zephyr:ref:`counter_api`
   * - Watchdog Timer (WDT)
     - :kconfig:option:`CONFIG_WATCHDOG`
     - :dtcompatible:`raspberrypi,pico-watchdog`
     - :external+zephyr:ref:`watchdog_api`
   * - Flash
     - :kconfig:option:`CONFIG_FLASH`
     - :dtcompatible:`raspberrypi,pico-flash-controller`
     - :external+zephyr:ref:`flash_api` and
       :external+zephyr:ref:`flash_map_api`
   * - PIO
     - :kconfig:option:`CONFIG_PIO_RPI_PICO`
     - :dtcompatible:`raspberrypi,pico-pio`
     - N/A
   * - UART (PIO)
     - :kconfig:option:`CONFIG_SERIAL`
     - :dtcompatible:`raspberrypi,pico-uart-pio`
     - :external+zephyr:ref:`uart_api`
   * - SPI (PIO)
     - :kconfig:option:`CONFIG_SPI`
     - :dtcompatible:`raspberrypi,pico-spi-pio`
     - :external+zephyr:ref:`spi_api`
   * - DMA
     - :kconfig:option:`CONFIG_DMA`
     - :dtcompatible:`raspberrypi,pico-dma`
     - :external+zephyr:ref:`dma_api`
   * - HWINFO
     - :kconfig:option:`CONFIG_HWINFO`
     - N/A
     - :external+zephyr:ref:`hwinfo_api`
   * - VREG
     - :kconfig:option:`CONFIG_REGULATOR`
     - :dtcompatible:`raspberrypi,core-supply-regulator`
     - :external+zephyr:ref:`regulator_api`
   * - RESET
     - :kconfig:option:`CONFIG_RESET`
     - :dtcompatible:`raspberrypi,pico-reset`
     - :external+zephyr:ref:`reset_api`
   * - CLOCK
     - :kconfig:option:`CONFIG_CLOCK_CONTROL`
     - | :dtcompatible:`raspberrypi,pico-clock-controller`
       | :dtcompatible:`raspberrypi,pico-clock`
     - :external+zephyr:ref:`clock_control_api`
   * - NVIC
     - N/A
     - :dtcompatible:`arm,v6m-nvic`
     - Nested Vector :external+zephyr:ref:`interrupts_v2` Controller
   * - SYSTICK
     - N/A
     - :dtcompatible:`arm,armv6m-systick`
     -

Other hardware features are not currently supported by Zephyr. The default
configuration can be found in the different Kconfig files:

.. zephyr-keep-sorted-start re(^\* :bridle_file:`\w)

* :bridle_file:`boards/waveshare/rp2040_lcd_0_96/waveshare_rp2040_lcd_0_96_defconfig`

.. zephyr-keep-sorted-stop

Board Configurations
====================

The board can be configured for the following different use cases.

.. rubric:: :command:`west build -b waveshare_rp2040_lcd_0_96`

Use the serial port UART0 on edge header as
Zephyr console and for the shell.

.. rubric:: :command:`west build -b waveshare_rp2040_lcd_0_96 -S usb-console`

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
8 PWM function unit each with 2 channels beside a dedicated Timer unit. The
channel PWM4 B is available on the on-board backlight LED. All channels of PWM0
until PWM7 are available on the |Raspberry Pi Pico| header.

ADC/TS Ports
============

The `RP2040 <RP2040 SoC_>`_ MCU has 1 ADC with 4 channels and an additional
fifth channel for the on-chip temperature sensor (TS). The ADC channels 0-2
are available on the |Raspberry Pi Pico| header. ADC channel 3 will be used
for internal on-board voltage monitoring.

The external voltage reference ADC_VREF is directly connected to the 3.3V
power supply.

SPI Port
========

The `RP2040 <RP2040 SoC_>`_ MCU has 2 SPIs. To the edge connectors SPI0 is
usable for external devices over GP19 (MOSI), GP16 (MISO), GP18 (SCK), and
GP17 (CSn) on the |Raspberry Pi Pico| header. SPI1 will be used for internal
on-board LCD as write only half duplex interface over GP11 (MOSI), GP10 (SCK),
and GP9 (CSn), but is also prepared for reconfiguration as an alternative
interface to external devices over GP11 (MOSI), GP12 (MISO), GP10 (SCK),
and GP9 (CSn) on the |Raspberry Pi Pico| header.

I2C Port
========

The `RP2040 <RP2040 SoC_>`_ MCU has 2 I2Cs. The default serial bus I2C0 and
the alternative I2C1 are usable for external devices over GP4 (I2C0_SDA),
GP5 (I2C0_SCL), GP14 (I2C1_SDA), and GP15 (I2C1_SCL) on the |Raspberry Pi Pico|
header.

Serial Port
===========

The `RP2040 <RP2040 SoC_>`_ MCU has 2 UARTs. One of the UARTs (UART0) is
connected to external devices over GP0 (TX) and GP1 (RX) on the |Raspberry
Pi Pico| header, optional with full featured EIA 232D handshake signals, and
is the Zephyr console. UART1 is not available in any default setup.

USB Device Port
===============

The `RP2040 <RP2040 SoC_>`_ MCU has a (native) USB device port that can be used
to communicate with a host PC. See the
:external+zephyr:zephyr:code-sample-category:`usb` sample applications for more,
such as the :external+zephyr:zephyr:code-sample:`usb-cdc-acm` sample which sets
up a virtual serial port that echos characters back to the host PC. As an
alternative to the default Zephyr console on serial port the Bridle
:ref:`snippet-usb-console` can be used to enable
:external+zephyr:ref:`usb_device_cdc_acm` and switch the console to USB:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |waveshare_rp2040_lcd_0_96_VID|, idProduct=\ |waveshare_rp2040_lcd_0_96_PID_CON|, bcdDevice=\ |waveshare_rp2040_lcd_0_96_BCD_CON|
         USB device strings: Mfr=1, Product=2, SerialNumber=3
         Product: |waveshare_rp2040_lcd_0_96_PStr_CON|
         Manufacturer: |waveshare_rp2040_lcd_0_96_VStr|
         SerialNumber: B69F8448A6E91514

.. include:: /includes/rpi_waveshare_urb_pid_list.txt

Programmable I/O (PIO)
**********************

The `RP2040 SoC`_ comes with two PIO periherals. These are two simple
co-processors that are designed for I/O operations. The PIOs run a custom
instruction set, generated from a custom assembly language. PIO programs
are assembled using :program:`pioasm`, a tool provided by Raspberry Pi.
Further information can be found in the `Raspberry Pi Pico C/C++ SDK`_
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

If you don't have an SWD adapter, you can flash the board with a UF2 file.
By default, building an app for this board will generate a
:file:`build/zephyr/zephyr.uf2` file. If the board is powered on with
the :kbd:`BOOTSEL` button pressed, it will appear on the host as a mass
storage device:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |rpi_VID|, idProduct=\ |rpi_rp2040_PID|, bcdDevice=\ |rpi_rp2040_BCD|
         USB device strings: Mfr=1, Product=2, SerialNumber=0
         Product: |rpi_rp2040_PStr|
         Manufacturer: |rpi_VStr|
         SerialNumber: E0C9125B0D9B

The UF2 file should be drag-and-dropped or copied on command line to the
device, which will then flash the board.

RP2040 Boot-ROM
---------------

Each `RP2040 SoC`_ ships the `UF2 compatible <UF2 bootloader_>`_ bootloader
pico-bootrom-rp2040_, a native support in silicon. The full source for the
RP2040 bootrom at pico-bootrom-rp2040_ includes versions B0, B1 and B2 of
the bootrom, which correspond to the same silicon revisions, respectively.

Note that every time you build a program for the RP2040, the Pico SDK selects
an appropriate second stage bootloader based on what kind of external QSPI
Flash type the board configuration you are building for was giving. There
are |several versions of boot2|_ for different flash chips, and each one is
exactly 256 bytes of code which is put right at the start of the eventual
program binary. On Zephyr the :code:`boot2` versions are part of the
`Raspberry Pi Pico HAL`_ module. Possible selections:

:|CONFIG_RP2_FLASH_AT25SF128A|: |boot2_at25sf128a.S|_
:|CONFIG_RP2_FLASH_GENERIC_03H|: |boot2_generic_03h.S|_
:|CONFIG_RP2_FLASH_IS25LP080|: |boot2_is25lp080.S|_
:|CONFIG_RP2_FLASH_W25Q080|: |boot2_w25q080.S|_
:|CONFIG_RP2_FLASH_W25X10CL|: |boot2_w25x10cl.S|_

The board set this option to |CONFIG_RP2_FLASH_W25Q080|.

Further information can be found in the `RP2040 Datasheet`_, sections with
title :emphasis:`"Bootrom"` and :emphasis:`"Processor Controlled Boot Sequence"`
or Brian Starkey's Blog article `Pico serial bootloader`_

Using SEGGER JLink
------------------

You can flash the board with a SEGGER JLink debug probe as described in
:external+zephyr:ref:`Building, Flashing and Debugging <west-flashing>`.

Here is an example of building and flashing the
:external+zephyr:zephyr:code-sample:`blinky` application.

   .. zephyr-app-commands::
      :app: zephyr/samples/basic/blinky
      :build-dir: waveshare_rp2040_lcd_0_96
      :board: waveshare_rp2040_lcd_0_96/rp2040
      :flash-args: -r jlink
      :west-args: -p
      :goals: flash

Using OpenOCD
-------------

To use `PicoProbe`_ or `Raspberry Pi Debug Probe`_, you must configure
:program:`udev`. Create a file in :file:`/etc/udev.rules.d` with any name,
and write the line below:

   .. container:: highlight highlight-none notranslate literal-block

      .. parsed-literal::

         ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="0004", MODE="660", GROUP="plugdev", TAG+="uaccess"
         ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="000c", MODE="660", GROUP="plugdev", TAG+="uaccess"

This example is valid for the case that the user joins to :code:`plugdev`
groups.

The board has an SWD interface that can be used to program and debug the
on-board RP2040. This interface can be utilized by OpenOCD. To use it
with the RP2040, OpenOCD version 0.12.0 or later is needed. If you are using a
Debian based system (including RaspberryPi OS, Ubuntu, and more), using the
`pico_setup.sh`_ script is a convenient way to set up the forked version of
OpenOCD. Depending on the interface used (such as JLink), you might need to
checkout to a branch that supports this interface, before proceeding. Build
and install OpenOCD as described in the README.

Here is an example of building and flashing the
:external+zephyr:zephyr:code-sample:`blinky` application.

   .. zephyr-app-commands::
      :app: zephyr/samples/basic/blinky
      :build-dir: waveshare_rp2040_lcd_0_96
      :board: waveshare_rp2040_lcd_0_96/rp2040
      :gen-args: \
                 -DOPENOCD=/usr/local/bin/openocd \
                 -DOPENOCD_DEFAULT_PATH=/usr/local/share/openocd/scripts \
                 -DWAVESHARE_RP2040_DEBUG_ADAPTER=picoprobe
      :west-args: -p
      :flash-args: -r openocd
      :goals: flash

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
:external+zephyr:ref:`Building, Flashing and Debugging <west-debugging>`.

Using OpenOCD
-------------

Install OpenOCD as described for flashing the board.

Here is an example for debugging the
:external+zephyr:zephyr:code-sample:`blinky` application.

   .. zephyr-app-commands::
      :app: zephyr/samples/basic/blinky
      :build-dir: waveshare_rp2040_lcd_0_96
      :board: waveshare_rp2040_lcd_0_96/rp2040
      :maybe-skip-config:
      :gen-args: \
                 -DOPENOCD=/usr/local/bin/openocd \
                 -DOPENOCD_DEFAULT_PATH=/usr/local/share/openocd/scripts \
                 -DWAVESHARE_RP2040_DEBUG_ADAPTER=raspberrypi-swd
      :west-args: -p
      :flash-args: -r openocd
      :goals: debug
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

Basic Samples
*************

LED Blinky and Fade
===================

.. include:: blinky_fade.rsti

Hello Shell with USB-CDC/ACM Console
====================================

.. include:: helloshell.rsti

More Samples
************

Display Test and Demonstration
==============================

.. include:: display_test.rsti

References
**********

.. target-notes::
