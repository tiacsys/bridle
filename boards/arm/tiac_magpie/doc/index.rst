.. _tiac_magpie_board:

TiaC Magpie STM32F777NIHx
#########################

Overview
********

The TiaC Magpie STM32F777NIHx boards offer combinations of performance
and power that provide an affordable and flexible way for users to build
prototypes and try out new concepts target communication systems.

The board requires any separate JTAG/SWD probe, e.g. the ST-LINK/V2
debugger/programmer.

.. rubric:: Key Features

- STM32 microcontroller in TFBGA216 package
- Ethernet compliant with IEEE-802.3-2002 (depending on STM32 support)
- USB full-speed device (depending on STM32 support)
- USB full-speed host with 7 port hub (depending on STM32 support)
- 2 user LEDs
- reset push-button
- 25.000 MHz high-speed on-board crystal oscillator (for system clock)
- 32.768 kHz low-speed on-board crystal oscillator (for on-chip RTC)
- Board connectors:

  - JTAG/SWD
  - UART Console over USB with Micro-AB
  - USB device with Micro-AB
  - Ethernet RJ45 (depending on STM32 support)
  - 6 2x8 pin header with dedicated CAN and USB busses
  - 5 2x7 pin header with spare GPIO
  - Single power-supply input: 12V/3A external sources

.. image:: img/tiac_magpie.svg
   :alt: Magpie STM32F777NIHx
   :align: center

.. More information about the board can be found at the
   `TiaC Magpie STM32F777NIHx website`_.

.. ...........................................................................

Hardware
********

The STM32F777NIHx on the TiaC Magpie board provides the following hardware
components:

- STM32F777NIHx in TFBGA216 package
- ARM 32-bit Cortex®-M7 CPU with DPFPU
- Chrom-ART Accelerator
- ART Accelerator
- 216 MHz max CPU frequency
- VDD from 1.7 V to 3.6 V
- 2 MB Flash
- 512 KB SRAM
- 16-bit timers (10)
- 32-bit timers (2)
- SPI (6)
- I2C (4)
- I2S (3)
- USART (4)
- UART (4)
- USB OTG Full Speed (1)
- USB OTG Full Speed and High Speed (1)
- 10/100 Ethernet MAC with MII/RMII and MDIO (1)
- CAN (2)
- SAI (2)
- Dual Mode Quad SPI (1)
- GPIO (up to 168) with external interrupt capability
- Digital Filters for Sigma Delta Modulator (DFSDM)
  with 8 channels / 4 filters
- 12-bit ADC with 24 channels / 2.4 MSPS (3)
- 12-bit DAC with 2 channels (2)
- 16-channel DMA
- Cryptographic Acceleration for AES 128, 192, 256, triple DES,
  HASH (MD5, SHA-1, SHA-2), and HMAC
- True Random Number Generator (RNG)
- CRC calculation unit
- RTC: subsecond accuracy, hardware calendar
- 96-bit unique ID

More information about the STM32F777NIHx can be found at the website about
`STM32F777NI on www.st.com`_ or in the `STM32F777 Reference Manual (RM0410)`_
and the `STM32F7 Series Cortex®-M7 Processor Programming Manual (PM0253)`_.

Supported Features
==================

The Zephyr ``tiac_magpie`` board configuration supports the following
hardware features:

.. table:: Hardware Supported Features in Zephyr
   :class: longtable
   :align: center

   +-----------+------------+-------------------------------------+
   | Interface | Controller | Driver/Component                    |
   +===========+============+=====================================+
   | NVIC      | on-chip    | Nested Vector Interrupt Controller  |
   +-----------+------------+-------------------------------------+
   | UART      | on-chip    | Serial Port                         |
   +-----------+------------+-------------------------------------+
   | PINMUX    | on-chip    | pinmux                              |
   +-----------+------------+-------------------------------------+
   | GPIO      | on-chip    | gpio                                |
   +-----------+------------+-------------------------------------+
   | ETHERNET  | on-chip    | ethernet (*)                        |
   +-----------+------------+-------------------------------------+
   | USB       | on-chip    | usb_device                          |
   +-----------+------------+-------------------------------------+
   | CAN       | on-chip    | can                                 |
   +-----------+------------+-------------------------------------+
   | I2C       | on-chip    | i2c                                 |
   +-----------+------------+-------------------------------------+
   | SPI       | on-chip    | spi                                 |
   +-----------+------------+-------------------------------------+
   | PWM       | on-chip    | pwm                                 |
   +-----------+------------+-------------------------------------+
   | ADC       | on-chip    | ADC Controller                      |
   +-----------+------------+-------------------------------------+
   | COUNTER   | on-chip    | Real-Time Clock                     |
   +-----------+------------+-------------------------------------+
   | WATCHDOG  | on-chip    | Independent Watchdog                |
   +-----------+------------+-------------------------------------+
   | RNG       | on-chip    | True Random Number Generator        |
   +-----------+------------+-------------------------------------+

(*) tiac_magpie with soc cut-A (Device marking A) has some ethernet
    instability (https://github.com/zephyrproject-rtos/zephyr/issues/26519).
    Use of cut-Z is advised.
    see restrictions errata:
    https://www.st.com/resource/en/errata_sheet/DM00257543.pdf

Other hardware features are not yet supported on this Zephyr port.

The default configuration can be found in the defconfig file:
``boards/arm/tiac_magpie/tiac_magpie_defconfig``

.. For mode details please refer to
   `TiaC Magpie STM32F777NIHx board User Manual`_.

Default Zephyr Peripheral Mapping:
----------------------------------

The TiaC Magpie STM32F777NIHx board is configured as follows:

- UART 7 TX/RX/RTS/CTS : PE8/PE7/PE9/PE10 (Zephyr Shell Console)
- JTAG(SWD) TMS/TCK/TDI/TDO/TRST : PA13/PA14/PA15/PB3/PB4 (ST-Link)
- User LED 1/2 : PG11/PG12
- ETH : PA0, PA1, PA2, PA3, PB0, PB1, PB8, PB11, PC1, PC2, PC3, PC4, PC5,
  (PC6/PC7), PG13, PG14, PI10
- USB OTG FS DM/DP (device) : PA11/PA12
- USB OTG HS DM/DP (host/hub) : (PB14/PB15)
- CAN 1 TX/RX : PH13/PH14
- CAN 2 RX/TX : PB12/PB13
- I2C 2 SDA/SCL : PF0/PF1
- I2C 4 SCL/SDA : PF14/PF15
- SPI 5 MOSI/NSS/SCK/MISO : PF11/PH5/PH6/PH7
- PWM TIM 8 CH1/2/3 : PI5/PI6/PI7
- ADC 3 IN9/IN14/IN15 : PF3/PF4/PF5

System Clock
------------

The STM32F777NIHx System Clock on the TiaC Magpie board could be driven by an
internal or external oscillator, as well as the main PLL clock. By default,
the System clock is driven by the PLL clock at 216 MHz, driven by an 25 MHz
high-speed on-board clock.

Serial Port
-----------

The STM32F777NIHx on the TiaC Magpie board has 4 UARTs and 4 USARTs, but not
all are open usable or accessible. The Zephyr console output is assigned to
UART 7. Default settings are 115200 8N1.

Pin Header
----------

The five TiaC Magpie pin headers ``TMPH[1..5]`` have the following layout:

.. image:: img/tiac_magpie_ph.svg
   :alt: Magpie Pin Header
   :align: center

.. ...........................................................................

Programming and Debugging
*************************

Applications for the ``tiac_magpie`` board configuration can be built and
flashed in the usual way (see :ref:`build_an_application` and
:ref:`application_run` for more details).

Flashing
========

The TiaC Magpie STM32F777NIHx needs an ST-LINK/V2 debug tool adapter.

Flashing an application to TiaC Magpie STM32F777NIHx
----------------------------------------------------

Here is an example for the :ref:`hello_world` application.

Run a serial host program to connect with your TiaC Magpie board.

.. code-block:: console

   $ screen /dev/ttyUSBx 115200,cs8,parenb,-parodd,-cstopb

Build and flash the application:

.. zephyr-app-commands::
   :zephyr-app: zephyr/samples/hello_world
   :build-dir: hello_world-tiac_magpie
   :board: tiac_magpie
   :goals: build flash
   :host-os: unix
   :compact:

You should see the following message on the console:

.. code-block:: console

   *** Booting Zephyr OS version x.y.z  ***
   Hello World! tiac_magpie

Debugging
=========

You can debug an application in the usual way. Here is an example for the
:ref:`hello_world` application.

.. zephyr-app-commands::
   :zephyr-app: zephyr/samples/hello_world
   :build-dir: hello_world-tiac_magpie
   :board: tiac_magpie
   :maybe-skip-config:
   :goals: debug
   :host-os: unix

Examples and Demonstrations
===========================

Zephyr provides a large number of samples and demonstration applications,
some of which can be used for the start-up of the TiaC Magpie without any
further modification:

.. toctree::
   :maxdepth: 1
   :glob:

   samples/**/*

.. ...........................................................................

Detailed Specification
**********************

STM32CubeMX Pin Multiplexing
============================

The STM32F7 exposes its various function blocks to the outside of the
device through a programmable I/O multiplex matrix on its hundreds of
pins. In order to be able to create and modify the configuration data
for this matrix in a semantically correct way, the CPU manufacturer
provides the tool `STM32CubeMX`_. This tool must then be used with the
IOC project file provided by this documentation to edit or export the
exact corresponding pin configurations of the given hardware design,
e.g. to CSV representation or PDF report:

* TiaC Magpie STM32F7 IOC project file: :download:`STM32F777NIHx.ioc`
* TiaC Magpie STM32F7 PDF report file: :download:`STM32F777NIHx.pdf`

.. csv-table:: STM32F7 Pin Multiplexing
   :file: STM32F777NIHx_no_alt.csv
   :encoding: ISO-8859-1
   :class: longtable
   :align: center
   :delim: ,
   :widths: 12, 24, 12, 36, 36
   :header-rows: 1
   :stub-columns: 1

Pin Header 1
------------

Alternate functions on the TiaC Magpie pin header ``TMPH1``:

.. csv-filter:: TMPH1 Pin Multiplexing
   :file: STM32F777NIHx_with_alt.csv
   :encoding: ISO-8859-1
   :class: longtable
   :align: center
   :delim: ,
   :widths: 16, 6, 16, 12, 12, 12, 12, 12, 12, 12
   :included_cols: 4,1,3,6,7,8,10,11,12,13
   :include: {1: '(PA10|PC10|PC11|PC12|PD0|PD1|PD2|PD3|PD4|PI2|PI3|PI9)$'}
   :header-rows: 1
   :stub-columns: 1
.. :include: {4: '(TMPH1)'} <-- doesn't work

Pin Header 2
------------

Alternate functions on the TiaC Magpie pin header ``TMPH2``:

.. csv-filter:: TMPH2 Pin Multiplexing
   :file: STM32F777NIHx_with_alt.csv
   :encoding: ISO-8859-1
   :class: longtable
   :align: center
   :delim: ,
   :widths: 16, 6, 16, 12, 12, 12, 12, 12, 12, 12
   :included_cols: 4,1,3,6,7,8,9,10,12,13
   :include: {1: '(PA9|PD10|PD14|PD15|PF4|PF5|PG8|PH3|PH5|PI0|PI1|PI15)$'}
   :header-rows: 1
   :stub-columns: 1
.. :include: {4: '(TMPH2)'} <-- doesn't work

Pin Header 3
------------

Alternate functions on the TiaC Magpie pin header ``TMPH3``:

.. csv-filter:: TMPH3 Pin Multiplexing
   :file: STM32F777NIHx_with_alt.csv
   :encoding: ISO-8859-1
   :class: longtable
   :align: center
   :delim: ,
   :widths: 16, 6, 16, 12, 12, 12, 12, 16
   :included_cols: 4,1,3,7,8,9,10,14
   :include: {1: '(PG2|PG3|PG4|PG5|PH2|PH6|PH7|PH8|PH9|PH10|PH11|PH12)$'}
   :header-rows: 1
   :stub-columns: 1
.. :include: {4: '(TMPH3)'} <-- doesn't work

Pin Header 4
------------

Alternate functions on the TiaC Magpie pin header ``TMPH4``:

.. csv-filter:: TMPH4 Pin Multiplexing
   :file: STM32F777NIHx_with_alt.csv
   :encoding: ISO-8859-1
   :class: longtable
   :align: center
   :delim: ,
   :widths: 16, 6, 16, 12, 12, 12, 12
   :included_cols: 4,1,3,7,8,9,13
   :include: {1: '(PE0|PE1|PF2|PF3|PG15|PI4|PI5|PI6|PI7|PI12|PI13|PI14)$'}
   :header-rows: 1
   :stub-columns: 1
.. :include: {4: '(TMPH4)'} <-- doesn't work

Pin Header 5
------------

Alternate functions on the TiaC Magpie pin header ``TMPH5``:

.. csv-filter:: TMPH5 Pin Multiplexing
   :file: STM32F777NIHx_with_alt.csv
   :encoding: ISO-8859-1
   :class: longtable
   :align: center
   :delim: ,
   :widths: 16, 6, 16, 12, 12, 12
   :included_cols: 4,1,3,6,9,10
   :include: {1: '(PE11|PE12|PE13|PE14|PE15|PF11|PF12|PF13|PF14|PF15|PG0|PG1)$'}
   :header-rows: 1
   :stub-columns: 1
.. :include: {4: '(TMPH5)'} <-- doesn't work

.. ...........................................................................

.. _TiaC Magpie STM32F777NIHx website:
   https://www.st.com/en/evaluation-tools/nucleo-f767zi.html

.. _TiaC Magpie STM32F777NIHx board User Manual:
   http://www.st.com/resource/en/user_manual/dm00244518.pdf

.. _STM32F777NI on www.st.com:
   https://www.st.com/en/microcontrollers-microprocessors/stm32f777ni.html

.. _STM32F7 Series Cortex®-M7 Processor Programming Manual (PM0253):
   https://www.st.com/resource/en/programming_manual/DM00237416.pdf

.. _STM32F777 Reference Manual (RM0410):
   https://www.st.com/resource/en/reference_manual/DM00224583.pdf

.. _STM32CubeMX:
   https://www.st.com/en/development-tools/stm32cubemx.html
