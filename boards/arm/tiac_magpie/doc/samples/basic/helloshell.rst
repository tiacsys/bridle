.. _tiac_magpie_led_helloshell-sample:

Hello Shell
###########

Overview
********

See :ref:`helloshell` for the original description.

.. _tiac_magpie_led_helloshell-sample-requirements:

Requirements
************

The TiaC Magpie with already configured UART console support.

Building and Running
********************

Build and flash Hello Shell as follows:

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :build-dir: helloshell-tiac_magpie
   :board: tiac_magpie
   :goals: build flash
   :host-os: unix

After flashing and the board has booted, you will be presented with a shell
prompt. All shell commands are available and would looks like:

.. code-block:: console

   Hello World! I'm THE SHELL from tiac_magpie


   uart:~$ help
   Please press the <Tab> button to see all available commands.
   You can also use the <Tab> button to prompt or auto-complete all commands or its subcommands.
   You can try to call commands with <-h> or <--help> parameter for more information.

   Shell supports following meta-keys:
     Ctrl + (a key from: abcdefklnpuw)
     Alt  + (a key from: bf)
   Please refer to shell documentation for more details.

   Available commands:
     adc      :ADC commands
     bridle   :Bridle commands.
     clear    :Clear screen.
     device   :Device commands
     devmem   :Read/write physical memory"devmem address [width [value]]
     flash    :Flash shell commands
     gpio     :GPIO commands
     hello    :say hello
     help     :Prints the help message.
     history  :Command history.
     hwinfo   :HWINFO commands
     i2c      :I2C commands
     kernel   :Kernel commands
     log      :Commands for controlling logger
     pwm      :PWM shell commands
     resize   :Console gets terminal screen size or assumes default in case the
               readout fails. It must be executed after each terminal width change
               to ensure correct text display.
     sensor   :Sensor commands
     shell    :Useful, not Unix-like shell commands.

   uart:~$ hello -h
   hello - say hello
   uart:~$ hello
   Hello from shell.

   uart:~$ hwinfo devid
   Length: 12
   ID: 0x9e6b44aea1e2b8980c4d32a6

   uart:~$ kernel version
   Zephyr version 3.3.0

   uart:~$ bridle version
   Bridle version 3.3.1

   uart:~$ bridle version long
   Bridle version 3.3.1.0

   uart:~$ bridle info
   Zephyr: 3.3.0
   Bridle: 3.3.1

   uart:~$ device list
   devices:
   - rcc@40023800 (READY)
   - interrupt-controller@40013c00 (READY)
   - gpio@40022800 (READY)
     requires: rcc@40023800
   - gpio@40022400 (READY)
     requires: rcc@40023800
   - gpio@40022000 (READY)
     requires: rcc@40023800
   - gpio@40021C00 (READY)
     requires: rcc@40023800
   - gpio@40021800 (READY)
     requires: rcc@40023800
   - gpio@40021400 (READY)
     requires: rcc@40023800
   - gpio@40021000 (READY)
     requires: rcc@40023800
   - gpio@40020C00 (READY)
     requires: rcc@40023800
   - gpio@40020800 (READY)
     requires: rcc@40023800
   - gpio@40020400 (READY)
     requires: rcc@40023800
   - gpio@40020000 (READY)
     requires: rcc@40023800
   - reset-controller (READY)
     requires: rcc@40023800
   - serial@40007800 (READY)
     requires: rcc@40023800
     requires: reset-controller
   - serial@40004c00 (READY)
     requires: rcc@40023800
     requires: reset-controller
   - rtc@40002800 (READY)
     requires: rcc@40023800
   - adc@40012200 (READY)
     requires: rcc@40023800
   - i2c@40006000 (READY)
     requires: rcc@40023800
   - i2c@40005800 (READY)
     requires: rcc@40023800
   - pwm (READY)
     requires: rcc@40023800
     requires: reset-controller
   - flash-controller@40023c00 (READY)
   - spi@40013400 (READY)
     requires: rcc@40023800

   uart:~$ history
   [  0] history
   [  1] device list
   [  2] bridle info
   [  3] bridle version long
   [  4] bridle version
   [  5] kernel version
   [  6] hwinfo devid
   [  7] hello
   [  8] hello -h
   [  9] help

Simple GPIO Operations
======================

.. rubric:: Switch user LED 2 on and off

.. code-block:: console

   uart:~$ gpio get gpio@40021800 12
   Reading gpio@40021800 pin 12
   Value 0

   uart:~$ gpio conf gpio@40021800 12 out
   Configuring gpio@40021800 pin 12

   uart:~$ gpio set gpio@40021800 12 1
   Writing to gpio@40021800 pin 12

   uart:~$ gpio set gpio@40021800 12 0
   Writing to gpio@40021800 pin 12

   uart:~$ gpio blink gpio@40021800 12
   Blinking port gpio@40021800 index 12. Hit any key to exit

Simple ADC Acquisition
======================

.. rubric:: Read 12-bit from ADC3/IN9

.. code-block:: console

   uart:~$ adc adc@40012200 acq_time 1 tick
   uart:~$ adc adc@40012200 resolution 12

   uart:~$ adc adc@40012200 read 9
   read: 454

   uart:~$ adc adc@40012200 print
   adc@40012200:
   Gain: 1
   Reference: INTERNAL
   Acquisition Time: 0
   Channel ID: 9
   Resolution: 12

Simple Flash Access
===================

.. rubric:: Print HEX Dump

.. code-block:: console

   uart:~$ flash read flash-controller@40023c00 12140 40
   00012140: 00 30 74 69 61 63 5f 6d  61 67 70 69 65 00 48 65 |.0tiac_m agpie.He|
   00012150: 6c 6c 6f 20 57 6f 72 6c  64 21 20 49 27 6d 20 54 |llo Worl d! I'm T|
   00012160: 48 45 20 53 48 45 4c 4c  20 66 72 6f 6d 20 25 73 |HE SHELL  from %s|
   00012170: 0a 00 69 6c 6c 65 67 61  6c 20 6f 70 74 69 6f 6e |..illega l option|

Simple I2C Operations
=====================

.. rubric:: Scan I2C bus 2

.. code-block:: console

   uart:~$ i2c scan i2c@40005800
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
   00:             -- -- -- -- -- -- -- -- -- -- -- --
   10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   20: 20 21 -- -- -- -- -- -- -- -- -- -- -- -- -- --
   30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   40: 40 41 42 43 44 45 46 -- -- -- -- -- -- -- -- --
   50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   70: -- -- -- -- -- -- -- --
   9 devices found on i2c@40005800

.. rubric:: Configure GPIO pins on first IO expander to output

.. code-block:: console

   uart:~$ i2c read_byte i2c@40005800 20 0
   Output: 0xc0

   uart:~$ i2c read_byte i2c@40005800 20 3
   Output: 0xff

   uart:~$ i2c write_byte i2c@40005800 20 3 0
   uart:~$ i2c read_byte i2c@40005800 20 3
   Output: 0x0

.. rubric:: Setup GPIO pins on first IO expander to output

* each odd GPIO to high(1)
* each even GPIO to low(0)

.. code-block:: console

   uart:~$ i2c read_byte i2c@40005800 20 1
   Output: 0xff

   uart:~$ i2c write_byte i2c@40005800 20 1 0x55
   uart:~$ i2c read_byte i2c@40005800 20 1
   Output: 0x55

   uart:~$ i2c read_byte i2c@40005800 20 0
   Output: 0x55
