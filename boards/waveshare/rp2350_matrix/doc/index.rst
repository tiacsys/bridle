.. _waveshare_rp2350_matrix:

Waveshare RP2350-Matrix
#######################

The `RP2350 SoC`_ by Raspberry Pi Ltd. is a small sized and low-cost 32-bit
dual ARM Cortex-M33 and dual 32-bit Hazard3 RISC-V (RV32IMAC+) microcontroller
and predestined for versatile board designs. The Waveshare RP2350 board series
based on this microcontroller offers a wide range with different scaling
factors, in size, features and interfaces for communication, input and output.

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

The peripherals of the `RP2350 SoC`_ can be routed to various pins on
the board. The configuration of these routes can be modified through
:external+zephyr:ref:`DTS <devicetree>`. Please refer to the datasheet
to see the possible routings for each peripheral. The default assignments
for the board is defined below.

.. include:: pinouts.rsti

Supported Features
******************

Similar to the |zephyr:board:rpi_pico2| the board configuration supports the
following hardware features:

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
     - :dtcompatible:`arm,v6m-nvic`
     - Nested Vector :external+zephyr:ref:`interrupts_v2` Controller
   * - SYSTICK
     - N/A
     - :dtcompatible:`arm,armv6m-systick`
     -

Other hardware features are not currently supported by Zephyr. The default
configuration can be found in the different Kconfig files:

.. zephyr-keep-sorted-start re(^\* :bridle_file:`\w)

* :bridle_file:`boards/waveshare/rp2350_matrix/waveshare_rp2350_matrix_rp2350a_hazard3_defconfig`
* :bridle_file:`boards/waveshare/rp2350_matrix/waveshare_rp2350_matrix_rp2350a_m33_defconfig`

.. zephyr-keep-sorted-stop

Board Configurations
====================

The board can be configured for the following different use cases.

.. rubric:: :command:`west build -b waveshare_rp2350_matrix/rp2350a/m33`

Use the serial port UART0 on edge header as
Zephyr console and for the shell.
Running on Cortex-M33 core.

.. rubric:: :command:`west build -b waveshare_rp2350_matrix/rp2350a/m33 -S usb-console`

Use the native USB device port with CDC-ACM as
Zephyr console and for the shell.
Running on Cortex-M33 core.

.. rubric:: :command:`west build -b waveshare_rp2350_matrix/rp2350a/hazard3`

Use the serial port UART0 on edge header as
Zephyr console and for the shell.
Running on Hazard3/RISC-V core. :brd:`EXPERIMENTAL`

.. rubric:: :command:`west build -b waveshare_rp2350_matrix/rp2350a/hazard3 -S usb-console`

Use the native USB device port with CDC-ACM as
Zephyr console and for the shell.
Running on Hazard3/RISC-V core. :brd:`EXPERIMENTAL`

Connections and IOs
===================

The `Waveshare wiki`_ has detailed information about board connections.
Download the different schematics or datasheets as linked above per board
for more details. The pinout diagrams can also be found there.

System Clock
============

The `RP2350A <RP2350 SoC_>`_ MCU is configured to use the 12㎒ external crystal
with the on-chip PLL generating the 150㎒ system clock. The internal AHB and
APB units are set up in the same way as the upstream `Raspberry Pi Pico C/C++
SDK`_ libraries.

GPIO (PWM) Ports
================

The `RP2350A <RP2350 SoC_>`_ MCU has 1 GPIO cell which covers all I/O pads and
8 PWM function unit each with 2 channels beside a dedicated Timer unit. The
channels A and B of PWM2 are available on the |Waveshare RP2350 Matrix PCB Pads|,
the channels A nd B of PWM3 and channel A of PWM4 are available on the |Waveshare
RP2350 Matrix| header.

ADC/TS Ports
============

The `RP2350A <RP2350 SoC_>`_ MCU has 1 ADC with 4 channels and an additional
fifth channel for the on-chip temperature sensor (TS). The ADC channels 0-3
are available on the |Waveshare RP2350 Matrix| header.

The external voltage reference ADC_VREF is directly connected to the 3.3V
power supply.

SPI Port
========

The `RP2350A <RP2350 SoC_>`_ MCU has 2 SPIs. To the edge connectors, SPI0 is
usable for external devices over GP19 (MOSI), GP16 (MISO), GP18 (SCK), and
GP17 (CSn) on the |Waveshare RP2350 Matrix| header.

I2C Port
========

The `RP2350A <RP2350 SoC_>`_ MCU has 2 I2Cs. To the edge connectors, I2C0 is
usable for external devices over GP12 (I2C0_SDA), and GP13 (I2C0_SCL), on the
|Waveshare RP2350 Matrix| header.

The I2C1 is connected internally over GP6 (I2C1_SDA) and GP7 (I2C1_SCL) to the
on-board 6D/IMU sensor (accelerometer and gyroscope).

Serial Port
===========

The `RP2350A <RP2350 SoC_>`_ MCU has 2 UARTs. One of the UARTs (UART1) is
connected to external devices over GP10 (TX) and GP11 (RX) on the |Waveshare
RP2350 Matrix| header and is the Zephyr console. UART0 is available on the
|Waveshare RP2350 Matrix PCB Pads|, optional with full featured EIA 232D modem
signals.

USB Device Port
===============

The `RP2350A <RP2350 SoC_>`_ MCU has a (native) USB device port that can be used
to communicate with a host PC. See the
:external+zephyr:zephyr:code-sample-category:`usb` sample applications for more,
such as the :external+zephyr:zephyr:code-sample:`usb-cdc-acm` sample which sets
up a virtual serial port that echos characters back to the host PC. As an
alternative to the default Zephyr console on serial port the Bridle
:ref:`snippet-usb-console` can be used to enable
:external+zephyr:ref:`usb_device_cdc_acm` and switch the console to USB

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |waveshare_rp2350_matrix_VID|, idProduct=\ |waveshare_rp2350_matrix_PID_CON|, bcdDevice=\ |waveshare_rp2350_matrix_BCD_CON|
         USB device strings: Mfr=1, Product=2, SerialNumber=3
         Product: |waveshare_rp2350_matrix_PStr_CON|
         Manufacturer: |waveshare_rp2350_matrix_VStr|
         SerialNumber: B46993A480CF94B1

.. include:: /includes/rpi_waveshare_urb_pid_list.txt

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

.. include:: blinky_fade.rsti

Hello Shell with USB-CDC/ACM Console
====================================

.. include:: helloshell.rsti

More Samples
************

3-Axis accelerometer data on USB-CDC/ACM Console
================================================

The samples are prepared for the on-board :hwftlbl-cps:`6-DOF` accelerometer
and gryoscope, connected to the :rpi-pico-i2c:`I2C1` bus, but works only with
the accelerometer data.

Polling Mode
------------

Get 3-axis accelerometer data from the on-board sensor (polling mode) using
the :external+zephyr:ref:`Sensors API <sensor>`. See also Zephyr sample
:external+zephyr:zephyr:code-sample:`accel_polling`.

.. include:: 3dof_accel_polling.rsti

Trigger Mode
------------

Get 3-axis accelerometer data from the on-board sensor (trigger mode) using
the :external+zephyr:ref:`Sensors API <sensor>`. See also Zephyr sample
:external+zephyr:zephyr:code-sample:`accel_trig`.

.. include:: 3dof_accel_trigger.rsti

6-DOF accelerometer and gryoscope data on USB-CDC/ACM Console
=============================================================

The samples are prepared for the on-board :hwftlbl-cps:`6-DOF` accelerometer
and gryoscope, connected to the :rpi-pico-i2c:`I2C1` bus.

6DOF Motion Dataready
---------------------

Get 3-axis accelerometer data, 3-axis gryoscope data, and sensor temperature
form the on-board sensor (trigger mode) using the
:external+zephyr:ref:`Sensors API <sensor>`. See also Zephyr sample
:external+zephyr:zephyr:code-sample:`6dof_motion_drdy`.

.. include:: 6dof_motion_drdy.rsti

Display Test and Demonstration
==============================

.. include:: display_test.rsti

References
**********

.. target-notes::
