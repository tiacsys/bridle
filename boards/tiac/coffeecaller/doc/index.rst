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

.. include:: hardware.rsti

Positions
=========

.. include:: positions.rsti

Pinouts
=======

.. include:: pinouts.rsti

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
     - :kconfig:option:`CONFIG_USB_DEVICE_STACK_NEXT`
     - :dtcompatible:`nordic,nrf-usbd`
     - :external+zephyr:ref:`usb_device_next_api`
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

.. zephyr-keep-sorted-start re(^\* :bridle_file:`\w)

* :bridle_file:`boards/tiac/coffeecaller/coffeecaller_nrf52_nrf52840_defconfig`

.. zephyr-keep-sorted-stop

Board Configurations
====================

The |bridle:board:coffeecaller_nrf52| board can be configured
for the following different use cases.

.. zephyr-keep-sorted-start re(^\.\. rubric:: :command:`\w)

.. rubric:: :command:`west build -b coffeecaller_nrf52`

Use the native USB device port with CDC-ACM as Zephyr console and for the shell.

.. zephyr-keep-sorted-stop

User LED
========

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
============

The |bridle:board:coffeecaller_nrf52| board feature four RGB LEDs for user
purposes in strip (serial) interconnection at GPIO port 0 line 26.

* WS2812 Strip @ :strong:`P0.26`
  |CRT| :dts:`aliases { led-strip = &led_strip; };`

User Button
===========

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
================================

The |bridle:board:coffeecaller_nrf52| board feature two independent PWM
function units with 4 channels each. The PWM0 channel 0 will be used for
the on-board passive magnetic buzzer and PWM1 channel 0 to 3 are reserved
for driving servo motors.

Serial Port
===========

The |bridle:board:coffeecaller_nrf52| board feature one two wire UART
(RxD/TxD) at USART0 acassible on the *free pin header* with the default
settings of 115200/8N1 without any flow control (no XON/XOFF, no RTS/CTS).

* TxD @ :strong:`P0.06`
* RxD @ :strong:`P0.08`

USB Device Port
===============

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

.. zephyr-keep-sorted-start re(^\* \|\w)

* ``grove_gpios``: GPIO mapping
* ``grove_pwms``: PWM mapping

.. zephyr-keep-sorted-stop

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

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

   .. zephyr-keep-sorted-stop

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

Here is an example for the :external+zephyr:zephyr:code-sample:`hello_world`
application. First, run your favorite terminal program to listen for output.
Replace :code:`<tty_device>` with the port where the board can be found. For
example, under Linux, :code:`/dev/ttyACM0`.

   .. code-block:: console

      $ minicom -b 115200 -8 -c on -D <tty_device>

Then build and flash the application in the usual way.

   .. zephyr-app-commands::
      :app: zephyr/samples/hello_world
      :build-dir: coffeecaller_nrf52
      :board: coffeecaller_nrf52/nrf52840
      :west-args: -p
      :flash-args: -r uf2
      :goals: flash
      :host-os: unix
      :compact:

You should see the following message on the console:

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…*\*\*\*
         Hello World! coffeecaller_nrf52/nrf52840

.. hint::

   Programming via the **UF2 bootloader is the default setting** and does
   not always need to be explicitly specified as the flash runner using
   :program:`west flash`!

Debugging
=========

The SWD interface can be used to debug the board. To achieve this, you can
either use SEGGER JLink, OpenOCD or PyOCD and follow the instruction in
:external+zephyr:ref:`Building, Flashing and Debugging <west-debugging>`.

You can debug an application in the usual way. Here is an example for
debugging the :external+zephyr:zephyr:code-sample:`hello_world` application:

   .. zephyr-app-commands::
      :app: zephyr/samples/hello_world
      :build-dir: coffeecaller_nrf52
      :board: coffeecaller_nrf52/nrf52840
      :maybe-skip-config:
      :west-args: -p
      :debug-args: -r jlink
      :goals: debug
      :host-os: unix

Tests and Evaluation
********************

Hello Shell on the USB Console (CDC/ACM)
========================================

.. include:: helloshell.rsti

Basic Samples
*************

There are 3 samples that allow you to test that the push buttons and LEDs
on the board are working properly with Zephyr. You can build and flash the
examples to make sure Zephyr is running correctly on your board. The button
and LED definitions can be found in
:bridle_file:`boards/tiac/coffeecaller/coffeecaller_nrf52_nrf52840.dts`.

User LED Blinky by GPIO
=======================

.. include:: blinky.rsti

User LED On/Off by GPIO Button
==============================

.. include:: button.rsti

WS2812 LED Test Pattern over GPIO
=================================

.. include:: led_strip.rsti

More Samples
************

User GPIO Button Input dump
===========================

.. include:: input_dump.rsti

Sounds from the speaker
=======================

.. include:: buzzer.rsti

Drive a servo motor
===================

.. include:: servo.rsti

Grove Module Samples
********************

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

LED Switch with Grove LED Button (Qwiic signals as GPIO)
========================================================

.. include:: button_grove.rsti

References
**********

.. target-notes::

.. |LED Shields| replace:: :ref:`grove_led_shield`
.. |Button Shields| replace:: :ref:`grove_button_shield`
.. |Sensor Shields| replace:: :ref:`grove_sensor_shield`
