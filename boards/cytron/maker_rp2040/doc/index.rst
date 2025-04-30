.. _cytron_maker_rp2040:

Cytron Maker RP2040
###################

The `RP2040 SoC`_ by Raspberry Pi Ltd. is a small sized and low-cost 32-bit
dual ARM Cortex-M0+ microcontroller and predestined for versatile board
designs. The Cytron Maker RP2040 board series based on this microcontroller
offers a wide range with different scaling factors, in size, features and
interfaces for communication, input and output.

Supported Boards
****************

Hardware
========

.. tabs::

   .. group-tab:: Maker Nano RP2040

      .. _cytron_maker_nano_rp2040:

      .. include:: maker-nano-rp2040/hardware.rsti

   .. group-tab:: Maker Pi RP2040

      .. _cytron_maker_pi_rp2040:

      .. include:: maker-pi-rp2040/hardware.rsti

Positions
=========

.. tabs::

   .. group-tab:: Maker Nano RP2040

      .. include:: maker-nano-rp2040/positions.rsti

   .. group-tab:: Maker Pi RP2040

      .. _cytron_maker_pi_rp2040_positions:

      .. include:: maker-pi-rp2040/positions.rsti

Pinouts
=======

The peripherals of the `RP2040 SoC`_ can be routed to various pins on
the board. The configuration of these routes can be modified through
:external+zephyr:ref:`DTS <devicetree>`. Please refer to the datasheet
to see the possible routings for each peripheral. The default assignments
for the various Cytron Maker RP2040 boards are defined below separately
in a single tab.

.. tabs::

   .. group-tab:: Maker Nano RP2040

      .. include:: maker-nano-rp2040/pinouts.rsti

   .. group-tab:: Maker Pi RP2040

      .. include:: maker-pi-rp2040/pinouts.rsti

Supported Features
******************

Similar to the |zephyr:board:rpi_pico| the Cytron Maker RP2040 board
configuration supports the following hardware features:

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
     - :dtcompatible:`arm,v6m-nvic`
     - Nested Vector :external+zephyr:ref:`interrupts_v2` Controller
   * - SYSTICK
     - N/A
     - :dtcompatible:`arm,armv6m-systick`
     -

Other hardware features are not currently supported by Zephyr. The default
configuration can be found in the different Kconfig files:

   - :bridle_file:`boards/cytron/maker_rp2040/cytron_maker_nano_rp2040_defconfig`
   - :bridle_file:`boards/cytron/maker_rp2040/cytron_maker_pi_rp2040_defconfig`

Board Configurations
====================

The Cytron Maker RP2040 boards can be configured for the following different
use cases.

.. tabs::

   .. group-tab:: Maker Nano RP2040

      .. rubric:: :command:`west build -b cytron_maker_nano_rp2040`

      Use the serial port UART0 on edge header as
      Zephyr console and for the shell.

      .. rubric:: :command:`west build -b cytron_maker_nano_rp2040 -S usb-console`

      Use the native USB device port with CDC-ACM as
      Zephyr console and for the shell.

   .. group-tab:: Maker Pi RP2040

      .. rubric:: :command:`west build -b cytron_maker_pi_rp2040`

      Use the serial port UART0 on edge header as
      Zephyr console and for the shell.

      .. rubric:: :command:`west build -b cytron_maker_pi_rp2040 -S usb-console`

      Use the native USB device port with CDC-ACM as
      Zephyr console and for the shell.

Connections and IOs
===================

The `Cytron Marktplace`_ has detailed information about board connections.
Download the different schematics or datasheets as linked above per board
for more details. The pinout diagrams can also be found there.

.. _cytron_maker_rp2040_grove_if:

Laced Grove Signal Interface
----------------------------

Both the |Maker Nano RP2040| and the |Maker Pi RP2040| offer the option of
connecting hardware modules via a variety of |Grove connectors|.
These are provided by a specific interface for general signal mapping, the
|Laced Grove Signal Interface|.

Following mappings are well known:

   * ``grove_gpios``: GPIO mapping
   * ``grove_pwms``: PWM mapping

.. tabs::

   .. group-tab:: Maker Nano RP2040

      In addition to the |Arduino Nano| header, there are also
      2 |Grove connectors| (Qwiic/STEMMA QT).

      .. tabs::

         .. group-tab:: GPIO mapping ``grove_gpios``

            This is the **GPIO signal line mapping** from the `Arduino Nano R3`_
            header bindet with :dtcompatible:`arduino-nano-header-r3` to the set
            of |Grove connectors| provided as |Laced Grove Signal Interface|.

            **This list must not be stable!**

            .. include:: maker-nano-rp2040/grove_gpios.rsti

         .. group-tab:: PWM mapping ``grove_pwms``

            The corresponding mapping is always board or SOC specific.
            In addition to the **PWM signal line mapping**, the valid
            references to the PWM function units in the SOC or on the
            board are therefore also defined as **Grove PWM Labels**.
            The following table reflects the currently supported mapping
            for :code:`cytron_maker_nano_rp2040`, but this list will be
            growing up with further development and maintenance.

            **This list must not be complete or stable!**

            .. include:: maker-nano-rp2040/grove_pwms.rsti

   .. group-tab:: Maker Pi RP2040

      In addition to the on-board hader for DC and servo motors, there are also
      7 |Grove connectors| (Qwiic/STEMMA QT).

      .. tabs::

         .. group-tab:: GPIO mapping ``grove_gpios``

            This is the **GPIO signal line mapping** from the `RP2040 SOC`_
            to the set of |Grove connectors| provided as |Laced Grove Signal
            Interface|.

            **This list must not be stable!**

            .. include:: maker-pi-rp2040/grove_gpios.rsti

         .. group-tab:: PWM mapping ``grove_pwms``

            The corresponding mapping is always board or SOC specific.
            In addition to the **PWM signal line mapping**, the valid
            references to the PWM function units in the SOC or on the
            board are therefore also defined as **Grove PWM Labels**.
            The following table reflects the currently supported mapping
            for :code:`cytron_maker_nano_rp2040`, but this list will be
            growing up with further development and maintenance.

            **This list must not be complete or stable!**

            .. include:: maker-pi-rp2040/grove_pwms.rsti

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
the |Maker Nano RP2040|, almost all 16 PWM channels are available on the edge
connectors, although some channels are occupied by special signals if their
function is enabled. On |Maker Pi RP2040| the channels PWM4 A to PWM5 B are
reserved for the on-board DC motor H-bridge driver and also PWM5 A to PWM7 B
for driving servo motors. The PWM3 channel A will be used for the on-board
Piezo buzzer on the two boards |Maker Nano RP2040| and |Maker Pi RP2040|.
But the PWM operation is not enable by default. Only if
:kconfig:option:`CONFIG_PWM_RPI_PICO` is enabled then the first user LED or
Piezo buzzer is driven by PWM instead of by GPIO.

ADC/TS Ports
============

The `RP2040 <RP2040 SoC_>`_ MCU has 1 ADC with 4 channels and an additional
fifth channel for the on-chip temperature sensor (TS). The ADC channels 0-3
are available on the |Arduino Nano| header, channel 0-1 also on one of the
two Qwiic / STEMMA QT compatiple connectors on |Maker Nano RP2040|, but this
is not the default pin operation. On |Maker Pi RP2040| only the ADC channel
0-2 are available on three of the four Grove compatiple connectors, ADC
channel 3 will be used for internal on-board voltage monitoring.

The external voltage reference ADC_VREF is directly connected to the 3.3V
power supply.

SPI Port
========

The `RP2040 <RP2040 SoC_>`_ MCU has 2 SPIs. The serial bus SPI0 is connect to
external devices over GP19 (MOSI), GP16 (MISO), GP18 (SCK), and GP17 (CSn)
on the |Arduino Nano| header of |Maker Nano RP2040| or over GP3 (MOSI),
GP4 (MISO), GP2 (SCK), and GP5 (CSn) by two Grove compatiple connectors on
the |Maker Pi RP2040|. SPI1 is not available in any default setup.

I2C Port
========

The `RP2040 <RP2040 SoC_>`_ MCU has 2 I2Cs. The serial bus I2C0 and I2C1 are
connect to external devices over GP12 (I2C0_SDA), GP13 (I2C0_SCL),
GP26 (I2C1_SDA), and GP27 (I2C1_SCL) on the |Arduino Nano| header of
|Maker Nano RP2040| or over GP16 (I2C0_SDA), GP17 (I2C0_SCL) by default or
alternatively over GP4 (I2C0_SDA), GP5 (I2C0_SCL), GP2 (I2C1_SDA) and
GP3 (I2C1_SCL) on the Grove compatiple connectors on the |Maker Pi RP2040|.

Serial Port
===========

The `RP2040 <RP2040 SoC_>`_ MCU has 2 UARTs. One of the UARTs (UART0) is
connected to external devices over GP0 (TX) and GP1 (RX) on both the
|Maker Nano RP2040| and the |Maker Pi RP2040| header in same manner
and is the Zephyr console.

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

   .. tabs::

      .. group-tab:: Maker Nano RP2040

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |cytron_maker_nano_rp2040_VID|, idProduct=\ |cytron_maker_nano_rp2040_PID_CON|, bcdDevice=\ |cytron_maker_nano_rp2040_BCD_CON|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |cytron_maker_nano_rp2040_PStr_CON|
               Manufacturer: |cytron_maker_nano_rp2040_VStr|
               SerialNumber: BF002B12140C620C

      .. group-tab:: Maker Pi RP2040

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |cytron_maker_pi_rp2040_VID|, idProduct=\ |cytron_maker_pi_rp2040_PID_CON|, bcdDevice=\ |cytron_maker_pi_rp2040_BCD_CON|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |cytron_maker_pi_rp2040_PStr_CON|
               Manufacturer: |cytron_maker_pi_rp2040_VStr|
               SerialNumber: BF002B12140C620C

To integrate specific USB device functions that do not follow
a USB standard class, the following alternate identifier numbers
are available for the various Cytron Maker RP2040 and RP2350 boards
according to the `Raspberry Pi USB product ID list`_:

.. container:: twocol

   .. container:: leftside

      .. rubric:: RP2040

      :|rpi_cytron_maker_pi_rp2040_URB_PID|: |Maker Nano RP2040|
      :|rpi_cytron_maker_nano_rp2040_URB_PID|: |Maker Pi RP2040|
      :|rpi_cytron_maker_uno_rp2040_URB_PID|: Maker UNO RP2040
      :|rpi_cytron_edu_pico_URB_PID|: EDU PICO
      :|rpi_cytron_edu_pico_rp2040_URB_PID|: EDU PICO
      :|rpi_cytron_p_iriv_io_ctrl_URB_PID|: IRIV IO Controller

   .. container:: rightside

      .. rubric:: RP2350

      :|rpi_cytron_motion_2350_pro_URB_PID|: MOTION 2350 Pro

|nbsp|

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

If you don't have an SWD adapter, you can flash the Cytron Maker RP2040 boards
with a UF2 file. By default, building an app for this board will generate a
:file:`build/zephyr/zephyr.uf2` file. If the board is powered on with the
:kbd:`BOOTSEL` button pressed, it will appear on the host as a mass
storage device:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |rpi_VID|, idProduct=\ |rpi_rp2040_PID|, bcdDevice=\ |rpi_rp2040_BCD|
         USB device strings: Mfr=1, Product=2, SerialNumber=0
         Product: |rpi_rp2040_PStr|
         Manufacturer: |rpi_VStr|
         SerialNumber: E0C9125B0D9B

The UF2 file should be drag-and-dropped or copied on command line to the
device, which will then flash the Cytron Maker RP2040 board.

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

:|CONFIG_RP2_FLASH_AT25SF128A|: |boot2_at25sf128a.S|_
:|CONFIG_RP2_FLASH_GENERIC_03H|: |boot2_generic_03h.S|_
:|CONFIG_RP2_FLASH_IS25LP080|: |boot2_is25lp080.S|_
:|CONFIG_RP2_FLASH_W25Q080|: |boot2_w25q080.S|_
:|CONFIG_RP2_FLASH_W25X10CL|: |boot2_w25x10cl.S|_

All Cytron Maker RP2040 boards set this option to |CONFIG_RP2_FLASH_W25Q080|.
Further information can be found in the `RP2040 Datasheet`_, sections with
title :emphasis:`"Bootrom"` and :emphasis:`"Processor Controlled Boot Sequence"`
or Brian Starkey's Blog article `Pico serial bootloader`_

Using SEGGER JLink
------------------

You can flash the Cytron Maker RP2040 boards with a SEGGER JLink debug probe as
described in :external+zephyr:ref:`Building, Flashing and Debugging <west-flashing>`.

Here is an example of building and flashing the
:external+zephyr:zephyr:code-sample:`blinky` application.

.. zephyr-app-commands::
   :app: zephyr/samples/basic/blinky
   :board: cytron_maker_pi_rp2040
   :build-dir: cytron_maker_rp2040
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

The |Maker Pi RP2040| has an SWD interface that can be used to program and
debug the on board RP2040. This interface can be utilized by OpenOCD. To use it
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
   :board: cytron_maker_pi_rp2040
   :build-dir: cytron_maker_rp2040
   :goals: flash
   :west-args: -p
   :flash-args: -r openocd
   :gen-args: \
              -DOPENOCD=/usr/local/bin/openocd \
              -DOPENOCD_DEFAULT_PATH=/usr/local/share/openocd/scripts \
              -DCYTRON_RP2040_DEBUG_ADAPTER=picoprobe

Set the environment variables :strong:`OPENOCD` to
:file:`/usr/local/bin/openocd` and :strong:`OPENOCD_DEFAULT_PATH` to
:file:`/usr/local/share/openocd/scripts`. This should work with the OpenOCD
that was installed with the default configuration. This configuration also
works with an environment that is set up by the `pico_setup.sh`_ script.

:strong:`CYTRON_RP2040_DEBUG_ADAPTER` specifies what debug adapter is
used for debugging. If :strong:`CYTRON_RP2040_DEBUG_ADAPTER` was not
assigned, :dfn:`cmsis-dap` is used by default. The other supported adapters
are :dfn:`picoprobe`, :dfn:`raspberrypi-swd`, :dfn:`jlink` and
:dfn:`blackmagicprobe`. How to connect :dfn:`picoprobe` and
:dfn:`raspberrypi-swd` is described in `Getting Started Guide with Raspberry
Pi Pico`_. Any other SWD debug adapter maybe also work with this configuration.
The value of :strong:`CYTRON_RP2040_DEBUG_ADAPTER` is cached, so it can
be omitted from :program:`west flash` and :program:`west debug` if it was
previously set while running :program:`west build`.
:strong:`CYTRON_RP2040_DEBUG_ADAPTER` is used in an argument to OpenOCD as
:code:`"source [find interface/${CYTRON_RP2040_DEBUG_ADAPTER}.cfg]"`. Thus,
:strong:`CYTRON_RP2040_DEBUG_ADAPTER` needs to be assigned the file name of
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
   :board: cytron_maker_pi_rp2040
   :build-dir: cytron_maker_rp2040
   :maybe-skip-config:
   :goals: debug
   :west-args: -p
   :flash-args: -r openocd
   :gen-args: \
              -DOPENOCD=/usr/local/bin/openocd \
              -DOPENOCD_DEFAULT_PATH=/usr/local/share/openocd/scripts \
              -DCYTRON_RP2040_DEBUG_ADAPTER=raspberrypi-swd
   :host-os: unix

As with flashing, you can specify the debug adapter by specifying
:strong:`CYTRON_RP2040_DEBUG_ADAPTER` at :program:`west build` time.
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

   .. group-tab:: Maker Nano RP2040

      .. rubric:: WS2812 LED Test Pattern by PIO

      .. image:: maker-nano-rp2040/ws2812b.gif
         :align: right
         :alt: Maker Nano RP2040 WS2812 LED Test Pattern

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`led-strip`.

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/led/led_strip
         :board: cytron_maker_nano_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Blue User LED Blinky by GPIO

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`blinky`.

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky
         :board: cytron_maker_nano_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Blue User LED Blinky by PWM

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`pwm-blinky`.

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky_pwm
         :board: cytron_maker_nano_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Blue User LED Fade by PWM

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`fade-led`.

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/fade_led
         :board: cytron_maker_nano_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Blue User LED On/Off by GPIO Button

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`button`.

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/button
         :board: cytron_maker_nano_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

   .. group-tab:: Maker Pi RP2040

      .. rubric:: WS2812 LED Test Pattern by PIO

      .. image:: maker-pi-rp2040/ws2812b.gif
         :align: right
         :alt: Maker Pi RP2040 WS2812 LED Test Pattern

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`led-strip`.

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/led/led_strip
         :board: cytron_maker_pi_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Blue User LED Blinky by GPIO

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`blinky`.

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky
         :board: cytron_maker_pi_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Blue User LED Blinky by PWM

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`pwm-blinky`.

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky_pwm
         :board: cytron_maker_pi_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Blue User LED Fade by PWM

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`fade-led`.

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/fade_led
         :board: cytron_maker_pi_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Blue User LED On/Off by GPIO Button

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`button`.

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/button
         :board: cytron_maker_pi_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

Hello Shell with USB-CDC/ACM Console
====================================

.. tabs::

   .. group-tab:: Maker Nano RP2040

      .. rubric:: Hello Shell

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :board: cytron_maker_nano_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. include:: maker-nano-rp2040/helloshell.rsti

   .. group-tab:: Maker Pi RP2040

      .. rubric:: Hello Shell

      .. zephyr-app-commands::
         :app: bridle/samples/helloshell
         :board: cytron_maker_pi_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. include:: maker-pi-rp2040/helloshell.rsti

Input dump with USB-CDC/ACM Console
===================================

Prints all input events as defined by the shields Devicetree. See also Zephyr
sample: :external+zephyr:zephyr:code-sample:`input-dump`.

.. tabs::

   .. group-tab:: Maker Nano RP2040

      Print the input events related to the one on-board user button
      using the :external+zephyr:ref:`Input subsystem API <input>`. That are:

      | :hwftlbl-btn:`BTN1` : :dts:`zephyr,code = <INPUT_KEY_0>;`

      .. rubric:: Devicetree compatible

      - :dtcompatible:`zephyr,lvgl-keypad-input` with devicetree relation
        :dts:`lvgl_keypad: lvgl-keypad { input = <&gpio_keys>; };`

        | :hwftlbl-btn:`BTN1` :
          :dts:`input-codes = <INPUT_KEY_0>;` :
          :dts:`lvgl-codes = <LV_KEY_ENTER>;`

      .. rubric:: Button Input Dump

      .. zephyr-app-commands::
         :app: zephyr/samples/subsys/input/input_dump
         :board: cytron_maker_nano_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Simple logging output on target

      .. container:: highlight highlight-console notranslate no-copybutton

         .. parsed-literal::

            \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
            W: BUS RESET
            W: BUS RESET
            \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*
            Input sample started
            I: input event: dev=gpio_keys        SYN type= 1 code= 11 value=1
            I: input event: dev=gpio_keys        SYN type= 1 code= 11 value=0

   .. group-tab:: Maker Pi RP2040

      Print the input events related to the two on-board user button
      using the :external+zephyr:ref:`Input subsystem API <input>`. That are:

      | :hwftlbl-btn:`BTN1` : :dts:`zephyr,code = <INPUT_KEY_0>;`
      | :hwftlbl-btn:`BTN2` : :dts:`zephyr,code = <INPUT_KEY_1>;`

      .. rubric:: Devicetree compatible

      - :dtcompatible:`zephyr,lvgl-keypad-input` with devicetree relation
        :dts:`lvgl_keypad: lvgl-keypad { input = <&gpio_keys>; };`

        | :hwftlbl-btn:`BTN1` :
          :dts:`input-codes = <INPUT_KEY_0>;` :
          :dts:`lvgl-codes = <LV_KEY_ENTER>;`
        | :hwftlbl-btn:`BTN2` :
          :dts:`input-codes = <INPUT_KEY_1>;` :
          :dts:`lvgl-codes = <LV_KEY_NEXT>;`

      .. rubric:: Button Input Dump

      .. zephyr-app-commands::
         :app: zephyr/samples/subsys/input/input_dump
         :board: cytron_maker_pi_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Simple logging output on target

      .. container:: highlight highlight-console notranslate no-copybutton

         .. parsed-literal::

            \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
            W: BUS RESET
            W: BUS RESET
            \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*
            Input sample started
            I: input event: dev=gpio_keys        SYN type= 1 code= 11 value=1
            I: input event: dev=gpio_keys        SYN type= 1 code= 11 value=0
            I: input event: dev=gpio_keys        SYN type= 1 code=  2 value=1
            I: input event: dev=gpio_keys        SYN type= 1 code=  2 value=0

Sounds from the speaker with USB-CDC/ACM Console
================================================

.. tabs::

   .. group-tab:: Maker Nano RP2040

      .. rubric:: Piezo Buzzer Test

      .. image:: maker-nano-rp2040/buzzer.jpg
         :align: right
         :alt: Maker Nano RP2040 Piezo Buzzer Test

      The sample is prepared for the on-board :hwftlbl-spk:`PWM_BUZZER` connected
      to the PWM channel at :rpi-pico-pio:`GP22` / :rpi-pico-pwm:`PWM6` (PWM3CHA).

      The PWM period is 880 ㎐, twice the concert pitch frequency of 440 ㎐.

      .. literalinclude:: ../maker_buzzer.dtsi
         :caption: maker_buzzer.dtsi
         :language: DTS
         :encoding: ISO-8859-1
         :emphasize-lines: 3,11,18
         :linenos:
         :start-at: / {

      Invoke :program:`west build` and :program:`west flash`:

      .. zephyr-app-commands::
         :app: bridle/samples/buzzer
         :board: cytron_maker_nano_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Simple test execution on target

      #. play a beep
      #. play a folk song
      #. play a chrismas song

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **buzzer beep**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **buzzer play folksong**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **buzzer play xmastime**

   .. group-tab:: Maker Pi RP2040

      .. rubric:: Piezo Buzzer Test

      .. image:: maker-pi-rp2040/buzzer.jpg
         :align: right
         :alt: Maker Pi RP2040 Piezo Buzzer Test

      The sample is prepared for the on-board :hwftlbl-spk:`PWM_BUZZER` connected
      to the PWM channel at :rpi-pico-pio:`GP22` / :rpi-pico-pwm:`PWM6` (PWM3CHA).

      The PWM period is 880 ㎐, twice the concert pitch frequency of 440 ㎐.

      .. literalinclude:: ../maker_buzzer.dtsi
         :caption: maker_buzzer.dtsi
         :language: DTS
         :encoding: ISO-8859-1
         :emphasize-lines: 3,11,18
         :linenos:
         :start-at: / {

      Invoke :program:`west build` and :program:`west flash`:

      .. zephyr-app-commands::
         :app: bridle/samples/buzzer
         :board: cytron_maker_pi_rp2040
         :build-dir: cytron_maker_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Simple test execution on target

      #. play a beep
      #. play a folk song
      #. play a chrismas song

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **buzzer beep**
            :bgn:`uart:~$` **buzzer play folksong**
            :bgn:`uart:~$` **buzzer play xmastime**

Drive a motor with USB-CDC/ACM Console
======================================

.. tabs::

   .. group-tab:: Maker Nano RP2040

      .. rubric:: Servomotor Test

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`servo-motor`.

      .. hint::

         The |Maker Nano RP2040| can't drive any servo motor without additional
         equipment. This example is not applicable.

   .. group-tab:: Maker Pi RP2040

      .. rubric:: Servomotor Test

      .. image:: img/servo.png
         :align: right
         :alt: Maker Pi RP2040 Servomotor Test

      The sample is prepared for servomotor :hwftlbl-act:`PWM_SERVO_0` at
      first on-board channel at :rpi-pico-pio:`GP12` / :rpi-pico-pwm:`PWM12`
      (PWM6CHA).

      .. literalinclude:: ../makerpi_servo.dtsi
         :caption: makerpi_servo.dtsi
         :language: DTS
         :encoding: ISO-8859-1
         :emphasize-lines: 3,14,33
         :linenos:
         :start-at: / {

      .. tsn-include:: snippets/pwm-servo/README.rst
         :docset: bridle
         :start-after: .. _snippet-pwm-servo-cytron-maker-pi-rp2040:
         :end-before: .. literalinclude:

Display Test and Demonstration
==============================

This samples and test applications are only applicable together with the
|Waveshare 2.4 LCD| shield. This LCD module have to connected by free wiring.

.. tabs::

   .. group-tab:: Maker Nano RP2040

      Connect the |Waveshare 2.4 LCD| module by free wiring to the
      |Arduino Nano| header. Following module's pin assignments
      for *Arduino Nano R3*.

      .. list-table::
         :align: center
         :width: 50%
         :widths: 5, 45, 5, 45

         * - .. rubric:: Pin
           - .. rubric:: |Maker Nano RP2040|
           - .. rubric:: Pin
           - .. rubric:: |Waveshare 2.4 LCD|

         * - :rpi-pico-pin:`17`
           - :rpi-pico-vdd:`3V3(OUT)`
           - :rpi-pico-pin:`1`
           - :hwftlbl-vdd:`VCC`

         * - :rpi-pico-pin:`29`
           - :rpi-pico-gnd:`GND`
           - :rpi-pico-pin:`2`
           - :hwftlbl:`GND`

         * - :rpi-pico-pin:`14`
           - :rpi-pico-spi-dfl:`SPI0_TX` : D11
           - :rpi-pico-pin:`3`
           - :hwftlbl-scr:`DIN`
             :hwftlbl-spi:`COPI`

             ILI9341 Serial Data Input

         * - :rpi-pico-pin:`16`
           - :rpi-pico-spi-dfl:`SPI0_SCK` : D13
           - :rpi-pico-pin:`4`
           - :hwftlbl-scr:`CLK`
             :hwftlbl-spi:`SCK`

             ILI9341 Serial Clock Input

         * - :rpi-pico-pin:`13`
           - :rpi-pico-spi-dfl:`SPI0_CSN` : D10
           - :rpi-pico-pin:`5`
           - :hwftlbl-scr:`CS`
             :hwftlbl-spi:`CSN`

             ILI9341 Chip Select Input

         * - :rpi-pico-pin:`10`
           - :rpi-pico-pio:`GP7` : D7
           - :rpi-pico-pin:`6`
           - :hwftlbl-scr:`DC`
             :hwftlbl-pio:`DC`

             ILI9341 Data/Command

         * - :rpi-pico-pin:`11`
           - :rpi-pico-pio:`GP8` : D8
           - :rpi-pico-pin:`7`
           - :hwftlbl-scr:`RST`
             :hwftlbl-pio:`RST`

             ILI9341 Reset

         * - :rpi-pico-pin:`12`
           - :rpi-pico-pio:`GP9` :rpi-pico-pwm:`PWM9` : D9
           - :rpi-pico-pin:`8`
           - :hwftlbl-scr:`BL`
             :hwftlbl-pio:`BL`
             :hwftlbl-pwm:`BL`

             LCD Backlight

      .. rubric:: LCD Orientation and Bit Order Test

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`display`.

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/display
         :board: cytron_maker_nano_rp2040
         :shield: waveshare_2_4_lcd
         :build-dir: cytron_maker_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: LVGL Basic Sample

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`lvgl`.

      .. zephyr-app-commands::
         :app: zephyr/samples/subsys/display/lvgl
         :board: cytron_maker_nano_rp2040
         :shield: waveshare_2_4_lcd
         :build-dir: cytron_maker_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      This sample comes with a Shell command line access to the LVGL backend
      on the console, here configured for a USB console:

      .. rubric:: Simple test execution on target

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

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
            Heap at 0x200010c8 contains 2047 units in 11 buckets

              bucket#    min units        total      largest      largest
                         threshold       chunks      (units)      (bytes)
              -----------------------------------------------------------
                    1            2            1            2           12
                   10         1024            1         1550        12396

            12408 free bytes, 3560 allocated bytes, overhead = 412 bytes (2.5%)

   .. group-tab:: Maker Pi RP2040

      Connect the |Waveshare 2.4 LCD| module by free wiring to the
      |Grove connectors|. Following module's pin assignments for
      *Grove System*.

      .. list-table::
         :align: center
         :width: 50%
         :widths: 15, 5, 30, 5, 45

         * - .. rubric:: Grove
           - .. rubric:: Pin
           - .. rubric:: |Maker Pi RP2040|
           - .. rubric:: Pin
           - .. rubric:: |Waveshare 2.4 LCD|

         * - :hwftlbl-con:`2`
           - :rpi-pico-pin:`3`
           - :rpi-pico-vdd:`3V3(OUT)`
           - :rpi-pico-pin:`1`
           - :hwftlbl-vdd:`VCC`

         * - :hwftlbl-con:`2`
           - :rpi-pico-pin:`4`
           - :rpi-pico-gnd:`GND`
           - :rpi-pico-pin:`2`
           - :hwftlbl:`GND`

         * - :hwftlbl-con:`2`
           - :rpi-pico-pin:`1`
           - :rpi-pico-spi-dfl:`SPI0_TX` : D3
           - :rpi-pico-pin:`3`
           - :hwftlbl-scr:`DIN`
             :hwftlbl-spi:`MOSI`

             ILI9341 Serial Data Input

         * - :hwftlbl-con:`2`
           - :rpi-pico-pin:`2`
           - :rpi-pico-spi-dfl:`SPI0_SCK` : D2
           - :rpi-pico-pin:`4`
           - :hwftlbl-scr:`CLK`
             :hwftlbl-spi:`SCK`

             ILI9341 Serial Clock Input

         * - :hwftlbl-con:`3`
           - :rpi-pico-pin:`1`
           - :rpi-pico-spi-dfl:`SPI0_CSN` : D5
           - :rpi-pico-pin:`5`
           - :hwftlbl-scr:`CS`
             :hwftlbl-spi:`CSN`

             ILI9341 Chip Select Input

         * - :hwftlbl-con:`5`
           - :rpi-pico-pin:`2`
           - :rpi-pico-pio:`GP6` : D6
           - :rpi-pico-pin:`6`
           - :hwftlbl-scr:`DC`
             :hwftlbl-pio:`DC`

             ILI9341 Data/Command

         * - :hwftlbl-con:`7`
           - :rpi-pico-pin:`1`
           - :rpi-pico-pio:`GP28` : D28 (ADC2)
           - :rpi-pico-pin:`7`
           - :hwftlbl-scr:`RST`
             :hwftlbl-pio:`RST`

             ILI9341 Reset

         * - :hwftlbl-con:`7`
           - :rpi-pico-pin:`2`
           - :rpi-pico-pio:`GP7` :rpi-pico-pwm:`PWM7` : D7
           - :rpi-pico-pin:`8`
           - :hwftlbl-scr:`BL`
             :hwftlbl-pio:`BL`
             :hwftlbl-pwm:`BL`

             LCD Backlight
      .. rubric:: LCD Orientation and Bit Order Test

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`display`.

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/display
         :board: cytron_maker_pi_rp2040
         :shield: waveshare_2_4_lcd
         :build-dir: cytron_maker_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: LVGL Basic Sample

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`lvgl`.

      .. zephyr-app-commands::
         :app: zephyr/samples/subsys/display/lvgl
         :board: cytron_maker_pi_rp2040
         :shield: waveshare_2_4_lcd
         :build-dir: cytron_maker_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      This sample comes with a Shell command line access to the LVGL backend
      on the console, here configured for a USB console:

      .. rubric:: Simple test execution on target

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

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
            Heap at 0x200010c8 contains 2047 units in 11 buckets

              bucket#    min units        total      largest      largest
                         threshold       chunks      (units)      (bytes)
              -----------------------------------------------------------
                    1            2            1            2           12
                   10         1024            1         1550        12396

            12408 free bytes, 3560 allocated bytes, overhead = 412 bytes (2.5%)

References
**********

.. target-notes::
