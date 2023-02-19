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
   Zephyr version 3.0.0

   uart:~$ bridle version
   Bridle version 3.0.1

   uart:~$ bridle version long
   Bridle version 3.0.1.0

   uart:~$ bridle info
   Zephyr: 3.0.0
   Bridle: 3.0.1

   uart:~$ device list
   devices:
   - rcc@40023800 (READY)
   - GPIOK (READY)
     requires: rcc@40023800
   - GPIOJ (READY)
     requires: rcc@40023800
   - GPIOI (READY)
     requires: rcc@40023800
   - GPIOH (READY)
     requires: rcc@40023800
   - GPIOG (READY)
     requires: rcc@40023800
   - GPIOF (READY)
     requires: rcc@40023800
   - GPIOE (READY)
     requires: rcc@40023800
   - GPIOD (READY)
     requires: rcc@40023800
   - GPIOC (READY)
     requires: rcc@40023800
   - GPIOB (READY)
     requires: rcc@40023800
   - GPIOA (READY)
     requires: rcc@40023800
   - interrupt-controller@40013c00 (READY)
   - RTC_0 (READY)
     requires: rcc@40023800
   - UART_7 (READY)
     requires: rcc@40023800
   - UART_4 (READY)
     requires: rcc@40023800
   - ADC_3 (READY)
     requires: rcc@40023800
   - I2C_4 (READY)
     requires: rcc@40023800
   - I2C_2 (READY)
     requires: rcc@40023800
   - PWM_8 (READY)
     requires: rcc@40023800
   - FLASH_CTRL (READY)
   - SPI_4 (READY)
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

   uart:~$ gpio get GPIOG 12
   Reading GPIOG pin 12
   Value 0
   uart:~$ gpio conf GPIOG 12 out
   Configuring GPIOG pin 12
   uart:~$ gpio set GPIOG 12 1
   Writing to GPIOG pin 12
   uart:~$ gpio set GPIOG 12 0
   Writing to GPIOG pin 12
   uart:~$ gpio blink GPIOG 12
   Blinking port GPIOG index 12. Hit any key to exit

Simple ADC Acquisition
======================

.. rubric:: Read 12-bit from ADC3/IN9

.. code-block:: console

   uart:~$ adc ADC_3 acq_time 1 tick
   uart:~$ adc ADC_3 resolution 12

   uart:~$ adc ADC_3 read 9
   read: 489

   uart:~$ adc ADC_3 print
   ADC_3:
   Gain: 1
   Reference: INTERNAL
   Acquisition Time: 0
   Channel ID: 9
   Resolution: 12

Simple Flash Access
===================

.. rubric:: Print HEX Dump

.. code-block:: console

   uart:~$ flash read FLASH_CTRL 13000 40
   00013000: 20 76 65 72 73 69 6f 6e  20 28 77 2f 6f 20 74 77 | version  (w/o tw|
   00013010: 65 61 6b 29 2e 00 6c 6f  6e 67 00 42 72 69 64 6c |eak)..lo ng.Bridl|
   00013020: 65 20 76 65 72 73 69 6f  6e 20 28 77 69 74 68 20 |e versio n (with |
   00013030: 74 77 65 61 6b 29 2e 00  48 65 6c 6c 6f 20 66 72 |tweak).. Hello fr|

Simple I2C Operations
=====================

.. rubric:: Scan I2C bus 2

.. code-block:: console

   uart:~$ i2c scan I2C_2
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
   00:             -- -- -- -- -- -- -- -- -- -- -- --
   10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   20: 20 21 -- -- -- -- -- -- -- -- -- -- -- -- -- --
   30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   40: 40 41 42 43 44 45 46 -- -- -- -- -- -- -- -- --
   50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   70: -- -- -- -- -- -- -- --
   9 devices found on I2C_2

.. rubric:: Configure GPIO pins on first IO expander to output

.. code-block:: console

   uart:~$ i2c read_byte I2C_2 20 0
   Output: 0xc0
   uart:~$ i2c read_byte I2C_2 20 3
   Output: 0xff
   uart:~$ i2c write_byte I2C_2 20 3 0
   uart:~$ i2c read_byte I2C_2 20 3
   Output: 0x0

.. rubric:: Setup GPIO pins on first IO expander to output

* each odd GPIO to high(1)
* each even GPIO to low(0)

.. code-block:: console

   uart:~$ i2c read_byte I2C_2 20 1
   Output: 0xff
   uart:~$ i2c write_byte I2C_2 20 1 0x55
   uart:~$ i2c read_byte I2C_2 20 1
   Output: 0x55
   uart:~$ i2c read_byte I2C_2 20 0
   Output: 0x55
