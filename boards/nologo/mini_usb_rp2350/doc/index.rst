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

The `Mini USB RP2350`_ is a :bbl:`mini sized` RP2350A development board.
The on-board PCB USB-A connector makes it plug-and-play instantly.
The castellated module allows soldering direct to carrier boards.

.. list-table::
   :align: center
   :width: 100%
   :widths: 66, 33

   * - .. rubric:: Features and Resources
     - .. rubric:: Printed Circuit Board

   * - :hwftlbl-vdd:`5V/300㎃`
       :hwftlbl-vdd:`3.3V/500㎃`
       :hwftlbl-vdd:`3.3V(OUT)`

       :hwftlbl:`150㎒`
       :hwftlbl:`4㎆/16㎆`
       :hwftlbl:`520㎅`
       :hwftlbl-btn:`RST`
       :hwftlbl-led:`RGB`
       :hwftlbl-con:`USB-A`
       :hwftlbl-dbg:`UF2`

       :hwftlbl-pio:`25`
       :hwftlbl-pwm:`16`
       :hwftlbl-adc:`4`
       :hwftlbl-i2c:`2`
       :hwftlbl-spi:`2`
       :hwftlbl-uart:`2`

       .. rst-class:: rst-columns

       - Dual core Arm Cortex-M33 and dual core Hazard3 (RV32IMAC+) RISC-V
         processor running up to 150㎒
       - :bbk:`520㎅` on-chip SRAM
       - :bbl:`4㎆` on-board QSPI flash with XIP capabilities
         – optional :brd:`16㎆`
       - USB 1.1 controller (host/device)
       - On-board :bbl:`PCB USB-A connector`
       - On-board :bbl:`RGB LED` (NeoPixel)
       - On-board :bbl:`3.3V LDO regulator with 500㎃`
       - On-board :bbl:`RESET` button
       - On-board :bbk:`BOOT` button
       - :bbl:`15 GPIO` pins via :bbk:`edge pinout`
       - :bbl:`13 GPIO` pins via :bbl:`solder points`
       - :bbk:`2 UART` peripherals
       - :bbk:`2 I2C` controllers
       - :bbk:`2 SPI` controllers
       - :bbk:`16 PWM` channels
       - :bbl:`4 ADC` analog inputs
       - 12 Programmable I/O (PIO) state machines for custom peripherals
       - 1 Watchdog timer peripheral
       - 1 Temperature sensor on-chip

       .. rubric:: Design Data
       .. rst-class:: rst-columns

       - `Mini USB RP2350 Schematic`_
       - `Mini USB RP2350 Schematic (PNG file)`_
       - `Mini USB RP2350 STEP 3D-Model`_
       - `Mini USB RP2350 STEP 3D-Model (STEP file)`_
       - `Mini USB RP2350 WS2812 Test`_
       - `Mini USB RP2350 WS2812 Test (UF2 file)`_

     - .. image:: img/mini_usb_rp2350.jpg
          :align: center
          :alt: NoLogo Mini USB RP2350

Positions
=========

.. list-table::
   :align: center
   :width: 66%
   :header-rows: 1

   * - .. image:: img/positions.jpg
          :align: center
          :width: 500
          :alt: NoLogo Mini USB RP2350 details

   * - .. container:: twocol

          .. container:: leftside

             1. :strong:`PCB USB-A port`
             #. | :strong:`ME6231C33`
                | 500㎃ low dropout, low noise LDO
             #. | :strong:`On-board flash memory`
                | 4㎆ NOR-Flash :strong:`W25Q32JV`
                | 16㎆ NOR-Flash :strong:`W25Q128JV`
             #. :strong:`RP2350A`
             #. | :strong:`WS2812B`
                | RGB LED

          .. container:: rightside

             6. | :strong:`BOOT button`
                | press it when resetting to enter download mode
             #. :strong:`RESET button`
             #. | :strong:`Maker Port`
                | Qwiic / STEMMA QT compatible connector and pinout
                  with conversion cable to Grove connector
                  supports **I2C0** (default), UART0, GPIO/PWM
             #. | :strong:`RP2350A pins`
                | 13 solder points, including 13 GPIO pins

.. rubric:: Data Sheets
.. rst-class:: rst-columns

- .. rubric:: `RP2350 SoC`_
- `RP2350 Datasheet`_
- `Hardware design with RP2350`_
- .. rubric:: W25Q32JV_
- `W25Q32JV Datasheet`_
- .. rubric:: W25Q128JV_
- `W25Q128JV Datasheet`_
- .. rubric:: WS2812B_
- `WS2812B Datasheet V5`_
- `WS2812B Datasheet V2`_
- `WS2812B Datasheet V1`_
- `Understanding the WS2812`_
- `WS2812B with RP2040 PIO & DMA`_
- .. rubric:: ME6231C33_
- `ME6231 Datasheet`_
- .. rubric:: `Grove System`_
- `Grove Digital Layout`_
- `Grove UART Layout`_
- `Grove I2C Layout`_

Pinouts
=======

The peripherals of the `RP2350 SoC`_ can be routed to various pins on
the board. The configuration of these routes can be modified through
:external+zephyr:ref:`DTS <devicetree>`. Please refer to the datasheet
to see the possible routings for each peripheral. The default assignment
is showing below.

External pin mapping on the |Mini USB RP2350| is :strong:`not identical`
to the original |zephyr:board:rpi_pico| board. Almost all pins are rearranged
in a more compact order. Likewise, the voltage sense and monitoring functions
are not integrated. Thus all internal RP2350A GPIO lines are available for free
use, insofar there is sufficient space for them on the outer edge of the board
or on the bottom side by additional solder points.

GPIO line 22 is not only exclusively routed to the on-board user RGB LED. It is
also accessible on the bottom side on one of the 13 solder pads. The **analog
voltage reference** is internally hard-wired to the digital 3.3V power supply
and **is not decoupled** by a simple resistor. There is no option to change
this from outside the board.

.. list-table::
   :align: center
   :width: 100%
   :widths: 66, 33

   * - .. rubric:: Pin Mapping
     - .. rubric:: Pinout

   * - :on-edge(1-18):
          :hwftlbl-pio:`3`
          :hwftlbl-pwm:`3`
          :hwftlbl-adc:`4`
          :hwftlbl-i2c:`1`
          :hwftlbl-spi:`1`
          :hwftlbl-uart:`1`

       :on-qwiic(QC,QD):
          :hwftlbl-pio:`2`
          :hwftlbl-i2c:`1`
          :hwftlbl-uart:`1`

       :on-pads(A-M):
          :hwftlbl-pio:`12`
          :hwftlbl-pwm:`8`

       :on-board:
          :hwftlbl-led:`1 RGB`

       .. rubric:: Default Zephyr Peripheral Mapping

       |nbsp|

       .. rst-class:: rst-columns edge-pinout

       - | :rpi-pico-pin:`1` :rpi-pico-uart-dfl:`UART0_TX` : GP0 (PWM0)
       - | :rpi-pico-pin:`2` :rpi-pico-uart-dfl:`UART0_RX` : GP1 (PWM1)
       - | :rpi-pico-pin:`3` PIO/PWM : :rpi-pico-pio:`GP2` :rpi-pico-pwm:`PWM2`
       - | :rpi-pico-pin:`4` PIO/PWM : :rpi-pico-pio:`GP3` :rpi-pico-pwm:`PWM3`
       - | :rpi-pico-pin:`5` :rpi-pico-spi-dfl:`SPI0_RX` : GP4 (PWM4)
       - | :rpi-pico-pin:`6` :rpi-pico-spi-dfl:`SPI0_CSN` : GP5 (PWM5)
       - | :rpi-pico-pin:`7` :rpi-pico-spi-dfl:`SPI0_SCK` : GP6 (PWM6)
       - | :rpi-pico-pin:`8` :rpi-pico-spi-dfl:`SPI0_TX` : GP7 (PWM7)
       - | :rpi-pico-pin:`9` PIO/PWM : :rpi-pico-pio:`GP8` :rpi-pico-pwm:`PWM8`
       - | :rpi-pico-pin:`A` PIO/PWM : :rpi-pico-pio:`GP9` :rpi-pico-pwm:`PWM9`
       - | :rpi-pico-pin:`B` PIO/PWM : :rpi-pico-pio:`GP10` :rpi-pico-pwm:`PWM10`
       - | :rpi-pico-pin:`C` PIO/PWM : :rpi-pico-pio:`GP11` :rpi-pico-pwm:`PWM11`
       - | :rpi-pico-pin:`D` PIO/PWM : :rpi-pico-pio:`GP12` :rpi-pico-pwm:`PWM12`
       - | :rpi-pico-pin:`E` PIO/PWM : :rpi-pico-pio:`GP13` :rpi-pico-pwm:`PWM13`
       - | :rpi-pico-pin:`10` :rpi-pico-i2c:`I2C1_SDA` : GP14 (PWM14)
       - | :rpi-pico-pin:`11` :rpi-pico-i2c:`I2C1_SCL` : GP15 (PWM15)
       - | :rpi-pico-pin:`QD` :rpi-pico-i2c-dfl:`I2C0_SDA` : GP16 (PWM0)
       - | :rpi-pico-pin:`QC` :rpi-pico-i2c-dfl:`I2C0_SCL` : GP17 (PWM1)
       - | :rpi-pico-pin:`F` PIO/PWM : :rpi-pico-pio:`GP18` :rpi-pico-pwm:`PWM2`
       - | :rpi-pico-pin:`G` PIO/PWM : :rpi-pico-pio:`GP19` :rpi-pico-pwm:`PWM3`
       - | :rpi-pico-pin:`H` PIO/PWM : :rpi-pico-pio:`GP20` :rpi-pico-pwm:`PWM4`
       - | :rpi-pico-pin:`I` PIO/PWM : :rpi-pico-pio:`GP21` :rpi-pico-pwm:`PWM5`
       - | :rpi-pico-pin:`J` :rpi-pico-pio:`PIO0` : GP22 (PWM6)
         | :rpi-pico-pin-nc:`nc` on-board user :rpi-pico-sys:`RGB_LED_DI`
       - | :rpi-pico-pin:`K` PIO/PWM : :rpi-pico-pio:`GP23` :rpi-pico-pwm:`PWM7`
       - | :rpi-pico-pin:`L` PIO/PWM : :rpi-pico-pio:`GP24` :rpi-pico-pwm:`PWM8`
       - | :rpi-pico-pin:`M` PIO/PWM : :rpi-pico-pio:`GP25` :rpi-pico-pwm:`PWM9`
       - | :rpi-pico-pin:`12` :rpi-pico-adc:`ADC_CH0` : GP26 (PWM10)
       - | :rpi-pico-pin:`13` :rpi-pico-adc:`ADC_CH1` : GP27 (PWM11)
       - | :rpi-pico-pin:`14` :rpi-pico-adc:`ADC_CH2` : GP28 (PWM12)
       - | :rpi-pico-pin:`15` :rpi-pico-adc:`ADC_CH3` : GP29 (PWM13)
       - | :rpi-pico-pin:`16` :rpi-pico-vdd:`3V3(OUT)`
       - | :rpi-pico-pin:`17` :rpi-pico-gnd:`GND`
       - | :rpi-pico-pin:`18` :rpi-pico-vdd:`VSYS`

       .. rubric:: Devicetree compatible

       - :dtcompatible:`nologo,miniusb-header`
       - :dtcompatible:`nologo,miniusb-pcbpads`

     - .. image:: img/pinouts.jpg
          :align: center
          :width: 100%
          :alt: NoLogo Mini USB RP2350 edge pinout

Default Zephyr Peripheral Mapping:
----------------------------------

.. rst-class:: rst-columns

- UART0_TX : GP0
- UART0_RX : GP1
- UART0_CTS : GP2 (optional, not default)
- UART0_RTS : GP3 (optional, not default)
- SPI0_RX : GP4
- SPI0_CSN : GP5
- SPI0_SCK : GP6
- SPI0_TX : GP7
- GPIO8 : GP8 (free usable)
- GPIO9 : GP9 (free usable pad)
- GPIO10 : GP10 (free usable pad)
- GPIO11 : GP11 (free usable pad)
- GPIO12 : GP12 (free usable pad)
- GPIO13 : GP13 (free usable pad)
- I2C1_SDA : GP14
- I2C1_SCL : GP15
- I2C0_SDA : GP16 (Qwiic)
- I2C0_SCL : GP17 (Qwiic)
- GPIO18 : GP18 (free usable pad)
- GPIO19 : GP19 (free usable pad)
- GPIO20 : GP20 (free usable pad)
- GPIO21 : GP21 (free usable pad)
- PIO0 : GP22
- GPIO23 : GP23 (free usable pad)
- GPIO24 : GP24 (free usable pad)
- GPIO25 : GP25 (free usable pad)
- ADC_CH0 : GP26
- ADC_CH1 : GP27
- ADC_CH2 : GP28
- ADC_CH3 : GP29

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
     - :zephyr:ref:`pinctrl_api`
   * - GPIO
     - :kconfig:option:`CONFIG_GPIO`
     - :dtcompatible:`raspberrypi,pico-gpio`
     - :zephyr:ref:`gpio_api`
   * - UART
     - :kconfig:option:`CONFIG_SERIAL`
     - :dtcompatible:`raspberrypi,pico-uart`
     - :zephyr:ref:`uart_api`
   * - UDC (USB Device Controller)
     - :kconfig:option:`CONFIG_USB_DEVICE_STACK_NEXT`
     - :dtcompatible:`raspberrypi,pico-usbd`
     - :zephyr:ref:`usb_device_next_api`
   * - I2C
     - :kconfig:option:`CONFIG_I2C`
     - :dtcompatible:`raspberrypi,pico-i2c`
     - :zephyr:ref:`i2c_api`
   * - SPI
     - :kconfig:option:`CONFIG_SPI`
     - :dtcompatible:`raspberrypi,pico-spi`
     - :zephyr:ref:`spi_api`
   * - PWM
     - :kconfig:option:`CONFIG_PWM`
     - :dtcompatible:`raspberrypi,pico-pwm`
     - :zephyr:ref:`pwm_api`
   * - ADC
     - :kconfig:option:`CONFIG_ADC`
     - :dtcompatible:`raspberrypi,pico-adc`
     - :zephyr:ref:`adc_api`
   * - Temperature (Sensor)
     - :kconfig:option:`CONFIG_SENSOR`
     - :dtcompatible:`raspberrypi,pico-temp`
     - :zephyr:ref:`sensor`
   * - Timer (Counter)
     - :kconfig:option:`CONFIG_COUNTER`
     - :dtcompatible:`raspberrypi,pico-timer`
     - :zephyr:ref:`counter_api`
   * - Watchdog Timer (WDT)
     - :kconfig:option:`CONFIG_WATCHDOG`
     - :dtcompatible:`raspberrypi,pico-watchdog`
     - :zephyr:ref:`watchdog_api`
   * - Flash
     - :kconfig:option:`CONFIG_FLASH`
     - :dtcompatible:`raspberrypi,pico-flash-controller` (!)
     - :zephyr:ref:`flash_api` and
       :zephyr:ref:`flash_map_api`
   * - PIO
     - :kconfig:option:`CONFIG_PIO_RPI_PICO`
     - :dtcompatible:`raspberrypi,pico-pio`
     - N/A
   * - UART (PIO)
     - :kconfig:option:`CONFIG_SERIAL`
     - :dtcompatible:`raspberrypi,pico-uart-pio`
     - :zephyr:ref:`uart_api`
   * - SPI (PIO)
     - :kconfig:option:`CONFIG_SPI`
     - :dtcompatible:`raspberrypi,pico-spi-pio`
     - :zephyr:ref:`spi_api`
   * - WS2812 (PIO)
     - :kconfig:option:`CONFIG_LED_STRIP`
     - :dtcompatible:`worldsemi,ws2812-rpi-pico-pio`
     - N/A
   * - DMA
     - :kconfig:option:`CONFIG_DMA`
     - :dtcompatible:`raspberrypi,pico-dma`
     - :zephyr:ref:`dma_api`
   * - HWINFO
     - :kconfig:option:`CONFIG_HWINFO`
     - N/A
     - :zephyr:ref:`hwinfo_api`
   * - VREG
     - :kconfig:option:`CONFIG_REGULATOR`
     - :dtcompatible:`raspberrypi,core-supply-regulator` (!)
     - :zephyr:ref:`regulator_api`
   * - RESET
     - :kconfig:option:`CONFIG_RESET`
     - :dtcompatible:`raspberrypi,pico-reset`
     - :zephyr:ref:`reset_api`
   * - CLOCK
     - :kconfig:option:`CONFIG_CLOCK_CONTROL`
     - | :dtcompatible:`raspberrypi,pico-clock-controller`
       | :dtcompatible:`raspberrypi,pico-clock`
     - :zephyr:ref:`clock_control_api`
   * - NVIC
     - N/A
     - :dtcompatible:`arm,v8m-nvic`
     - Nested Vector :zephyr:ref:`interrupts_v2` Controller
   * - SYSTICK
     - N/A
     - :dtcompatible:`arm,v8m-systick`
     -

(!) POWMAN with VREG and QMI (Flash) on RP2350 not yet supported by Zephyr.

    See section **Peripherals RP2350** in upstream issue:
    https://github.com/zephyrproject-rtos/zephyr/issues/53810

Other hardware features are not currently supported by Zephyr. The default
configuration can be found in the different Kconfig files:

.. zephyr-keep-sorted-start re(^\* :bridle_file:`\w)

* :bridle_file:`boards/nologo/mini_usb_rp2350/mini_usb_rp2350_rp2350a_m33_defconfig`

.. zephyr-keep-sorted-stop

Board Configurations
====================

The |Mini USB RP2350| board offers an assembly option with 16㎆ Flash,
which is mapped as a hardware revision.

.. zephyr-keep-sorted-start re(^\.\. rubric:: :command:`\w)

.. rubric:: :command:`west build -b mini_usb_rp2350/rp2350a/m33`

Use the native USB device port with CDC-ACM as Zephyr console and for the
shell. Setup QSPI Flash controller to work with 4㎆.

.. rubric:: :command:`west build -b mini_usb_rp2350@16mb/rp2350a/m33`

Use the native USB device port with CDC-ACM as Zephyr console and for the
shell. Setup QSPI Flash controller to work with 16㎆.

.. rubric:: :command:`west build -b mini_usb_rp2350@4mb/rp2350a/m33`

Use the native USB device port with CDC-ACM as Zephyr console and for the
shell. Setup QSPI Flash controller to work with 4㎆ – the same as the default
board configuration ``mini_usb_rp2350``.

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

The RP2350 SoC comes with three PIO periherals. These are three simple
co-processors that are designed for I/O operations. The PIOs run a custom
instruction set, generated from a custom assembly language. PIO programs
are assembled using :command:`pioasm`, a tool provided by Raspberry Pi.

Zephyr does not (currently) assemble PIO programs. Rather, they should be
manually assembled and embedded in source code. An example of how this is done
can be found at :zephyr_file:`drivers/serial/uart_rpi_pico_pio.c`.

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

Using UF2
---------

You can flash the |Mini USB RP2350| with a UF2 file. By default, building an
application for this board will generate a :file:`build/zephyr/zephyr.uf2`
file. If the board is powered on with the ``BOOTSEL`` button pressed, it will
appear on the host as a mass storage device. The UF2 file should be
drag-and-dropped to the device, which will flash the board.

Debugging
=========

There is no SWD interface, thus debugging is not possible on thsi board.

Hello Shell on the USB Console (CDC/ACM)
========================================

.. rubric:: Hello Shell on ``@4mb`` revision (default)

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :board: mini_usb_rp2350/rp2350a/m33
   :build-dir: mini_usb_rp2350
   :west-args: -p
   :goals: flash
   :compact:

.. rubric:: Hello Shell on ``@16mb`` revision

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :board: mini_usb_rp2350@16mb/rp2350a/m33
   :build-dir: mini_usb_rp2350
   :west-args: -p
   :goals: flash
   :compact:

Simple test execution on target
-------------------------------

(text in bold is a command input)

   .. admonition:: System
      :class: note dropdown toggle-shown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **hwinfo devid**
            Length: 8
            ID: 0xbd774b2618daaa7d

            :bgn:`uart:~$` **kernel version**
            Zephyr version |zephyr_version_number_em|

            :bgn:`uart:~$` **bridle version**
            Bridle version |shortversion_number_em|

            :bgn:`uart:~$` **bridle version long**
            Bridle version |longversion_number_em|

            :bgn:`uart:~$` **bridle info**
            Zephyr: |zephyr_release_number_em|
            Bridle: |release_number_em|

   .. admonition:: Devices
      :class: note dropdown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **device list**
            devices:
            - clock-controller\ @\ 40010000 (READY)
              DT node labels: clocks
            - reset-controller\ @\ 40020000 (READY)
              DT node labels: reset
            - cdc-acm-console-uart (READY)
              DT node labels: cdc_acm_console_uart
            - uart\ @\ 40070000 (READY)
              DT node labels: uart0
            - watchdog\ @\ 400d8000 (READY)
              DT node labels: wdt0
            - timer\ @\ 400b8000 (READY)
              DT node labels: timer1
            - timer\ @\ 400b0000 (READY)
              DT node labels: timer0
            - pio\ @\ 50200000 (READY)
              DT node labels: ((pio_hw_t \*)0x50200000u)
            - dma\ @\ 50000000 (READY)
              DT node labels: dma
            - gpio-port\ @\ 0 (READY)
              DT node labels: gpio0 gpio0_lo
            - adc\ @\ 400a0000 (READY)
              DT node labels: adc
            - i2c\ @\ 40090000 (READY)
              DT node labels: i2c0 grove_i2c
            - dietemp (READY)
              DT node labels: die_temp

   .. admonition:: Timer
      :class: note dropdown

      .. rubric:: Operate with the tow on-chip timer units:

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **timer oneshot timer0 0 1000000**
            :bgn:`timer: Alarm triggered`

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **timer oneshot timer1 0 1000000**
            :bgn:`timer: Alarm triggered`

   .. admonition:: Die Temperature Sensor
      :class: note dropdown

      .. rubric:: Operate with the on-chip temperature sensor on ADC channel 4:

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **sensor info**
            device name: dietemp, vendor: Raspberry Pi Foundation, model: pico-temp, friendly name: RP2350 chip temperature

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **sensor get dietemp**
            :bgn:`channel type=12(die_temp) index=0 shift=5 num_samples=1 value=122018715213ns (28.162114)`

   .. admonition:: ADC Channel
      :class: note dropdown

      .. rubric:: Operate with the ADC channels 0 until 4:

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **adc adc@400a0000 resolution 12**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **adc adc@400a0000 read 0**
            read: 973

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **adc adc@400a0000 read 1**
            read: 684

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **adc adc@400a0000 read 2**
            read: 795

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **adc adc@400a0000 read 3**
            read: 682

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **adc adc@400a0000 read 4**
            read: 876

   .. admonition:: I2C on Qwiic with BMP280
      :class: note dropdown

      The Mini USB RP2350 has no on-board I2C devices. For this example an
      |Grove BMP280 Sensor|_ was plugged into the Qwiic connector.

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **log enable none i2c_dw**

            :bgn:`uart:~$` **i2c scan i2c0**
                 0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
            00:             -- -- -- -- -- -- -- -- -- -- -- --
            10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            70: -- -- -- -- -- -- -- 77
            1 devices found on i2c0

            :bgn:`uart:~$` **log enable inf i2c_dw**

      The I2C address ``0x77`` is a Bosch BMP280 Air Pressure Sensor and their
      Chip-ID can read from register ``0xd0``. The Chip-ID must be ``0x58``:

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **i2c read_byte i2c0 77 d0**
            Output: 0x58

More Samples
************

LED Blinky and Fade
===================

.. hint::

   Neither LED Blinky nor LED Fade can be built and executed on standard
   |Mini USB RP2350|, because this system has only one digital RGB LED.
   A simple GPIO or PWM control is not possible!

WS2812 LED Test Pattern by PIO
==============================

.. zephyr-app-commands::
   :app: zephyr/samples/drivers/led/led_strip
   :board: mini_usb_rp2350/rp2350a/m33
   :build-dir: mini_usb_rp2350
   :west-args: -p
   :goals: flash
   :compact:

Simple test execution on target
-------------------------------

   .. admonition:: Console Output
      :class: note dropdown toggle-shown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*
            [00:00:04.001,000] <inf> main: Found LED strip device ws2812-single
            [00:00:04.001,000] <inf> main: Displaying pattern on strip

Grove Module Samples
********************

All currently supported Grove modules can be reused on the Qwiic / STEMMA QT
connector using a conversion cable. Only the corresponding shield stacks need
to be specified.

Hello Shell with sensor access to Grove BMP280
==============================================

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :board: mini_usb_rp2350/rp2350a/m33
   :shield: "grove_sens_bmp280"
   :build-dir: mini_usb_rp2350
   :west-args: -p
   :goals: flash
   :compact:

Simple test execution on target
-------------------------------

(text in bold is a command input)

   .. admonition:: Devices
      :class: note dropdown

      .. rubric:: Only an excerpt from the full list:

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **device list**
            devices:
              … … …
            - bmp280\ @\ 77 (READY)
              … … …

   .. admonition:: Sensor access from Zephyr Shell
      :class: note dropdown toggle-shown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **sensor info**
            device name: dietemp, vendor: Raspberry Pi Foundation, model: pico-temp, friendly name: RP2350 chip temperature
            device name: bmp280\ @\ 77, vendor: Bosch Sensortec GmbH, model: bme280, friendly name: (null)

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **sensor get bmp280@77**
            :bgn:`channel type=13(ambient_temp) index=0 shift=16 num_samples=1 value=42141326449ns (22.519989)`
            :bgn:`channel type=14(press) index=0 shift=23 num_samples=1 value=42141326449ns (99.312500)`
            :bgn:`channel type=16(humidity) index=0 shift=21 num_samples=1 value=42141326449ns (0.000000)`

LED Blinky with Grove LED Button (Qwiic signals as GPIO)
========================================================

.. zephyr-app-commands::
   :app: zephyr/samples/basic/blinky
   :board: mini_usb_rp2350/rp2350a/m33
   :shield: "grove_btn_d16 grove_led_d17 grove_pwm_led_d17 x_grove_testbed"
   :build-dir: mini_usb_rp2350
   :west-args: -p
   :goals: flash
   :compact:

Simple test execution on target
-------------------------------

   .. admonition:: Console Output
      :class: note dropdown toggle-shown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            … … …
            LED state: OFF
            LED state: ON
            LED state: OFF
            LED state: ON
            LED … … …

LED Fade with Grove LED Button (Qwiic signals as PWM)
=====================================================

.. zephyr-app-commands::
   :app: zephyr/samples/basic/fade_led
   :board: mini_usb_rp2350/rp2350a/m33
   :shield: "grove_btn_d16 grove_led_d17 grove_pwm_led_d17 x_grove_testbed"
   :build-dir: mini_usb_rp2350
   :west-args: -p
   :goals: flash
   :compact:

Simple test execution on target
-------------------------------

   .. admonition:: Console Output
      :class: note dropdown toggle-shown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            PWM-based LED fade
            Using pulse width 0%
            Using pulse width 2%
            Using pulse width 4%
            … … …
            Using pulse width 94%
            Using pulse width 96%
            Using pulse width 98%
            Using pulse width 96%
            Using pulse width 94%
            … … …
            Using pulse width 4%
            Using pulse width 2%
            Using pulse width 0%
            Using pulse width 2%
            Using pulse width 4%
            Using pulse width … … …

LED Switch with Grove LED Button (Qwiic signals as GPIO)
========================================================

.. zephyr-app-commands::
   :app: zephyr/samples/basic/button
   :board: mini_usb_rp2350/rp2350a/m33
   :shield: "grove_btn_d16 grove_led_d17 grove_pwm_led_d17 x_grove_testbed"
   :build-dir: mini_usb_rp2350
   :west-args: -p
   :goals: flash
   :compact:

Simple test execution on target
-------------------------------

   .. admonition:: Console Output
      :class: note dropdown toggle-shown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            Set up button at gpio@40014000 pin 16
            Set up LED at gpio@40014000 pin 17
            Press the button
            Button pressed at 1050252053
            Button pressed at 1338164194
            Button pressed at 1515853740
            Button pressed at 1595751687
            Button … … …

References
**********

.. target-notes::
