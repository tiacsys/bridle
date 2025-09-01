.. _seeeduino_lotus:

Seeeduino Lotus Cortex-M0+
##########################

Overview
********

The Seeeduino Lotus Cortex-M0+ is an Arduino form factor development board
based on an Atmel SAMD21 ARM with onboard LEDs, USB port, and range of 14
digital I/O (10 of which support PWM) and 6 analog I/O broken out onto
|Arduino UNO R3| header and multiple |Grove connectors|.

.. image:: img/seeeduino_lotus.jpg
   :align: center
   :alt: Seeeduino Lotus Cortex-M0+

Hardware
********

.. rst-class:: rst-columns

- `ATSAMD21G18A`_ ARM Cortex-M0+ processor at 48 MHz
- 32.768 kHz crystal oscillator
- 256 KiB flash memory and 32 KiB of RAM
- 3 user LEDs (blue/Rx/Tx)
- One reset button
- Native USB port
- 12 |Grove connectors|
- |Arduino UNO R3| header
- Arduino ICSP header
- `MP2617B`_, switching battery charger (max. 2A)
- JST2.0 Li-Po battery connector

Supported Features
==================

The :code:`seeeduino_lotus` board configuration supports the following
hardware features:

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
     - :dtcompatible:`atmel,sam0-pinctrl`
     - :external+zephyr:ref:`pinctrl_api`
   * - GPIO
     - :kconfig:option:`CONFIG_GPIO`
     - :dtcompatible:`atmel,sam0-gpio`
     - :external+zephyr:ref:`gpio_api`
   * - UART
     - :kconfig:option:`CONFIG_SERIAL`
     - :dtcompatible:`atmel,sam0-uart`
     - :external+zephyr:ref:`uart_api`
   * - UDC (USB Device Controller)
     - :kconfig:option:`CONFIG_USB_DEVICE_STACK_NEXT`
     - :dtcompatible:`atmel,sam0-usb`
     - :external+zephyr:ref:`usb_device_next_api`
   * - I2C
     - :kconfig:option:`CONFIG_I2C`
     - :dtcompatible:`atmel,sam0-i2c`
     - :external+zephyr:ref:`i2c_api`
   * - SPI
     - :kconfig:option:`CONFIG_SPI`
     - :dtcompatible:`atmel,sam0-spi`
     - :external+zephyr:ref:`spi_api`
   * - PWM
     - :kconfig:option:`CONFIG_PWM`
     - :dtcompatible:`atmel,sam0-tcc-pwm`
     - :external+zephyr:ref:`pwm_api`
   * - DAC
     - :kconfig:option:`CONFIG_DAC`
     - :dtcompatible:`atmel,sam0-dac`
     - :external+zephyr:ref:`dac_api`
   * - ADC
     - :kconfig:option:`CONFIG_ADC`
     - :dtcompatible:`atmel,sam0-adc`
     - :external+zephyr:ref:`adc_api`
   * - RTC
     - :kconfig:option:`CONFIG_RTC`
     - :dtcompatible:`atmel,sam0-rtc`
     - :external+zephyr:ref:`rtc_api`
   * - Timer (Counter)
     - :kconfig:option:`CONFIG_COUNTER`
     - :dtcompatible:`atmel,sam0-tcc`
     - :external+zephyr:ref:`counter_api`
   * - Watchdog Timer (WDT)
     - :kconfig:option:`CONFIG_WATCHDOG`
     - :dtcompatible:`atmel,sam0-watchdog`
     - :external+zephyr:ref:`watchdog_api`
   * - Flash
     - :kconfig:option:`CONFIG_FLASH`
     - :dtcompatible:`atmel,sam0-nvmctrl`
     - :external+zephyr:ref:`flash_api` and
       :external+zephyr:ref:`flash_map_api`
   * - DMA
     - :kconfig:option:`CONFIG_DMA`
     - :dtcompatible:`atmel,sam0-dmac`
     - :external+zephyr:ref:`dma_api`
   * - HWINFO
     - :kconfig:option:`CONFIG_HWINFO`
     - :dtcompatible:`atmel,sam0-id`
     - :external+zephyr:ref:`hwinfo_api`
   * - CLOCK / PM
     - **not supported**
     - | :dtcompatible:`atmel,samd2x-gclk`
       | :dtcompatible:`atmel,samd2x-pm`
     - :external+zephyr:ref:`clock_control_api`
   * - NVIC
     - N/A
     - | :dtcompatible:`atmel,sam0-eic`
       | :dtcompatible:`arm,v6m-nvic`
     - Nested Vector :external+zephyr:ref:`interrupts_v2` Controller
   * - SYSTICK
     - N/A
     - :dtcompatible:`arm,armv6m-systick`
     -

Other hardware features are not currently supported by Zephyr.

The default configuration can be found in the Kconfig file
:bridle_file:`boards/seeed/seeeduino_lotus/seeeduino_lotus_defconfig`.

Board Configurations
====================

The :code:`seeeduino_lotus` board can be configured for the following different
use cases.

.. zephyr-keep-sorted-start re(^\.\. rubric:: :command:`\w)

.. rubric:: :command:`west build -b seeeduino_lotus -S usb-console`

Use the USB device port with CDC-ACM as Zephyr console and for the shell.

.. rubric:: :command:`west build -b seeeduino_lotus`

Use the serial port SERCOM2 as Zephyr console and for the shell.

.. zephyr-keep-sorted-stop

Connections and IOs
===================

The `Seeeduino Lotus Cortex-M0+ wiki`_ has detailed information about
the board including `pinouts <Seeeduino Lotus Cortex-M0+ Pinouts_>`_
and the `schematic <Seeeduino Lotus Cortex-M0+ Schematic_>`_.

.. _seeeduino_lotus_grove_if:

Laced Grove Signal Interface
----------------------------

In addition to the |Arduino UNO R3| header, there are also 12 |Grove connectors|.
These are provided by a specific interface for general signal mapping, the
|Laced Grove Signal Interface|.

Following mappings are well known:

.. zephyr-keep-sorted-start re(^\* \|\w)

* ``grove_gpios``: GPIO mapping
* ``grove_pwms``: PWM mapping

.. zephyr-keep-sorted-stop

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GPIO mapping ``grove_gpios``

      This is the **GPIO signal line mapping** from the `Arduino Uno R3`_
      header bindet with :dtcompatible:`arduino-header-r3` to the set of
      |Grove connectors| provided as |Laced Grove Signal Interface|.

      .. include:: grove_gpios.rsti

   .. group-tab:: PWM mapping ``grove_pwms``

      The corresponding mapping is always board or SOC specific. In addition
      to the **PWM signal line mapping**, the valid references to the PWM
      function units in the SOC or on the board are therefore also defined
      as **Grove PWM Labels**. The following table reflects the currently
      supported mapping for :code:`seeeduino_lotus`, but this list will be
      growing up with further development and maintenance.

      **This list must not be complete!**

      .. include:: grove_pwms.rsti

   .. zephyr-keep-sorted-stop

System Clock
============

The SAMD21 MCU is configured to use the 32 kHz external crystal with
the on-chip PLL generating the 48 MHz system clock. The internal APB
and GCLK unit are set up in the same way as the upstream Arduino
libraries.

GPIO (PWM) Ports
================

The SAMD21 MCU has 2 GPIO ports, 3 PWM able Timer/Capture-Counter (TCC) and
2 simple Timer/Counter (TC). On the Lotus Cortex-M0+, TCC2 channel 1 is
available on first user LED (blue), all other user LEDs can be controlled
as GPIO. Only if :kconfig:option:`CONFIG_PWM_SAM0_TCC` is enabled then the
first user LED (blue) is driven by TCC2 instead of by GPIO. All channels of
TCC0 are available on the |Arduino UNO R3| header and the |Grove connectors|
(see above, :ref:`seeeduino_lotus_grove_if`).

ADC/DAC Ports
=============

The SAMD21 MCU has 1 DAC and 1 ADC. On the Lotus Cortex-M0+, the DAC voltage
output (VOUT) is available on A0 of the |Arduino UNO R3| header. The ADC
channels 2-5 and 10 are available on A1-A5 of the |Arduino UNO R3| header.

The external voltage reference VREFA can be used optional for the DAC and
ADC on same time and is available on AREF of the |Arduino UNO R3| header.

SPI Port
========

The SAMD21 MCU has 6 SERCOM based SPIs. On the Lotus Cortex-M0+, SERCOM1
can be put into SPI mode and used to connect to devices over D11 (MOSI),
D12 (MISO), and D13 (SCK) of the |Arduino UNO R3| header.

I2C Port
========

The SAMD21 MCU has 6 SERCOM based I2Cs. On the Lotus Cortex-M0+, SERCOM3
is available on D18 (SDA) and D19 (SCL) of the |Arduino UNO R3| header and
on pin 1 (SCL) and pin 2 (SDA) of the two Grove I2C connectors.

Serial Port
===========

The SAMD21 MCU has 6 SERCOM based USARTs. On the Lotus Cortex-M0+, SERCOM2
is available on D0 (RX) and D1 (TX) of the |Arduino UNO R3| header and is the
Zephyr console. SERCOM5 is available on pin 1 (RX) and pin 2 (TX) of the Grove
UART connector and is an optional second serial port for applications.

USB Device Port
===============

The SAMD21 MCU has a (native) USB device port that can be used to communicate
with a host PC. See the :external+zephyr:zephyr:code-sample-category:`usb`
sample applications for more, such as the
:external+zephyr:zephyr:code-sample:`usb-cdc-acm` sample which sets up a virtual
serial port that echos characters back to the host PC. As an alternative to the
default Zephyr console on serial port the Bridle :ref:`snippet-usb-console` can
be used to enable :external+zephyr:ref:`usb_device_cdc_acm` and switch the
console to USB:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |seeeduino_lotus_VID|, idProduct=\ |seeeduino_lotus_PID_CON|, bcdDevice=\ |seeeduino_lotus_BCD_CON|
         USB device strings: Mfr=1, Product=2, SerialNumber=3
         Product: |seeeduino_lotus_PStr_CON|
         Manufacturer: |seeeduino_lotus_VStr|
         SerialNumber: 9973734CA4207846

Programming and Debugging
*************************

The Lotus Cortex-M0+ ships the BOSSA compatible `UF2 bootloader`_ also known as
`Arduino Zero Bootloader`_, a modern `SAM-BA`_ (Boot Assistant) replacement.
The bootloader can be entered by pressing the RST button twice:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |seeeduino_lotus_VID_UF2|, idProduct=\ |seeeduino_lotus_PID_UF2|, bcdDevice=\ |seeeduino_lotus_BCD_UF2|
         USB device strings: Mfr=1, Product=2, SerialNumber=0
         Product: |seeeduino_lotus_PStr_UF2|
         Manufacturer: |seeeduino_lotus_VStr_UF2|

Additionally, if :kconfig:option:`CONFIG_USB_CDC_ACM` is enabled then the
bootloader will be entered automatically when you run :program:`west flash`.

.. image:: img/seeeduino_lotus_swd.jpg
   :align: right
   :scale: 50%
   :alt: Seeeduino Lotus Cortex-M0+ SWD Programming Port

.. tip::

   When ever you need to restore this original bootloader you should read
   and following the directions in `Flashing the Arduino Bootloader using
   DAP Link`_.
   There is also a backup copy of the original bootloader together with
   a ready to use Segger JFlash control file inside the Bridel project:

      * :bridle_file:`boards/seeed/seeeduino_lotus/doc/bootloader/samd21_sam_ba.hex`
      * :bridle_file:`boards/seeed/seeeduino_lotus/doc/bootloader/samd21_sam_ba.jflash`

There is also a SWD header (J10, not populated) on board which have to be
used with tools like Segger J-Link for programming for bootloader restore
or direct programming and debugging.

Flashing
========

#. Build the Zephyr kernel and the
   :external+zephyr:zephyr:code-sample:`hello_world` sample application:

   .. zephyr-app-commands::
      :app: zephyr/samples/hello_world
      :board: seeeduino_lotus
      :build-dir: seeeduino_lotus
      :west-args: -p
      :goals: build
      :compact:

#. Connect the Lotus Cortex-M0+ to your host computer using USB.

#. Connect a 3.3 V USB to serial adapter to the board and to the
   host. See the `Serial Port`_ section above for the board's pin
   connections.

#. Run your favorite terminal program to listen for output. Under Linux the
   terminal should be :code:`/dev/ttyUSB0`. For example:

   .. code-block:: console

      minicom -D /dev/ttyUSB0 -o

   The :code:`-o` option tells minicom not to send the modem initialization
   string. Connection should be configured as follows:

      - Speed: 115200
      - Data: 8 bits
      - Parity: None
      - Stop bits: 1

#. Pressing the RST button twice quickly to enter bootloader mode.

#. Flash the image:

   .. code-block:: bash

      west flash -d build/seeeduino_lotus

   You should see "Hello World! seeeduino_lotus" in your terminal.

Debugging
=========

**Debugging is only possible over SWD!**

#. Do the for the debug session necessary steps as before except
   enter the bootloader mode and the flashing.

#. Connect the Segger J-Link to the SWD header (J10).

#. Flash the image and attach a debugger to your board:

   .. zephyr-app-commands::
      :app: zephyr/samples/hello_world
      :board: seeeduino_lotus
      :build-dir: seeeduino_lotus
      :gen-args: -DBOARD_FLASH_RUNNER=openocd
      :west-args: -p
      :goals: debug
      :compact:

   You should ends up in a debug console (e.g. a GDB session).

More Samples
************

LED Blinky
==========

.. zephyr-app-commands::
   :app: zephyr/samples/basic/blinky
   :board: seeeduino_lotus
   :build-dir: seeeduino_lotus
   :west-args: -p
   :goals: flash
   :compact:

LED Fade
========

.. zephyr-app-commands::
   :app: zephyr/samples/basic/fade_led
   :board: seeeduino_lotus
   :build-dir: seeeduino_lotus
   :west-args: -p
   :goals: flash
   :compact:

Basic Threads
=============

.. zephyr-app-commands::
   :app: zephyr/samples/basic/threads
   :board: seeeduino_lotus
   :build-dir: seeeduino_lotus
   :west-args: -p
   :goals: flash
   :compact:

Hello Shell with USB-CDC/ACM Console
====================================

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :board: seeeduino_lotus
   :build-dir: seeeduino_lotus
   :west-args: -p -S usb-console
   :goals: flash
   :compact:

.. rubric:: Simple test execution on target

(text in bold is a command input)

.. tabs::

   .. group-tab:: Basics

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **hello -h**
            hello - say hello
            :bgn:`uart:~$` **hello**
            Hello from shell.

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **hwinfo devid**
            Length: 16
            ID: 0xefa3ee60dfcb11ed9973734ca4207846

            :bgn:`uart:~$` **kernel version**
            Zephyr version |zephyr_version_number_em|

            :bgn:`uart:~$` **bridle version**
            Bridle version |shortversion_number_em|

            :bgn:`uart:~$` **bridle version long**
            Bridle version |longversion_number_em|

            :bgn:`uart:~$` **bridle info**
            Zephyr: |zephyr_release_number_em|
            Bridle: |release_number_em|

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **device list**
            devices:
            - eic\ @\ 40001800 (READY)
              DT node labels: eic
            - gpio\ @\ 41004480 (READY)
              DT node labels: portb
            - gpio\ @\ 41004400 (READY)
              DT node labels: porta
            - snippet_cdc_acm_console_uart (READY)
              DT node labels: snippet_cdc_acm_console_uart
            - sercom\ @\ 42001c00 (READY)
              DT node labels: sercom5 grove_serial
            - sercom\ @\ 42001000 (READY)
              DT node labels: sercom2 arduino_serial
            - adc\ @\ 42004000 (READY)
              DT node labels: adc
            - dac\ @\ 42004800 (READY)
              DT node labels: dac0
            - nvmctrl\ @\ 41004000 (READY)
              DT node labels: nvmctrl
            - sercom\ @\ 42001400 (READY)
              DT node labels: sercom3 arduino_i2c grove_i2c
            - tcc\ @\ 42002800 (READY)
              DT node labels: tcc2
            - tcc\ @\ 42002400 (READY)
              DT node labels: tcc1 grove_pwm_d8
            - tcc\ @\ 42002000 (READY)
              DT node labels: tcc0 grove_pwm_d2 grove_pwm_d3 grove_pwm_d4 grove_pwm_d5 grove_pwm_d6 grove_pwm_d7 grove_pwm_d18 grove_pwm_d19
            - leds (READY)

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **history**
            [  0] history
            [  1] device list
            [  2] bridle info
            [  3] bridle version long
            [  4] bridle version
            [  5] kernel version
            [  6] hwinfo devid
            [  7] hello
            [  8] hello -h

   .. group-tab:: GPIO

      Operate with the red Rx user LED:

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **gpio get gpio@41004480 3**
            0

            :bgn:`uart:~$` **gpio conf gpio@41004480 3 ol0**

            :bgn:`uart:~$` **gpio set gpio@41004480 3 1**
            :bgn:`uart:~$` **gpio set gpio@41004480 3 0**

            :bgn:`uart:~$` **gpio blink gpio@41004480 3**
            Hit any key to exit

   .. group-tab:: PWM

      Operate with the blue user LED:

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec tcc@42002800 1 20000 20000**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec tcc@42002800 1 20000 19000**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec tcc@42002800 1 20000 18000**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec tcc@42002800 1 20000 17000**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec tcc@42002800 1 20000 16000**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec tcc@42002800 1 20000 15000**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec tcc@42002800 1 20000 10000**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec tcc@42002800 1 20000 5000**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec tcc@42002800 1 20000 2500**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec tcc@42002800 1 20000 500**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **pwm usec tcc@42002800 1 20000 0**

   .. group-tab:: DAC/ADC

      Operate with the loop-back wire from A0 (DAC CH0 VOUT)
      to A1 (ADC CH2 AIN):

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **dac setup dac@42004800 0 10**
            :bgn:`uart:~$` **adc adc@42004000 resolution 12**
            :bgn:`uart:~$` **adc adc@42004000 acq_time 10 us**
            :bgn:`uart:~$` **adc adc@42004000 channel positive 2**

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **dac write_value dac@42004800 0 512**
            :bgn:`uart:~$` **adc adc@42004000 read 2**
            read: 2025

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **dac write_value dac@42004800 0 1023**
            :bgn:`uart:~$` **adc adc@42004000 read 2**
            read: 4061

   .. group-tab:: Flash access

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **flash read nvmctrl@41004000 1361c 40**
            0001361C: 73 65 65 65 64 75 69 6e  6f 5f 6c 6f 74 75 73 00 \|seeeduin o_lotus.\|
            0001362C: 48 65 6c 6c 6f 20 57 6f  72 6c 64 21 20 49 27 6d \|Hello Wo rld! I'm\|
            0001363C: 20 54 48 45 20 53 48 45  4c 4c 20 66 72 6f 6d 20 \| THE SHE LL from \|
            0001364C: 25 73 0a 00 28 75 6e 73  69 67 6e 65 64 29 20 63 \|%s..(uns igned) c\|

      .. rubric:: Erase, Write and Verify

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **flash read nvmctrl@41004000 3c000 40**
            0003C000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            0003C010: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            0003C020: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            0003C030: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|

            :bgn:`uart:~$` **flash test nvmctrl@41004000 3c000 400 2**
            Erase OK.
            Write OK.
            Verified OK.
            Erase OK.
            Write OK.
            Verified OK.
            Erase-Write-Verify test done.

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **flash read nvmctrl@41004000 3c000 40**
            0003C000: 00 01 02 03 04 05 06 07  08 09 0a 0b 0c 0d 0e 0f \|........ ........\|
            0003C010: 10 11 12 13 14 15 16 17  18 19 1a 1b 1c 1d 1e 1f \|........ ........\|
            0003C020: 20 21 22 23 24 25 26 27  28 29 2a 2b 2c 2d 2e 2f \| !"#$%&' ()*+,-./\|
            0003C030: 30 31 32 33 34 35 36 37  38 39 3a 3b 3c 3d 3e 3f \|01234567 89:;<=>?\|

            :bgn:`uart:~$` **flash page_info 3c000**
            Page for address 0x3c000:
            start offset: 0x3c000
            size: 256
            index: 960

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **flash erase nvmctrl@41004000 3c000 400**
            Erase success.

            :bgn:`uart:~$` **flash read nvmctrl@41004000 3c000 40**
            0003C000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            0003C010: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            0003C020: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|
            0003C030: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff \|........ ........\|

   .. group-tab:: I2C

      The Lotus Cortex-M0+ has no on-board I2C devices. For this example the
      |Grove BMP280 Sensor|_ was connected.

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **log enable none i2c_sam0**

            :bgn:`uart:~$` **i2c scan sercom@42001400**
                 0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
            00:             -- -- -- -- -- -- -- -- -- -- -- --
            10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            70: -- -- -- -- -- -- -- 77
            1 devices found on sercom\ @\ 42001400

            :bgn:`uart:~$` **log enable inf i2c_sam0**

      The I2C address ``0x77`` is a Bosch BMP280 Air Pressure Sensor and their
      Chip-ID can read from register ``0xd0``. The Chip-ID must be ``0x58``:

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **i2c read_byte sercom@42001400 77 d0**
            Output: 0x58

References
**********

.. target-notes::
