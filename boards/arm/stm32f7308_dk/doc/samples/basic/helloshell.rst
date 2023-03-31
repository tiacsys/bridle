.. _stm32f7308_dk_led_helloshell-sample:

Hello Shell
###########

Overview
********

See :ref:`helloshell` for the original description.

.. _stm32f7308_dk_led_helloshell-sample-requirements:

Requirements
************

The TiaC Magpie with already configured UART console support.

Building and Running
********************

Build and flash Hello Shell as follows:

.. zephyr-app-commands::
   :app: bridle/samples/helloshell
   :build-dir: helloshell-stm32f7308_dk
   :board: stm32f7308_dk
   :conf: prj-hwstartup.conf
   :gen-args: -DCONFIG_MEMC=y
   :goals: build flash
   :west-args: -p always
   :host-os: unix

After flashing and the board has booted, you will be presented with a shell
prompt. All shell commands are available and would looks like:

.. code-block:: console

   Hello World! I'm THE SHELL from stm32f7308_dk


   uart:~$ help
   Please press the <Tab> button to see all available commands.
   You can also use the <Tab> button to prompt or auto-complete all commands or its subcommands.
   You can try to call commands with <-h> or <--help> parameter for more information.

   Shell supports following meta-keys:
     Ctrl + (a key from: abcdefklnpuw)
     Alt  + (a key from: bf)
   Please refer to shell documentation for more details.

   Available commands:
     adc     :ADC commands
     bridle  :Bridle commands.
     device  :Device commands
     devmem  :Read/write physical memory"devmem address [width [value]]
              Usage:
              Read memory at address with optional width:
              devmem address [width]
              Write memory at address with mandatory width and value:
              devmem address <width> <value>
     flash   :Flash shell commands
     gpio    :GPIO commands
     help    :Prints the help message.
     hwinfo  :HWINFO commands
     i2c     :I2C commands
     pwm     :PWM shell commands

   uart:~$ bridle version
   Bridle version 3.3.0

   uart:~$ bridle version long
   Bridle version 3.3.0.0

   uart:~$ bridle info
   Zephyr: 3.3.0
   Bridle: 3.3.0

   uart:~$ hwinfo devid
   Length: 12
   ID: 0x93aacb90d37a11edbe3f7b34

   uart:~$ device list
   devices:
   - rcc@40023800 (READY)
   - interrupt-controller@40013c00 (READY)
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
   - serial@40011400 (READY)
     requires: rcc@40023800
     requires: reset-controller
   - serial@40004400 (READY)
     requires: rcc@40023800
     requires: reset-controller
   - rtc@40002800 (READY)
     requires: rcc@40023800
   - memory-controller@a0000000 (READY)
     requires: rcc@40023800
   - nor-psram (READY)
     requires: memory-controller@a0000000
   - adc@40012200 (READY)
     requires: rcc@40023800
   - adc@40012100 (READY)
     requires: rcc@40023800
   - adc@40012000 (READY)
     requires: rcc@40023800
   - i2c@40005c00 (READY)
     requires: rcc@40023800
   - i2c@40005800 (READY)
     requires: rcc@40023800
   - i2c@40005400 (READY)
     requires: rcc@40023800
   - pwm (READY)
     requires: rcc@40023800
     requires: reset-controller
   - qspi-nor-flash@0 (READY)
     requires: rcc@40023800
   - flash-controller@40023c00 (READY)

Simple External Memory Operations
=================================

.. rubric:: Erase, write and verify QSPI NOR Flash

.. code-block:: console

   uart:~$ flash test qspi-nor-flash@0 0 1000 5
   Erase OK.
   Write OK.
   Erase OK.
   Write OK.
   Erase OK.
   Write OK.
   Erase OK.
   Write OK.
   Erase OK.
   Write OK.
   Erase-Write test done.

.. rubric:: Read, erase, write and verify QSPI NOR Flash

.. code-block:: console

   uart:~$ flash read qspi-nor-flash@0 0 80
   00000000: 00 01 02 03 04 05 06 07  08 09 0a 0b 0c 0d 0e 0f |........ ........|
   00000010: 10 11 12 13 14 15 16 17  18 19 1a 1b 1c 1d 1e 1f |........ ........|
   00000020: 20 21 22 23 24 25 26 27  28 29 2a 2b 2c 2d 2e 2f | !"#$%&' ()*+,-./|
   00000030: 30 31 32 33 34 35 36 37  38 39 3a 3b 3c 3d 3e 3f |01234567 89:;<=>?|
   00000040: 40 41 42 43 44 45 46 47  48 49 4a 4b 4c 4d 4e 4f |@ABCDEFG HIJKLMNO|
   00000050: 50 51 52 53 54 55 56 57  58 59 5a 5b 5c 5d 5e 5f |PQRSTUVW XYZ[\]^_|
   00000060: 60 61 62 63 64 65 66 67  68 69 6a 6b 6c 6d 6e 6f |`abcdefg hijklmno|
   00000070: 70 71 72 73 74 75 76 77  78 79 7a 7b 7c 7d 7e 7f |pqrstuvw xyz{|}~.|

   uart:~$ flash erase qspi-nor-flash@0 0 1000
   Erase success.

   uart:~$ flash write qspi-nor-flash@0 40 deadbeef
   Write OK.
   Verified.

   uart:~$ flash read qspi-nor-flash@0 0 80
   00000000: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff |........ ........|
   00000010: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff |........ ........|
   00000020: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff |........ ........|
   00000030: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff |........ ........|
   00000040: ef be ad de ff ff ff ff  ff ff ff ff ff ff ff ff |........ ........|
   00000050: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff |........ ........|
   00000060: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff |........ ........|
   00000070: ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff |........ ........|

.. rubric:: Write…, read, write, read and dump FMC PSRAM

.. code-block:: console

   uart:~$ devmem 60000040 32 0
   Using data width 32
   Writing value 0x0

   uart:~$ devmem 60000044 32 0
   Using data width 32
   Writing value 0x0

   uart:~$ devmem 60000048 32 0
   Using data width 32
   Writing value 0x0

   uart:~$ devmem 6000004c 32 0
   Using data width 32
   Writing value 0x0

   uart:~$ devmem 60000040 32
   Using data width 32
   Read value 0x0

   uart:~$ devmem 60000040 32 deadbeef
   Using data width 32
   Writing value 0x0

   uart:~$ devmem 60000040 32
   Using data width 32
   Read value 0xdeadbeef

   uart:~$ devmem dump -a 60000000 -s 128
   60000000: 10 11 12 41 14 05 46 57  4c 01 4f 5b 0c 4d 16 07 |...A..FW L.O[.M..|
   60000010: 14 51 12 13 54 15 16 17  58 1d 5a 1b 5c 55 1e 1d |.Q..T... X.Z.\U..|
   60000020: 00 31 72 31 74 25 a6 27  2d 21 0a 2b 3c 2d 26 37 |.1r1t%.' -!.+<-&7|
   60000030: 36 11 33 33 14 35 76 35  38 3d 1b 3f 35 3d 1e 3f |6.33.5v5 8=.?5=.?|
   60000040: ef be ad de 00 00 00 00  00 00 00 00 00 00 00 00 |........ ........|
   60000050: 55 51 53 53 54 55 56 57  5c 5d 5b 5b 5c 5d 5e 5f |UQSSTUVW \][[\]^_|
   60000060: 60 61 66 61 74 75 66 65  6c 69 6a 6b 64 6d 66 6f |`afatufe lijkdmfo|
   60000070: 70 75 53 73 55 75 56 77  58 51 7b 5b 5c 7d 74 75 |puSsUuVw XQ{[\}tu|

Simple GPIO Operations
======================

.. rubric:: Switch user LD5 (red) on and off

.. code-block:: console

   uart:~$ gpio get gpio@40020000 7
   Reading gpio@40020000 pin 7
   Value 0

   uart:~$ gpio conf gpio@40020000 7 out
   Configuring gpio@40020000 pin 7

   uart:~$ gpio set gpio@40020000 7 1
   Writing to gpio@40020000 pin 7

   uart:~$ gpio set gpio@40020000 7 0
   Writing to gpio@40020000 pin 7

   uart:~$ gpio blink gpio@40020000 7
   Blinking port gpio@40020000 index 1. Hit any key to exit

Simple PWM Operations
=====================

.. rubric:: Pulse user LD6 (green) and dimm from on to off

.. code-block:: console

   uart:~$ pwm usec pwm 4 20000 20000
   uart:~$ pwm usec pwm 4 20000 10000
   uart:~$ pwm usec pwm 4 20000 5000
   uart:~$ pwm usec pwm 4 20000 2500
   uart:~$ pwm usec pwm 4 20000 625
   uart:~$ pwm usec pwm 4 20000 312
   uart:~$ pwm usec pwm 4 20000 156
   uart:~$ pwm usec pwm 4 20000 78
   uart:~$ pwm usec pwm 4 20000 0

Simple ADC Acquisition
======================

.. rubric:: Read 12-bit from ADC1/IN6 (Arduino header)

.. code-block:: console

   uart:~$ adc adc@40012000 acq_time 1 tick
   uart:~$ adc adc@40012000 resolution 12

   uart:~$ adc adc@40012000 read 6
   read: 532

   uart:~$ adc adc@40012000 print
   adc@40012000:
   Gain: 1
   Reference: INTERNAL
   Acquisition Time: 0
   Channel ID: 6
   Resolution: 12

Simple I2C Operations
=====================

.. rubric:: Scan I2C bus 1

.. code-block:: console

   uart:~$ i2c scan i2c@40005400
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
   00:             -- -- -- -- -- -- -- -- -- -- -- --
   10: -- -- -- -- -- -- -- -- -- -- 1a -- -- -- -- --
   20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   70: -- -- -- -- -- -- -- --
   9 devices found on i2c@40005400

.. rubric:: Scan I2C bus 2 (Arduino header)

.. code-block:: console

   uart:~$ i2c scan i2c@40005800
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
   00:             -- -- -- -- -- -- -- -- -- -- -- --
   10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   70: -- -- -- -- -- -- -- --
   9 devices found on i2c@40005800

.. rubric:: Scan I2C bus 3

.. code-block:: console

   uart:~$ i2c scan i2c@40005c00
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
   00:             -- -- -- -- -- -- -- -- -- -- -- --
   10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   30: -- -- -- -- -- -- -- -- 38 -- -- -- -- -- -- --
   40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   70: -- -- -- -- -- -- -- --
   9 devices found on i2c@40005c00
