.. _waveshare_rp2350:

Waveshare RP2350
################

The `RP2350 SoC`_ by Raspberry Pi Ltd. is a small sized and low-cost 32-bit
dual ARM Cortex-M33/ 32Bit Risc-V microcontroller and predestined for versatile board
designs. The Waveshare RP2350 board series based on this microcontroller
offers a wide range with different scaling factors, in size, features and
interfaces for communication, input and output.

Supported Boards
****************

Hardware
========

.. tabs::

   .. group-tab:: RP2350-CAN

      .. _rp2350_can:

      .. include:: rp2350-can/hardware.rsti


Positions
=========

.. tabs::

   .. group-tab:: RP2350-CAN

      .. include:: rp2350-can/positions.rsti


Pinouts
=======

The peripherals of the `RP2350 SoC`_ can be routed to various pins on
the board. The configuration of these routes can be modified through
:external+zephyr:ref:`DTS <devicetree>`. Please refer to the datasheet
to see the possible routings for each peripheral. The default assignments
for the various Waveshare RP2350 boards are defined below separately
in a single tab.

.. tabs::

   .. group-tab:: RP2350-CAN

      .. include:: rp2350-can/pinouts.rsti


Supported Features
******************

Similar to the |zephyr:board:rpi_pico| the Waveshare RP2350 board configuration
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
     - :dtcompatible:`raspberrypi,pico-uart`
     - :external+zephyr:ref:`uart_api`
   * - UDC (USB Device Controller)
     - :kconfig:option:`CONFIG_USB_DEVICE_STACK`
     - :dtcompatible:`raspberrypi,pico-usbd`
     - :external+zephyr:ref:`usb_api`
   * - I2C
     - :kconfig:option:`CONFIG_I2C`
     - :dtcompatible:`raspberrypi,pico-i2c`
     - :external+zephyr:ref:`i2c_api`
   * - SPI
     - :kconfig:option:`CONFIG_SPI`
     - :dtcompatible:`raspberrypi,pico-spi`
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
     - :dtcompatible:`arm,v8m-nvic`
     - Nested Vector :external+zephyr:ref:`interrupts_v2` Controller
   * - SYSTICK
     - :dtcompatible:`arm,armv8m-systick`
     - N/A
     -

Other hardware features are not currently supported by Zephyr. The default
configuration can be found in the different Kconfig files:

   - :bridle_file:`boards/waveshare/rp2350/rp2350_can_rp2350a_m33_defconfig`


Board Configurations
====================

The Waveshare RP2350 boards can be configured for the following different
use cases. The |RP2350-Plus| board offers an assembly option with 16㎆ Flash,
which is mapped as a hardware revision.

.. tabs::

   .. group-tab:: RP2350-CAN

      .. rubric:: :command:`west build -b rp2350_can/rp2350a/m33`

      Use the serial port UART0 on edge header as
      Zephyr console and for the shell.

      .. rubric:: :command:`west build -b rp2350_can/rp2350a/m33 -S usb-console`

      Use the native USB device port with CDC-ACM as
      Zephyr console and for the shell.


Connections and IOs
===================

The `Waveshare wiki`_ has detailed information about board connections.
Download the different schematics or datasheets as linked above per board
for more details. The pinout diagrams can also be found there.

System Clock
============


GPIO (PWM) Ports
================


ADC/TS Ports
============


SPI Port
========

The `RP2350 <RP2350 SoC_>`_ MCU has 2 SPIs. To the edge connectors SPI0 is
connect to external devices over GP19 (MOSI), GP16 (MISO), GP18 (SCK), and
GP17 (CSn) on the |Waveshare RP2350-CAN| uses  over GP11 (MOSI), GP12 (MISO),
GP10 (SCK), and GP9 (CSn) for can-controller.


I2C Port
========


Serial Port
===========

The `RP2350 <RP2350 SoC_>`_ MCU has 2 UARTs. One of the UARTs (UART0) is
connected to external devices over GP0 (TX) and GP1 (RX).


USB Device Port
===============

The `RP2350 <RP2350 SoC_>`_ MCU has a (native) USB device port that can be used
to communicate with a host PC. See the
:external+zephyr:zephyr:code-sample-category:`usb` sample applications for more,
such as the :external+zephyr:zephyr:code-sample:`usb-cdc-acm` sample which sets
up a virtual serial port that echos characters back to the host PC.
As an alternative to the default Zephyr console on serial port the
Bridle :ref:`snippet-usb-console` can be used to enable
:external+zephyr:ref:`usb_device_cdc_acm` and switch the console to USB

.. tabs::

   .. group-tab:: RP2350-One

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |rp2350_can_VID|, idProduct=\ |rp2350_can_PID_CON|, bcdDevice=\ |waveshare_rp2350_BCD_CON|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |rp2350_can_PStr_CON|
               Manufacturer: |rp2350_can_VStr|
               SerialNumber: B69F8448A6E91514


|nbsp|

Programmable I/O (PIO)
**********************

The `RP2350 SoC`_ comes with two PIO periherals. These are two simple
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

If you don't have an SWD adapter, you can flash the Waveshare RP2350 boards
with a UF2 file. By default, building an app for this board will generate a
:file:`build/zephyr/zephyr.uf2` file. If the board is powered on with the
:kbd:`BOOTSEL` button pressed, it will appear on the host as a mass
storage device:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |rpi_VID|, idProduct=\ |rpi_rp2350_PID|, bcdDevice=\ |rpi_rp2350_BCD|
         USB device strings: Mfr=1, Product=2, SerialNumber=0
         Product: |rpi_rp2350_PStr|
         Manufacturer: |rpi_VStr|
         SerialNumber: E0C9125B0D9B

The UF2 file should be drag-and-dropped or copied on command line to the
device, which will then flash the Waveshare RP2350 board.

Each `RP2350 SoC`_ ships the `UF2 compatible <UF2 bootloader_>`_ bootloader
pico-bootrom_, a native support in silicon. The full source for the RP2350
bootrom at pico-bootrom_ includes versions 1, 2 and 3 of the bootrom, which
correspond to the B0, B1 and B2 silicon revisions, respectively.

Note that every time you build a program for the RP2350, the Pico SDK selects
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

All Waveshare RP2350 boards set this option to |CONFIG_RP2_FLASH_W25Q080|.
Further information can be found in the `RP2350 Datasheet`_, sections with
title :emphasis:`"Bootrom"` and :emphasis:`"Processor Controlled Boot Sequence"`
or Brian Starkey's Blog article `Pico serial bootloader`_

Using SEGGER JLink
------------------

You can flash the Waveshare RP2350 boards with a SEGGER JLink debug probe as
described in
:external+zephyr:ref:`Building, Flashing and Debugging <west-flashing>`.

Here is an example of building and flashing the
:external+zephyr:zephyr:code-sample:`blinky` application.

.. zephyr-app-commands::
   :app: zephyr/samples/basic/blinky
   :board: rp2350_can/rp2350a/m33
   :build-dir: rp2350_can
   :goals: flash
   :flash-args: -r jlink
   :west-args: -p

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

The |RP2350-LCD-0.96| and |RP2350-Plus| has an SWD interface that can be used
to program and debug the on board RP2350. This interface can be utilized by
OpenOCD. To use it with the RP2350, OpenOCD version 0.12.0 or later is needed.
If you are using a Debian based system (including RaspberryPi OS, Ubuntu,
and more), using the `pico_setup.sh`_ script is a convenient way to set up
the forked version of OpenOCD. Depending on the interface used (such as JLink),
you might need to checkout to a branch that supports this interface, before
proceeding. Build and install OpenOCD as described in the README.

Here is an example of building and flashing the
:external+zephyr:zephyr:code-sample:`blinky` application.

.. zephyr-app-commands::
   :app: zephyr/samples/basic/blinky
   :board: rp2350_can/rp2350a/m33
   :build-dir: rp2350_can
   :goals: flash
   :west-args: -p
   :flash-args: -r openocd
   :gen-args: \
              -DOPENOCD=/usr/local/bin/openocd \
              -DOPENOCD_DEFAULT_PATH=/usr/local/share/openocd/scripts \
              -DWAVESHARE_RP2350_DEBUG_ADAPTER=picoprobe

Set the environment variables :strong:`OPENOCD` to
:file:`/usr/local/bin/openocd` and :strong:`OPENOCD_DEFAULT_PATH` to
:file:`/usr/local/share/openocd/scripts`. This should work with the OpenOCD
that was installed with the default configuration. This configuration also
works with an environment that is set up by the `pico_setup.sh`_ script.

:strong:`WAVESHARE_RP2350_DEBUG_ADAPTER` specifies what debug adapter is
used for debugging. If :strong:`WAVESHARE_RP2350_DEBUG_ADAPTER` was not
assigned, :dfn:`cmsis-dap` is used by default. The other supported adapters
are :dfn:`picoprobe`, :dfn:`raspberrypi-swd`, :dfn:`jlink` and
:dfn:`blackmagicprobe`. How to connect :dfn:`picoprobe` and
:dfn:`raspberrypi-swd` is described in `Getting Started Guide with Raspberry
Pi Pico`_. Any other SWD debug adapter maybe also work with this configuration.
The value of :strong:`WAVESHARE_RP2350_DEBUG_ADAPTER` is cached, so it can
be omitted from :program:`west flash` and :program:`west debug` if it was
previously set while running :program:`west build`.
:strong:`WAVESHARE_RP2350_DEBUG_ADAPTER` is used in an argument to OpenOCD as
:code:`"source [find interface/${WAVESHARE_RP2350_DEBUG_ADAPTER}.cfg]"`. Thus,
:strong:`WAVESHARE_RP2350_DEBUG_ADAPTER` needs to be assigned the file name of
the debug adapter.

You can also flash the board with the following command that directly calls
OpenOCD (assuming a SEGGER JLink adapter is used):

.. code-block:: console

   $ openocd -f interface/jlink.cfg    \
             -c 'transport select swd' \
             -f target/rp2350.cfg      \
             -c "adapter speed 2000"   \
             -c 'targets rp2350.core0' \
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
   :board: rp2350_can/rp2350a/m33
   :build-dir: rp2350_can
   :maybe-skip-config:
   :goals: debug
   :west-args: -p
   :flash-args: -r openocd
   :gen-args: \
              -DOPENOCD=/usr/local/bin/openocd \
              -DOPENOCD_DEFAULT_PATH=/usr/local/share/openocd/scripts \
              -DWAVESHARE_RP2350_DEBUG_ADAPTER=raspberrypi-swd
   :host-os: unix

As with flashing, you can specify the debug adapter by specifying
:strong:`WAVESHARE_RP2350_DEBUG_ADAPTER` at :program:`west build` time.
No needs to specify it at :program:`west debug` time.

You can also debug with OpenOCD and gdb launching from command-line.
Run the following command:

.. code-block:: console

   $ openocd -f interface/jlink.cfg    \
             -c 'transport select swd' \
             -f target/rp2350.cfg      \
             -c "adapter speed 2000"   \
             -c 'targets rp2350.core0'

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

   .. group-tab:: RP2350-One

      .. rubric:: WS2812 LED Test Pattern by PIO

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`led-strip`.

      .. image:: rp2350-one/ws2812b.gif
         :align: right
         :alt: Waveshare RP2350-One WS2812 LED Test Pattern

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/led/led_strip
         :board: rp2350_can/rp2350a/m33
         :build-dir: rp2350_can
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. hint::

         Neither LED Blinky nor LED Fade can be built and executed on
         |RP2350-One|, because this system has only one digital RGB LED.
         A simple GPIO or PWM control is not possible!


Hello Shell with USB-CDC/ACM Console
====================================

.. tabs::

   .. group-tab:: RP2350-CAN

      .. rubric:: Hello Shell

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :board: rp2350_can/rp2350a/m33
         :build-dir: rp2350_can
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. include:: rp2350-can/helloshell.rsti


CANnectivity
============

.. tabs::

   .. group-tab:: RP2350-CAN

      .. rubric:: Hello Shell

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :board: rp2350_can/rp2350a/m33
         :build-dir: rp2350_can
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. include:: rp2350-can/cannectivity.rsti



References
**********

.. target-notes::
