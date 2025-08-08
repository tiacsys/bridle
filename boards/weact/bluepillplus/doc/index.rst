.. _weact_bluepillplus:

WeAct BluePill+
###############

The WeAct Blue Pill Plus board is available in different versions, each with
a specific microcontroller from different silicon vendors in standard package
size LQFP48. It is a clone of the original hobbyist Blue Pill board solderd
with either STM32F0_ or STM32F1_ microcontrollers. Partially, Zephyr upstream
boards also exist. See the :emphasis:`Links / References` column below.

+--------------+--------+-----------------------------------------+-------+-------+------+--------+--------------------------------------+
| Architecture | Vendor | MCU Series / Line / Type                | Clock | Flash | SRAM | Status | Links / References                   |
+==============+========+===========+============+================+=======+=======+======+========+======================================+
| |ACM4|       | |GD|_  | GD32F30x_ | GD32F303_  | |GD32F303CC|_  | 120㎒ | 256㎅ | 48㎅ ||notyet|| |BluePill-Plus|_                     |
+--------------+--------+-----------+------------+----------------+-------+-------+------+--------+                                      |
| |ACM3|       | |STM|_ | STM32F1_  | STM32F103_ | |STM32F103CB|_ | 72㎒  | 128㎅ | 20㎅ | |okay| | |STM32-base BluePill-Plus|_          |
|              |        |           |            +----------------+-------+-------+------+        |                                      |
|              |        |           |            | |STM32F103C8|_ | 72㎒  | 64㎅  | 20㎅ |        |                                      |
|              +--------+-----------+------------+----------------+-------+-------+------+--------+--------------------------------------+
|              | |GS|_  | APM32_    | APM32F103_ | |APM32F103CB|_ | 96㎒  | 128㎅ | 20㎅ ||notyet|| |BluePill-Plus-APM32|_               |
|              |        |           |            +----------------+-------+-------+------+        |                                      |
|              |        |           |            | |APM32F103C8|_ | 96㎒  | 64㎅  | 20㎅ |        |                                      |
|              +--------+-----------+------------+----------------+-------+-------+------+        +--------------------------------------+
|              | |GD|_  | GD32F10x_ | GD32F103_  | |GD32F103CB|_  | 108㎒ | 128㎅ | 20㎅ |        | |BluePill-Plus-GD32|_                |
|              |        |           |            +----------------+-------+-------+------+        |                                      |
|              |        |           |            | |GD32F103C8|_  | 108㎒ | 64㎅  | 20㎅ |        |                                      |
|              +--------+-----------+------------+----------------+-------+-------+------+        +--------------------------------------+
|              | |WCH|_ | CH32F_    | CH32F103_  | |CH32F103C8|_  | 72㎒  | 64㎅  | 20㎅ |        | |BluePill-Plus-CH32|_                |
|              |        |           |            +----------------+-------+-------+------+        |                                      |
|              |        |           |            | |CH32F103C6|_  | 72㎒  | 32㎅  | 10㎅ |        |                                      |
+--------------+        +-----------+------------+----------------+-------+-------+------+        |                                      |
| |RVQ3A|      |        | CH32V_    | CH32V103_  | |CH32V103C8|_  | 80㎒  | 64㎅  | 20㎅ |        |                                      |
|              |        |           |            +----------------+-------+-------+------+        |                                      |
|              |        |           |            | |CH32V103C6|_  | 80㎒  | 32㎅  | 10㎅ |        |                                      |
+--------------+        +-----------+------------+----------------+-------+-------+------+--------+                                      |
| |RVQ4B|      |        | CH32V_    | CH32V203_  | |CH32V203C8|_  | 144㎒ | 64㎅  | 20㎅ | |warn| | |zephyr:board:bluepillplus_ch32v203| |
|              |        |           |            +----------------+-------+-------+------+        |                                      |
|              |        |           |            | |CH32V203C6|_  | 144㎒ | 32㎅  | 10㎅ |        |                                      |
+--------------+--------+-----------+------------+----------------+-------+-------+------+--------+--------------------------------------+

:|okay|:

   .. admonition:: fully supported, no known issues
      :class: hint dropdown

      * |STM32F103CB|: ``weact_bluepillplus_stm32f103cb``
      * |STM32F103C8|: ``weact_bluepillplus_stm32f103c8``

:|warn|:

   .. admonition:: not yet completed, as full SoC driver support is missing:
      :class: warning dropdown

      * |CH32V203C8|: ``weact_bluepillplus_ch32v203c8``
      * |CH32V203C6|: ``weact_bluepillplus_ch32v203c6``

:|notyet|:

   .. admonition:: not yet supported, as SoC support is missing:
      :class: error dropdown

      * |GD32F303CC|: ``weact_bluepillplus_gd32f303cc``
      * |APM32F103CB|: ``weact_bluepillplus_apm32f103cb``
      * |APM32F103C8|: ``weact_bluepillplus_apm32f103c8``
      * |GD32F103CB|: ``weact_bluepillplus_gd32f103cb``
      * |GD32F103C8|: ``weact_bluepillplus_gd32f103c8``
      * |CH32F103C8|: ``weact_bluepillplus_ch32f103c8``
      * |CH32F103C6|: ``weact_bluepillplus_ch32f103c6``
      * |CH32V103C8|: ``weact_bluepillplus_ch32v103c8``
      * |CH32V103C6|: ``weact_bluepillplus_ch32v103c6``

Supported Boards
****************

Hardware
========

.. tabs::

   .. group-tab:: STM32F1

      .. _weact_bluepillplus-stm32f103cb:

      .. _weact_bluepillplus-stm32f103c8:

      .. include:: stm32f1/hardware.rsti

   .. group-tab:: CH32V2

      .. _weact_bluepillplus-ch32v203c8:

      .. _weact_bluepillplus-ch32v203c6:

      .. include:: ch32v2/hardware.rsti

Positions
=========

.. tabs::

   .. group-tab:: STM32F1

      .. include:: stm32f1/positions.rsti

   .. group-tab:: CH32V2

      .. include:: ch32v2/positions.rsti

Pinouts
=======

The peripherals of the different populated microcontrollers can be routed to
various pins on the boards edge connectors. The configuration of these routes
can be modified through :external+zephyr:ref:`DTS <devicetree>`. Please refer
to the datasheets to see the possible routings for each peripheral. The default
assignment is defined below in a single table.

.. tabs::

   .. group-tab:: STM32F1

      .. include:: pinouts.rsti

   .. group-tab:: CH32V2

      .. include:: pinouts.rsti

Supported Features
******************

The |bridle:board:weact_bluepillplus| board configuration supports
the following Zephyr hardware features:

.. tabs::

   .. group-tab:: STM32F1

      .. include:: stm32f1/features.rsti

   .. group-tab:: CH32V2

      .. include:: ch32v2/features.rsti

Board Configurations
====================

The |bridle:board:weact_bluepillplus| boards can be configured
for the following different use cases.

.. tabs::

   .. group-tab:: STM32F1

      .. include:: stm32f1/configurations.rsti


   .. group-tab:: CH32V2

      .. include:: ch32v2/configurations.rsti

System and Real-Time Clock
--------------------------

The STM32 system clock (SYSCLK) on the |bridle:board:weact_bluepillplus| boards
can be driven by an internal or external oscillator, as well as the main PLL
clock. By default the system clock is provided by the PLL clock with 72㎒ on
STM32F1 or up to 144㎒ on the other counterfeited chips, which is driven by
the external (on-board) 25㎒ crystal connected to the high-speed clock input.

The STM32 real-time clock (RTC) on the |bridle:board:weact_bluepillplus| boards
can be driven by an internal or external oscillator. By default, the real-time
clock will be driven by the external (on-board) 32.768㎑ crystal connected to
the low-speed clock input.

User LED
--------

The |bridle:board:weact_bluepillplus| boards feature one LED for user purposes
at GPIO port B line 2 (PB2) in parallel to the BOOT1 signal.
The LED is high active.

User Button
-----------

The |bridle:board:weact_bluepillplus| boards feature one tactile push button
for user purposes at GPIO port A line 0 (PA0) in parallel to the WKUP signal
and the first ADC channel. The push button is high active.

ADC/TS Ports
------------

The |bridle:board:weact_bluepillplus| boards features an 12-bit ADC with
10 external usable channels and, when supported, some additional channels
connected internaly to the on-chip temperature sensor (TS), the internal
provided voltage reference source (VREF) and the external battery voltage
(VBAT) when supported. The ADC channels 0-9 are available on the edge
connectors.

Serial Port
-----------

The |bridle:board:weact_bluepillplus| boards feature one two wire UART (RxD/TxD)
at USART1 and the standard pins (PA9/PA10) to be compatible with the STMicro
on-chip bootloader for firmware downloads over UART. The Zephyr console output
is assigned to this USART with the default settings of 115200/8N1 without any
flow control (no XON/XOFF, no RTS/CTS).

Programming and Debugging
*************************

Applications for the |bridle:board:weact_bluepillplus| board configuration
can be built and flashed in the usual Zephyr way (see
:external+zephyr:ref:`build_an_application` and
:external+zephyr:ref:`application_run` for more details).

Flashing
========

The |bridle:board:weact_bluepillplus| board needs an debug tool adapter, e.g.
ST-LINK/V2, SEGGER JLink, Arm CMSIS-DAP or similar.

Flashing an application
-----------------------

Here is an example for the :external+zephyr:zephyr:code-sample:`hello_world`
application.

Run a serial host program to connect with your
|bridle:board:weact_bluepillplus| board:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         :bgn:`user@host:~$` **screen /dev/ttyUSBx 115200,cs8,parenb,-parodd,-cstopb,-crtscts**

Build and flash the application:

   .. zephyr-app-commands::
      :app: zephyr/samples/hello_world
      :board: weact_bluepillplus_stm32f103c8
      :build-dir: weact_bluepillplus
      :west-args: -p
      :flash-args: -r openocd
      :goals: flash
      :host-os: unix
      :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         Hello World! weact_bluepillplus_stm32f103c8

Debugging
=========

The SWD interface can also be used to debug the board. To achieve this, you can
either use SEGGER JLink, OpenOCD or PyOCD.

You can debug an application in the usual way. Here is an example for the
:external+zephyr:zephyr:code-sample:`hello_world` application:

   .. zephyr-app-commands::
      :app: zephyr/samples/hello_world
      :board: weact_bluepillplus_stm32f103c8
      :build-dir: weact_bluepillplus
      :maybe-skip-config:
      :west-args: -p
      :debug-args: -r openocd
      :goals: debug
      :host-os: unix

Tests and Examples
******************

Hello Shell
===========

.. tabs::

   .. group-tab:: STM32F1

      .. tabs::

         .. group-tab:: |STM32F103CB|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: weact_bluepillplus_stm32f103cb
               :build-dir: weact_bluepillplus
               :gen-args: \
                  -DEXTRA_CONF_FILE="prj-hwstartup.conf" -DCONFIG_STM32_ENABLE_DEBUG_SLEEP_STOP=y
               :west-args: -p
               :flash-args: -r openocd
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [178/178] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       53668 B       128 KB     40.95%
                                  RAM:       17984 B        20 KB     87.81%
                             IDT_LIST:          0 GB        32 KB      0.00%

         .. group-tab:: |STM32F103C8|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: weact_bluepillplus_stm32f103c8
               :build-dir: weact_bluepillplus
               :gen-args: \
                  -DEXTRA_CONF_FILE="prj-hwstartup.conf" -DCONFIG_STM32_ENABLE_DEBUG_SLEEP_STOP=y
               :west-args: -p
               :flash-args: -r openocd
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [178/178] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       53668 B        64 KB     81.89%
                                  RAM:       17984 B        20 KB     87.81%
                             IDT_LIST:          0 GB        32 KB      0.00%

   .. group-tab:: CH32V2

      .. tabs::

         .. group-tab:: |CH32V203C8|

            |WCH-Tools|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: weact_bluepillplus_ch32v203c8
               :build-dir: weact_bluepillplus
               :gen-args: \
                  -DEXTRA_CONF_FILE="prj-hwstartup.conf" -DCONFIG_FLASH=n -DCONFIG_FLASH_SHELL=n
               :west-args: -p
               :flash-args: -r minichlink
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [149/149] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                  ROM:       46200 B        64 KB     70.50%
                                  RAM:        9388 B        20 KB     45.84%
                             IDT_LIST:          0 GB         4 KB      0.00%

         .. group-tab:: |CH32V203C6|

            |WCH-Tools|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: weact_bluepillplus_ch32v203c6
               :build-dir: weact_bluepillplus
               :gen-args: -DEXTRA_CONF_FILE="prj-minimal.conf"
               :west-args: -p
               :flash-args: -r minichlink
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [127/127] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                  ROM:       25076 B        32 KB     76.53%
                                  RAM:        8456 B        10 KB     82.58%
                             IDT_LIST:          0 GB         4 KB      0.00%

References
**********

.. target-notes::
