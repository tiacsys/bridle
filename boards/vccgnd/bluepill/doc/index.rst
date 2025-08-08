.. _vccgnd_bluepill:

VccGND BluePill
###############

The VccGND Blue Pill board is available in different versions, each with
a specific microcontroller from different silicon vendors in standard package
size LQFP48. It is a clone of the original hobbyist Blue Pill board solderd
with either STM32F0_ or STM32F1_ microcontrollers. Partially, Zephyr upstream
boards also exist. See the :emphasis:`Links / References` column below.

+--------------+--------+-----------------------------------------+-------+-------+------+--------+------------------------------+
| Architecture | Vendor | MCU Series / Line / Type                | Clock | Flash | SRAM | Status | Links / References           |
+==============+========+===========+============+================+=======+=======+======+========+==============================+
| |ACM3|       | |STM|_ | STM32F1_  | STM32F103_ | |STM32F103CB|_ | 72㎒  | 128㎅ | 20㎅ | |okay| | |BluePill-F1|_               |
|              |        |           |            +----------------+-------+-------+------+        |                              |
|              |        |           |            | |STM32F103C8|_ | 72㎒  | 64㎅  | 20㎅ | |nbsp| | |STM32-base BluePill-F1|_    |
|              |        |           |            |                |       |       |      |        |                              |
|              |        |           |            |                |       |       |      | |!|    | |zephyr:board:stm32_min_dev| |
+--------------+        +-----------+------------+----------------+-------+-------+------+--------+------------------------------+
| |ACM0|       |        | STM32F0_  | STM32F0x2_ | |STM32F072CB|_ | 48㎒  | 128㎅ | 16㎅ | |warn| | |BluePill-F0|_               |
|              |        |           |            +----------------+-------+-------+------+        |                              |
|              |        |           |            | |STM32F072C8|_ | 48㎒  | 64㎅  | 16㎅ |        | |STM32-base BluePill-F0|_    |
|              |        |           +------------+----------------+-------+-------+------+        |                              |
|              |        |           | STM32F0x1_ | |STM32F051C8|_ | 48㎒  | 64㎅  | 8㎅  |        |                              |
|              |        |           +------------+----------------+-------+-------+------+--------+                              |
|              |        |           | STM32F0x0_ | |STM32F030C8|_ | 48㎒  | 64㎅  | 8㎅  | |okay| |                              |
+--------------+--------+-----------+------------+----------------+-------+-------+------+--------+------------------------------+

:|okay|:

   .. admonition:: fully supported, no known issues
      :class: hint dropdown

      * |STM32F103CB|: ``vccgnd_bluepill_stm32f103cb``
      * |STM32F103C8|: ``vccgnd_bluepill_stm32f103c8``

:|warn|:

   .. admonition:: not yet completed, as the necessary hardware for development and testing is missing:
      :class: warning dropdown

      * |STM32F072CB|: ``vccgnd_bluepill_stm32f072cb``
      * |STM32F072C8|: ``vccgnd_bluepill_stm32f072c8``
      * |STM32F051C8|: ``vccgnd_bluepill_stm32f051c8``
      * |STM32F030C8|: ``vccgnd_bluepill_stm32f030c8``

:|!|:

   .. admonition:: Fakes and counterfeit microchips
      :class: error dropdown

      .. include:: /includes/counterfeited_stm32.txt

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         |counterfeit|

         :bgn:`-- west flash: rebuilding`
         :bgn:`-- west flash: using runner pyocd`
         :bgn:`-- runners.pyocd: Flashing file: build/vccgnd_bluepill/zephyr/zephyr.hex`
         :bl:`0001860` :brd:`E` :brd:`Not a genuine ST Device! Abort connection.` :rd:`[functions]`
         :bl:`0001905` :bbl:`I` Loading build/vccgnd_bluepill/zephyr/zephyr.hex at 0x08000000 [load_cmd]
         [==================================================] 100%
         :bl:`0004398` :bbl:`I` Erased 32768 bytes (32 sectors), programmed 32768 bytes (32 pages), skipped 0 bytes (0 pages) at 12.96 kB/s [loader]

Supported Boards
****************

Hardware
========

.. tabs::

   .. group-tab:: STM32F1

      .. _vccgnd_bluepill-stm32f103cb:

      .. _vccgnd_bluepill-stm32f103c8:

      .. include:: stm32f1/hardware.rsti

   .. group-tab:: STM32F0

      .. _vccgnd_bluepill-stm32f072cb:

      .. _vccgnd_bluepill-stm32f072c8:

      .. _vccgnd_bluepill-stm32f051c8:

      .. _vccgnd_bluepill-stm32f030c8:

      .. include:: stm32f0/hardware.rsti


Positions
=========

.. tabs::

   .. group-tab:: STM32F1

      .. include:: stm32f1/positions.rsti

   .. group-tab:: STM32F0

      .. include:: stm32f0/positions.rsti

Pinouts
=======

The peripherals of the different populated microcontrollers can be routed to
various pins on the boards edge connectors. The configuration of these routes
can be modified through :external+zephyr:ref:`DTS <devicetree>`. Please refer
to the datasheets to see the possible routings for each peripheral. The default
assignment is defined below in a single table.

.. tabs::

   .. group-tab:: STM32F1

      .. include:: stm32f1/pinouts.rsti

   .. group-tab:: STM32F0

      .. include:: stm32f0/pinouts.rsti

Supported Features
******************

The |bridle:board:vccgnd_bluepill| board configuration supports
the following Zephyr hardware features:

.. tabs::

   .. group-tab:: STM32F1

      .. include:: stm32f1/features.rsti

   .. group-tab:: STM32F0

      .. include:: stm32f0/features.rsti

Board Configurations
====================

The |bridle:board:vccgnd_bluepill| boards can be configured
for the following different use cases.

.. tabs::

   .. group-tab:: STM32F1

      .. include:: stm32f1/configurations.rsti


   .. group-tab:: STM32F0

      .. include:: stm32f0/configurations.rsti

System and Real-Time Clock
--------------------------

The STM32 system clock (SYSCLK) on the |bridle:board:vccgnd_bluepill| boards
can be driven by an internal or external oscillator, as well as the main PLL
clock. By default the system clock is provided by the PLL clock with 72㎒ on
STM32F1 or 48㎒ on STM32F0, which is driven by the external (on-board) 25㎒
crystal connected to the high-speed clock input.

The STM32 real-time clock (RTC) on the |bridle:board:vccgnd_bluepill| boards
can be driven by an internal or external oscillator. By default, the real-time
clock will be driven by the external (on-board) 32.768㎑ crystal connected to
the low-speed clock input.

User LED
--------

The |bridle:board:vccgnd_bluepill| boards feature one LED for user purposes
at GPIO port C line 13 (PC13).
The LED is low active.

ADC/TS Ports
------------

The |bridle:board:vccgnd_bluepill| boards features an 12-bit ADC with
10 external usable channels and, when supported, some additional channels
connected internaly to the on-chip temperature sensor (TS), the internal
provided voltage reference source (VREF) and the external battery voltage
(VBAT) when supported. The ADC channels 0-9 are available on the edge
connectors.

SPI Port
--------

The |bridle:board:vccgnd_bluepill| boards features one five wire SPI bus over
SPI2 also available on the edge connectors and the standard pins. SPI1 is not
available in any default setup.

I2C Port
--------

The |bridle:board:vccgnd_bluepill| boards features two I2C buses over at I2C1
and I2C2 also available on the edge connectors and the standard pins. I2C1 is
the BluePill standard bus.

CAN Port
--------

The |bridle:board:vccgnd_bluepill| boards with STM32F1 and STM32F072 features
one CAN controller, but without any CAN transceiver on board. The bus timing
is defined by the DTS and is preset to 1000 kBit/s. The calculation was
verified with the help of the `CAN Bit Time Calculation Sheet`_ and can also
assume smaller bit rates according to the following table. Note that the value
of **Prescaler**, **Seg 1** and **Seg 2** will be calculated on demand by the
Zephyr :external+zephyr:ref:`can_api` API together with the driver.

.. tabs::

   .. group-tab:: STM32F1

      .. list-table:: CAN bus timing calculation for STM32F1 @ 36㎒
         :class: longtable
         :align: center
         :widths: 10, 10, 10, 35, 35
         :header-rows: 1
         :stub-columns: 2

         * - Bit Rate
           - Sample Point at
           - Prescaler
           - Seg 1 (``prop-seg + phase-seg1``)
           - Seg 2 (``phase-seg2``)
         * - 1000 kBit/s
           - 88.9 %
           - 2
           - 15
           - 2
         * - 800 kBit/s
           - 88.9 %
           - 5
           - 7
           - 1
         * - 500 kBit/s
           - 88.9 %
           - 4
           - 15
           - 2
         * - 250 kBit/s
           - 88.9 %
           - 8
           - 15
           - 2
         * - 125 kBit/s
           - 88.9 %
           - 16
           - 15
           - 2
         * - 100 kBit/s
           - 88.9 %
           - 20
           - 15
           - 2
         * - 50 kBit/s
           - 88.9 %
           - 40
           - 15
           - 2
         * - 20 kBit/s
           - 88.9 %
           - 100
           - 15
           - 2
         * - 10 kBit/s
           - 88.9 %
           - 200
           - 15
           - 2

   .. group-tab:: STM32F0

      .. list-table:: CAN bus timing calculation for STM32F0 @ 48㎒
         :class: longtable
         :align: center
         :widths: 10, 10, 10, 35, 35
         :header-rows: 1
         :stub-columns: 2

         * - Bit Rate
           - Sample Point at
           - Prescaler
           - Seg 1 (``prop-seg + phase-seg1``)
           - Seg 2 (``phase-seg2``)
         * - 1000 kBit/s
           - 87.5 %
           - 3
           - 13
           - 2
         * - 800 kBit/s
           - 86.7 %
           - 4
           - 12
           - 2
         * - 500 kBit/s
           - 87.5 %
           - 6
           - 13
           - 2
         * - 250 kBit/s
           - 87.5 %
           - 12
           - 13
           - 2
         * - 125 kBit/s
           - 87.5 %
           - 24
           - 13
           - 2
         * - 100 kBit/s
           - 87.5 %
           - 30
           - 13
           - 2
         * - 50 kBit/s
           - 87.5 %
           - 60
           - 13
           - 2
         * - 20 kBit/s
           - 87.5 %
           - 150
           - 13
           - 2
         * - 10 kBit/s
           - 87.5 %
           - 300
           - 13
           - 2

Serial Port
-----------

The |bridle:board:vccgnd_bluepill| boards feature one two wire UART (RxD/TxD)
at USART1 and the standard pins (PA9/PA10) to be compatible with the STMicro
on-chip bootloader for firmware downloads over UART. The Zephyr console output
is assigned to this USART with the default settings of 115200/8N1 without any
flow control (no XON/XOFF, no RTS/CTS).

USB Device Port
---------------

The |bridle:board:vccgnd_bluepill| boards with STM32F1 and STM32F072 features
one (native) USB full-speed device port that can be used to communicate with
a host PC. See the
:external+zephyr:zephyr:code-sample-category:`usb`
sample applications for more, such as the
:external+zephyr:zephyr:code-sample:`usb-cdc-acm`
sample which sets up a virtual serial port that echos characters back to the
host PC. This boards provide the Zephyr console per default on the USB port
as :external+zephyr:ref:`usb_device_cdc_acm`:

.. tabs::

   .. group-tab:: STM32F1

      .. container:: highlight-console notranslate literal-block

         .. parsed-literal::

            USB device idVendor=\ |vccgnd_bluepill_STM32F1_VID|, idProduct=\ |vccgnd_bluepill_STM32F1_PID_CON|, bcdDevice=\ |vccgnd_bluepill_STM32F1_BCD_CON|
            USB device strings: Mfr=1, Product=2, SerialNumber=3
            Product: |vccgnd_bluepill_STM32F1_PStr_CON|
            Manufacturer: |vccgnd_bluepill_STM32F1_VStr|
            SerialNumber: 93F49F68D18508F0

   .. group-tab:: STM32F0

      .. container:: highlight-console notranslate literal-block

         .. parsed-literal::

            USB device idVendor=\ |vccgnd_bluepill_STM32F0_VID|, idProduct=\ |vccgnd_bluepill_STM32F0_PID_CON|, bcdDevice=\ |vccgnd_bluepill_STM32F0_BCD_CON|
            USB device strings: Mfr=1, Product=2, SerialNumber=3
            Product: |vccgnd_bluepill_STM32F0_PStr_CON|
            Manufacturer: |vccgnd_bluepill_STM32F0_VStr|
            SerialNumber: 8255970716DB9402

Programming and Debugging
*************************

Applications for the |bridle:board:vccgnd_bluepill| board configuration
can be built and flashed in the usual Zephyr way (see
:external+zephyr:ref:`build_an_application` and
:external+zephyr:ref:`application_run` for more details).

Flashing
========

The |bridle:board:vccgnd_bluepill| board needs an debug tool adapter, e.g.
ST-LINK/V2, SEGGER JLink, Arm CMSIS-DAP or similar.

Flashing an application
-----------------------

Here is an example for the :external+zephyr:zephyr:code-sample:`hello_world`
application.

Run a serial host program to connect with your
|bridle:board:vccgnd_bluepill| board:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         :bgn:`user@host:~$` **screen /dev/ttyUSBx 115200,cs8,parenb,-parodd,-cstopb,-crtscts**

Build and flash the application:

   .. zephyr-app-commands::
      :app: zephyr/samples/hello_world
      :board: vccgnd_bluepill_stm32f103c8
      :build-dir: vccgnd_bluepill
      :west-args: -p
      :flash-args: -r pyocd
      :goals: flash
      :host-os: unix
      :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         Hello World! vccgnd_bluepill_stm32f103c8

Debugging
=========

The SWD interface can also be used to debug the board. To achieve this, you can
either use SEGGER JLink, OpenOCD or PyOCD.

You can debug an application in the usual way. Here is an example for the
:external+zephyr:zephyr:code-sample:`hello_world` application:

   .. zephyr-app-commands::
      :app: zephyr/samples/hello_world
      :board: vccgnd_bluepill_stm32f103c8
      :build-dir: vccgnd_bluepill
      :maybe-skip-config:
      :west-args: -p
      :debug-args: -r pyocd
      :goals: debug
      :host-os: unix

Tests and Examples
******************

LED Blinky with USB-CDC/ACM Console
===================================

.. tabs::

   .. group-tab:: STM32F1

      .. tabs::

         .. group-tab:: |STM32F103CB|

            .. zephyr-app-commands::
               :app: zephyr/samples/basic/blinky
               :board: vccgnd_bluepill_stm32f103cb
               :build-dir: vccgnd_bluepill
               :west-args: -p -S usb-console
               :flash-args: -r pyocd
               :goals: flash
               :compact:

         .. group-tab:: |STM32F103C8|

            .. zephyr-app-commands::
               :app: zephyr/samples/basic/blinky
               :board: vccgnd_bluepill_stm32f103c8
               :build-dir: vccgnd_bluepill
               :west-args: -p -S usb-console
               :flash-args: -r pyocd
               :goals: flash
               :compact:

   .. group-tab:: STM32F0

      .. tabs::

         .. group-tab:: |STM32F072CB|

            .. zephyr-app-commands::
               :app: zephyr/samples/basic/blinky
               :board: vccgnd_bluepill_stm32f072cb
               :build-dir: vccgnd_bluepill
               :west-args: -p -S usb-console
               :flash-args: -r pyocd
               :goals: flash
               :compact:

         .. group-tab:: |STM32F072C8|

            .. zephyr-app-commands::
               :app: zephyr/samples/basic/blinky
               :board: vccgnd_bluepill_stm32f072c8
               :build-dir: vccgnd_bluepill
               :west-args: -p -S usb-console
               :flash-args: -r pyocd
               :goals: flash
               :compact:

Hello Shell
===========

.. tabs::

   .. group-tab:: STM32F1

      .. tabs::

         .. group-tab:: |STM32F103CB|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: vccgnd_bluepill_stm32f103cb
               :build-dir: vccgnd_bluepill
               :gen-args: \
                  -DEXTRA_CONF_FILE="prj-hwstartup.conf" -DCONFIG_STM32_ENABLE_DEBUG_SLEEP_STOP=y
               :west-args: -p
               :flash-args: -r pyocd
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [181/181] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       56148 B       128 KB     42.84%
                                  RAM:       18184 B        20 KB     88.79%
                             IDT_LIST:          0 GB        32 KB      0.00%

         .. group-tab:: |STM32F103C8|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: vccgnd_bluepill_stm32f103c8
               :build-dir: vccgnd_bluepill
               :gen-args: \
                  -DEXTRA_CONF_FILE="prj-hwstartup.conf" -DCONFIG_STM32_ENABLE_DEBUG_SLEEP_STOP=y
               :west-args: -p
               :flash-args: -r pyocd
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [181/181] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       56148 B        64 KB     85.68%
                                  RAM:       18184 B        20 KB     88.79%
                             IDT_LIST:          0 GB        32 KB      0.00%

   .. group-tab:: STM32F0

      .. tabs::

         .. group-tab:: |STM32F072CB|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: vccgnd_bluepill_stm32f072cb
               :build-dir: vccgnd_bluepill
               :gen-args: \
                  -DEXTRA_CONF_FILE="prj-minimal.conf" -DCONFIG_STM32_ENABLE_DEBUG_SLEEP_STOP=y \
                  -DCONFIG_ADC=y -DCONFIG_ADC_SHELL=y -DCONFIG_I2C=y -DCONFIG_I2C_SHELL=y
               :west-args: -p
               :flash-args: -r pyocd
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [159/159] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       37640 B       128 KB     28.72%
                                  RAM:        8912 B        16 KB     54.39%
                             IDT_LIST:          0 GB        32 KB      0.00%

         .. group-tab:: |STM32F072C8|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: vccgnd_bluepill_stm32f072c8
               :build-dir: vccgnd_bluepill
               :gen-args: \
                  -DEXTRA_CONF_FILE="prj-minimal.conf" -DCONFIG_STM32_ENABLE_DEBUG_SLEEP_STOP=y \
                  -DCONFIG_ADC=y -DCONFIG_ADC_SHELL=y -DCONFIG_I2C=y -DCONFIG_I2C_SHELL=y
               :west-args: -p
               :flash-args: -r pyocd
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [159/159] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       37640 B        64 KB     57.43%
                                  RAM:        8912 B        16 KB     54.39%
                             IDT_LIST:          0 GB        32 KB      0.00%

         .. group-tab:: |STM32F051C8|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: vccgnd_bluepill_stm32f051c8
               :build-dir: vccgnd_bluepill
               :gen-args: \
                  -DEXTRA_CONF_FILE="prj-tiny.conf" -DCONFIG_STM32_ENABLE_DEBUG_SLEEP_STOP=y \
                  -DCONFIG_ADC=y -DCONFIG_ADC_SHELL=y -DCONFIG_I2C=y -DCONFIG_I2C_SHELL=y
               :west-args: -p
               :flash-args: -r pyocd
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [159/159] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       34008 B        64 KB     51.89%
                                  RAM:        8112 B         8 KB     99.02%
                             IDT_LIST:          0 GB        32 KB      0.00%

         .. group-tab:: |STM32F030C8|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: vccgnd_bluepill_stm32f030c8
               :build-dir: vccgnd_bluepill
               :gen-args: \
                  -DEXTRA_CONF_FILE="prj-tiny.conf" -DCONFIG_STM32_ENABLE_DEBUG_SLEEP_STOP=y \
                  -DCONFIG_ADC=y -DCONFIG_ADC_SHELL=y -DCONFIG_I2C=y -DCONFIG_I2C_SHELL=y
               :west-args: -p
               :flash-args: -r pyocd
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [159/159] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       33776 B        64 KB     51.54%
                                  RAM:        8104 B         8 KB     98.93%
                             IDT_LIST:          0 GB        32 KB      0.00%

References
**********

.. target-notes::
