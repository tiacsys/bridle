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
     clear    :Clear screen.
     device   :Device commands
     gpio     :GPIO commands
     hello    :say hello
     help     :Prints the help message.
     history  :Command history.
     i2c      :I2C commands
     kernel   :Kernel commands
     log      :Commands for controlling logger
     resize   :Console gets terminal screen size or assumes default in case the
               readout fails. It must be executed after each terminal width change
               to ensure correct text display.
     shell    :Useful, not Unix-like shell commands.

   uart:~$ hello -h
   hello - say hello
   uart:~$ hello
   Hello from shell.

   uart:~$ device list
   devices:
   - STM32_CLK_RCC
   - stm32-exti
   - UART_7
   - RNG
   - sys_clock
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
   - I2C_4
   - I2C_2
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

