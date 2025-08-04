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

Serial Port
-----------

The |bridle:board:vccgnd_bluepill| boards feature one two wire UART (RxD/TxD)
at USART1 and the standard pins (PA9/PA10) to be compatible with the STMicro
on-chip bootloader for firmware downloads over UART. The Zephyr console output
is assigned to this USART with the default settings of 115200/8N1 without any
flow control (no XON/XOFF, no RTS/CTS).

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

                     [177/177] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       48372 B       128 KB     36.90%
                                  RAM:       17728 B        20 KB     86.56%
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

                     [177/177] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       48372 B        64 KB     73.81%
                                  RAM:       17728 B        20 KB     86.56%
                             IDT_LIST:          0 GB        32 KB      0.00%

   .. group-tab:: STM32F0

      .. tabs::

         .. group-tab:: |STM32F072CB|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: vccgnd_bluepill_stm32f072cb
               :build-dir: vccgnd_bluepill
               :gen-args: \
                  -DEXTRA_CONF_FILE="prj-minimal.conf" -DCONFIG_STM32_ENABLE_DEBUG_SLEEP_STOP=y
               :west-args: -p
               :flash-args: -r pyocd
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [149/149] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       24856 B       128 KB     18.96%
                                  RAM:        8472 B        16 KB     51.71%
                             IDT_LIST:          0 GB        32 KB      0.00%

         .. group-tab:: |STM32F072C8|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: vccgnd_bluepill_stm32f072c8
               :build-dir: vccgnd_bluepill
               :gen-args: \
                  -DEXTRA_CONF_FILE="prj-minimal.conf" -DCONFIG_STM32_ENABLE_DEBUG_SLEEP_STOP=y
               :west-args: -p
               :flash-args: -r pyocd
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [149/149] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       24856 B        64 KB     37.93%
                                  RAM:        8472 B        16 KB     51.71%
                             IDT_LIST:          0 GB        32 KB      0.00%

         .. group-tab:: |STM32F051C8|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: vccgnd_bluepill_stm32f051c8
               :build-dir: vccgnd_bluepill
               :gen-args: \
                  -DEXTRA_CONF_FILE="prj-tiny.conf" -DCONFIG_STM32_ENABLE_DEBUG_SLEEP_STOP=y
               :west-args: -p
               :flash-args: -r pyocd
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [149/149] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       22684 B        64 KB     34.61%
                                  RAM:        7672 B         8 KB     93.65%
                             IDT_LIST:          0 GB        32 KB      0.00%

         .. group-tab:: |STM32F030C8|

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :board: vccgnd_bluepill_stm32f030c8
               :build-dir: vccgnd_bluepill
               :gen-args: \
                  -DEXTRA_CONF_FILE="prj-tiny.conf" -DCONFIG_STM32_ENABLE_DEBUG_SLEEP_STOP=y
               :west-args: -p
               :flash-args: -r pyocd
               :goals: flash
               :compact:

            .. admonition:: memory consumption
               :class: hint dropdown

               .. container:: highlight highlight-console notranslate

                  .. parsed-literal::

                     [149/149] Linking C executable zephyr/zephyr.elf
                     Memory region         Used Size  Region Size  %age Used
                                FLASH:       22456 B        64 KB     34.27%
                                  RAM:        7664 B         8 KB     93.55%
                             IDT_LIST:          0 GB        32 KB      0.00%

References
**********

.. target-notes::
