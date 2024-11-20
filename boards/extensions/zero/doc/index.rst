.. _arduino_zero-extensions:

Arduino/Genuino Zero
####################

.. admonition:: Downstream Extension!
   :class: note

   This board description is a copy from Zephyr with identical name and will
   be used for further development, improvement and preparation of changes for
   Zephyr within Bridle. However, the original board description still lives
   within the Zephyr namespace under the exactly same board name:
   |zephyr:board:arduino_zero|.

Overview
********

The Arduino Zero is a maker-friendly development board with Atmel’s Embedded
Debugger (`EDBG`_), which provides a full debug interface without the need for
additional hardware.

.. image:: img/arduino_zero.jpg
   :align: center
   :alt: Arduino Zero

Hardware
********

   .. rst-class:: rst-columns

   - `ATSAMD21G18A`_ ARM Cortex-M0+ processor at 48 MHz
   - 32.768 kHz crystal oscillator
   - 256 KiB flash memory and 32 KiB of RAM
   - 3 user LEDs (L/Rx/Tx)
   - One reset button
   - On-board USB based EDBG unit with serial console
   - Native USB port
   - |Arduino UNO R3| header
   - Arduino ICSP header

Supported Features
==================

The :code:`arduino_zero` board configuration supports the following
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
     - :zephyr:ref:`pinctrl_api`
   * - GPIO
     - :kconfig:option:`CONFIG_GPIO`
     - :dtcompatible:`atmel,sam0-gpio`
     - :zephyr:ref:`gpio_api`
   * - UART
     - :kconfig:option:`CONFIG_SERIAL`
     - :dtcompatible:`atmel,sam0-uart`
     - :zephyr:ref:`uart_api`
   * - UDC (USB Device Controller)
     - :kconfig:option:`CONFIG_USB_DEVICE_STACK`
     - :dtcompatible:`atmel,sam0-usb`
     - :zephyr:ref:`usb_api`
   * - I2C
     - :kconfig:option:`CONFIG_I2C`
     - :dtcompatible:`atmel,sam0-i2c`
     - :zephyr:ref:`i2c_api`
   * - SPI
     - :kconfig:option:`CONFIG_SPI`
     - :dtcompatible:`atmel,sam0-spi`
     - :zephyr:ref:`spi_api`
   * - PWM
     - :kconfig:option:`CONFIG_PWM`
     - :dtcompatible:`atmel,sam0-tcc-pwm`
     - :zephyr:ref:`pwm_api`
   * - DAC
     - :kconfig:option:`CONFIG_DAC`
     - :dtcompatible:`atmel,sam0-dac`
     - :zephyr:ref:`dac_api`
   * - ADC
     - :kconfig:option:`CONFIG_ADC`
     - :dtcompatible:`atmel,sam0-adc`
     - :zephyr:ref:`adc_api`
   * - RTC
     - :kconfig:option:`CONFIG_RTC`
     - :dtcompatible:`atmel,sam0-rtc`
     - :zephyr:ref:`rtc_api`
   * - Timer (Counter)
     - :kconfig:option:`CONFIG_COUNTER`
     - :dtcompatible:`atmel,sam0-tcc`
     - :zephyr:ref:`counter_api`
   * - Watchdog Timer (WDT)
     - :kconfig:option:`CONFIG_WATCHDOG`
     - :dtcompatible:`atmel,sam0-watchdog`
     - :zephyr:ref:`watchdog_api`
   * - Flash
     - :kconfig:option:`CONFIG_FLASH`
     - :dtcompatible:`atmel,sam0-nvmctrl`
     - :zephyr:ref:`flash_api` and
       :zephyr:ref:`flash_map_api`
   * - DMA
     - :kconfig:option:`CONFIG_DMA`
     - :dtcompatible:`atmel,sam0-dmac`
     - :zephyr:ref:`dma_api`
   * - HWINFO
     - :kconfig:option:`CONFIG_HWINFO`
     - :dtcompatible:`atmel,sam0-id`
     - :zephyr:ref:`hwinfo_api`
   * - CLOCK / PM
     - **not supported**
     - | :dtcompatible:`atmel,samd2x-gclk`
       | :dtcompatible:`atmel,samd2x-pm`
     - :zephyr:ref:`clock_control_api`
   * - NVIC
     - N/A
     - | :dtcompatible:`atmel,sam0-eic`
       | :dtcompatible:`arm,v6m-nvic`
     - Nested Vector :zephyr:ref:`interrupts_v2` Controller
   * - SYSTICK
     - N/A
     - :dtcompatible:`arm,armv6m-systick`
     -

Other hardware features are not currently supported by Zephyr.

The extended default configuration can be found in the Kconfig artifact
:bridle_file:`boards/extensions/zero/arduino_zero.conf`. It will be add
automatically to the original board default configuration in
:zephyr_file:`boards/arduino/zero/arduino_zero_defconfig`.

Board Configurations
====================

The :code:`arduino_zero` board can be configured for the following different
use cases.

.. rubric:: :command:`west build -b arduino_zero`

Use the serial port SERCOM5 over EDBG as Zephyr console and for the shell.

.. rubric:: :command:`west build -b arduino_zero -S usb-console`

Use the native USB device port with CDC-ACM as Zephyr console and for the shell,
see :ref:`snippet-usb-console`.

Connections and IOs
===================

The `Arduino store`_ has detailed information about board connections. Download
the `Arduino Zero Schematic`_ or `Arduino Zero Design Data`_ for more detail.
There is also an `Arduino Zero Pinout Diagram`_.

System Clock
============

The SAMD21 MCU is configured to use the 32.768 kHz external crystal with the
on-chip PLL generating the 48 MHz system clock. The internal APB and GCLK unit
are set up in the same way as the upstream Arduino libraries.

GPIO (PWM) Ports
================

The SAMD21 MCU has 2 GPIO ports, 3 PWM able Timer/Capture-Counter (TCC) and
2 simple Timer/Counter (TC). On the Arduino Zero, TCC2 channel 1 is
available on first user LED (L), all other user LEDs can be controlled
as GPIO. Only if :kconfig:option:`CONFIG_PWM_SAM0_TCC` is enabled then the
first user LED (L) is driven by TCC2 instead of by GPIO. All channels of
TCC0 and TCC1 are available on the |Arduino UNO R3| header.

ADC/DAC Ports
=============

The SAMD21 MCU has 1 DAC and 1 ADC. On the Arduino Zero the DAC voltage
output (VOUT) is available on A0 of the |Arduino UNO R3| header. The ADC
channels 2-5 and 10 are available on A1-A5 of the |Arduino UNO R3| header.

The external voltage reference VREFA can be used optional for the DAC and
ADC on same time and is available on AREF of the |Arduino UNO R3| header.

SPI Port
========

.. image:: img/arduino_zero_spi.jpg
   :align: right
   :scale: 50%
   :alt: Arduino Zero SPI on 6 pin ICSP connector

The SAMD21 MCU has 6 SERCOM based SPIs. On the Arduino Zero, SERCOM4 is
available on the 6 pin ICSP connector at the edge of the board. To the
|Arduino UNO R3| header SERCOM1 is connect to external devices over D11 (MOSI),
D12 (MISO), and D13 (SCK). All signals of both busses are connected in
parallel to the Atmel EDBG.

I2C Port
========

The SAMD21 MCU has 6 SERCOM based I2Cs. On the Arduino Zero, SERCOM3 is
signals are connected in parallel to the Atmel EDBG.

Serial Port
===========

The SAMD21 MCU has 6 SERCOM based USARTs. One of the USARTs (SERCOM5) is
connected to the onboard Atmel Embedded Debugger (EDBG) and is the Zephyr
console. This is captured by the standard board configuration. SERCOM0 is
available on the D0 (RX) and D1 (TX) of the |Arduino UNO R3| header.

USB Device Port
===============

.. image:: img/arduino_zero_usb.jpg
   :align: right
   :scale: 50%
   :alt: Arduino Zero Native and Programming USB Ports

The SAMD21 MCU has a (native) USB device port that can be used to communicate
with a host PC. See Zephyr :zephyr:code-sample-category:`usb` for more, such as
the :zephyr:code-sample:`usb-cdc-acm` sample which sets up a virtual serial port
that echos characters back to the host PC. As an alternative to the default
Zephyr console on serial port the Bridle :ref:`snippet-usb-console` can be used
to enable :zephyr:ref:`usb_device_cdc_acm` and switch the console to USB:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |arduino_zero_VID|, idProduct=\ |arduino_zero_PID_CON|, bcdDevice=\ |arduino_zero_BCD_CON|
         USB device strings: Mfr=1, Product=2, SerialNumber=3
         Product: |arduino_zero_PStr_CON|
         Manufacturer: |arduino_zero_VStr|
         SerialNumber: 9CF503EE1D54A301

Programming and Debugging
*************************

The Arduino Zero ships the BOSSA compatible `UF2 bootloader`_ also known as
`Arduino Zero Bootloader`_, a modern `SAM-BA`_ (Boot Assistant) replacement.
The bootloader can be entered by pressing the RST button twice:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |arduino_zero_VID|, idProduct=\ |arduino_zero_PID_UF2|, bcdDevice=\ |arduino_zero_BCD_UF2|
         USB device strings: Mfr=1, Product=2, SerialNumber=0
         Product: |arduino_zero_PStr_UF2|
         Manufacturer: |arduino_zero_VStr|

Additionally, if :kconfig:option:`CONFIG_USB_CDC_ACM` is enabled then the
bootloader will be entered automatically when you run :program:`west flash`.

.. tip::

   When ever you need to restore this original bootloader you should read
   and following the directions in `Arduino Zero Advanced Features`_ and
   `Update the Bootloader on the Arduino Zero`_.
   There is also a backup copy of the original bootloader together with
   a ready to use Segger JFlash control file inside the Bridel project:

      * :bridle_file:`boards/extensions/zero/doc/bootloader/samd21_sam_ba.hex`
      * :bridle_file:`boards/extensions/zero/doc/bootloader/samd21_sam_ba.jflash`

   The Segger JFlash control file is only useful when the EDBG firmware
   was upgrade to the latest `J-Link firmware for Atmel EDBG`_. This was a
   special OEM firmware version for Atmel's Xplained Platforms, based on the
   `AT32UC3A4256S`_ 32-bit AVR microcontroller.

      .. danger::

         **It is neither guaranteed nor tested that the J-Link firmware
         for Atmel EDBG will also work on the EDGB populated on the Arduino
         Zero!**  See also the warning to Atmel Studio 7 below. In doubt
         you should never touch the EDBG firmware on Arduino Zero.

   So if that didn't happen, OpenOCD or, even easier, the small tool
   :program:`edbg`, the `CMSIS-DAP programmer`_ by a Microchip employee,
   should be used:

      .. code-block:: console

         $ srec_cat samd21_sam_ba.hex -Intel -Output samd21_sam_ba.bin -Binary
         $ edbg --list    # convert HEX to BIN file and get <your_edbg_sn>

         $ edbg --verbose --serial <your_edbg_sn> --target samd21 \
                --erase --program --verify --file samd21_sam_ba.bin

   It is also possible to use Microchip's own `Python MCU programmer`_
   together with the `Python Kit information`_ utility and write the
   Intel HEX file directly back to flash without conversion to BIN file:

      .. code-block:: console

         $ pykitinfo # get <your_edbg_sn>
         $ pymcuprog --verbose info --tool edbg --serialnumber <your_edbg_sn> \
                     --device atsamd21g18a --file samd21_sam_ba.hex \
                     --erase --verify write

.. rubric:: Atmel Embedded Debugger (EDBG)

The Arduino Zero also comes with an Atmel Embedded Debugger (`EDBG`_). That
provides a debug interface to the SAMD21 chip and is supported by OpenOCD
for bootloader restore or direct programming and debugging. The Atmel EDGB
is connected to the debug USB port for programming:

   .. container:: highlight-console notranslate literal-block

      .. parsed-literal::

         USB device idVendor=\ |atmel_VID|, idProduct=\ |atmel_PID_EDBG|, bcdDevice=\ |atmel_BCD_EDBG|
         USB device strings: Mfr=1, Product=2, SerialNumber=3
         Product: |atmel_PStr_EDBG|
         Manufacturer: |atmel_VStr|
         SerialNumber: E8VRDGVEYNKJTF8LS45K

.. image:: img/atmel_edbg_bd.svg
   :align: center
   :alt: Atmel Embedded Debugger (EDBG) Block Diagram

.. admonition:: Arduino Zero, Atmel EDBG, and Atmel Studio 7
   :class: danger

      .. image:: img/atmel_edbg.png
         :align: right
         :alt: Atmel Embedded Debugger (EDBG) Chip

      The Arduino Zero was designed in partnership with Atmel (now
      Microchip) which dedicated to this board a special USB PID with
      the major purpose to make the board recognizable and differentiate
      it form other evaluation boards in Atmel Studio. The EDBG chip is
      used on several Atmel evaluation boards and programmers, you can
      find the list `here <EDBG USB PID_>`_.
      You should consider the Arduino Zero dedicated USB PID (:code:`0x2157`)
      as another USB PID to add to that list. **During the manufacturing
      process Arduino upgrade the EDBG firmware and customize the USB
      descriptor fields.**

      -- https://github.com/arduino/ArduinoCore-samd/issues/286#issuecomment-354807646

   Upgrading the firmware with a new one provided by Atmel Studio 7 using
   the :program:`atfw.exe` tool will erase all the factory "Arduino Zero"
   USB configurations and will set the USB PID to :code:`0x2111`. **But
   consider that you couldn't revert the Arduino USB descriptor settings!**

Flashing
========

#. Build the Zephyr kernel and the :zephyr:code-sample:`hello_world` sample
   application:

   .. zephyr-app-commands::
      :app: zephyr/samples/hello_world
      :board: arduino_zero
      :build-dir: arduino_zero
      :west-args: -p
      :goals: build
      :compact:

#. Connect the Arduino Zero to your host computer using the **native USB**
   port (before the USB debug port) to rech the bootloader.

#. Connect the Arduino Zero to your host computer using the **USB debug**
   port (after the native USB port) to reach the virtual console of **EDBG**.

#. Run your favorite terminal program to listen for output. Under Linux the
   terminal should be :code:`/dev/ttyACM0`. For example:

   .. code-block:: console

      minicom -D /dev/ttyACM0 -o

   The :code:`-o` option tells minicom not to send the modem initialization
   string. Connection should be configured as follows:

      - Speed: 115200
      - Data: 8 bits
      - Parity: None
      - Stop bits: 1

#. Pressing the RST button twice quickly to enter bootloader mode.

#. Flash the image:

   .. code-block:: bash

      west flash -d build/arduino_zero

   You should see "Hello World! arduino_zero" in your terminal.

Debugging
=========

**Debugging is only possible over SWD with the help of EDBG!**

#. Do the for the debug session necessary steps as before except
   enter the bootloader mode and the flashing.

#. Flash the image and attach a debugger to your board:

   .. zephyr-app-commands::
      :app: zephyr/samples/hello_world
      :board: arduino_zero
      :build-dir: arduino_zero
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
   :board: arduino_zero
   :build-dir: arduino_zero
   :west-args: -p
   :goals: flash
   :compact:

LED Fade
========

.. zephyr-app-commands::
   :app: zephyr/samples/basic/fade_led
   :board: arduino_zero
   :build-dir: arduino_zero
   :west-args: -p
   :goals: flash
   :compact:

Basic Threads
=============

.. zephyr-app-commands::
   :app: zephyr/samples/basic/threads
   :board: arduino_zero
   :build-dir: arduino_zero
   :west-args: -p
   :goals: flash
   :compact:

Hello Shell with USB-CDC/ACM Console
====================================

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :board: arduino_zero
   :build-dir: arduino_zero
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
            ID: 0xde73d01ae52511ed9cf503ee1d54a301

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
              DT node labels: sercom5
            - sercom\ @\ 42000800 (READY)
              DT node labels: sercom0 arduino_serial
            - adc\ @\ 42004000 (READY)
              DT node labels: adc
            - dac\ @\ 42004800 (READY)
              DT node labels: dac0
            - nvmctrl\ @\ 41004000 (READY)
              DT node labels: nvmctrl
            - sercom\ @\ 42001400 (READY)
              DT node labels: sercom3 arduino_i2c
            - tcc\ @\ 42002800 (READY)
              DT node labels: tcc2
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

      Operate with the yellow Rx user LED:

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

      Operate with the builtin user LED:

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
            read: 2016

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **dac write_value dac@42004800 0 1023**
            :bgn:`uart:~$` **adc adc@42004000 read 2**
            read: 4047

   .. group-tab:: Flash access

      .. rubric:: Print HEX Dump

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **flash read nvmctrl@41004000 13548 40**
            00013548: 61 72 64 75 69 6e 6f 5f  7a 65 72 6f 00 48 65 6c \|arduino_ zero.Hel\|
            00013558: 6c 6f 20 57 6f 72 6c 64  21 20 49 27 6d 20 54 48 \|lo World ! I'm TH\|
            00013568: 45 20 53 48 45 4c 4c 20  66 72 6f 6d 20 25 73 0a \|E SHELL  from %s.\|
            00013578: 00 28 75 6e 73 69 67 6e  65 64 29 20 63 68 61 72 \|.(unsign ed) char\|

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

      The Arduino Zero has no on-board I2C devices. For this example the
      |Grove BMP280 Sensor|_ was connected.

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **log enable none i2c_sam0**

            :bgn:`uart:~$` **i2c scan sercom@42001400**
                 0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
            00:             -- -- -- -- -- -- -- -- -- -- -- --
            10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            20: -- -- -- -- -- -- -- -- 28 -- -- -- -- -- -- --
            30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
            70: -- -- -- -- -- -- -- 77
            2 devices found on sercom\ @\ 42001400

            :bgn:`uart:~$` **log enable inf i2c_sam0**

      The I2C address ``0x77`` is a Bosch BMP280 Air Pressure Sensor and their
      Chip-ID can read from register ``0xd0``. The Chip-ID must be ``0x58``:

      .. container:: highlight highlight-console notranslate

         .. parsed-literal::

            :bgn:`uart:~$` **i2c read_byte sercom@42001400 77 d0**
            Output: 0x58

      .. hint::

         The I2C address ``0x28`` is the **Data Gateway Interface** (`DGI`_)
         to the builtin Atmel `EDBG`_. See the old `ASF3`_ example code on
         GitHub, `SAM EDBG TWI Information Interface Example`_, to learn
         how to work with this I2C device:

            The DGI consists of several physical data interfaces to
            communicate with the host computer; I2C is only one of
            them. Communication over the interfaces is bidirectional.
            It can be used to send events and values from the ATSAMD21G18A,
            or as a generic printf-style data channel. Traffic over the
            interfaces can be timestamped on the EDBG for a more accurate
            tracing of events. Note that timestamping imposes an overhead
            that reduces maximal throughput. The DGI uses a proprietary
            protocol, and is thus only compatible with Atmel Studio.

            -- https://docs.arduino.cc/tutorials/zero/arduino-zero-edbg

References
**********

.. target-notes::
