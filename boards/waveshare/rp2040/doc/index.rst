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

      .. include:: rp2040-one/hardware.rsti

   .. group-tab:: RP2040-Zero

      .. _waveshare_rp2040_zero:

      .. include:: rp2040-zero/hardware.rsti

   .. group-tab:: RP2040-Matrix

      .. _waveshare_rp2040_matrix:

      .. include:: rp2040-matrix/hardware.rsti

   .. group-tab:: RP2040-Tiny

      .. _waveshare_rp2040_tiny:

      .. include:: rp2040-tiny/hardware.rsti

   .. group-tab:: RP2040-ETH

      .. _waveshare_rp2040_eth:

      .. include:: rp2040-eth/hardware.rsti

   .. group-tab:: RP2040-LCD-0.96

      .. _waveshare_rp2040_lcd_0_96:

      .. include:: rp2040-lcd-0.96/hardware.rsti

   .. group-tab:: RP2040-Plus

      .. _waveshare_rp2040_plus:

      .. include:: rp2040-plus/hardware.rsti

   .. group-tab:: RP2040-Geek

      .. _waveshare_rp2040_geek:

      .. include:: rp2040-geek/hardware.rsti

Positions
=========

.. tabs::

   .. group-tab:: RP2040-One

      .. include:: rp2040-one/positions.rsti

   .. group-tab:: RP2040-Zero

      .. include:: rp2040-zero/positions.rsti

   .. group-tab:: RP2040-Matrix

      .. include:: rp2040-matrix/positions.rsti

   .. group-tab:: RP2040-Tiny

      .. include:: rp2040-tiny/positions.rsti

   .. group-tab:: RP2040-ETH

      .. include:: rp2040-eth/positions.rsti

   .. group-tab:: RP2040-LCD-0.96

      .. include:: rp2040-lcd-0.96/positions.rsti

   .. group-tab:: RP2040-Plus

      .. include:: rp2040-plus/positions.rsti

   .. group-tab:: RP2040-Geek

      .. include:: rp2040-geek/positions.rsti

Pinouts
=======

The peripherals of the `RP2040 SoC`_ can be routed to various pins on
the board. The configuration of these routes can be modified through
:external+zephyr:ref:`DTS <devicetree>`. Please refer to the datasheet
to see the possible routings for each peripheral. The default assignments
for the various Waveshare RP2040 boards are defined below separately
in a single tab.

.. tabs::

   .. group-tab:: RP2040-One

      .. include:: rp2040-one/pinouts.rsti

   .. group-tab:: RP2040-Zero

      .. include:: rp2040-zero/pinouts.rsti

   .. group-tab:: RP2040-Matrix

      .. include:: rp2040-matrix/pinouts.rsti

   .. group-tab:: RP2040-Tiny

      .. include:: rp2040-tiny/pinouts.rsti

   .. group-tab:: RP2040-ETH

      .. include:: rp2040-eth/pinouts.rsti

   .. group-tab:: RP2040-LCD-0.96

      .. include:: rp2040-lcd-0.96/pinouts.rsti

   .. group-tab:: RP2040-Plus

      .. include:: rp2040-plus/pinouts.rsti

   .. group-tab:: RP2040-Geek

      .. include:: rp2040-geek/pinouts.rsti

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

   - :bridle_file:`boards/waveshare/rp2040/waveshare_rp2040_one_defconfig`
   - :bridle_file:`boards/waveshare/rp2040/waveshare_rp2040_zero_defconfig`
   - :bridle_file:`boards/waveshare/rp2040/waveshare_rp2040_matrix_defconfig`
   - :bridle_file:`boards/waveshare/rp2040/waveshare_rp2040_tiny_defconfig`
   - :bridle_file:`boards/waveshare/rp2040/waveshare_rp2040_eth_defconfig`
   - :bridle_file:`boards/waveshare/rp2040/waveshare_rp2040_lcd_0_96_defconfig`
   - :bridle_file:`boards/waveshare/rp2040/waveshare_rp2040_plus_defconfig`
   - :bridle_file:`boards/waveshare/rp2040/waveshare_rp2040_geek_defconfig`

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

The `RP2040 <RP2040 SoC_>`_ MCU has a (native) USB device port that can be used
to communicate with a host PC. See the
:external+zephyr:zephyr:code-sample-category:`usb` sample applications for more,
such as the :external+zephyr:zephyr:code-sample:`usb-cdc-acm` sample which sets
up a virtual serial port that echos characters back to the host PC.
As an alternative to the default Zephyr console on serial port the
Bridle :ref:`snippet-usb-console` can be used to enable
:external+zephyr:ref:`usb_device_cdc_acm` and switch the console to USB

.. tabs::

   .. group-tab:: RP2040-One

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |waveshare_rp2040_one_VID|, idProduct=\ |waveshare_rp2040_one_PID_CON|, bcdDevice=\ |waveshare_rp2040_one_BCD_CON|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |waveshare_rp2040_one_PStr_CON|
               Manufacturer: |waveshare_rp2040_one_VStr|
               SerialNumber: B69F8448A6E91514

   .. group-tab:: RP2040-Zero

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |waveshare_rp2040_zero_VID|, idProduct=\ |waveshare_rp2040_zero_PID_CON|, bcdDevice=\ |waveshare_rp2040_zero_BCD_CON|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |waveshare_rp2040_zero_PStr_CON|
               Manufacturer: |waveshare_rp2040_zero_VStr|
               SerialNumber: B69F8448A6E91514

   .. group-tab:: RP2040-Matrix

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |waveshare_rp2040_matrix_VID|, idProduct=\ |waveshare_rp2040_matrix_PID_CON|, bcdDevice=\ |waveshare_rp2040_matrix_BCD_CON|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |waveshare_rp2040_matrix_PStr_CON|
               Manufacturer: |waveshare_rp2040_matrix_VStr|
               SerialNumber: B69F8448A6E91514

   .. group-tab:: RP2040-Tiny

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |waveshare_rp2040_tiny_VID|, idProduct=\ |waveshare_rp2040_tiny_PID_CON|, bcdDevice=\ |waveshare_rp2040_tiny_BCD_CON|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |waveshare_rp2040_tiny_PStr_CON|
               Manufacturer: |waveshare_rp2040_tiny_VStr|
               SerialNumber: B69F8448A6E91514

   .. group-tab:: RP2040-ETH

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |waveshare_rp2040_eth_VID|, idProduct=\ |waveshare_rp2040_eth_PID_CON|, bcdDevice=\ |waveshare_rp2040_eth_BCD_CON|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |waveshare_rp2040_eth_PStr_CON|
               Manufacturer: |waveshare_rp2040_eth_VStr|
               SerialNumber: B69F8448A6E91514

   .. group-tab:: RP2040-LCD-0.96

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |waveshare_rp2040_lcd_0_96_VID|, idProduct=\ |waveshare_rp2040_lcd_0_96_PID_CON|, bcdDevice=\ |waveshare_rp2040_lcd_0_96_BCD_CON|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |waveshare_rp2040_lcd_0_96_PStr_CON|
               Manufacturer: |waveshare_rp2040_lcd_0_96_VStr|
               SerialNumber: B69F8448A6E91514

   .. group-tab:: RP2040-Plus

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |waveshare_rp2040_plus_VID|, idProduct=\ |waveshare_rp2040_plus_PID_CON|, bcdDevice=\ |waveshare_rp2040_plus_BCD_CON|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |waveshare_rp2040_plus_PStr_CON|
               Manufacturer: |waveshare_rp2040_plus_VStr|
               SerialNumber: B69F8448A6E91514

   .. group-tab:: RP2040-Geek

         .. container:: highlight-console notranslate literal-block

            .. parsed-literal::

               USB device idVendor=\ |waveshare_rp2040_geek_VID|, idProduct=\ |waveshare_rp2040_geek_PID_CON|, bcdDevice=\ |waveshare_rp2040_geek_BCD_CON|
               USB device strings: Mfr=1, Product=2, SerialNumber=3
               Product: |waveshare_rp2040_geek_PStr_CON|
               Manufacturer: |waveshare_rp2040_geek_VStr|
               SerialNumber: B69F8448A6E91514

To integrate specific USB device functions that do not follow
a USB standard class, the following alternate identifier numbers
are available for the various Waveshare RP2040 and RP2350 boards
according to the `Raspberry Pi USB product ID list`_:

.. container:: twocol

   .. container:: leftside

      .. rubric:: RP2040

      :|rpi_waveshare_rp2040_zero_URB_PID|: |RP2040-Zero|
      :|rpi_waveshare_rp2040_plus_URB_PID|: |RP2040-Plus|
      :|rpi_waveshare_rp2040_lcd_0_96_URB_PID|: |RP2040-LCD-0.96|
      :|rpi_waveshare_rp2040_lcd_1_28_URB_PID|: RP2040-LCD-1.28
      :|rpi_waveshare_rp2040_one_URB_PID|: |RP2040-One|
      :|rpi_waveshare_pwr_mgmt_hat_b_one_URB_PID|: Power Management HAT (B)
      :|rpi_waveshare_rp2040_eth_URB_PID|: |RP2040-ETH|
      :|rpi_waveshare_rp2040_geek_URB_PID|: |RP2040-Geek|
      :|rpi_waveshare_rp2040_touch_lcd_1_28_URB_PID|: RP2040-Touch-LCD-1.28
      :|rpi_waveshare_rp2040_pizero_URB_PID|: RP2040-PiZero
      :|rpi_waveshare_rp2040_tiny_URB_PID|: |RP2040-Tiny|
      :|rpi_waveshare_rp2040_matrix_URB_PID|: |RP2040-Matrix|
      :|rpi_waveshare_rp2040_ble_URB_PID|: RP2040-BLE
      :|rpi_waveshare_pico_cam_a_URB_PID|: PICO-Cam-A

   .. container:: rightside

      .. rubric:: RP2350

      :|rpi_waveshare_rp2350_zero_URB_PID|: RP2350-Zero
      :|rpi_waveshare_rp2350_plus_URB_PID|: RP2350-Plus
      :|rpi_waveshare_rp2350_tiny_URB_PID|: RP2350-Tiny
      :|rpi_waveshare_rp2350_lcd_1_28_URB_PID|: RP2350-LCD-1.28
      :|rpi_waveshare_rp2350_touch_lcd_1_28_URB_PID|: RP2350-Touch-LCD-1.28
      :|rpi_waveshare_rp2350_one_URB_PID|: RP2350-One
      :|rpi_waveshare_rp2350_geek_URB_PID|: RP2350-Geek
      :|rpi_waveshare_rp2350_lcd_0_96_URB_PID|: RP2350-LCD-0.96

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

If you don't have an SWD adapter, you can flash the Waveshare RP2040 boards
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

:|CONFIG_RP2_FLASH_AT25SF128A|: |boot2_at25sf128a.S|_
:|CONFIG_RP2_FLASH_GENERIC_03H|: |boot2_generic_03h.S|_
:|CONFIG_RP2_FLASH_IS25LP080|: |boot2_is25lp080.S|_
:|CONFIG_RP2_FLASH_W25Q080|: |boot2_w25q080.S|_
:|CONFIG_RP2_FLASH_W25X10CL|: |boot2_w25x10cl.S|_

All Waveshare RP2040 boards set this option to |CONFIG_RP2_FLASH_W25Q080|.
Further information can be found in the `RP2040 Datasheet`_, sections with
title :emphasis:`"Bootrom"` and :emphasis:`"Processor Controlled Boot Sequence"`
or Brian Starkey's Blog article `Pico serial bootloader`_

Using SEGGER JLink
------------------

You can flash the Waveshare RP2040 boards with a SEGGER JLink debug probe as
described in
:external+zephyr:ref:`Building, Flashing and Debugging <west-flashing>`.

Here is an example of building and flashing the
:external+zephyr:zephyr:code-sample:`blinky` application.

.. zephyr-app-commands::
   :app: zephyr/samples/basic/blinky
   :board: waveshare_rp2040_plus
   :build-dir: waveshare_rp2040
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

The |RP2040-LCD-0.96| and |RP2040-Plus| has an SWD interface that can be used
to program and debug the on board RP2040. This interface can be utilized by
OpenOCD. To use it with the RP2040, OpenOCD version 0.12.0 or later is needed.
If you are using a Debian based system (including RaspberryPi OS, Ubuntu,
and more), using the `pico_setup.sh`_ script is a convenient way to set up
the forked version of OpenOCD. Depending on the interface used (such as JLink),
you might need to checkout to a branch that supports this interface, before
proceeding. Build and install OpenOCD as described in the README.

Here is an example of building and flashing the
:external+zephyr:zephyr:code-sample:`blinky` application.

.. zephyr-app-commands::
   :app: zephyr/samples/basic/blinky
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
:external+zephyr:ref:`Building, Flashing and Debugging <west-debugging>`.

Using OpenOCD
-------------

Install OpenOCD as described for flashing the board.

Here is an example for debugging the
:external+zephyr:zephyr:code-sample:`blinky` application.

.. zephyr-app-commands::
   :app: zephyr/samples/basic/blinky
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

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`led-strip`.

      .. image:: rp2040-one/ws2812b.gif
         :align: right
         :alt: Waveshare RP2040-One WS2812 LED Test Pattern

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/led/led_strip
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

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`led-strip`.

      .. image:: rp2040-zero/ws2812b.gif
         :align: right
         :alt: Waveshare RP2040-Zero WS2812 LED Test Pattern

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/led/led_strip
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

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`led-strip`.

      .. image:: rp2040-matrix/ws2812b-5x5.gif
         :align: right
         :alt: Waveshare RP2040-Matrix WS2812 LED Test Pattern

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/led/led_strip
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

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`led-strip`.

      .. image:: rp2040-tiny/ws2812b.gif
         :align: right
         :alt: Waveshare RP2040-Tiny WS2812 LED Test Pattern

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/led/led_strip
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

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`led-strip`.

      .. image:: rp2040-eth/ws2812b.gif
         :align: right
         :alt: Waveshare RP2040-ETH WS2812 LED Test Pattern

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/led/led_strip
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

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`blinky`.

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky
         :board: waveshare_rp2040_lcd_0_96
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: LCD Backlight LED Blinky by PWM

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`pwm-blinky`.

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky_pwm
         :board: waveshare_rp2040_lcd_0_96
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: LCD Backlight LED Fade by PWM

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`fade-led`.

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

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`blinky`.

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky
         :board: waveshare_rp2040_plus
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Green User LED Blinky by PWM

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`pwm-blinky`.

      .. zephyr-app-commands::
         :app: zephyr/samples/basic/blinky_pwm
         :board: waveshare_rp2040_plus
         :build-dir: waveshare_rp2040
         :west-args: -p
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. rubric:: Green User LED Fade by PWM

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`fade-led`.

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

      .. image:: rp2040-geek/loopback_test_shield.jpg
         :align: right
         :alt: Waveshare RP2040-Geek with loopback wiring for tests

      .. rubric:: External LED Blinky by GPIO

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`blinky`.

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

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`pwm-blinky`.

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

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`fade-led`.

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

      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`button`.

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

      .. include:: rp2040-one/helloshell.rsti

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

      .. include:: rp2040-zero/helloshell.rsti

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

      .. include:: rp2040-matrix/helloshell.rsti

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

      .. include:: rp2040-tiny/helloshell.rsti

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

      .. include:: rp2040-eth/helloshell.rsti

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

      .. include:: rp2040-lcd-0.96/helloshell.rsti

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

      .. include:: rp2040-plus/helloshell.rsti

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

      .. include:: rp2040-geek/helloshell.rsti

Display Test and Demonstration
==============================

This samples and test applications are only applicable on the |RP2040-Matrix|,
|RP2040-LCD-0.96| and |RP2040-Geek| board. They will be built with activated
USB-CDC/ACM console.

.. tabs::

   .. group-tab:: RP2040-Matrix

      The following samples work with the chosen display. That is:

      | :hwftlbl-scr:`LED(5×5)` : :dts:`chosen { zephyr,display = &rgb_led_strip_matrix; };`
      | :hwftlbl-led:`5×5 RGB` : :dts:`&rgb_led_strip_matrix { led-strip = <&led_strip>; };`

      .. rubric:: LCD Orientation and Bit Order Test

      Using the :external+zephyr:ref:`Display driver API <display_api>` with chosen
      display. See also Zephyr sample: :external+zephyr:zephyr:code-sample:`display`.

      .. zephyr-app-commands::
         :app: zephyr/samples/drivers/display
         :board: waveshare_rp2040_matrix
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. list-table::
         :align: center
         :width: 66%
         :header-rows: 1

         * - .. image:: rp2040-matrix/ws2812b-5x5-display_test.gif
                :align: center
                :alt: Waveshare RP2040-Matrix Display Sample Animation
         * - .. rst-class:: centered

                :brd:`TOP LEFT`, :bgn:`TOP RIGHT`, :bbl:`BOTTOM RIGHT`

   .. group-tab:: RP2040-LCD-0.96

      The following samples work with the chosen display. That is:

      | :hwftlbl-scr:`LCD` : :dts:`chosen { zephyr,display = &lcd_panel; };`
      | :hwftlbl-scr:`ST7735S` : :dts:`lcd_panel: &st7735s_160x80 {};`

      .. rubric:: LCD Orientation and Bit Order Test

      Using the :external+zephyr:ref:`Display driver API <display_api>`
      with chosen display.
      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`display`.

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

         * - .. image:: rp2040-lcd-0.96/display.*
                :align: center
                :alt: Waveshare RP2040-LCD-0.96 Display Sample Animation
         * - .. rst-class:: centered

                :brd:`TOP LEFT`, :bgn:`TOP RIGHT`, :bbl:`BOTTOM RIGHT`

      .. rubric:: LVGL Basic Sample

      Using the LVGL module on top of the
      :external+zephyr:ref:`Display driver API <display_api>`
      with chosen display.
      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`lvgl`.

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

      | :hwftlbl-scr:`LCD` : :dts:`chosen { zephyr,display = &lcd_panel; };`
      | :hwftlbl-scr:`ST7789V` : :dts:`lcd_panel: &st7789v_240x135 {};`

      .. rubric:: LCD Orientation and Bit Order Test

      Using the :external+zephyr:ref:`Display driver API <display_api>`
      with chosen display.
      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`display`.

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

         * - .. image:: rp2040-geek/display.*
                :align: center
                :alt: Waveshare RP2040-Geek Display Sample Animation
         * - .. rst-class:: centered

                :brd:`TOP LEFT`, :bgn:`TOP RIGHT`, :bbl:`BOTTOM RIGHT`

      .. rubric:: LVGL Basic Sample

      Using the LVGL module on top of the
      :external+zephyr:ref:`Display driver API <display_api>`
      with chosen display.
      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`lvgl`.

      .. zephyr-app-commands::
         :app: zephyr/samples/subsys/display/lvgl
         :board: waveshare_rp2040_geek
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

TF/microSD Demonstration
========================

This samples and test applications are only applicable on the |RP2040-Geek|
board. They will be built with activated USB-CDC/ACM console.

.. tabs::

   .. group-tab:: RP2040-Geek

      The following samples work with the chosen SDHC interface in 1-bit
      mode and connected to SPI. That is:

      | :hwftlbl-spi:`SDHC` :
        :dts:`&spi0 { sdhc0: sdhc@0 { compatible = "zephyr,sdhc-spi-slot"; }; };`
      | :hwftlbl-dsk:`TF/microSD` :
        :dts:`&sdhc0 { mmc { compatible = "zephyr,sdmmc-disk"; }; };`

      .. rubric:: File system manipulation

      Using the :external+zephyr:ref:`File Systems API <file_system_api>`
      ontop of the :external+zephyr:ref:`Disk Access API <disk_access_api>`
      with chosen TF/microSD.
      See also Zephyr sample: :external+zephyr:zephyr:code-sample:`fs`.

      .. zephyr-app-commands::
         :app: zephyr/samples/subsys/fs/fs_sample
         :board: waveshare_rp2040_geek
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :flash-args: -r uf2
         :goals: flash
         :compact:

      .. image:: rp2040-geek/RP2040-GEEK.bmp
         :align: right
         :alt: Waveshare RP2040-Geek Demo Bitmap Image

      The TF/microSD card should be pre-formatted with FAT FS. If there are
      any files or directories present in the card, the sample lists them out
      on the console, e.g.:

         * :bbl:`(optional)` Boot Sector:
           :strong:`MBR` :emphasis:`(Master Boot Record)`
         * :bbl:`(optional)` 1st Primary Partition:
           :strong:`W95 FAT32 (LBA)` :emphasis:`(ID: 0x0C)`
         * FAT File System: :strong:`FAT (32-bit version)`
         * Content: :download:`rp2040-geek/RP2040-GEEK.bmp`

      .. rubric:: Simple logging output on target

      .. container:: highlight highlight-console notranslate no-copybutton

         .. parsed-literal::

            \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
            [00:00:00.464,000] :byl:`<wrn> udc_rpi: BUS RESET`
            [00:00:00.548,000] :byl:`<wrn> udc_rpi: BUS RESET`
            \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*
            [00:00:04.269,000] <inf> main: Block count 15759360
            Sector size 512
            Memory Size(MB) 7695
            Disk mounted.

            Listing dir /SD: ...
            [FILE] RP2040~1.BMP (size = 97254)

      In case when no files could be listed, because there are none (empty FS),
      :file:`some.dir` directory and :file:`other.txt` file will be created and
      list will run again to show them, e.g.:

         * :bbl:`(optional)` Boot Sector:
           :strong:`MBR` :emphasis:`(Master Boot Record)`
         * :bbl:`(optional)` 1st Primary Partition:
           :strong:`W95 FAT32 (LBA)` :emphasis:`(ID: 0x0C)`
         * FAT File System: :strong:`FAT (32-bit version)`
         * Content: :brd:`NONE (empty FS)`

      .. rubric:: Simple logging output on target

      .. container:: highlight highlight-console notranslate no-copybutton

         .. parsed-literal::

            \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
            [00:00:00.326,000] :byl:`<wrn> udc_rpi: BUS RESET`
            [00:00:00.406,000] :byl:`<wrn> udc_rpi: BUS RESET`
            \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*
            [00:00:04.192,000] <inf> main: Block count 15759360
            Sector size 512
            Memory Size(MB) 7695
            Disk mounted.

            Listing dir /SD: ...
            [00:00:04.317,000] <inf> main: Creating some dir entries in /SD:

            Listing dir /SD: ...
            [FILE] SOME.DAT (size = 0)
            [DIR ] SOME

      In there is no FS (or the FS is corrupted), the disk is attempted
      to re-format to FAT FS and list will run again to show them, e.g.:

         * Boot Sector: :brd:`NONE (empty boot sector, no partition table)`
           – :bbl:`(optional)` :strong:`MBR` :emphasis:`(Master Boot Record)`
         * 1st Primary Partition: :brd:`NONE (empty partition table entry)`
           – :bbl:`(optional)` :strong:`W95 FAT32 (LBA)` :emphasis:`(ID: 0x0C)`
         * FAT File System: :brd:`NONE (empty partition)`
         * Content: :brd:`NONE (empty FS)`

      .. rubric:: Simple logging output on target

      .. container:: highlight highlight-console notranslate no-copybutton

         .. parsed-literal::

            \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
            [00:00:00.367,000] :byl:`<wrn> udc_rpi: BUS RESET`
            [00:00:00.447,000] :byl:`<wrn> udc_rpi: BUS RESET`
            \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*
            [00:00:04.236,000] <inf> main: Block count 15759360
            Sector size 512
            Memory Size(MB) 7695
            Disk mounted.

            Listing dir /SD: ...
            [00:00:11.844,000] <inf> main: Creating some dir entries in /SD:

            Listing dir /SD: ...
            [FILE] SOME.DAT (size = 0)
            [DIR ] SOME

      .. tsn-include:: samples/subsys/fs/fs_sample/README.rst
         :docset: zephyr
         :start-after: sample lists them out on the debug serial output.
         :end-before: Building and Running EXT2 samples

      .. zephyr-app-commands::
         :app: zephyr/samples/subsys/fs/fs_sample
         :board: waveshare_rp2040_geek
         :build-dir: waveshare_rp2040
         :west-args: -p -S usb-console
         :gen-args: -DCONFIG_FS_FATFS_MOUNT_MKFS=n
         :flash-args: -r uf2
         :goals: flash
         :compact:

References
**********

.. target-notes::
