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
   :zephyr-app: bridle/samples/helloshell
   :build-dir: helloshell-tiac_magpie
   :board: tiac_magpie
   :goals: build flash
   :host-os: unix
   :compact:

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
     clear    :Clear screen.
     device   :Device commands
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

   uart:~$ device list
   devices:
   - STM32_CLK_RCC
   - stm32-exti
   - RTC_0
   - UART_7
   - UART_4
   - RNG
   - sys_clock
   - ADC_3
   - GPIOK
   - GPIOJ
   - GPIOI
   - GPIOH
   - GPIOG
   - GPIOF
   - GPIOE
   - GPIOD
   - GPIOC
   - GPIOB
   - GPIOA
   - FLASH_CTRL
   - I2C_4
   - I2C_2
   - PWM_8
   - SPI_5

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

Simple ADC Acquisition
======================

.. rubric:: Read 12-bit from ADC3/IN9

.. code-block:: console

   uart:~$ adc ADC_3 acq_time 1 tick
   uart:~$ adc ADC_3 resolution 12

   uart:~$ adc ADC_3 read 9
   read: 776

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

   uart:~$ flash read FLASH_CTRL 10000 40
   00010000: 4e 3a 0a 00 50 52 45 20  4b 45 52 4e 45 4c 20 31 |N:..PRE  KERNEL 1|
   00010010: 3a 0a 00 50 52 45 20 4b  45 52 4e 45 4c 20 32 3a |:..PRE K ERNEL 2:|
   00010020: 0a 00 44 65 76 69 63 65  20 63 6f 6d 6d 61 6e 64 |..Device  command|
   00010030: 73 00 4c 69 73 74 20 63  6f 6e 66 69 67 75 72 65 |s.List c onfigure|

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

