.. _arduino_zero:

Arduino/Genuino Zero
####################

.. admonition:: Downstream Copy!
   :class: note

   This board description is a copy from Zephyr with identical name and will
   be used for further development, improvement and preparation of changes for
   Zephyr within Bridle.  However, the original board description still lives
   within the Zephyr namespace under the exactly same board name:
   :ref:`zephyr:arduino_zero`.

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

The arduino_zero board configuration supports the following hardware
features:

+-----------+------------+------------------------------------------+
| Interface | Controller | Driver/Component                         |
+===========+============+==========================================+
| ADC       | on-chip    | Analogue to digital converter            |
+-----------+------------+------------------------------------------+
| DAC       | on-chip    | Digital to analogue converter            |
+-----------+------------+------------------------------------------+
| DMA       | on-chip    | Direct memory access                     |
+-----------+------------+------------------------------------------+
| Flash     | on-chip    | Can be used with LittleFS to store files |
+-----------+------------+------------------------------------------+
| GPIO      | on-chip    | I/O ports                                |
+-----------+------------+------------------------------------------+
| HWINFO    | on-chip    | Hardware info                            |
+-----------+------------+------------------------------------------+
| NVIC      | on-chip    | nested vector interrupt controller       |
+-----------+------------+------------------------------------------+
| PWM       | on-chip    | Pulse Width Modulation                   |
+-----------+------------+------------------------------------------+
| SPI       | on-chip    | Serial Peripheral Interface ports        |
+-----------+------------+------------------------------------------+
| SYSTICK   | on-chip    | systick                                  |
+-----------+------------+------------------------------------------+
| USART     | on-chip    | Serial ports                             |
+-----------+------------+------------------------------------------+
| USB       | on-chip    | USB device                               |
+-----------+------------+------------------------------------------+
| WDT       | on-chip    | Watchdog                                 |
+-----------+------------+------------------------------------------+

Other hardware features are not currently supported by Zephyr.

The default configuration can be found in the Kconfig
:bridle_file:`boards/arm/arduino_zero/arduino_zero_defconfig`.

Board Revisions
===============

The :code:`arduino_zero` board can be configured for the following revisions.
These are not really specific hardware revisions, rather than specific
configurations for different use cases.

.. rubric:: :code:`arduino_zero@uartcons`

Use the serial port SERCOM5 over EDBG as Zephyr console and for the shell.

.. rubric:: :code:`arduino_zero@usbcons`

Use the native USB device port with CDC-ACM as Zephyr console and for the shell.

Connections and IOs
===================

The `Arduino store`_ has detailed information about board connections.  Download
the `Arduino Zero Schematic`_ or `Arduino Zero Design Data`_ for more detail.
There is also an `Arduino Zero Pinout Diagram`_.

System Clock
============

The SAMD21 MCU is configured to use the 32.768 kHz external crystal with the
on-chip PLL generating the 48 MHz system clock.  The internal APB and GCLK unit
are set up in the same way as the upstream Arduino libraries.

GPIO (PWM) Ports
================

The SAMD21 MCU has 2 GPIO ports, 3 PWM able Timer/Capture-Counter (TCC) and
2 simple Timer/Counter (TC).  On the Arduino Zero, TCC2 channel 1 is
available on first user LED (L), all other user LEDs can be controlled
as GPIO.  Only if :kconfig:option:`CONFIG_PWM_SAM0_TCC` is enabled then the
first user LED (L) is driven by TCC2 instead of by GPIO.  All channels of
TCC0 are available on the |Arduino UNO R3| header.

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

The SAMD21 MCU has 6 SERCOM based SPIs.  On the Arduino Zero, SERCOM4 is
available on the 6 pin ICSP connector at the edge of the board.

Serial Port
===========

The SAMD21 MCU has 6 SERCOM based USARTs.  One of the USARTs (SERCOM5) is
connected to the onboard Atmel Embedded Debugger (EDBG) and is the Zephyr
console.  This is captured by the standard board revision ``uartcons``.
SERCOM0 is available on the D0 (RX) and D1 (TX) of the |Arduino UNO R3| header.

USB Device Port
===============

.. image:: img/arduino_zero_usb.jpg
   :align: right
   :scale: 50%
   :alt: Arduino Zero Native and Programming USB Ports

The SAMD21 MCU has a (native) USB device port that can be used to communicate
with a host PC.  See the :ref:`usb-samples` sample applications for more, such
as the :ref:`usb_cdc-acm` sample which sets up a virtual serial port that echos
characters back to the host PC.  As an alternative to the default Zephyr console
on serial port the special board revision ``usbcons`` can be used to enable
:ref:`usb_device_cdc_acm` and switch the console to USB::

   USB device idVendor=2341, idProduct=804d, bcdDevice= 3.03
   USB device strings: Mfr=1, Product=2, SerialNumber=3
   Product: Arduino Zero (CDC ACM)
   Manufacturer: Arduino LLC
   SerialNumber: 9CF503EE1D54A301

Programming and Debugging
*************************

The Arduino Zero ships the BOSSA compatible UF2 bootloader also known as
`Arduino Zero Bootloader`_, a modern `SAM-BA`_ (Boot Assistant) replacement.
The bootloader can be entered by pressing the RST button twice::

   USB device idVendor=2341, idProduct=004d, bcdDevice= 2.00
   USB device strings: Mfr=1, Product=2, SerialNumber=0
   Product: Arduino Zero
   Manufacturer: Arduino LLC

Additionally, if :kconfig:option:`CONFIG_USB_CDC_ACM` is enabled then the
bootloader will be entered automatically when you run :program:`west flash`.

.. tip::

   When ever you need to restore this original bootloader you should read
   and following the directions in `Arduino Zero Advanced Features`_ and
   `Update the Bootloader on the Arduino Zero`_.
   There is also a backup copy of the original bootloader together with
   a ready to use Segger JFlash control file inside the Bridel project:

   * :bridle_file:`boards/arm/arduino_zero/doc/bootloader/samd21_bossa_arduino.hex`
   * :bridle_file:`boards/arm/arduino_zero/doc/bootloader/samd21_bossa_arduino.jflash`

   The Segger JFlash control file is only usefull when the EDBG firmware
   was upgrade to the latest `J-Link firmware for Atmel EDBG`_.  This was a
   special OEM firmware version for Atmel's Xplained Platforms, based on the
   `AT32UC3A4256S`_ 32-bit AVR microcontroller.

      .. danger::

         **It is neither guaranteed nor tested that the J-Link firmware
         for Atmel EDBG will also work on the EDGB populated on the Arduino
         Zero!**  See also the warning to Atmel Studio 7 below.  In doubt
         you should never touch the EDBG firmware on Arduino Zero.

   So if that didn't happen, OpenOCD or, even easier, the small tool
   :program:`edbg`, the `CMSIS-DAP programmer`_ by a Microchip employee,
   should be used:

   .. code-block:: console

      srec_cat samd21_sam_ba.hex -Intel -Output samd21_sam_ba.bin -Binary
      edbg --list    # convert HEX to BIN file and get <your_edbg_sn>

      edbg --verbose --serial <your_edbg_sn> --target samd21 \
           --erase --program --verify --file samd21_sam_ba.bin

   It is also possible to use Microchip's own `Python MCU programmer`_
   together with the `Python Kit information`_ utility and write the
   Intel HEX file directly back to flash without conversion to BIN file:

   .. code-block:: console

      pykitinfo # get <your_edbg_sn>
      pymcuprog --verbose info --tool edbg --serialnumber <your_edbg_sn> \
                --device atsamd21g18a --file samd21_sam_ba.hex \
                --erase --verify write

.. rubric:: Atmel Embedded Debugger (EDBG)

The Arduino Zero also comes with an Atmel Embedded Debugger (`EDBG`_).  That
provides a debug interface to the SAMD21 chip and is supported by OpenOCD
for bootloader restore or direct programming and debugging. The Atmel EDGB
is connected to the debug USB port for programming::

   USB device idVendor=03eb, idProduct=2157, bcdDevice= 1.01
   USB device strings: Mfr=1, Product=2, SerialNumber=3
   Product: EDBG CMSIS-DAP
   Manufacturer: Atmel Corp.
   SerialNumber: E8VRDGVEYNKJTF8LS45K

.. image:: img/atmel_edbg_bd.svg
   :align: center
   :alt: Atmel Embedded Debugger (EDBG) Block Diagram

.. admonition:: Arduino Zero, Atmel EDBG, and Atmel Studio 7
   :class: danger

      .. image:: img/atmel_edbg.png
         :align: right
         :alt: Atmel Embedded Debugger (EDBG) Chip

      The Arduino Zero was designed in partership with Atmel (now
      Microchip) which dedicated to this board a special USB PID with
      the major purpose to make the board recognizable and differentiate
      it form other evaluation boards in Atmel Studio.  The EDBG chip is
      used on several Atmel evaluation boards and programmers, you can
      find the list
      `here <https://onlinedocs.microchip.com/pr/GUID-33422CDF-8B41-417C-9C31-E4521ADAE9B4-en-US-2/GUID-7EF3D274-1BA4-40A3-80C8-51D1D0E4FA75.html>`_.
      You should consider the Arduino Zero dedicated USB PID (:code:`0x2157`)
      as another USB PID to add to that list.  **During the manufacturing
      process Arduino upgrade the EDBG firmware and customize the USB
      descriptor fields.**

      -- https://github.com/arduino/ArduinoCore-samd/issues/286#issuecomment-354807646

   Upgrading the firmware with a new one provided by Atmel Studio 7 using
   the :program:`atfw.exe` tool will erase all the factory "Arduino Zero"
   USB configurations and will set the USB PID to :code:`0x2111`.  **But
   consider that you couldn't revert the Arduino USB descriptor settings!**

Flashing
========

#. Build the Zephyr kernel and the :ref:`hello_world` sample application:

   .. zephyr-app-commands::
      :zephyr-app: samples/hello_world
      :board: arduino_zero
      :goals: build
      :compact:

#. Connect the Arduino Zero to your host computer using the **native USB**
   port (before the USB debug port) to rech the bootloader.

#. Connect the Arduino Zero to your host computer using the **USB debug**
   port (after the native USB port) to reach the virtual console of **EDBG**.

#. Run your favorite terminal program to listen for output. Under Linux the
   terminal should be :code:`/dev/ttyACM0`. For example:

   .. code-block:: console

      $ minicom -D /dev/ttyACM0 -o

   The -o option tells minicom not to send the modem initialization
   string. Connection should be configured as follows:

   - Speed: 115200
   - Data: 8 bits
   - Parity: None
   - Stop bits: 1

#. Pressing the RST button twice quickly to enter bootloader mode.

#. Flash the image:

   .. zephyr-app-commands::
      :zephyr-app: samples/hello_world
      :board: arduino_zero
      :goals: flash
      :compact:

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
      :gen-args: -DBOARD_FLASH_RUNNER=openocd
      :goals: debug
      :compact:

   You should ends up in a debug console (e.g. a GDB session).

References
**********

.. target-notes::

.. _Arduino Store:
    https://store.arduino.cc/arduino-zero

.. _Arduino Zero Pinout Diagram:
    https://content.arduino.cc/assets/Pinout-ZERO_latest.pdf

.. _Arduino Zero Schematic:
    https://content.arduino.cc/assets/ArduinoZeroV4.0_sch.pdf

.. _Arduino Zero Design Data:
    https://content.arduino.cc/assets/ArduinoZeroV4.0_Reference.zip

.. _EDBG:
   https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-42096-Microcontrollers-Embedded-Debugger_User-Guide.pdf

.. _ATSAMD21G18A:
    https://www.microchip.com/product/ATSAMD21G18

.. _AT32UC3A4256S:
    https://www.microchip.com/product/AT32UC3A4256S

.. _Arduino Zero Bootloader:
    https://github.com/arduino/ArduinoCore-samd/tree/master/bootloaders/zero

.. _Arduino Zero Advanced Features:
    https://docs.arduino.cc/tutorials/zero/arduino-zero-edbg

.. _Update the Bootloader on the Arduino Zero:
    https://docs.arduino.cc/tutorials/zero/zero-bootloader-update

.. _J-Link firmware for Atmel EDBG:
    https://www.segger.com/jlink-edbg.html

.. _CMSIS-DAP programmer:
    https://github.com/ataradov/edbg

.. _Python MCU programmer:
    https://microchip-pic-avr-tools.github.io/pymcuprog

.. _Python Kit information:
    https://microchip-pic-avr-tools.github.io/pykitinfo

.. _SAM-BA:
    https://microchipdeveloper.com/atstart:sam-d21-bootloader

.. |Arduino UNO R3| replace::
   :ref:`Arduino UNO R3 <devicetree:dtbinding_arduino_header_r3>`
