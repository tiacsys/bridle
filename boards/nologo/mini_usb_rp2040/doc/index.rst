.. _mini_usb_rp2040:

Mini USB RP2040
###############

The `Mini USB RP2040`_ is a very small, low-cost and versatile Chinese board
from different manufactures or `AliExpress webshops for Mini USB RP2040`_.
It has no SWD interface, but a USB-A plug-in connector built directly into
the PCB with a direct connection to the RP2040 on-chip USB controller. The
Raspberry Pi Pico on-chip USB bootloader allows the ability to flash without
any adapter, in a drag-and-drop manner.

Board Overview
**************

Hardware
========

The `Mini USB RP2040`_ is a :bbl:`mini sized` RP2040 development board.
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

       :hwftlbl:`133㎒`
       :hwftlbl:`4㎆`
       :hwftlbl:`264㎅`
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

       - Dual core Arm Cortex-M0+ processor running up to 133㎒
       - :bbk:`264㎅` on-chip SRAM
       - :bbl:`4㎆` on-board QSPI flash with XIP capabilities
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
       - 8 Programmable I/O (PIO) state machines for custom peripherals
       - 1 Watchdog timer peripheral
       - 1 Temperature sensor on-chip

       .. rubric:: Design Data
       .. rst-class:: rst-columns

       - `Mini USB RP2040 Schematic`_
       - `Mini USB RP2040 Schematic (PNG file)`_
       - `Mini USB RP2040 STEP 3D-Model`_
       - `Mini USB RP2040 STEP 3D-Model (STEP file)`_
       - `Mini USB RP2040 WS2812 Test`_
       - `Mini USB RP2040 WS2812 Test (UF2 file)`_

     - .. image:: img/mini_usb_rp2040.jpg
          :align: center
          :alt: NoLogo Mini USB RP2040

Positions
=========

.. list-table::
   :align: center
   :width: 66%
   :header-rows: 1

   * - .. image:: img/positions.jpg
          :align: center
          :width: 500
          :alt: NoLogo Mini USB RP2040 details

   * - .. container:: twocol

          .. container:: leftside

             1. :strong:`PCB USB-A port`
             #. | :strong:`ME6231C33`
                | 500㎃ low dropout, low noise LDO
             #. | :strong:`On-board flash memory`
                | 4㎆ NOR-Flash :strong:`W25Q32JV`
             #. :strong:`RP2040`
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
             #. | :strong:`RP2040 pins`
                | 13 solder points, including 13 GPIO pins

.. rubric:: Data Sheets
.. rst-class:: rst-columns

- .. rubric:: `RP2040 SoC`_
- `RP2040 Datasheet`_
- `Hardware design with RP2040`_
- .. rubric:: W25Q32JV_
- `W25Q32JV Datasheet`_
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

The peripherals of the `RP2040 SoC`_ can be routed to various pins on
the board. The configuration of these routes can be modified through
:external+zephyr:ref:`DTS <devicetree>`. Please refer to the datasheet
to see the possible routings for each peripheral. The default assignment
is showing below.

External pin mapping on the |Mini USB RP2040| is :strong:`not identical`
to the original |zephyr:board:rpi_pico| board. Almost all pins are rearranged
in a more compact order. Likewise, the voltage sense and monitoring functions
are not integrated. Thus all internal R2040 GPIO lines are available for free
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
          :alt: NoLogo Mini USB RP2040 edge pinout

Default Zephyr Peripheral Mapping:
----------------------------------

.. rst-class:: rst-columns

- UART0_TX : GP0
- UART0_RX : GP1
- UART0_CTS : GP2 (optional, not default)
- UART0_RTS : GP3 (optional, not default)
- GPIO8 : GP8 (free usable)

Supported Features
******************

The |Mini USB RP2040| board configuration supports the following hardware
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
     - :kconfig:option:`CONFIG_USB_DEVICE_STACK`
     - :dtcompatible:`raspberrypi,pico-usbd`
     - :zephyr:ref:`usb_api`
   * - Flash
     - :kconfig:option:`CONFIG_FLASH`
     - :dtcompatible:`raspberrypi,pico-flash-controller`
     - :zephyr:ref:`flash_api` and
       :zephyr:ref:`flash_map_api`
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
     - :dtcompatible:`raspberrypi,core-supply-regulator`
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
     - :dtcompatible:`arm,v6m-nvic`
     - Nested Vector :zephyr:ref:`interrupts_v2` Controller
   * - SYSTICK
     - N/A
     - :dtcompatible:`arm,armv6m-systick`
     -

Other hardware features are not currently supported by Zephyr. The default
configuration can be found in the different Kconfig files:

   - :bridle_file:`boards/nologo/mini_usb_rp2040/mini_usb_rp2040_defconfig`

Connections and IOs
===================

Both the Chinese website about the `Mini USB RP2040`_ and almost all AliExpress
retailers provide a few information about the board connections. Some of the
data they give is pretty sketchy, especially those provided by retailers, which
keep things to the bare minimum and often mess it up. The content provided here
is the result of extensive technical evaluation, correction, rectification, and
supplementation of this publicly available information.

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
the |Mini USB RP2040|, almost all 16 PWM channels are available on the edge
connectors, although some channels are occupied by special signals if their
function is enabled.

Serial Port
===========

The `RP2040 <RP2040 SoC_>`_ MCU has 2 UARTs. One of the UARTs (UART0) is
connected to external devices over GP0 (TX) and GP1 (RX) on the edge
connectors. Optional the hardware handshake signals GP2 (CTS) and GP3 (RTS)
can be used for flow control.

USB Device Port
===============

The `RP2040 <RP2040 SoC_>`_ MCU has a (native) USB device port that can be used
to communicate with a host PC. See the
:external+zephyr:zephyr:code-sample-category:`usb` sample applications for more,
such as the :external+zephyr:zephyr:code-sample:`usb-cdc-acm` sample which sets
up a virtual serial port that echos characters back to the host PC. The
|Mini USB RP2040| provides the Zephyr console per default on the USB port
as :external+zephyr:ref:`usb_device_cdc_acm`:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |mini_usb_rp2040_VID|, idProduct=\ |mini_usb_rp2040_PID_CON|, bcdDevice=\ |mini_usb_rp2040_BCD_CON|
         USB device strings: Mfr=1, Product=2, SerialNumber=3
         Product: |mini_usb_rp2040_PStr_CON|
         Manufacturer: |mini_usb_rp2040_VStr|
         SerialNumber: B163A72F0CF0C97A

Programming and Debugging
*************************

Flashing
========

Using UF2
---------

You can flash the |Mini USB RP2040| with a UF2 file. By default, building an
application for this board will generate a :file:`build/zephyr/zephyr.uf2`
file. If the board is powered on with the ``BOOTSEL`` button pressed, it will
appear on the host as a mass storage device. The UF2 file should be
drag-and-dropped to the device, which will flash the board.

Debugging
=========

There is no SWD interface, thus debugging is not possible on thsi board.

Hello Shell on the USB Console (CDC/ACM)
========================================

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :board: mini_usb_rp2040
   :build-dir: mini_usb_rp2040
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
            - clock-controller\ @\ 40008000 (READY)
              DT node labels: clocks
            - reset-controller\ @\ 4000c000 (READY)
              DT node labels: reset
            - cdc-acm-console-uart (READY)
              DT node labels: cdc_acm_console_uart
            - uart\ @\ 40034000 (READY)
              DT node labels: uart0
            - dma\ @\ 50000000 (READY)
              DT node labels: dma
            - gpio-port\ @\ 0 (READY)
              DT node labels: gpio0
            - flash-controller\ @\ 18000000 (READY)
              DT node labels: ssi
            - vreg\ @\ 40064000 (READY)
              DT node labels: vreg

   .. admonition:: Voltage Regulator
      :class: note dropdown

      .. rubric:: Operate with the on-chip voltage regulator unit:

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **regulator vlist vreg**
            0.800 V
            0.850 V
            0.900 V
            0.950 V
            1.000 V
            1.050 V
            1.100 V
            1.150 V
            1.200 V
            1.250 V
            1.300 V

      .. rubric:: Trigger a power-off/on sequence:

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **hwinfo reset_cause**
            reset caused by:
            - pin

            :bgn:`uart:~$` **regulator disable vreg**
            \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*
            Hello World! I'm THE SHELL from mini_usb_rp2040

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **hwinfo reset_cause**
            reset caused by:
            - power-on reset

   .. admonition:: Flash Controller
      :class: note dropdown

      .. rubric:: Erase, Write and Verify

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **flash read ssi e0000 40**
            000E0000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            000E0010: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            000E0020: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            000E0030: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|

            :bgn:`uart:~$` **flash test ssi e0000 1000 2**
            Erase OK.
            Write OK.
            Verified OK.
            Erase OK.
            Write OK.
            Verified OK.
            Erase-Write-Verify test done.

      .. rubric:: Details

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **flash read ssi e0000 40**
            000E0000: 00 01 02 03 04 05 06 07  08 09 0a 0b 0c 0d 0e 0f \|........ ........\|
            000E0010: 10 11 12 13 14 15 16 17  18 19 1a 1b 1c 1d 1e 1f \|........ ........\|
            000E0020: 20 21 22 23 24 25 26 27  28 29 2a 2b 2c 2d 2e 2f \| !"#$%&' ()*+,-./\|
            000E0030: 30 31 32 33 34 35 36 37  38 39 3a 3b 3c 3d 3e 3f \|01234567 89:;<=>?\|

            :bgn:`uart:~$` **flash page_info e0000**
            Page for address 0xe0000:
            start offset: 0xe0000
            size: 4096
            index: 224

      .. rubric:: Revert

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **flash erase ssi e0000 1000**
            Erase success.

            :bgn:`uart:~$` **flash read ssi e0000 40**
            000E0000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            000E0010: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            000E0020: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            000E0030: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|

References
**********

.. target-notes::
