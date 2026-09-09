.. _mini_usb_rp2350:

Mini USB RP2350
###############

The `Mini USB RP2350`_ is a very small, low-cost and versatile Chinese board
from different manufactures or `AliExpress webshops for Mini USB RP2350`_.
It has no SWD interface, but a USB-A plug-in connector built directly into
the PCB with a direct connection to the RP2350A on-chip USB controller. The
Raspberry Pi Pico on-chip USB bootloader allows the ability to flash without
any adapter, in a drag-and-drop manner.

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

The peripherals of the `RP2350 SoC`_ can be routed to various pins on
the board. The configuration of these routes can be modified through
:external+zephyr:ref:`DTS <devicetree>`. Please refer to the datasheet
to see the possible routings for each peripheral. The default assignment
is showing below.

.. include:: pinouts.rsti

Default Zephyr Peripheral Mapping:
----------------------------------

.. include:: pinmap.rsti

Supported Features
******************

The |Mini USB RP2350| board configuration supports the following hardware
features:

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
   * - WS2812 (PIO)
     - :kconfig:option:`CONFIG_LED_STRIP`
     - :dtcompatible:`worldsemi,ws2812-rpi-pico-pio`
     - N/A
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
     - N/A
     - :dtcompatible:`arm,v8m-systick`
     -

Other hardware features are not currently supported by Zephyr. The default
configuration can be found in the different Kconfig files:

.. zephyr-keep-sorted-start re(^\* :bridle_file:`\w)

* :bridle_file:`boards/nologo/mini_usb_rp2350/mini_usb_rp2350_rp2350a_hazard3_0_defconfig`
* :bridle_file:`boards/nologo/mini_usb_rp2350/mini_usb_rp2350_rp2350a_m33_0_defconfig`

.. zephyr-keep-sorted-stop

Board Configurations
====================

The |Mini USB RP2350| board offers an assembly option with 16㎆ Flash,
which is mapped as a hardware revision.

.. zephyr-keep-sorted-start re(^\.\. rubric:: :command:`\w)

.. rubric:: :command:`west build -b mini_usb_rp2350/rp2350a/hazard3_0`

Use the native USB device port with CDC-ACM as Zephyr console and for the
shell. Setup QSPI Flash controller to work with 4㎆.
Running on Hazard3/RISC-V core. :brd:`EXPERIMENTAL`

.. rubric:: :command:`west build -b mini_usb_rp2350/rp2350a/m33_0`

Use the native USB device port with CDC-ACM as Zephyr console and for the
shell. Setup QSPI Flash controller to work with 4㎆.
Running on Cortex-M33 core.

.. rubric:: :command:`west build -b mini_usb_rp2350@16mb/rp2350a/hazard3_0`

Use the native USB device port with CDC-ACM as Zephyr console and for the
shell. Setup QSPI Flash controller to work with 16㎆.
Running on Hazard3/RISC-V core. :brd:`EXPERIMENTAL`

.. rubric:: :command:`west build -b mini_usb_rp2350@16mb/rp2350a/m33_0`

Use the native USB device port with CDC-ACM as Zephyr console and for the
shell. Setup QSPI Flash controller to work with 16㎆.
Running on Cortex-M33 core.

.. rubric:: :command:`west build -b mini_usb_rp2350@4mb/rp2350a/hazard3_0`

Use the native USB device port with CDC-ACM as Zephyr console and for the
shell. Setup QSPI Flash controller to work with 4㎆ – the same as the default
board configuration ``mini_usb_rp2350/rp2350a/hazard3_0``.
Running on Hazard3/RISC-V core. :brd:`EXPERIMENTAL`

.. rubric:: :command:`west build -b mini_usb_rp2350@4mb/rp2350a/m33_0`

Use the native USB device port with CDC-ACM as Zephyr console and for the
shell. Setup QSPI Flash controller to work with 4㎆ – the same as the default
board configuration ``mini_usb_rp2350/rp2350a/m33_0``.
Running on Cortex-M33 core.

.. zephyr-keep-sorted-stop

Connections and IOs
===================

Both the Chinese website about the `Mini USB RP2350`_ and almost all AliExpress
retailers provide a few information about the board connections. Some of the
data they give is pretty sketchy, especially those provided by retailers, which
keep things to the bare minimum and often mess it up. The content provided here
is the result of extensive technical evaluation, correction, rectification, and
supplementation of this publicly available information.

.. _mini_usb_rp2350_grove_if:

Laced Grove Signal Interface
----------------------------

The |Mini USB RP2350| offers the option of connecting hardware modules via one
single Qwiic/STEMMA QT (|Grove connectors|). This is provided by a specific
interface for general signal mapping, the |Laced Grove Signal Interface|.

Following mappings are well known:

.. zephyr-keep-sorted-start re(^\* \|\w)

* ``grove_gpios``: GPIO mapping
* ``grove_pwms``: PWM mapping

.. zephyr-keep-sorted-stop

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GPIO mapping ``grove_gpios``

      This is the **GPIO signal line mapping** from the `RP2350 SOC`_ to the
      set of |Grove connectors| provided as |Laced Grove Signal Interface|.

      **This list must not be stable!**

      .. include:: grove_gpios.rsti

   .. group-tab:: PWM mapping ``grove_pwms``

      The corresponding mapping is always board or SOC specific. In addition
      to the **PWM signal line mapping**, the valid references to the PWM
      function units in the SOC or on the board are therefore also defined
      as **Grove PWM Labels**. The following table reflects the currently
      supported mapping for :code:`mini_usb_rp2350`, but this list will be
      growing up with further development and maintenance.

      **This list must not be complete or stable!**

      .. include:: grove_pwms.rsti

   .. zephyr-keep-sorted-stop

System Clock
============

The `RP2350 <RP2350 SoC_>`_ MCU is configured to use the 12㎒ external crystal
with the on-chip PLL generating the 125㎒ system clock. The internal AHB and
APB units are set up in the same way as the upstream `Raspberry Pi Pico C/C++
SDK`_ libraries.

GPIO (PWM) Ports
================

The `RP2350 <RP2350 SoC_>`_ MCU has 1 GPIO cell which covers all I/O pads and
8 PWM function unit each with 2 channels beside a dedicated Timer unit. On
the |Mini USB RP2350|, almost all 16 PWM channels are available on the edge
connectors, although some channels are occupied by special signals if their
function is enabled.

ADC/TS Ports
============

The `RP2350 <RP2350 SoC_>`_ MCU has 1 ADC with 4 channels and an additional
fifth channel for the on-chip temperature sensor (TS). The ADC channels 0-3
are available on the edge connectors.

The external voltage reference ADC_VREF is directly connected to the 3.3V
power supply.

SPI Port
========

The `RP2350 <RP2350 SoC_>`_ MCU has 2 SPIs. The serial bus SPI0 is connect to
external devices over GP7 (MOSI), GP4 (MISO), GP6 (SCK), and GP5 (CSn) on the
edge connectors. SPI1 is not available in any default setup.

I2C Port
========

The `RP2350 <RP2350 SoC_>`_ MCU has 2 I2Cs. The serial bus I2C0 and I2C1 are
connect to external devices by default over GP16 (I2C0_SDA), GP17 (I2C0_SCL)
on the Grove compatible Qwiic/STEMMA QT connector and GP14 (I2C1_SDA),
GP15 (I2C1_SCL) on the edge connectors. I2C1 is available but disabled in
any default setup.

Serial Port
===========

The `RP2350 <RP2350 SoC_>`_ MCU has 2 UARTs. One of the UARTs (UART0) is
connected to external devices over GP0 (TX) and GP1 (RX) on the edge
connectors. Optional the hardware handshake signals GP2 (CTS) and GP3 (RTS)
can be used for flow control.

USB Device Port
===============

The `RP2350 <RP2350 SoC_>`_ MCU has a (native) USB device port that can be used
to communicate with a host PC. See the
:external+zephyr:zephyr:code-sample-category:`usb` sample applications for more,
such as the :external+zephyr:zephyr:code-sample:`usb-cdc-acm` sample which sets
up a virtual serial port that echos characters back to the host PC. The
|Mini USB RP2350| provides the Zephyr console per default on the USB port
as :external+zephyr:ref:`usb_device_cdc_acm`:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |mini_usb_rp2350_VID|, idProduct=\ |mini_usb_rp2350_PID_CON|, bcdDevice=\ |mini_usb_rp2350_BCD_CON|
         USB device strings: Mfr=1, Product=2, SerialNumber=3
         Product: |mini_usb_rp2350_PStr_CON|
         Manufacturer: |mini_usb_rp2350_VStr|
         SerialNumber: B163A72F0CF0C97A

Programmable I/O (PIO)
**********************

The `RP2350 SoC`_ comes with three PIO periherals. These are three simple
co-processors that are designed for I/O operations. The PIOs run a custom
instruction set, generated from a custom assembly language. PIO programs
are assembled using :program:`pioasm`, a tool provided by Raspberry Pi.
Further information can be found in the `Raspberry Pi Pico C/C++ SDK`_
document, section with title :emphasis:`"Using PIOASM, the PIO Assembler"`.

Zephyr does not (currently) assemble PIO programs. Rather, they should be
manually assembled and embedded in source code. An example of how this is done
can be found at :zephyr_file:`drivers/serial/uart_rpi_pico_pio.c` or
:zephyr_file:`drivers/spi/spi_rpi_pico_pio.c`.

Sample: SPI via PIO
===================

The :zephyr_file:`samples/sensor/bme280/README.rst` sample includes a
demonstration of using the PIO SPI driver to communicate with an
environmental sensor. The PIO SPI driver supports using any
combination of GPIO pins for an SPI bus, as well as allowing up to
four independent SPI buses on a single board (using the two SPI
devices as well as both PIO devices).

Programming and Debugging
*************************

Flashing
========

The board can only be flashed with a UF2 file. There is no SWD connector.

Using UF2
---------

By default, building an application for the board will generate a
:file:`build/zephyr/zephyr.uf2` file. If the board is powered on with
the :kbd:`BOOTSEL` button pressed, it will appear on the host as a mass
storage device:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |rpi_VID|, idProduct=\ |rpi_rp2350_PID|, bcdDevice=\ |rpi_rp2350_BCD|
         USB device strings: Mfr=1, Product=2, SerialNumber=0
         Product: |rpi_rp2350_PStr|
         Manufacturer: |rpi_VStr|
         SerialNumber: E9DB4B801D503140

The UF2 file should be drag-and-dropped or copied on command line to the
device, which will then flash the board.

RP2350 Boot-ROM
---------------

Each `RP2350 SoC`_ ships the `UF2 compatible <UF2 bootloader_>`_ bootloader
pico-bootrom-rp2350_, a native support in silicon. The full source for the
RP2350 bootrom at pico-bootrom-rp2350_ includes versions A2, A3 and A4 of
the bootrom, which correspond to the same silicon revisions, respectively.

Note that every time you build a program for the RP2350, the Pico SDK selects
and creates an appropriate image definition and/or partition table block with
attributes and precedes it in the firmware. Further information can be found
in the `RP2350 Datasheet`_, sections with title :emphasis:`"Bootrom"` and
:emphasis:`"Processor Controlled Boot Sequence"`.

Debugging
=========

The board does not provide any SWD connector, thus debugging software
is not possible.

Basic Samples
*************

LED Blinky and Fade
===================

.. include:: led_strip.rsti

Hello Shell on the USB Console (CDC/ACM)
========================================

.. include:: helloshell.rsti

More Samples
************

.. rubric:: Grove Module Samples

All currently supported Grove modules can be reused on the Qwiic / STEMMA QT
connector using a conversion cable. Only the corresponding shield stacks need
to be specified.

Hello Shell with sensor access to Grove BMP280
==============================================

.. include:: helloshell_grove.rsti

BME280 humidity and pressure sensor with Grove BMP280
=====================================================

.. include:: bme280_grove.rsti

LED Blinky with Grove LED Button (Qwiic signals as GPIO)
========================================================

.. include:: blinky_grove.rsti

LED Fade with Grove LED Button (Qwiic signals as PWM)
=====================================================

.. include:: fade_grove.rsti

LED Switch with Grove LED Button (Qwiic signals as GPIO)
========================================================

.. include:: button_grove.rsti

References
**********

.. target-notes::

.. |LED Shields| replace:: :ref:`grove_led_shield`
.. |Button Shields| replace:: :ref:`grove_button_shield`
.. |Sensor Shields| replace:: :ref:`grove_sensor_shield`
