.. _coffeecaller_nrf52_board:

TiaC CoffeeCaller nRF52
#######################

Overview
********

The TiaC CoffeeCaller nRF52 board is based on the **aQFN73** package of the
**nRF52840** chip. See the `nRF52840 Product Overview <nRF52840_>`_ for a
short description of the key features of the chip or the more detailed
`nRF52840 Product Specification`_ for all technical details.

Hardware
========

The board is **powered by 5V via the USB-C connector** and has a **3.3V/200㎃
LDO** as needed by the chip and other peripherals on the board. It features
**5 user buttons**, **4 GPIO LEDs**, **WS2812 RGB Strip with 4 LEDs**,
**4 servo PIN headers**, **SHT40 temperature and humidity sensor**, **qwIIC
Connector** and a **PWM buzzer**. Schematics and KiCad design files can be
found in the `TiaC CoffeeCaller nRF52 website`_.

.. list-table::
   :align: center
   :width: 100%
   :widths: 66, 33

   * - .. rubric:: Features and Resources
     - .. rubric:: Printed Circuit Board

   * - :hwftlbl-vdd:`5V/150㎃`
       :hwftlbl-vdd:`3.3V/200㎃`

       :hwftlbl:`64㎒`
       :hwftlbl:`1㎆`
       :hwftlbl:`256㎅`
       :hwftlbl-con:`USB-C`
       :hwftlbl-dbg:`UF2`
       :hwftlbl-dbg:`SWD`

       :hwftlbl-btn:`RST`
       :hwftlbl-btn:`BOOT`
       :hwftlbl-btn:`USER`
       :hwftlbl-led:`WHITE`
       :hwftlbl-led:`RGB`
       :hwftlbl-spk:`PASSIVE`
       :hwftlbl-act:`Servo Motor`

       :hwftlbl-mtr:`TH` :
       :hwftlbl-tmp:`T`
       :hwftlbl-hty:`H`

       :hwftlbl-pio:`17`
       :hwftlbl-pwm:`5`
       :hwftlbl-i2c:`2`
       :hwftlbl-uart:`1`

       .. rst-class:: rst-columns

       - Single core Arm Cortex-M4 processor running up to 64㎒
       - :bbk:`256㎅` on-chip SRAM
       - :bbk:`1㎆` on-chip flash with XIP capabilities
       - USB 1.1 controller (device)
       - On-board :bbk:`USB-C micro connector`
       - On-board :bbl:`3.3V LDO regulator with 200㎃`
       - On-board :bbk:`RESET` button
       - On-board :bbl:`BOOT` button
       - On-board :bbl:`4 User button`
       - On-board :bbl:`4 User LEDs`
       - On-board :bbl:`4 User RGB LED`
       - On-board :bbl:`1 User PWM Buzzer`
       - On-board :bbl:`4 User PWM Servo Motor` connectors
       - :bbl:`8 GPIO` pins via :bbk:`Free pin header`
       - :bbk:`1 UART` peripherals
       - :bbk:`1 I2C` controllers
       - :bbl:`5 PWM` channels
       - :bbl:`TH`: temperature and humidity (`SHT40 <SHT4x_>`_)
       - 1 Watchdog timer peripheral

       .. rubric:: Design Data
       .. rst-class:: rst-columns

       - `TiaC CoffeeCaller nRF52 website`_
       - `TiaC CoffeeCaller nRF52 Schematic (v1.0.1)`_
       - `TiaC CoffeeCaller nRF52 UF2 bootloader`_

     - .. image:: img/coffeecaller.jpg
          :alt: TiaC CoffeeCaller nRF52
          :align: center

Positions
=========

.. todo:: Export more design notes from KiCad and show here.

Pinouts
=======

.. todo:: Create a pinout for the *free pin header*, maybe with KiCad.

Supported Features
******************

The |bridle:board:coffeecaller_nrf52| board configuration supports
the following Zephyr hardware features:

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
     - :dtcompatible:`nordic,nrf-pinctrl`
     - :external+zephyr:ref:`pinctrl_api`
   * - GPIO
     - :kconfig:option:`CONFIG_GPIO`
     - | :dtcompatible:`nordic,nrf-gpio`
       | :dtcompatible:`nordic,nrf-gpiote`
     - :external+zephyr:ref:`gpio_api`
   * - UART
     - :kconfig:option:`CONFIG_SERIAL`
     - :dtcompatible:`nordic,nrf-uarte`
     - :external+zephyr:ref:`uart_api`
   * - UDC (USB Device Controller)
     - :kconfig:option:`CONFIG_USB_DEVICE_STACK`
     - :dtcompatible:`nordic,nrf-usbd`
     - :external+zephyr:ref:`usb_api`
   * - RADIO (L1: GFSK / O-QPSK, L2: IEEE 802.15.4)
     - :kconfig:option:`CONFIG_NET_L2_IEEE802154`
     - | :dtcompatible:`nordic,nrf-radio`
       | :dtcompatible:`nordic,nrf-ieee802154`
     - :external+zephyr:ref:`ieee802154_interface`
   * - I2C
     - :kconfig:option:`CONFIG_I2C`
     - :dtcompatible:`nordic,nrf-twi`
     - :external+zephyr:ref:`i2c_api`
   * - WS2812 (GPIO)
     - :kconfig:option:`CONFIG_LED_STRIP`
     - :dtcompatible:`worldsemi,ws2812-gpio`
     - N/A
   * - PWM
     - :kconfig:option:`CONFIG_PWM`
     - :dtcompatible:`nordic,nrf-pwm`
     - :external+zephyr:ref:`pwm_api`
   * - Watchdog Timer (WDT)
     - :kconfig:option:`CONFIG_WATCHDOG`
     - :dtcompatible:`nordic,nrf-wdt`
     - :external+zephyr:ref:`watchdog_api`
   * - Flash
     - :kconfig:option:`CONFIG_FLASH`
     - :dtcompatible:`nordic,nrf52-flash-controller`
     - :external+zephyr:ref:`flash_api` and
       :external+zephyr:ref:`flash_map_api`
   * - HWINFO
     - :kconfig:option:`CONFIG_HWINFO`
     - N/A
     - :external+zephyr:ref:`hwinfo_api`
   * - CLOCK
     - :kconfig:option:`CONFIG_CLOCK_CONTROL`
     - | :dtcompatible:`nordic,nrf-clock`
       | :dtcompatible:`nordic,nrf52-hfxo`
     - :external+zephyr:ref:`clock_control_api`
   * - NVIC
     - N/A
     - :dtcompatible:`arm,v7m-nvic`
     - Nested Vector :external+zephyr:ref:`interrupts_v2` Controller
   * - SYSTICK
     - N/A
     - :dtcompatible:`arm,armv7m-systick`
     -

Other hardware features are not currently supported by Zephyr. The default
configuration can be found in the different Kconfig files:

   - :bridle_file:`boards/tiac/coffeecaller/coffeecaller_nrf52_nrf52840_defconfig`

Board Configurations
====================

The |bridle:board:coffeecaller_nrf52| board can be configured
for the following different use cases.

.. rubric:: :command:`west build -b coffeecaller_nrf52`

Use the native USB device port with CDC-ACM as Zephyr console and for the shell.

User LED
--------

The |bridle:board:coffeecaller_nrf52| board feature four white LEDs for user
purposes at GPIO port 1. The LEDs are all low active.

* LD1 (white) @ :strong:`P1.06`
  |CRT| :dts:`aliases { led0 = &ld1; };`
* LD2 (white) @ :strong:`P1.07`
  |CRT| :dts:`aliases { led1 = &ld2; };`
* LD3 (white) @ :strong:`P1.02`
  |CRT| :dts:`aliases { led2 = &ld3; };`
* LD4 (white) @ :strong:`P1.04`
  |CRT| :dts:`aliases { led3 = &ld4; };`

User RGB LED
------------

The |bridle:board:coffeecaller_nrf52| board feature four RGB LEDs for user
purposes in strip (serial) interconnection at GPIO port 0 line 26.

* WS2812 Strip @ :strong:`P0.26`
  |CRT| :dts:`aliases { led-strip = &led_strip; };`

User Button
-----------

The |bridle:board:coffeecaller_nrf52| board feature one tactile push button
for boot select purpose at GPIO port 0 line 4 and four further push buttons
for user purposes at GPIO port 0 and 1. The push button are all low active.

* BUTTON0 (big) @ :strong:`P0.04`
  |CRT| :dts:`aliases { sw0 = &button0; mcuboot-button0 = &button0; };`
* BUTTON1 (small) @ :strong:`P0.31`
  |CRT| :dts:`aliases { sw1 = &button1; };`
* BUTTON2 (small) @ :strong:`P0.29`
  |CRT| :dts:`aliases { sw2 = &button2; };`
* BUTTON3 (small) @ :strong:`P0.03`
  |CRT| :dts:`aliases { sw3 = &button3; };`
* BUTTON4 (small) @ :strong:`P1.15`
  |CRT| :dts:`aliases { sw4 = &button4; };`
* RESET (small)

User PWM Buzzer and Servo Motors
--------------------------------

The |bridle:board:coffeecaller_nrf52| board feature two independent PWM
function units with 4 channels each. The PWM0 channel 0 will be used for
the on-board passive magnetic buzzer and PWM1 channel 0 to 3 are reserved
for driving servo motors.

Serial Port
-----------

The |bridle:board:coffeecaller_nrf52| board feature one two wire UART
(RxD/TxD) at USART0 acassible on the *free pin header* with the default
settings of 115200/8N1 without any flow control (no XON/XOFF, no RTS/CTS).

* TxD @ :strong:`P0.06`
* RxD @ :strong:`P0.08`

USB Device Port
---------------

The |bridle:board:coffeecaller_nrf52| board features one (native) USB full-speed
device port that can be used to communicate with a host PC. See the
:external+zephyr:zephyr:code-sample-category:`usb`
sample applications for more, such as the
:external+zephyr:zephyr:code-sample:`usb-cdc-acm`
sample which sets up a virtual serial port that echos characters back to the
host PC. This board provide the Zephyr console per default on the USB port
as :external+zephyr:ref:`usb_device_cdc_acm`:

.. container:: highlight-console notranslate literal-block

   .. parsed-literal::

      USB device idVendor=\ |coffeecaller_nrf52_VID|, idProduct=\ |coffeecaller_nrf52_PID_CON|, bcdDevice=\ |coffeecaller_nrf52_BCD_CON|
      USB device strings: Mfr=1, Product=2, SerialNumber=3
      Product: |coffeecaller_nrf52_PStr_CON|
      Manufacturer: |coffeecaller_nrf52_VStr|
      SerialNumber: 9D167F0C551481F7

Connections and IOs
===================

Selecting the pins
------------------

Pins can be configured in the board pinctrl file (
:bridle_file:`boards/tiac/coffeecaller/nrf52840-pinctrl.dtsi`
). To see the available mappings, open the `nRF52840 Product Specification`_,
**chapter 7** *Hardware and Layout*. In the **table 7.1.1** *aQFN73 ball
assignments* select the pins marked *General purpose I/O*. Note that pins
marked as *low frequency I/O only* can only be used in under-10㎑
applications. They are not suitable for 115200 speed of UART.

.. _coffeecaller_nrf52_grove_if:

Laced Grove Signal Interface
----------------------------

The |bridle:board:coffeecaller_nrf52| board offers the option of connecting
hardware modules via one single Qwiic/STEMMA QT (|Grove connectors|). This is
provided by a specific interface for general signal mapping, the
|Laced Grove Signal Interface|.

Following mappings are well known:

   * ``grove_gpios``: GPIO mapping
   * ``grove_pwms``: PWM mapping (not yet finally supported)

.. tabs::

   .. group-tab:: GPIO mapping ``grove_gpios``

      This is the **GPIO signal line mapping** from the nRF52840_ to the
      set of |Grove connectors| provided as |Laced Grove Signal Interface|.

      **This list must not be stable!**

      .. include:: grove_gpios.rsti

   .. group-tab:: PWM mapping ``grove_pwms``

      The corresponding mapping is always board or SOC specific. In addition
      to the **PWM signal line mapping**, the valid references to the PWM
      function units in the SOC or on the board are therefore also defined
      as **Grove PWM Labels**. The following table reflects the currently
      supported mapping for :code:`coffeecaller_nrf52`, but this list will
      be growing up with further development and maintenance.

      **This list must not be complete or stable!**

      .. include:: grove_pwms.rsti

Programming and Debugging
*************************

The |bridle:board:coffeecaller_nrf52| board features an
`UF2 based bootloader <TiaC CoffeeCaller nRF52 UF2 bootloader_>`_
to program the application by copying the :file:`build/zephyr/zephyr.uf2` file
to the mounted mass storage device :file:`TiaCCoffee`. If the board is powered
on with the :code:`BOOTSEL` button pressed (the **big BUTTON0**), it will appear
on the host as a mass storage device:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |coffeecaller_nrf52_VID_UF2|, idProduct=\ |coffeecaller_nrf52_PID_UF2|, bcdDevice=\ |coffeecaller_nrf52_BCD_UF2|
         USB device strings: Mfr=1, Product=2, SerialNumber=3
         Product: |coffeecaller_nrf52_PStr_UF2|
         Manufacturer: |coffeecaller_nrf52_VStr_UF2|
         SerialNumber: 9D167F0C551481F7

.. tip::

   When ever you need to restore this original bootloader you should read
   and following the directions in `Building and flashing the CoffeeCaller
   bootloader`_.
   There is also a backup copy of the original bootloader together with
   a ready to use SEGGER JFlash control file inside the Bridel project:

      * :bridle_file:`boards/tiac/coffeecaller/doc/bootloader/nrf52840_0.9.2-17-gbdac0b2_s140_7.3.0.hex`
      * :bridle_file:`boards/tiac/coffeecaller/doc/bootloader/nrf52840_0.9.2-17-gbdac0b2_s140_7.3.0.jflash`

There is also a SWD header (SWD1) on board which have to be used with tools
like SEGGER JLink for bootloader restore, for programming, or direct
programming and debugging.

Flashing
========

Using UF2
---------

The UF2 file should be copied on command line or drag-and-dropped via UI file
manager to this new mass storage device, which will flash the board.

Here is an example for the :zephyr:code-sample:`hello_world` application.
First, run your favorite terminal program to listen for output.
Replace :code:`<tty_device>` with the port where the board can be found. For
example, under Linux, :code:`/dev/ttyACM0`.

   .. code-block:: console

      $ minicom -b 115200 -8 -c on -D <tty_device>

Then build and flash the application in the usual way.

   .. zephyr-app-commands::
      :app: zephyr/samples/hello_world
      :board: coffeecaller_nrf52
      :build-dir: coffeecaller_nrf52
      :west-args: -p
      :flash-args: -r uf2
      :goals: flash
      :host-os: unix
      :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         Hello World! coffeecaller_nrf52/nrf52840

Debugging
=========

The SWD interface can be used to debug the board. To achieve this, you can
either use SEGGER JLink, OpenOCD or PyOCD and follow the instruction in
:external+zephyr:ref:`Building, Flashing and Debugging <west-debugging>`.

You can debug an application in the usual way. Here is an example for
debugging the :external+zephyr:zephyr:code-sample:`hello_world` application:

   .. zephyr-app-commands::
      :app: zephyr/samples/hello_world
      :board: coffeecaller_nrf52
      :build-dir: coffeecaller_nrf52
      :maybe-skip-config:
      :west-args: -p
      :debug-args: -r jlink
      :goals: debug
      :host-os: unix

Tests and Examples
******************

Hello Shell on the USB Console (CDC/ACM)
========================================

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :board: coffeecaller_nrf52
   :build-dir: coffeecaller_nrf52
   :west-args: -p
   :flash-args: -r uf2
   :goals: flash
   :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         Hello World! I'm THE SHELL from coffeecaller_nrf52
         :bgn:`uart:~$` **█**

Simple test execution on target
-------------------------------

(text in bold is a command input)

   .. admonition:: System
      :class: note dropdown toggle-shown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **hwinfo devid**
            Length: 8
            ID: 0x9d167f0c551481f7

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
            - clock\ @\ 40000000 (READY)
              DT node labels: clock
            - gpio\ @\ 50000300 (READY)
              DT node labels: gpio1
            - gpio\ @\ 50000000 (READY)
              DT node labels: gpio0
            - cdc_acm_uart0 (READY)
              DT node labels: cdc_acm_uart0
            - uart\ @\ 40002000 (READY)
              DT node labels: uart0
            - flash-controller\ @\ 4001e000 (READY)
              DT node labels: flash_controller
            - i2c\ @\ 40003000 (READY)
              DT node labels: i2c0
            - pwm\ @\ 40021000 (READY)
              DT node labels: pwm1
            - pwm\ @\ 4001c000 (READY)
              DT node labels: pwm0
            - leds (READY)
            - temp\ @\ 4000c000 (READY)
              DT node labels: temp
            - sht4x\ @\ 46 (READY)
              DT node labels: sht4x

   .. admonition:: Operate with the PWM buzzer
      :class: note dropdown

         #. concert pitch: 440 ㎐
         #. Piezo middle frequency: 1,000 ㎑
         #. Piezo resonance: 2,730 ㎑
         #. Piezo high frequency: 10,000 ㎑
         #. higher frequencies: 11 ㎑, 12 ㎑, 13 ㎑, 14 ㎑, 15 ㎑

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec pwm0 0 2273 1136**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec pwm0 0 2000 1000**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec pwm0 0 366 183**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec pwm0 0 100 50**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec pwm0 0 90 45**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec pwm0 0 83 41**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec pwm0 0 77 39**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec pwm0 0 71 36**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec pwm0 0 66 33**

   .. admonition:: Operate with the PWM servo
      :class: note dropdown

         #. on 0.500 ㎳ ≲ -90°
         #. on 1.500 ㎳ ≅   0°
         #. on 2.500 ㎳ ≳ +90°

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec pwm1 0 20000 500**
            :bgn:`uart:~$` **pwm usec pwm1 0 20000 1500**
            :bgn:`uart:~$` **pwm usec pwm1 0 20000 2500**

   .. admonition:: Die Temperature and I2C T/H Sensor
      :class: note dropdown

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **sensor info**
            device name: sht4x\ @\ 46, vendor: Sensirion AG, model: sht4x, friendly name: (null)
            device name: temp\ @\ 4000c000, vendor: Nordic Semiconductor, model: nrf-temp, friendly name: (null)

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **sensor get temp**
            :bgn:`channel type=12(die_temp) index=0 shift=5 num_samples=1 value=660970642089ns (26.749999)`

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **sensor get sht4x**
            :bgn:`channel type=13(ambient_temp) index=0 shift=6 num_samples=1 value=692580444335ns (27.622261)`
            :bgn:`channel type=16(humidity) index=0 shift=6 num_samples=1 value=692580444335ns (39.897215)`

   .. admonition:: Flash Controller
      :class: note dropdown

      .. rubric:: Erase, Write and Verify

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **flash read flash_controller e0000 40**
            000E0000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            000E0010: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            000E0020: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            000E0030: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|

            :bgn:`uart:~$` **flash test flash_controller e0000 1000 2**
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

            :bgn:`uart:~$` **flash read flash_controller e0000 40**
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

            :bgn:`uart:~$` **flash erase flash_controller e0000 1000**
            Erase success.

            :bgn:`uart:~$` **flash read flash_controller e0000 40**
            000E0000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            000E0010: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            000E0020: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            000E0030: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|

   .. admonition:: I2C on Qwiic with BMP280
      :class: note dropdown

      The |bridle:board:coffeecaller_nrf52| board has one on-board I2C devices.
      For this example an additional |Grove BMP280 Sensor|_ was plugged into
      the Qwiic connector.

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **i2c scan i2c0**
                 0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
            00:             -- -- -- -- -- -- -- -- -- -- -- --
            10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            40: -- -- -- -- -- -- 46 -- -- -- -- -- -- -- -- --
            50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            70: -- -- -- -- -- -- -- 77
            1 devices found on i2c0

      The I2C address ``0x46`` is the on-board `SHT40 <SHT4x_>`_ T/H Sensor.

      The I2C address ``0x77`` is a Bosch BMP280 Air Pressure Sensor and their
      Chip-ID can read from register ``0xd0``. The Chip-ID must be ``0x58``:

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **i2c read_byte i2c0 77 d0**
            Output: 0x58

More Samples
************

There are 3 samples that allow you to test that the push buttons and LEDs
on the board are working properly with Zephyr. You can build and flash the
examples to make sure Zephyr is running correctly on your board. The button
and LED definitions can be found in
:bridle_file:`boards/tiac/coffeecaller/coffeecaller_nrf52_nrf52840.dts`.

User LED Blinky by GPIO
=======================

See also Zephyr sample: :external+zephyr:zephyr:code-sample:`blinky`.

   .. zephyr-app-commands::
      :app: zephyr/samples/basic/blinky
      :board: coffeecaller_nrf52
      :build-dir: coffeecaller_nrf52
      :west-args: -p
      :flash-args: -r uf2
      :goals: flash
      :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         LED state: OFF
         LED state: ON
         LED state: OFF
         LED state: ON
         LED … … …

User LED On/Off by GPIO Button
==============================

See also Zephyr sample: :external+zephyr:zephyr:code-sample:`button`.

   .. zephyr-app-commands::
      :app: zephyr/samples/basic/button
      :board: coffeecaller_nrf52
      :build-dir: coffeecaller_nrf52
      :west-args: -p
      :flash-args: -r uf2
      :goals: flash
      :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         Set up button at gpio\ @\ 50000000 pin 4
         Set up LED at gpio\ @\ 50000300 pin 6
         Press the button
         Button pressed at 834903
         Button pressed at 834909
         Button pressed at 875997
         Button pressed at 876002
         Button pressed at 917520
         Button pressed at 917525
         Button … … …

WS2812 LED Test Pattern over GPIO
=================================

See also Zephyr sample: :external+zephyr:zephyr:code-sample:`led-strip`.

   .. zephyr-app-commands::
      :app: zephyr/samples/drivers/led/led_strip
      :board: coffeecaller_nrf52
      :build-dir: coffeecaller_nrf52
      :west-args: -p
      :flash-args: -r uf2
      :goals: flash
      :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         [00:00:04.013,671] <inf> main: Found LED strip device ws2812
         [00:00:04.013,671] <inf> main: Displaying pattern on strip

User GPIO Button Input dump
===========================

See also Zephyr sample: :external+zephyr:zephyr:code-sample:`input-dump`.

   .. zephyr-app-commands::
      :app: zephyr/samples/subsys/input/input_dump
      :board: coffeecaller_nrf52
      :build-dir: coffeecaller_nrf52
      :west-args: -p
      :flash-args: -r uf2
      :goals: flash
      :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         Input sample started
         I: input event: dev=buttons          SYN type= 1 code= 11 value=1
         I: input event: dev=buttons          SYN type= 1 code= 11 value=0
         I: input event: dev=buttons          SYN type= 1 code=  2 value=1
         I: input event: dev=buttons          SYN type= 1 code=  2 value=0
         I: input event: dev=buttons          SYN type= 1 code=  3 value=1
         I: input event: dev=buttons          SYN type= 1 code=  3 value=0
         I: input event: dev=buttons          SYN type= 1 code=  4 value=1
         I: input event: dev=buttons          SYN type= 1 code=  4 value=0
         I: input event: dev=buttons          SYN type= 1 code=  5 value=1
         I: input event: dev=buttons          SYN type= 1 code=  5 value=0

Sounds from the speaker
=======================

This Bridle sample is applicable for the on-board passive magnetic buzzer
connected to the PWM0 channel 0.

   .. zephyr-app-commands::
      :app: bridle/samples/buzzer
      :board: coffeecaller_nrf52
      :build-dir: coffeecaller_nrf52
      :west-args: -p
      :flash-args: -r uf2
      :goals: flash
      :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         [00:00:04.014,892] <inf> buzzersh: Buzzer shell is ready!
         :bgn:`uart:~$` **█**

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

Drive a servo motor
===================

See also Zephyr sample: :external+zephyr:zephyr:code-sample:`servo-motor`.

This Zephyr sample is applicable for first on-board servo motor connector
corresponding to the PWM1 channel 0.

   .. tsn-include:: snippets/pwm-servo/README.rst
      :docset: bridle
      :start-after: .. _snippet-pwm-servo-tiac-coffeecaller-nrf52:
      :end-before: .. literalinclude:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         Servomotor control

Grove Module Samples
********************

All currently supported Grove modules can be reused on the Qwiic / STEMMA QT
connector using a conversion cable. Only the corresponding shield stacks need
to be specified.

Hello Shell with sensor access to Grove BMP280
==============================================

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :board: coffeecaller_nrf52
   :shield: "grove_sens_bmp280"
   :build-dir: coffeecaller_nrf52
   :west-args: -p
   :flash-args: -r uf2
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
            device name: bmp280\ @\ 77, vendor: Bosch Sensortec GmbH, model: bme280, friendly name: (null)
            device name: sht4x\ @\ 46, vendor: Sensirion AG, model: sht4x, friendly name: (null)
            device name: temp\ @\ 4000c000, vendor: Nordic Semiconductor, model: nrf-temp, friendly name: (null)

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **sensor get bmp280@77**
            :bgn:`channel type=13(ambient_temp) index=0 shift=16 num_samples=1 value=83516265870ns (27.299987)`
            :bgn:`channel type=14(press) index=0 shift=23 num_samples=1 value=83516265870ns (99.054687)`
            :bgn:`channel type=16(humidity) index=0 shift=21 num_samples=1 value=83516265870ns (0.000000)`

BME280 humidity and pressure sensor with Grove BMP280
=====================================================

See also Zephyr sample: :external+zephyr:zephyr:code-sample:`bme280`.

   .. zephyr-app-commands::
      :app: zephyr/samples/sensor/bme280
      :board: coffeecaller_nrf52
      :shield: "grove_sens_bmp280"
      :build-dir: coffeecaller_nrf52
      :west-args: -p
      :flash-args: -r uf2
      :goals: flash
      :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         [00:00:00.000,305] <dbg> temp_nrf5: temp_nrf5_sample_fetch: sample: 112
         [00:00:00.000,305] <dbg> temp_nrf5: temp_nrf5_channel_get: Temperature:28,0
         [00:00:00.002,838] <dbg> BME280: bme280_chip_init: ID OK (BMP280)
         [00:00:00.012,084] <dbg> BME280: bme280_chip_init: "bmp280\ @\ 77" OK
         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         Found device "**bmp280@77**", getting sensor data
         temp: 27.319976; press: 99.58593; humidity: 0.7812
         [00:00:04.032,348] <dbg> temp_nrf5: temp_nrf5_sample_fetch: sample: 112
         [00:00:04.032,348] <dbg> temp_nrf5: temp_nrf5_channel_get: Temperature:28,0
         temp: 27.319976; press: 99.58593; humidity: 0.7812
         temp: 27.319976; press: 99.58593; humidity: 0.7812
         temp: 27.319976; press: 99.58593; humidity: 0.7812
         [00:00:08.032,531] <dbg> temp_nrf5: temp_nrf5_sample_fetch: sample: 109
         [00:00:08.032,531] <dbg> temp_nrf5: temp_nrf5_channel_get: Temperature:27,250000
         temp: 27.319976; press: 99.58593; humidity: 0.7812
         temp: 27.319976; press: 99.58593; humidity: 0.7812
         temp: 27.319976; press: 99.58593; humidity: 0.7812
         temp: 27.319976; press: 99.58593; humidity: 0.7812
         temp: 27.319976; press: 99.58593; humidity: 0.7812
         … … …

LED Blinky with Grove LED Button (Qwiic signals as GPIO)
========================================================

See also Zephyr sample: :external+zephyr:zephyr:code-sample:`blinky`.

   .. zephyr-app-commands::
      :app: zephyr/samples/basic/blinky
      :board: coffeecaller_nrf52
      :shield: "grove_btn_d16 grove_led_d17 x_grove_testbed"
      :build-dir: coffeecaller_nrf52
      :west-args: -p
      :flash-args: -r uf2
      :goals: flash
      :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         LED state: OFF
         LED state: ON
         LED state: OFF
         LED state: ON
         LED … … …

LED Switch with Grove LED Button (Qwiic signals as GPIO)
========================================================

See also Zephyr sample: :external+zephyr:zephyr:code-sample:`button`.

   .. zephyr-app-commands::
      :app: zephyr/samples/basic/button
      :board: coffeecaller_nrf52
      :shield: "grove_btn_d16 grove_led_d17 x_grove_testbed"
      :build-dir: coffeecaller_nrf52
      :west-args: -p
      :flash-args: -r uf2
      :goals: flash
      :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         \*\*\* Booting Zephyr OS build v\ |zephyr_version_number_em| \*\*\*
         Set up button at gpio\ @\ 50000000 pin 20
         Set up LED at gpio\ @\ 50000000 pin 24
         Press the button
         Button pressed at 914048
         Button pressed at 969568
         Button pressed at 976710
         Button pressed at 1000039
         Button pressed at 1097113
         Button pressed at 1114151
         Button … … …

References
**********

.. target-notes::
